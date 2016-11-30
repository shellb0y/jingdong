import logstash
import logging.config
import ConfigParser
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
logging_conf_path = os.path.normpath(os.path.join(root_path, 'logging.conf'))

logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger("zt")
logger.addHandler(logstash.LogstashHandler('115.28.102.142', 55514))

config = ConfigParser.ConfigParser()

extra = {
    # 'host': 'unknow',
    'program': 'jingdong',
    'device_id':'unkown'
}

try:
    private_conf_file = os.path.normpath(os.path.join(root_path, 'private.conf'))
    config.readfp(open(private_conf_file, "r"))
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

