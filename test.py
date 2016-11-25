import ctypes
dll = ctypes.windll.LoadLibrary( 'libs/haoe_jd_for_e.dll' )
test  = dll.login
test.restypes = ctypes.c_char_p

cookie = test('18445755374','6a97an')
a=ctypes.c_char_p(cookie)
print a.value