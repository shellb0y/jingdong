import auth
import unittest

class Auth_Sign_TestSuite(unittest.TestCase):
    def auth_test(self):
        req_data = auth.get_req_data('jd_60aaf2f598861', 'e4e333')
        print  req_data

        resp = 'aHLnhbKM9oBtKHz0nVBtCtRI5vdKL0kEJSj85AR8sXiImjeOMj8xF+UhTWTXBgO4XV2QitZNleNzLP34rB0uAFK09+lzAsyuAhgCwXGz5YwkQ4hpnbx8vqwX1ZGaRkE590kX4nsrDFtOFqNklC1FStEKZBNQNrTd1J1hlDqudi7sxmZgh48TLno39B+dPuhP7PpKIkO9JAdoHP9KuVyoWA=='
        resp_data = auth.get_resp_data(resp)
        cookie = auth.get_cookie(resp_data)
        print  cookie