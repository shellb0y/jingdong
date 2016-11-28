import ctypes

dll = ctypes.windll.LoadLibrary('libs/sign5.3.0.dll')
# test  = dll.login
# test.restypes = ctypes.c_char_p
#
# cookie = test('18445755374','6a97an')
# a=ctypes.c_char_p(cookie)
# print a.value

st=ctypes.create_string_buffer('0'*13)
# test  = dll.jd_sign
# test.rest

sBuf = b'0'
pStr = ctypes.c_char_p()
pStr.value = sBuf

test = dll.jd_sign
# test.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
sign = test('newUserInfo', 'dsfdsfdsfdsfdsfds', '{"flag":"nickname"}', pStr)
print st.value
print sign
