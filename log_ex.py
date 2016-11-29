import logstash
import logging.config
import ConfigParser

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("zt")
logger.addHandler(logstash.LogstashHandler('115.28.102.142', 55514))

config = ConfigParser.ConfigParser()

extra = {
    # 'host': 'unknow',
    'program': 'jingdong',
    'device_id':'unkown'
}

try:
    config.readfp(open("private.conf", "r"))
    # extra['host'] = config.get("log", "host")
    extra['device_id'] = config.get("log", "device_id")
except Exception, e:
    pass


def debug(msg):
    logger.debug(msg, extra=extra)


def info(msg):
    logger.info(msg, extra=extra)


def warn(msg):
    logger.warn(msg, extra=extra)


def error(msg):
    logger.error(msg, extra=extra)

