# -*- coding: utf-8 -*-
import auth
import unittest
import base_data

class Auth_Sign_TestSuite(unittest.TestCase):

    def auth_test(self):
        req_data = auth.get_req_data(u'琴猪遣颠悄'.encode('utf-8'), 'xiaheibacheng18','867323020350896-a086c68dae09')
        print  req_data

        resp = 'aHLnhbKM9oBtKHz0nVBtCtRI5vdKL0kEJSj85AR8sXiImjeOMj8xF+UhTWTXBgO4XV2QitZNleNzLP34rB0uAFK09+lzAsyuAhgCwXGz5YwkQ4hpnbx8vqwX1ZGaRkE590kX4nsrDFtOFqNklC1FStEKZBNQNrTd1J1hlDqudi7sxmZgh48TLno39B+dPuhP7PpKIkO9JAdoHP9KuVyoWA=='
        #resp_data = auth.get_resp_data(resp)
        cookie = auth.get_cookie(resp)
        print  cookie

    def sign_test(self):
        sign_data = auth.sign('newUserInfo', base_data.get_random_number() + '-' + base_data.get_random_letter_number(12),
                         '{"flag":"nickname"}')
        print sign_data