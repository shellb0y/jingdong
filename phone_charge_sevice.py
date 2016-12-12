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
import redis
import hashlib
import datetime


def get_account(uuid):
    logger.info('get jd account')
    url = base_data.JD_ACCOUNT_API_GET
    while True:
        try:
            logger.debug('GET %s' % url)
            resp = requests.get(url)
            logger.debug(resp.text)

            account_json = resp.json()
            account = json.loads(account_json['_data'])
            account['account_id'] = account_json['account_id']
            logger.info('get jd account:%s,%s' % (account['username'], account['password']))
            user_agent = base_data.get_user_agent()
            # adsl_service.reconnect()
            try:
                login = http_handler.login.Login(account['username'], account['password'], uuid, user_agent)
                cookie = login.get_cookie()
                logger.info('login success,cookie:%s' % cookie)
                account['cookie'] = cookie

                # h5_cookie = login.get_h5_cookie(cookie)
                # logger.info('get h5 cookie:%s' % h5_cookie)
                #
                # cookie = 'pt_key=%s;pwdt_id=%s;sid=%s;guid=%s;pt_pin=%s;mobilev=%s' % (
                #     h5_cookie['pt_key'], h5_cookie['pwdt_id'], h5_cookie['sid'], h5_cookie['guid'],
                #     h5_cookie['pt_pin'], h5_cookie['mobilev'])
                # account['h5_cookie'] = cookie
                account['valid'] = 1
                return account
            except Exception, e:
                account['valid'] = 0
                logger.debug('POST %s\n%s' % (base_data.JD_ACCOUNT_API_POST, json.dumps(account)))

                while True:
                    try:
                        logger.error('account invalid,send to server')
                        resp = requests.post(base_data.JD_ACCOUNT_API_POST, json=account)
                        logger.info('resp:%s' % resp.text)
                        if resp.text == '1':
                            logger.info('success')
                        else:
                            logger.warn('maybe faild')
                    except Exception, e:
                        time.sleep(60)
                        continue
        except Exception, e:
            logger.error('get jd account faild')
            time.sleep(60)
            continue


def des_encryption(mobile):
    url = 'http://115.28.102.142:8081/api/des/encode/%s' % mobile
    while True:
        try:
            resp = requests.get(url)
            mobile = resp.text
            return mobile
        except Exception, e:
            logger.error('des encryption faild')
            time.sleep(60)
            continue


def save_order(data, id=0):
    while True:
        try:
            logger.info('save trade data')
            _data = {'order_id': id, 'data': data}
            logger.debug('POST %s\n%s' % (base_data.ORDER_SAVE_API_POST, json.dumps(_data)))
            resp = requests.post(base_data.ORDER_SAVE_API_POST, json=_data)
            logger.debug(resp.text)
            if resp.text == '-1' or resp.text == '0':
                logger.warn('maybe faild')
                time.sleep(60)
            else:
                logger.info('sucess')

            return resp.text
        except Exception:
            logger.error(traceback.format_exc())
            time.sleep(60)
            continue


# def set_order_status(id, status):
#     while True:
#         try:
#             data = {id: id, status: status}
#             resp = requests.post(base_data.ORDER_STATUS_API_POST, data=urllib.urlencode(data))
#             if resp.text == '1':
#                 logger.info('success')
#             else:
#                 logger.warn('set order status maybe faild')
#         except Exception, e:
#             logger.error('set order status faild\n%s' % traceback.format_exc())
#             time.sleep(60)
#             continue


def callback_partner_and_save_order(data, success, order_id, pc_cookie=''):
    while True:
        try:
            logger.info('callback begin')
            t = str(int(round(time.time() * 1000)))
            _data = {'partner_order_id': data['partner_order_id'], 'amount': data['partner_price'],
                     'money': float(data['money']) / 100,
                     'trade_no': data['trade_no'],
                     'success': success, 't': t,
                     'sign': hashlib.md5(
                         str(data['amount']) + data['partner_order_id'] + json.loads(data['partner'])['secret'] + str(
                             success) + t +
                         data['trade_no'])}
            resp = requests.get(urllib.unquote_plus(data['callback']), params=_data)
            if resp.text == '1':
                logger.info('sucess')
                data['callback_status'] = u'回调成功'
            else:
                logger.warn('faild')
                data['callback_status'] = u'回调失败'

            break
        except Exception:
            logger.error(traceback.format_exc())
            data['callback_status'] = u'回调异常'
            continue
    if success:
        while True:
            try:
                pay_task_data = {
                    "module": {
                        "worker": [
                            {
                                "assembly": "FBServer.Pay.TrainJD.Pay_RechargePhoneBillJD,FBServer.Pay.TrainJD.dll",
                                "type": 0,
                                "parms": ''
                            }
                        ],
                        "payer": [
                            "{0}"
                        ]
                    },
                    "sessionId": '',
                    "data": {
                        "siteNo": "jingdong_phone",
                        "ticketOrderNo": data['jd_order_id'],
                        "sysOrderNo": order_id,
                        "loginUser": data['account']["username"],
                        "loginPwd": data['account']["password"],
                        "exData": {
                            "Cookie": pc_cookie,
                            "userId": '',
                            "mCookie": '',
                            "orderId": "",
                            "payurl": ""
                        },
                        "creatTime": str(datetime.datetime.now()),
                        "amount": float(data['money']) / 100,
                        "isPay": "false"
                    }
                }
                url = 'http://op.yikao666.cn/JDTrainOpen/CreatePayTaskByPhone'
                pay_task_data = json.dumps(pay_task_data)
                logger.debug('POST %s\n%s' % (url, pay_task_data))
                resp = requests.post(url, data={'send_data': pay_task_data})
                logger.info(resp.text)
                break
            except Exception, e:
                logger.error('callback pay faild')
                logger.error(traceback.format_exc())
                time.sleep(60)
                continue
    save_order(data, order_id)


def phone_charge():
    pool = redis.ConnectionPool(host='139.199.65.115', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while True:
        order_id = 0
        success = 0

        try:
            print 'redis brpop'
            result = r.brpop('order_platform:phone_charge:order', 5)
            if result:
                trade_no = result[1]
                logger.info('get trade no:%s' % trade_no)
                data = r.hgetall('order_platform:phone_charge:trade_no:%s' % trade_no)
                logger.info('get trade data:%s' % data)

                if not data:  # trade data loss
                    save_order({'trade_no': trade_no, 'status': u'数据丢失'})
                    logger.error('trade_no %s data loss' % trade_no)
                    continue
            else:
                continue
        except Exception, e:
            logger.error(e.message)
            time.sleep(5)
            continue

        data['status'] = '正在下单'
        data['partner_price'] = ''
        order_id = save_order(data)

        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        # data = {'mobile':'15763563256','parterner_id':'123654','amount':100,callback:''}
        mobile = des_encryption(data['mobile'])
        account = get_account(uuid)

        data['account'] = {'account_id': account['account_id'], 'username': account['username'],
                           'password': account['password']}
        pc_cookie = account['pc_cookie']
        try:
            headers = {
                'Charset': 'UTF-8',
                'jdc-backup': account['cookie'],
                'Connection': 'close',
                'Cookie': account['cookie'],
                'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            body = {"mobile": mobile}
            sign = auth.sign('searchPczPriceList', uuid, json.dumps(body))
            url = 'http://api.m.jd.com/client.action?functionId=searchPczPriceList&clientVersion=5.3.0&build=36639&client=android&d_brand=nubia&screen=1920*1080&partner=waps007&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                uuid, sign[1], sign[0])

            logger.info('get jd price')
            resp = requests.post(url, data='body=' + urllib.quote_plus(json.dumps(body)) + '&', headers=headers)
            resp = resp.json()
            data['providerName'] = resp['providerName']
            data['areaName'] = resp['areaName']

            if data['providerName'] == u'移动':
                data['partner_price'] = 98
            elif data['providerName'] == u'联通':
                data['partner_price'] = 98
            else:
                data['partner_price'] = 97

            sku = filter(lambda s: s['facePrice'] == str(data['amount']), resp['skuList'])
            if len(sku) == 0:
                callback_partner_and_save_order(data, 0, order_id)
                continue

            # data['jdPrice'] = float(sku[0]['jdPrice']) / 100 - account['compon'][0]["price"]
            # # "dxqids": "7929697981",
            # body = {"dxqids": account['compon'][0]["id"], "facePrice": data['amount'], "isBingding": "0", "isNote": "0",
            #         "jdPrice": str(data['jdPrice']),
            #         "payType": "10", "type": "1", "contact": "false", "mobile": mobile}

            data['jdPrice'] = float(sku[0]['jdPrice']) / 100
            # "dxqids": "7929697981",
            body = {"facePrice": data['amount'], "isBingding": "0", "isNote": "0",
                    "jdPrice": str(data['jdPrice']),
                    "payType": "0", "type": "1", "contact": "false", "mobile": mobile}
            sign = auth.sign('submitPczOrder', uuid, json.dumps(body))
            url = 'http://api.m.jd.com/client.action?functionId=submitPczOrder&client=android&clientVersion=5.3.0&build=36639&osVersion=4.4.2&screen=1280*720&partner=tencent&uuid=%s&area=1_0_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
                uuid, sign[1], sign[0])
            body = 'body=' + urllib.quote_plus(json.dumps(body)) + '&'
            logger.debug('POST %s\n%s' % (url, body))
            resp = requests.post(url, data=body, headers=headers)
            ret = resp.json()
            logger.debug(resp.text)
            if ret['orderId']:
                data['jd_order_id'] = ret['orderId']
                data['money'] = ret['money']
                data['status'] = u'下单成功,等待支付'
                success = 1
                logger.info('%s charge success,callback' % data['mobile'])
            else:
                data['status'] = u'下单失败'
                logger.error('%s charge faild\n%s' % data['mobile'], traceback.format_exc())

        except Exception, e:
            data['status'] = u'下单异常'
            logger.error(traceback.format_exc())
        finally:
            r.delete('order_platform:phone_charge:trade_no:%s' % trade_no)
            callback_partner_and_save_order(data, success, order_id, pc_cookie)
