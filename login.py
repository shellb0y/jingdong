import ctypes
import hashlib
import ctypes
import base64
import binascii

d_encrypt = ctypes.windll.LoadLibrary( 'libs/login.dll' )
KEY = "47 44 50 64 46 53 61 6D 74 61 6B 53 67 78 52 64"

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hex_format_space(self,data):
        return ' '.join(data[i:i+2] for i in range(0, len(data), 2))

    def get_req_data(self,cmd1=2,cmd2=6):
        jd_uuid = '867323020350896-a086c68dae09'
        account = '00%s%s0020%s' % (hex(len(self.username)).replace('0x',''), self.username.encode('hex'), str(
            hashlib.md5(self.password).hexdigest().encode('hex')))
        account = '000200' + hex(len(account)/2).replace('0x','') + account
        device_finger_print = '00040034' + ('000a0001000402020020' + hashlib.md5('a086c68dae09###ss').hexdigest().upper()).encode('hex')
        device = '0008005d000200640007616e64726f69640005342e342e320005352e312e300008313238302a37323000056a64617070000' \
                 '4776966690000001c%s000000010005312e342e320048001100036e6f7800034d693400034d49340000' %(jd_uuid.encode('hex'))
        header = '0YXX0000000000000001000000010000000100000000000%d000%d0064011100' % (cmd1, cmd2)

        data = (header + account + device_finger_print + device).upper()
        length = hex(len(data)/2).replace('0x','')

        if length <= 256:
            data = data.replace('Y','0').replace('XX',length)
        else:
            data = data.replace('Y',length[0]).replace('XX',length[1:3])

        encrypt_addr = d_encrypt.Teaencryption(KEY, data)
        encrypt_p = ctypes.c_char_p(encrypt_addr)

        req_data = KEY + ' ' +  encrypt_p.value
        req_data_array = map(lambda x: int(x, 16), req_data.split(' '))
        return  base64.b64encode(bytearray(req_data_array))

    def get_resp_data(self,resp_data):
        pass

login = Login('jd_60aaf2f598861', 'e4e333')
req_data = login.get_req_data()
print  req_data

resp = 'aHLnhbKM9oBtKHz0nVBtCtRI5vdKL0kEJSj85AR8sXiImjeOMj8xF+UhTWTXBgO4XV2QitZNleNzLP34rB0uAFK09+lzAsyuAhgCwXGz5YwkQ4hpnbx8vqwX1ZGaRkE590kX4nsrDFtOFqNklC1FStEKZBNQNrTd1J1hlDqudi7sxmZgh48TLno39B+dPuhP7PpKIkO9JAdoHP9KuVyoWA=='
data= bytearray(base64.b64decode(resp))
print data