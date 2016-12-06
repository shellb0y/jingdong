# -*- coding: utf-8 -*-
import base_data
import log_ex as logger
import requests
import json
import http_handler
import traceback
import time
import os
import adsl

PLACEORDERINTERVAL = 5
# FAILDWAITING = 180

adsl_service = adsl.Adsl({"name": u"宽带连接".encode('gbk'),
                          "username": "057474432953",
                          "password": "734206"})


def place_order():
    while True:
        partner_order_id = ''

        try:
            currentHour = int(time.strftime('%H', time.localtime(time.time())))
            if currentHour > 22 or currentHour < 7:
                print 'sleep a hour'
                time.sleep(3600)
                continue

            logger.info('--------------------------')
            logger.info('get jingdong train data')
            try:
                resp = requests.get('http://op.yikao666.cn/JDTrainOpen/getTaskForJD')
                train = resp.json()
                partner_order_id = train['order_id']
                logger.debug(json.dumps(train))
            except Exception, e:
                print 'get jingdong train data faild'
                time.sleep(5)
                continue

            train = json.loads(train['data'])
            username = train['data']['exData2']['user']
            password = train['data']['exData2']['pwd']
            logger.info('get orderid:%s,username:%s,password:%s,logon...' % (partner_order_id, username, password))

            uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
            user_agent = base_data.get_user_agent()

            adsl_service.reconnect()

            login = http_handler.login.Login(username, password, uuid, user_agent)
            cookie = login.get_cookie()
            logger.info('login success,cookie:%s' % cookie)

            h5_cookie = login.get_h5_cookie(cookie)
            logger.info('get h5 cookie:%s' % h5_cookie)

            order = http_handler.order.Order(uuid, user_agent, h5_cookie)
            passengers = train['data']['passengersInfo']
            logger.info('add passenger %s' % json.dumps(passengers))
            passenger_ids = ','.join(order.add_passenger(passengers))
            logger.info('add passenger success.ids:%s.' % passenger_ids)

            order_data = order.gen_order(train, passenger_ids)
            logger.info('order generate success,id:%s.get token...' % order_data['orderid'])
            order_data = order.get_token(order_data)
            logger.info('order token success,%s' % order_data['token'])

            couponid = ''
            couponPrice = ''

            if train['data']['exData2'].has_key('couponid'):
                couponid = train['data']['exData2']['couponid']
                logger.info('get couponid %s' % couponid)
            if train['data']['exData2'].has_key('couponPrice'):
                couponPrice = train['data']['exData2']['couponPrice']
                logger.info('get couponPrice %s' % couponPrice)

            if not (couponid and couponPrice):
                order_data['couponid'] = ''
                order_data['couponPrice'] = ''
            else:
                order_data['couponid'] = couponid
                order_data['couponPrice'] = int(float(couponPrice) * 100)

            logger.info('submit:%s' % json.dumps(order_data))
            if order.submit(order_data):
                logger.info('get order details')
                order_details = order.get_details(order_data['orderid'])
                if order_details:
                    logger.info('erpOrderId %s,callback start...' % order_details['erpOrderId'])
                    resp = requests.get(
                        'http://op.yikao666.cn/JDTrainOpen/CallBackForMJD?order_id=%s&jdorder_id=%s&success=true&order_no=%s&amount=%s&order_src=app' % (
                            partner_order_id, order_details['erpOrderId'], order_data['orderid'],
                            order_details['onlinePayFee']))
                    logger.info(resp.text)
                    logger.info('ALL SUCCESS')
                    time.sleep(PLACEORDERINTERVAL)
                else:
                    logger.error('order place faild')
            else:
                logger.error('submit maybe faild')

        except Exception, e:
            logger.error(traceback.format_exc())

            if partner_order_id:
                url = 'http://op.yikao666.cn/JDTrainOpen/CallBackForMJD?order_id=%s&success=false&order_src=app&msg=%s'
                logger.info('callback start.%s' % url)
                resp = requests.get(
                    url % (partner_order_id, e.message))
                logger.info(resp.text)

                time.sleep(PLACEORDERINTERVAL)


def login_from_api():
    while True:
        try:
            account = http_handler.account.getFromWenbin(adsl)
            if account:
                url = 'http://114.55.34.8:1218/?name=jd_login&opt=put&auth=Fb@345!'
                data = json.dumps(account)
                logger.info('send to queue...,%s' % data)
                resp = requests.put(url, data=data)
                if resp.text == 'HTTPSQS_PUT_OK':
                    logger.info('ALL SUCCESS')
                else:
                    logger.info('send to queue faild\n%s,exit' % resp.text)
                    exit()
        except Exception, e:
            logger.error(traceback.format_exc())
            time.sleep(5)


def login_from_txt():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    account_txt = os.path.normpath(os.path.join(root_path, 'account/account.txt'))

    while True:
        if not os.path.isfile(account_txt):
            print 'account txt not found'
            time.sleep(20)
            continue

        file_object = open(account_txt)
        try:
            accounts = file_object.readlines()
        except Exception, e:
            logger.error('read file faild')
            continue
        finally:
            file_object.close()

        os.rename(account_txt,
                  os.path.normpath(os.path.join(root_path, 'account/' + str(int(time.time())) + '.txt')))
        for account in accounts:
            try:
                ac = account.split(',')
                username = ac[0]
                password = ac[1]

                logger.info('uname:%s,pwd:%s,login...' % (username, password))
                uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
                user_agent = base_data.get_user_agent()

                login = http_handler.login.Login(username, password, uuid, user_agent)
                cookie = login.get_cookie()
                logger.info('login success,cookie:%s' % cookie)

                h5_cookie = login.get_h5_cookie(cookie)
                logger.info('get h5 cookie:%s' % h5_cookie)

                cookie = 'pt_key=%s;pwdt_id=%s;sid=%s;guid=%s;pt_pin=%s;mobilev=%s' % (
                    h5_cookie['pt_key'], h5_cookie['pwdt_id'], h5_cookie['sid'], h5_cookie['guid'],
                    h5_cookie['pt_pin'], h5_cookie['mobilev'])


            except Exception, e:
                logger.error(traceback.format_exc())
