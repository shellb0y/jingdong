# -*- coding: utf-8 -*-
import unittest
import requests
import base_data


class httpHandlerTest(unittest.TestCase):
    def test_post_order(self):
        resp = requests.post(base_data.ORDER_SAVE_API_POST,json={'id':1,'data':{'status':u'下单失败','TEST':None}})
        print resp.text
    def test_set_status(self):
        resp = requests.post(base_data.ORDER_SETSTATUS_API_POST,
                             data={'order_id': 'bd95cf4b26d04d2cb85bbfc9d4a16117', 'status': '充值成功'})
        print resp.text