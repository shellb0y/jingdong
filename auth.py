import ctypes
import hashlib
import ctypes
import base64
import time
import base_data
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
login_dll_path = os.path.normpath(os.path.join(root_path, 'libs/login5.6.dll'))
sign_dll_path = os.path.normpath(os.path.join(root_path, 'libs/sign.dll'))

# print login_dll_path,sign_dll_path

d_encrypt_dll = ctypes.windll.LoadLibrary(login_dll_path)
sign_dll = ctypes.windll.LoadLibrary(sign_dll_path)
KEY = "47 44 50 64 46 53 61 6D 74 61 6B 53 67 78 52 64"


def sign(function_id, uuid, body):
    st = str(int(round(time.time() * 1000)))
    data = 'functionId=%s&body=%s&uuid=%s&client=android&clientVersion=5.6.0' % (function_id, body, uuid)
    # print sys.getsizeof(data)
    data_len = len(data) + 17
    mod = data_len % 8
    if mod > 0:
        st = st[:len(st) - mod] + '6583619'[-mod:]
    sign_data_addr = sign_dll.jd_sign(function_id, uuid, body, st)
    sign_data_p = ctypes.c_char_p(sign_data_addr)
    return (sign_data_p.value, st)


def hex_format_space(data):
    return ' '.join(data[i:i + 2] for i in range(0, len(data), 2))


def get_req_data(username, password, jd_uuid, cmd1=2, cmd2=6):
    # jd_uuid = '867323020350896-a086c68dae09'
    username_len = hex(len(username)).replace('0x', '')
    if len(username_len) == 1:
        username_len = '0' + username_len
    account = '00%s%s0020%s' % (username_len, username.encode('hex'), str(
        hashlib.md5(password).hexdigest().encode('hex')))

    account = '000200' + hex(len(account) / 2).replace('0x', '') + account
    device_finger_print = '00040034' + (
        '000a0001000404020020' + hashlib.md5(jd_uuid.split('-')[1] + base_data.get_random_letter_number(7)).hexdigest().upper()).encode('hex')
    device = '0008005d000200640007616e64726f69640005342e342e320005352e342e300008313238302a37323000056a646170700004776966690000001c%s000000010005322e342e300048001100036e6f7800034d693400034d49340000' % (
                 jd_uuid.encode('hex'))
    header = '0YXX0000000000000001000000010000000100000000000%d000%d0064011100' % (cmd1, cmd2)

    data = (header + account + device_finger_print + device).upper()
    length = hex(len(data) / 2).replace('0x', '')

    if len(str(length)) < 3:
        data = data.replace('Y', '0').replace('XX', length)
    else:
        data = data.replace('Y', length[0]).replace('XX', length[1:3])

    encrypt_addr = d_encrypt_dll.Teaencryption(KEY, data)
    encrypt_p = ctypes.c_char_p(encrypt_addr)

    req_data = KEY + ' ' + encrypt_p.value
    req_data_array = map(lambda x: int(x, 16), req_data.split(' '))
    return base64.b64encode(bytearray(req_data_array))


def to_hex_str(s):
    byte = str(hex(ord(s))).replace('0x', '')
    if len(byte) == 1:
        byte = '0' + byte
    return byte


def get_resp_data(resp_data):
    resp_data_array = map(to_hex_str, base64.b64decode(resp_data))
    resp_data_hex = ' '.join(resp_data_array)
    decrypt_addr = d_encrypt_dll.TeaDecrypt(KEY, resp_data_hex)
    decrypt_p = ctypes.c_char_p(decrypt_addr)

    return decrypt_p.value.replace(' ', '')


def get_cookie(resp_data):
    resp_data = get_resp_data(resp_data)
    pin_index = resp_data.find('C00010') + 10
    if pin_index == 1:
        raise ValueError('NOT FOUND')
    pin_hex = resp_data[pin_index:]
    pin = ''.join(map(lambda x: chr(int(x, 16)), hex_format_space(pin_hex).split(' ')))

    whwswswws = ''
    wssl_start = resp_data.find('1100003700')
    if wssl_start == -1:
        raise ValueError('whwswswws start index not found')
        # print 'whwswswws start index not found'
    else:
        wssl_stop = resp_data.find('000A0048')
        if wssl_stop == -1:
            # wssl_stop = resp_data.find('000A0058')
            raise ValueError('whwswswws stop index not found')
            # print 'whwswswws start index not found'
        else:
            whwswswws = resp_data[wssl_start + 10:wssl_stop]

    if whwswswws and whwswswws != '00':
        whwswswws = ''.join(map(lambda x: chr(int(x, 16)), hex_format_space(whwswswws).split(' ')))

    wskey_hex = ''
    wskey_start = resp_data.find('0A0058')
    wskey_stop = resp_data.find('000E')
    if wskey_start == -1:
        wskey_start = resp_data.find('0A0048')
    if wskey_start == -1:
        wskey_start = resp_data.find('4163636')
        wskey_hex = resp_data[wskey_start:]
    if wskey_start == -1:
        wskey_start = resp_data.find('080019')
        wskey_hex = resp_data[wskey_start + 6:]

    if not wskey_hex:
        wskey_hex = resp_data[wskey_start + 6:wskey_stop]
    wskey_array = map(lambda x: int(x, 16), hex_format_space(wskey_hex).split(' '))
    wskey = base64.b64encode(bytearray(wskey_array)).replace('+', '-').replace('==', '').replace('/', '_')
    return 'pin=%s; wskey=%s; whwswswws=%s' % (pin, wskey, whwswswws)


if __name__ == "__main__":
    req_data = get_req_data('jd_60aaf2f598861', 'e4e333', '867323020350896-a086c68dae09')
    print  req_data

    # resp = 'aHLnhbKM9oBtKHz0nVBtCtRI5vdKL0kEJSj85AR8sXiImjeOMj8xF+UhTWTXBgO4XV2QitZNleNzLP34rB0uAFK09+lzAsyuAhgCwXGz5YwkQ4hpnbx8vqwX1ZGaRkE590kX4nsrDFtOFqNklC1FStEKZBNQNrTd1J1hlDqudi7sxmZgh48TLno39B+dPuhP7PpKIkO9JAdoHP9KuVyoWA=='
    # cookie = get_cookie(resp)
    # print  cookie
    #
    # pin = ''.join(map(lambda x: chr(int(x, 16)), hex_format_space('00BF000000000000000100000001000000016256F6710002000600640111770003006F000100770013756E737570706F727465642076657273696F6E0054E8AFB7E58D87E7BAA7E887B3E69C80E696B0E78988E69CACE4BDBFE794A8EFBC88E58D87E7BAA7E8B7AFE5BE84EFBC9AE68891E79A843EE8AEBEE7BDAE3EE585B3E4BA8E3EE6A380E6B58BE69BB4E696B0EFBC89001E0029687474703A2F2F73746F726167652E6A642E636F6D2F6A646D6F62696C652F4A444D616C6C2E61706B').split(' ')))
    # print pin
    #
    resp = '/udsS0mqmpA6L8dkBCJj/yB/3FPykD3ZqAwK4DNOzw6vNPpdYsu9oPr8yvmCIrkcdffcp756Vjf420/Xyc4b1dYzvqsEd3DeQByOl+lLLeoYIvxH2uTgpc75As/nQha2rcxtAyFGRsJEs17SpZP/tu0zz1Tzwho+jJqAWkjEHkWfI6jpeJnKE+KZGOvk1kegM43Wu3D3cvE='
    cookie = get_cookie(resp)
    print  cookie
    #
    # sign_data = sign('newUserInfo', base_data.get_random_number() + '-' + base_data.get_random_letter_number(12),
    #                  '{"flag":"nickname"}')
    # print sign_data
