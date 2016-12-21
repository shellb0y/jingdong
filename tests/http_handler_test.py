# -*- coding: utf-8 -*-
import http_handler
import unittest
import json
import os
import log_ex as logger
import base_data


class httpHandlerTest(unittest.TestCase):
    def setUp(self):
        # self.uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
        # self.user_agent = base_data.get_user_agent()
        self.name = 'jd_60aaf2f598861'
        self.pwd = 'e4e333'
        self.uuid = '823466913984714-pgveoceqje9l'
        self.user_agent = 'Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba'

    def test_login_get_cookie(self):
        login = http_handler.login.Login(self.name, self.pwd, self.uuid, self.user_agent)
        cookie = login.get_cookie()
        print  cookie

        # 'pin=jd_6c83b7ced8f82; wskey=AAFYPqedAEB0jJpekbc2xrHYpXq23i8kZnjOdUlQe622prlRwbc75dQJI-j0H4-LOrvk6HXQbMcwZmokvl-vfNengScS8l-A; whwswswws= '

    def test_get_h5_cookie(self):
        login = http_handler.login.Login(self.name, self.pwd, self.uuid, self.user_agent)
        cookie = login.get_h5_cookie('pin=jd_79cf9db2ba962; wskey=AAFYP6NbAEBwRKUgACTrxuiT5KxQzGwR7EJloNamFpbnZ48EQV3JJD69P59ZDVVHJ6ArP8jb62j6dE-rrTZD9StYikwGjixP; whwswswws=')
        print  cookie

    def test_add_passenger(self):
        train = {
            "data": "{\"module\":{\"worker\":[{\"assembly\":\"FBServer.Order.TrainJD.Order_TrainJD,FBServer.Order.TrainJD.dll,1.0.0.0\",\"type\":0,\"parms\":null}]," \
                    "\"payer\":null},\"sessionId\":null,\"data\":{\"ticketsInfo\":[{\"coachNo\":\"K582\",\"departure\":\"新余\",\"dptStation\":\"XUG\",\"destination\":" \
                    "\"绍兴\",\"arrStation\":\"SOH\",\"dptDate\":\"2016-12-24\",\"dptTime\":\"\",\"ticketPrice\":102.0000,\"optionType\":1}],\"contactInfo\":{\"name\":" \
                    "\"唐元康\",\"IDCard\":\"522624199409150011\",\"mobileNo\":\"18902440756\"},\"passengersInfo\":[" \
                    "{\"name\":\"唐元康\",\"IDType\":\"1\",\"IDCard\":\"522624199409150011\",\"mobileNo\":\"18902440756\"}," \
                    "{\"name\":\"陈丽茹\",\"IDType\":\"1\",\"IDCard\":\"210703195010243428\",\"mobileNo\":\"18902440756\"}," \
                    "{\"name\":\"孙会利\",\"IDType\":\"1\",\"IDCard\":\"610525198802140449\",\"mobileNo\":\"18902440756\"}," \
                    "{\"name\":\"高光\",\"IDType\":\"1\",\"IDCard\":\"320113195401294818\",\"mobileNo\":\"18902440756\"}" \
                    "],\"count\":1,\"exData1\":\"1\",\"exData2\":{\"user\":\"18445987832\",\"pwd\":\"3128q8\",\"couponid\":\"7865961648\",\"cookie\":\"TrackID=1igYV_nR-c1Xcn31vmHpGSbbKCb2NiIfKYWDh2bffSAagoa0MtilxlZRGCg-dyBkS1fJQUS66VSnBQeMQfJqFHcWnie1yo0-jFy7_n93gRE0;pinId=4DRXx_1ixkgpVC1gDXfQprV9-x-f3wj7;pin=jd_4a84ed835a56c;unick=jd_184459pvw;thor=2CE5F863693E279BBC34C2CA7E5B28542A5E68AB73B0419509C1E35E2AB7C30C47793B7DAD2843F4443F14880C646CD4D046DD6B88DDF255909FD11384D5AFB231EAA96F3D1C7A8C7AF8DF9B2D2C520244FC2A26B80F25236B82736B4F66130DAF9E42818D072EC2C7C1476454F4C555E1F7E32E7A8EB78517FA3DC6D379C069813778561C2199C3DA47F9004E056E12733E860DC5390C9286AADEB22410B280;_tp=GPoeuUizCLMXDKCXARIR9ZGFMBf9OusAvE24ytdi7vI%3D;logining=1;_pst=jd_4a84ed835a56c;ceshi3.com=pbv0P2fT7tjeyVIT5vWMFaT4wXNcWW3TB5ox3GKDDAQs2weUyZIcMPIXX4T0lcA_;JSESSIONID=C3B6CE6CC42A2708A45B9DD122DDF549.s1;alc=4eRYpTSYCROtwVTVz9MuNg==;mp=18445987832;ol=1\",\"orderUser\":\"system\",\"taskType\":1},\"fee\":0}}",
            "order_id": "44fe848464944b79b126c07349d89f96"}
        data = json.loads(train['data'])
        cookie = {'mobilev': 'touch',
                  'pt_key': 'app_openAAFYPqqjADCO0ZuYk8Bm87ZIFFfyVY1E4W52WnX5mYCjkfUiG4_Ilav_G5_juxSxj4_9uLaw5Vc',
                  'pwdt_id': 'jd_6c83b7ced8f82', 'sid': '11d5ed824ad3ed57ebae72000f62d1fw',
                  'guid': 'e50917141b0a2b4070d176e69b9ed64e2f016b58ca59e25c44dca391d636429e',
                  'pt_pin': 'jd_6c83b7ced8f82'}
        order = http_handler.order.Order(self.uuid, self.user_agent, cookie)
        print order.add_passenger(data['data']['passengersInfo'])

    def test_order_submit(self):
        train = {
            "data": "{\"module\":{\"worker\":[{\"assembly\":\"FBServer.Order.TrainJD.Order_TrainJD,FBServer.Order.TrainJD.dll,1.0.0.0\",\"type\":0,\"parms\":null}],\"payer\":null},\"sessionId\":null,\"data\":{\"ticketsInfo\":[{\"coachNo\":\"K582\",\"departure\":\"新余\",\"dptStation\":\"XUG\",\"destination\":\"绍兴\",\"arrStation\":\"SOH\",\"dptDate\":\"2016-12-24\",\"dptTime\":\"\",\"ticketPrice\":102.0000,\"optionType\":1}],\"contactInfo\":{\"name\":\"唐元康\",\"IDCard\":\"522624199409150011\",\"mobileNo\":\"18902440756\"},\"passengersInfo\":[{\"name\":\"唐元康\",\"IDType\":\"1\",\"IDCard\":\"522624199409150011\",\"mobileNo\":\"18902440756\"}],\"count\":1,\"exData1\":\"1\",\"exData2\":{\"user\":\"18445987832\",\"pwd\":\"3128q8\",\"couponid\":\"7865961648\",\"cookie\":\"TrackID=1igYV_nR-c1Xcn31vmHpGSbbKCb2NiIfKYWDh2bffSAagoa0MtilxlZRGCg-dyBkS1fJQUS66VSnBQeMQfJqFHcWnie1yo0-jFy7_n93gRE0;pinId=4DRXx_1ixkgpVC1gDXfQprV9-x-f3wj7;pin=jd_4a84ed835a56c;unick=jd_184459pvw;thor=2CE5F863693E279BBC34C2CA7E5B28542A5E68AB73B0419509C1E35E2AB7C30C47793B7DAD2843F4443F14880C646CD4D046DD6B88DDF255909FD11384D5AFB231EAA96F3D1C7A8C7AF8DF9B2D2C520244FC2A26B80F25236B82736B4F66130DAF9E42818D072EC2C7C1476454F4C555E1F7E32E7A8EB78517FA3DC6D379C069813778561C2199C3DA47F9004E056E12733E860DC5390C9286AADEB22410B280;_tp=GPoeuUizCLMXDKCXARIR9ZGFMBf9OusAvE24ytdi7vI%3D;logining=1;_pst=jd_4a84ed835a56c;ceshi3.com=pbv0P2fT7tjeyVIT5vWMFaT4wXNcWW3TB5ox3GKDDAQs2weUyZIcMPIXX4T0lcA_;JSESSIONID=C3B6CE6CC42A2708A45B9DD122DDF549.s1;alc=4eRYpTSYCROtwVTVz9MuNg==;mp=18445987832;ol=1\",\"orderUser\":\"system\",\"taskType\":1},\"fee\":0}}",
            "order_id": "44fe848464944b79b126c07349d89f96"}
        data = json.loads(train['data'])

        passenger_id = ['1221203', '1218390']
        cookie = {'mobilev': 'touch',
                  'pt_key': 'app_openAAFYP4yaADCYJ7Pb_2BuI-EDKqKgFMaVygFFLlylRVUPVssKQy5Ee0pDm4QQ0qOTx15duxGCjyw',
                  'pwdt_id': 'jd_6c83b7ced8f82', 'sid': '80e6a4c9b38d29d0e5b512511700694w',
                  'guid': 'fa4e006bb1d73e8b5bdebf0ceef24d352abd911c16f95e3056a457b3f774ad9f',
                  'pt_pin': 'jd_6c83b7ced8f82'}
        order = http_handler.order.Order(self.uuid, self.user_agent, cookie)
        order_data = order.gen_order(data, passenger_id)
        print order_data

        order_data = order.get_token(order_data)
        print order_data['token']

        couponid = ''
        couponPrice = ''

        if data['data']['exData2'].has_key('couponid'):
            couponid = data['data']['exData2']['couponid']
        if data['data']['exData2'].has_key('couponPrice'):
            couponPrice = data['data']['exData2']['couponPrice']

        if not (couponid and couponPrice):
            couponid = couponPrice = ''

        order_data['couponid'] = couponid
        order_data['couponPrice'] = couponPrice

        order.submit(order_data)

    def test_get_order_details(self):
        cookie = {'mobilev': 'touch',
                  'pt_key': 'app_openAAFYP4yaADCYJ7Pb_2BuI-EDKqKgFMaVygFFLlylRVUPVssKQy5Ee0pDm4QQ0qOTx15duxGCjyw',
                  'pwdt_id': 'jd_6c83b7ced8f82', 'sid': '80e6a4c9b38d29d0e5b512511700694w',
                  'guid': 'fa4e006bb1d73e8b5bdebf0ceef24d352abd911c16f95e3056a457b3f774ad9f',
                  'pt_pin': 'jd_6c83b7ced8f82'}
        order = http_handler.order.Order(self.uuid, self.user_agent, cookie)
        print order.get_details(1252297)
