# -*- coding: utf-8 -*-
import unittest
import requests
import base_data


class httpHandlerTest(unittest.TestCase):
    def test_post_order(self):
        resp = requests.post(base_data.ORDER_SAVE_API_POST,json={'id':1,'data':{'status':u'下单失败','TEST':None}})
        print resp.text