import base_data
import log_ex as logger
import requests
import json
import http_handler
import traceback
from time import ctime, sleep
import argparse
import sys

PLACEORDERINTERVAL = 20
FAILDWAITING = 180


def place_order():
    while True:
        try:
            partner_order_id = ''
            order_id = ''

            logger.info('--------------------------')
            logger.info('get jingdong train data')
            try:
                resp = requests.get('http://op.yikao666.cn/JDTrainOpen/getTaskForJD')
                train = resp.json()
                partner_order_id = train['order_id']
                logger.debug(json.dumps(train))
            except Exception, e:
                logger.error('get jingdong train data faild')
                sleep(5)
                continue

            train = json.loads(train['data'])
            username = train['data']['exData2']['user']
            password = train['data']['exData2']['pwd']
            logger.info('get orderid:%s,username:%s,password:%s,logon...' % (partner_order_id, username, password))

            uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
            user_agent = base_data.get_user_agent()

            login = http_handler.login.Login(username, password, uuid, user_agent)
            cookie = login.get_cookie()
            logger.info('login success,cookie:%s' % cookie)

            h5_cookie = login.get_h5_cookie(cookie)
            logger.info('get h5 cookie:%s' % h5_cookie)

            order = http_handler.order.Order(uuid, user_agent, h5_cookie)
            passengers = train['data']['passengersInfo']
            logger.info('add passenger %s' % json.dumps(passengers))
            passenger_ids = ','.join(order.add_passenger(passengers))
            logger.info('add passenger success.ids:%s.\nREADY:' % passenger_ids)

            order_data = order.get_token(train)
            logger.info('order generate success,id:%s.get token...' % order_data['order_id'])
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
                couponid = couponPrice = ''

            order_data['couponid'] = couponid
            order_data['couponPrice'] = couponPrice
            logger.info('submit:%s' % json.dumps(order_data))
            print order.submit(order_data)
            sleep(PLACEORDERINTERVAL)

        except Exception, e:
            logger.error(traceback.format_exc())
            sleep(FAILDWAITING)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            place_order()
        elif sys.argv[1] == '-spp':
            print 'spp'
        else:
            print 'no support'
    else:
        print 'no support'
