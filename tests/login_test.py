import unittest
import http_handler
import base_data


class HttpSqsTestSuite(unittest.TestCase):
    def test_login(self):
        user_agent = base_data.get_user_agent()
        uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        login = http_handler.login.Login('jd_60aaf2f598861', 'e4e333', uuid, user_agent)
        cookie = login.get_cookie()
        print cookie
        print login.get_h5_cookie(cookie)
