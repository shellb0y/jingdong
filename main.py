# -*- coding: utf-8 -*-
import sys
import service
import phone_charge_sevice

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            service.place_order()
        elif sys.argv[1] == '-spc--s':
            phone_charge_sevice.sync_status_from_jd()
        elif sys.argv[1] == '-spc':
            phone_charge_sevice.phone_charge()
        elif sys.argv[1] == '-l':
            service.login_from_api()
        else:
            print 'no support'
    else:
        print 'no support'
