# -*- coding: utf-8 -*-
import sys
import service

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            service.place_order()
        elif sys.argv[1] == '-spp':
            print 'spp'
        elif sys.argv[1] == '-l':
            service.login_from_api()
        else:
            print 'no support'
    else:
        print 'no support'
