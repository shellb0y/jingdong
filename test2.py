# -*- coding: utf-8 -*-

import base64
def hex_format_space(data,step=2):
    return ' '.join(data[i:i + 2] for i in range(0, len(data), step))

data = '008F000000000000000100000001000000014E36F77100020006006401110000370000' \
       '000A004800015838108A0040BE45F7E31E2FB63698B422FAEA7670304ADA1E605DB62E49F97' \
       '9795AF5093F6D9457AFB49AB3F76679C9CE6DB0A6CAE90AF1F86D3FEBA8322274EF09C425379' \
       '1000E000800784CE000F099C0001000106A645F36306161663266353938383631'
pin_index = data.find('C00010') + 10
if pin_index == 1:
    print 'NOT FOUND'
pin_hex = data[pin_index:]

pin = ''.join(map(lambda x: chr(int(x, 16)), hex_format_space(pin_hex).split(' ')))
print pin

whwswswws = ''
wssl_start = data.find('1100003700')
if wssl_start == -1:
    print 'whwswswws start index not found'
else:
    wssl_stop = data.find('000A0048')
    if wssl_stop == -1:
        wssl_stop = data.find('000A0058')
        print 'whwswswws stop index not found'
    else:
        whwswswws = data[wssl_start + 10:wssl_stop]

whwswswws = ''.join(map(lambda x: chr(int(x, 16)), hex_format_space(whwswswws).split(' ')))
print whwswswws

wskey_hex = ''

wskey_start = data.find('000A0048')
wskey_stop = data.find('000E')
if wskey_start == -1:
    wskey = data.find('000A0058')
if wskey_start == -1:
    wskey_start = data.find('4163636')
    wskey_hex = data[wskey_start:]
if wskey_start == -1:
    wskey_start = data.find('080019')
    wskey_hex = data[wskey_start + 6:]

wskey_hex = data[wskey_start + 8:wskey_stop]
print hex_format_space(wskey_hex)
wskey_array = map(lambda x: int(x, 16), hex_format_space(wskey_hex).split(' '))
wskey = base64.b64encode(bytearray(wskey_array)).replace('+','-').replace('==','').replace('/','_')
print 'pin=%s; wskey=%s; whwswswws=%s'%(pin,wskey,whwswswws)