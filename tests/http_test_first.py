import requests
import unittest
import auth
import base_data
import urllib
import time


class HttpFirstTest(unittest.TestCase):
    def login_test(self):
        url = 'http://wlogin.m.jd.com/applogin_v2'
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12)
        print uuid

        data = auth.get_req_data('jd_617e8c5befc3a', 'p36yo4', uuid)
        req = requests.post(url, data=data, headers={'User-Agent': 'Android WJLoginSDK 1.4.2'})
        resp = req.text
        print resp

        cookie = auth.get_cookie(resp)
        print cookie

    def get_user_info_test(self):
        body = '{"flag":"nickname"}'
        cookie = 'pin=jd_6582fa47d7f63; wskey=AAFYO9LhAEAvZd4SkJUmXtKswJpE6Em1zYrPwUBdZ584nWtIEIlcEecOwHozbrtKLARgOUYLI0Dv3oRV26cTBsxKfpeAAiIx; whwswswws='
        uuid= ''
        sign = auth.sign('newUserInfo',uuid,body)
        print sign

        url = 'http://api.m.jd.com/client.action?functionId=newUserInfo&clientVersion=5.3.0&build=36639&client=android&d_brand=ZTE&d_model=SCH-I779&osVersion=4.4.2&screen=1280*720&partner=tencent&uuid=%s&area=1_2802_0_0&networkType=wifi&st=%s&sign=%s&sv=122' % (
            uuid, sign[1], sign[0])
        print url

        req = requests.post(url, data='body=' + urllib.quote(body) + '&', headers={
            'Charset': 'UTF-8',
            'Connection': 'close',
            'Cookie': cookie,
            'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.2; Nexus Build/KOT49H)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        print req.text