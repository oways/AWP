########################################################################
# (AWP) Akamai WAF Python based Collector 
# Source: https://github.com/oways/AWP/
########################################################################

import base64
import logging
import time
from logging.handlers import SysLogHandler
from .conf import *
import redis

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=(1048576*5), backupCount=1)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log(e, type='error'):
	if type == 'debug':
		logger.debug(str(e))
	else:
		logger.error(str(e))

def decoder(data):
	data = data.decode('utf-8')
	return base64.b64decode(data).decode('utf-8')

def sendSyslog(data):
	mylogger = logging.getLogger('AWP_Collector')
	mylogger.setLevel(logging.INFO)
	handler = SysLogHandler(address = (syslogHost, syslogPort), facility=SysLogHandler.LOG_LOCAL5)
	# Log format
	formatter = logging.Formatter('%(message)r')
	handler.setFormatter(formatter)
	mylogger.addHandler(handler)
	mylogger.info(data)
	if debug:
		log('Syslog sent', 'debug')
	time.sleep(0.005)

def syslog(redisContext):
	# Connect to Redis
	R = redis.Redis(host=redisContext['server'], port=redisContext['port'])
	while True:
		try:
			data = R.lpop(redisContext['key'])
			if data:
				if debug:
					log(data,'debug')
				sendSyslog(decoder(data))
		except Exception as e:
			log(e)

