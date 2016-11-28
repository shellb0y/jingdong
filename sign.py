import ctypes
import time
import base_data

sign_dll = ctypes.windll.LoadLibrary( 'libs/sign5.3.0.dll' )

def sign(functionId,uuid,body):
    st = str(time.time()).replace('.', '')
    sign_data_addr = sign_dll.jd_sign(functionId,uuid,body,st)
    sign_data_p = ctypes.c_char_p(sign_data_addr)
    return sign_data_p.value

if __name__=="__main__":
    sign_data = sign('newUserInfo',base_data.get_random_number()+'-'+base_data.get_random_letter_number(12),'{"flag":"nickname"}')
    print sign_data