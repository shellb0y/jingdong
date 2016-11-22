import ctypes
import hashlib


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getReqData(self,cmd1,cmd2):
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

        print data


def encipher(v, k):
    y = ctypes.c_int32(v[0])
    z = ctypes.c_int32(v[1])
    sum = ctypes.c_int32(0)
    delta = 0x61c88647
    n = 16
    w = [0, 0]

    while n > 0:
        y.value += z.value << 4 ^ z.value >> 5 + sum.value ^ z.value + k[sum.value & 3]
        sum.value -= delta
        z.value += y.value << 4 ^ y.value >> 5 + sum.value ^ y.value + k[sum.value >> 11 & 3]
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w

login = Login('zt.freedom@gmail.com', '000000')
print login.getReqData(2,6)