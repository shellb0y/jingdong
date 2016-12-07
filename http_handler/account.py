import requests
import log_ex as logger
import base_data
import http_handler
import json
import time
import traceback
import adsl


# {"smobile":"13585468575","syzm":"598756"}
def getFromHttpSqs(adsl):
    # url = 'http://vooaa.cn:98/give.do?pw=2985256&number=1'
    url = 'http://139.199.65.115:1218/?name=jd_wait_login&opt=get&auth=Fb@345!'
    logger.info('GET %s' % url)
    resp = requests.get(url)
    if resp.text == 'HTTPSQS_GET_END':
        time.sleep(5)
        return None

    _account = resp.json()

    logger.info('resp: %s' % json.dumps(_account))
    if not _account:
        return

    account = {'username': _account['username'], 'password': _account['password'], 'valid': 0, 'cookie': '',
               'h5_cookie': ''}
    logger.info('uname:%s,pwd:%s,login...' % (account['username'], account['password']))
    uuid = base_data.get_random_number() + '-' + base_data.get_random_letter_number(12).lower()
    user_agent = base_data.get_user_agent()

    adsl.reconnect()

    try:
        login = http_handler.login.Login(account['username'], account['password'], uuid, user_agent)
        cookie = login.get_cookie()
        logger.info('login success,cookie:%s' % cookie)
        account['cookie'] = cookie

        h5_cookie = login.get_h5_cookie(cookie)
        logger.info('get h5 cookie:%s' % h5_cookie)

        cookie = 'pt_key=%s;pwdt_id=%s;sid=%s;guid=%s;pt_pin=%s;mobilev=%s' % (
            h5_cookie['pt_key'], h5_cookie['pwdt_id'], h5_cookie['sid'], h5_cookie['guid'],
            h5_cookie['pt_pin'], h5_cookie['mobilev'])

        account['h5_cookie'] = cookie
        account['valid'] = 1
    except Exception, e:
        logger.error('login faild\n%s' % traceback.format_exc())

    # while True:
    #     try:
    #         resp = requests.get('http://vooaa.cn:98/update.do?smobile=%s&nstatus=%d&pw=46hg6u6' % (
    #             account['username'], account['valid']))
    #         if resp.text == 'ok':
    #             logger.info('callback success')
    #         else:
    #             logger.info('callback faild:%s' % resp.text)
    #
    #         resp = requests.post('http://115.28.102.142:8000/api/mobilepay/account/jd_login_api',
    #                              data=json.dumps(account), headers={'Content-Type': 'application/json'})
    #         if resp.text:
    #             logger.info('save account success')
    #             break
    #     except Exception, e:
    #         time.sleep(180)

    return account
