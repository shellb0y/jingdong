import requests
import auth
import json
import log_ex as logger


def get_cookie(name, pwd, uuid, headers={'User-Agent': 'Android WJLoginSDK 1.4.2'}):
    logger.debug('get-cookie[get_req_data]:%s %s %s' % (name, pwd, uuid))
    url = 'http://wlogin.m.jd.com/applogin_v2'
    data = auth.get_req_data(name, pwd, uuid)

    logger.debug('POST %s\n%s\n%s' % (url, data, json.dumps(headers)))
    resp = requests.post(url, data=data, headers=headers)
    resp_text = resp.text
    logger.debug('resp: %s' % (resp_text))

    try:
        cookie = auth.get_cookie(resp_text)
        return cookie
    except Exception, e:
        raise Exception('cookie parse error', e)
