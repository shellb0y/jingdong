# -*- coding: utf-8 -*-
# import ctypes
#
# dll = ctypes.windll.LoadLibrary('libs/sign5.3.0.dll')
# test  = dll.login
# test.restypes = ctypes.c_char_p
#
# cookie = test('18445755374','6a97an')
# a=ctypes.c_char_p(cookie)
# print a.value

# st=ctypes.create_string_buffer('0'*13)
# test  = dll.jd_sign
# test.rest

# sBuf = b'0'
# pStr = ctypes.c_char_p()
# pStr.value = sBuf
#
# test = dll.jd_sign
# # test.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
# sign = test('newUserInfo', 'dsfdsfdsfdsfdsfds', '{"flag":"nickname"}', pStr)
# print st.value
# print sign

# a='cheCi=G5&seatType=edz&seatPrice=55300&fromStationCode=VNP&fromStationName=%E5%8C%97%E4%BA%AC%E5%8D%97&toStationCode=AOH&toStationName=%E4%B8%8A%E6%B5%B7%E8%99%B9%E6%A1%A5&trainDate=1480435200000&passengerIds=1204607&contact=%E5%90%B4%E5%8B%87%E5%88%9A&phone=13978632546&realBook=1&account=&password='
# a_ = a.split('&')
# data = {}
# for t in a_:
#     _t = t.split('=')
#     data[_t[0]]=_t[1]
#
# print data

# import re
#
# file_object = open('order_submit_response')
# try:
#      all_the_text = file_object.read( )
#      onlinePayFee = re.findall(r'<input type="hidden" name="onlinePayFee" value="(.*)"/>', all_the_text)
#
#      print onlinePayFee
# finally:
#      file_object.close( )

# import base64
# def to_hex_str(s):
#     byte = str(hex(ord(s))).replace('0x', '')
#     if len(byte) == 1:
#         byte = '0' + byte
#     return byte
#
# def hex_format_space(data):
#     return ' '.join(data[i:i + 2] for i in range(0, len(data), 2))
#
# a=15963256325
# print hex(a)
# hex = hex_format_space(str(a).encode('hex'))
#
# print str(a).encode('hex')
#
# req_data_array = map(lambda x: int(x, 16), hex.split(' '))
# # print req_data_array
# print base64.b64encode(bytearray(req_data_array))
#
# b = 't+itDImrWSiR\/V6gD6ei8A=='
# c = base64.b64decode(b)
# print c.encode('hex')
#
# import datetime
# print str(datetime.datetime.now())
#
# import time
# _from = int(time.mktime(time.strptime('2016-12-20 14:50:00','%Y-%m-%d %H:%M:%S')))
# t = time.time()
# _to = int(t)
# print  _to-_from < 15*60
#
# i=1
# print ++i


import ctypes
import hashlib
import ctypes
import base64
import time
import base_data
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
login_dll_path = os.path.normpath(os.path.join(root_path, '../libs/login5.6.dll'))

# print login_dll_path,sign_dll_path

print login_dll_path
d_encrypt_dll = ctypes.windll.LoadLibrary(login_dll_path)
encrypt_addr = d_encrypt_dll.Teaencryption("47 44 50 64 46 53 61 6D 74 61 6B 53 67 78 52 64", "01 05 00 00 00 00 00 00 00 01 00 00 00 01 00 00 00 01 00 00 00 00 00 02 00 06 00 64 01 11 00 00 02 00 34 00 10 6A 64 5F 33 30 70 32 31 36 31 32 31 36 30 69 37 00 20 66 30 37 32 39 33 39 36 34 65 63 37 36 38 35 34 66 35 32 31 61 32 65 33 33 30 61 38 65 62 32 62 00 04 00 34 30 30 30 61 30 30 30 31 30 30 30 34 30 34 30 32 30 30 32 30 30 43 43 43 43 35 43 35 36 33 45 44 31 44 32 31 36 41 37 36 33 34 33 38 46 33 36 38 45 30 36 43 00 08 00 5D 00 02 00 64 00 07 61 6E 64 72 6F 69 64 00 05 34 2E 34 2E 32 00 05 35 2E 34 2E 30 00 08 31 32 38 30 2A 37 32 30 00 05 6A 64 61 70 70 00 04 77 69 66 69 00 00 00 1C 38 36 37 33 32 33 30 32 30 33 35 30 38 39 36 2D 61 30 38 36 63 36 38 64 61 65 30 39 00 00 00 01 00 05 32 2E 34 2E 30 00 48 00 11 00 03 6E 6F 78 00 03 4D 69 34 00 03 4D 49 34 00 00")
encrypt_p = ctypes.c_char_p(encrypt_addr)
print encrypt_p.value

decrypt_addr = d_encrypt_dll.TeaDecrypt("47 44 50 64 46 53 61 6D 74 61 6B 53 67 78 52 64", "B8 8F 67 8C 11 96 48 F8 D6 EE 70 BA F6 8C B8 52 9B 40 88 67 45 CF DC 51 5D 61 0D 51 6F ED A2 6C B6 C6 C8 D9 6C 0D 2A F9 8C C7 B4 99 83 1F ED D5 35 6A 16 E7 36 32 BE FB 45 73 7C 63 18 25 50 B7 10 15 EA 55 B3 B4 D6 CC 04 C3 B9 8D 62 2E AB DF 47 3C 48 0B 81 28 62 76 29 5C 59 E9 4C 3C DA 93 FF FD E5 4B 07 D0 A4 B1 80 9E 97 72 BB 4B 28 C0 9D 75 80 DF 06 01 E5 57 12 E5 BC CA 78 6A C4 30 D5 F2 DB 47 27 8E 07 BE 7F 88 8E 1D 41 B2 03 2E D6 14 74 AB 3C DA 23 7D")
decrypt_p = ctypes.c_char_p(decrypt_addr)
print decrypt_p.value

import requests
resp = requests.get(
                        'http://115.29.79.63:9000/api/Cookie/Get?username=%s&password=%s' % ('1321321321', '321321321'),
                        timeout=1)