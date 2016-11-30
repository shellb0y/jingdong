import base_data
import log_ex as logger
import requests
import json
import traceback
from time import ctime, sleep
import argparse
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            print 'exe'
        elif sys.argv[1] == '-spp':
            print 'spp'
        else:
            print 'no support'
    else:
        print 'no support'