import os
import time


class Adsl(object):
    def __init__(self,adsl_account):
        self.name = adsl_account["name"]
        self.username = adsl_account["username"]
        self.password = adsl_account["password"]

    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)

    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)

    def reconnect(self):
        self.disconnect()
        self.connect()
