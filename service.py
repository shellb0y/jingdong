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
import urllib
import auth

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
                url = 'http://op.yikao666.cn/JDTrainOpen/CallBackForMJD?order_id=%s&success=false&order_src=app&msg=%s' % (
                    partner_order_id, e.message)
                logger.info('callback start.%s' % url)
                resp = requests.get(url)
                logger.info(resp.text)

                time.sleep(PLACEORDERINTERVAL)


def get_account(uuid, category='jd_90_5'):
    url = 'http://115.28.102.142:8000/api/mobilepay/account/%s' % category
    while True:
        try:
            resp = requests.get(url)
            account = resp.json()

            user_agent = base_data.get_user_agent()
            # adsl_service.reconnect()
            try:
                login = http_handler.login.Login(account['username'], account['password'], uuid, user_agent)
                cookie = login.get_cookie()
                logger.info('login success,cookie:%s' % cookie)
                account['cookie'] = cookie
            except Exception, e:
                # TODO:send to server
                logger.error('account valid')
                continue

            return account
        except Exception, e:
            logger.error('get jd account faild')
            time.sleep(180)
            continue


def des_encryption(mobile):
    url = 'http://115.28.102.142:8000/api/des/encode/%s' % mobile
    while True:
        try:
            resp = requests.get(url)
            mobile = resp.text
            return mobile
        except Exception, e:
            logger.error('des encryption faild')
            time.sleep(180)
            continue

def save_order(data):
    url = 'http://115.28.102.142:8000/api/mobilepay/order'
    while True:
        try:
            resp = requests.post(url)
            if resp.text == 1:
                return True
            else:
                return False
        except Exception, e:
            logger.error('save order faild')
            time.sleep(180)
            continue

def phone_charge():
    while True:
        try:
            url = 'http://139.199.65.115:1218/?name=phone_charge&opt=get&auth=Fb@345!'
            resp = requests.get(url)
            data = resp.json()
        except Exception, e:
            logger.error('phone charge data not found')
            time.sleep(5)
            continue

        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        # data = {'mobile':'15763563256','parterner_id':'123654','amount':100,callback:''}
        mobile = des_encryption(data['mobile'])
        account = get_account(uuid)

        try:
            body = {"dxqids": "7929697981", "facePrice": "100.0", "isBingding": "0", "isNote": "0", "jdPrice": "94.80",
                    "payType": "10",
                    "type": "1", "contact": "false", "mobile": mobile}
            sign = auth.sign('submitPczOrder', uuid, json.dumps(body))
            url = 'http://api.m.jd.com/client.action?functionId=submitPczOrder&client=android&clientVersion=5.3.0&build=36639&d_brand=ZTE&d_model=SCH-I779&osVersion=4.4.2&screen=1280*720&partner=tencent&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                uuid, sign[1], sign[0])

            headers = {
                'Charset': 'UTF-8',
                'jdc-backup': account['cookie'],
                'Connection': 'close',
                'Cookie': account['cookie'],
                'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

            resp = requests.post(url, data='body=' + urllib.quote_plus(json.dumps(body)) + '&', headers=headers)
            ret = resp.json()
            if ret['success']:
                # TODO:save order,Cala,callback parterner
                logger.info('%s charge success' % data['mobile'])
            else:
                #TODO:save order,callback parterner
                logger.error('%s charge faild' % data['mobile'])

                #TODO:save order
        except Exception,e:
            # TODO:send to server,callback parterner
            logger.error('%s charge faild' % data['mobile'])


def login_from_api():
    while True:
        try:
            account = http_handler.account.getFromHttpSqs(adsl)
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
