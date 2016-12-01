import requests
import unittest
import json
import os
import time

class HttpSqsTestSuite(unittest.TestCase):
    def test_put(self):
        url = 'http://114.55.34.8:1218/?name=jd_login&opt=put&auth=Fb@345!'
        data = {'username':'test','password':'1','cookie':'guid=8aa8e40b57ce8a5a9d446fc26363b2ee90390fc275a13627463d113a1c1d484f; pt_key=app_openAAFYP9OEADD-xRmjuVsvkglMot8HHyMe5357fEkAFN4pd2ch5qE5ALi_1ULcG98bRNsS4IPF94w; pt_pin=jd_4b7d68eafa24f; pwdt_id=jd_4b7d68eafa24f; sid=ae4f142080872880b30da89d2872c8ew; thor1=; pin=jd%5F4b7d68eafa24f; wskey=AAFYP9OEAEBC6MESMdfLD8pDfr2lZXMxVg4kPPiNXfOokjXnEaPht0AnwY39u67eL-Dfgd-qTbPq5kvmkiY0a4kvWwjY6mCP; whwswswws=; uuid=010154464953531-AE26AE26AE15'}
        resp = requests.put(url,data=json.dumps(data))
        if resp.text == 'HTTPSQS_PUT_OK':
            print 'OK'

    def test_read_file(self):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        account_txt = os.path.normpath(os.path.join(root_path, '../account/account.txt'))
        file_object = open(account_txt)
        try:
            all_the_text = file_object.readlines()
            for account in all_the_text:
                a = account.split(',')
                print a[0],a[1]
        finally:
            file_object.close()

    def test_rename_file(self):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        account_txt = os.path.normpath(os.path.join(root_path, '../account/account.txt'))
        os.rename(account_txt,os.path.normpath(os.path.join(root_path,'../account/' + str(int(time.time()))+'.txt')))