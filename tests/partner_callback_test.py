# -*- coding: utf-8 -*-
import requests
import unittest
import hashlib
import auth
import base_data
import urllib
import json
import time


class test_callback(unittest.TestCase):
    def test_yichongbao_callback(self):
        # url = 'http://120.27.134.79:23300/hf_gezi/chargeChannelAction/notifyUrl.do'
        url = 'http://120.76.97.52:8085/cmcchuafeiReceiver'
        trade_no = '20161219134637504GKDQABA00001'
        secret = '3!hw3nAP'
        success = '0'
        amount = '0'
        t = str(int(time.time()))
        data = {"trade_no": trade_no, "success": success,
                "sign": hashlib.md5('%s%s%s%s%s' % (amount, secret, success, t, trade_no)).hexdigest(), "amount":amount,
                "t": t}
        resp = requests.get(url, data)
        print resp.url
        print resp.text
