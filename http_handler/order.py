import auth

import re
file_object = file('order_submit_response','rb')
try:
     all_the_text = file_object.read()
     token = re.findall(r'<input type="hidden" name="token" value="(\w+)" />',all_the_text)
     if token:
         print token[0]
finally:
     file_object.close( )