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

def decoder(data):
	data = data.decode('utf-8')
	return base64.b64decode(data).decode('utf-8')

def sendSyslog(data, logger):
	syslogger = logging.getLogger('AWP')
	syslogger.setLevel(logging.INFO)
	handler = SysLogHandler(address = (syslogHost, syslogPort), facility=SysLogHandler.LOG_LOCAL5)
	# Log format
	formatter = logging.Formatter('%(message)r')
	handler.setFormatter(formatter)
	syslogger.addHandler(handler)
	syslogger.info(data)
	if debug:
		logger.debug('Syslog sent', 'debug')
	time.sleep(0.005)

def syslog(redisContext,logger):
	# Connect to Redis
	R = redis.Redis(host=redisContext['server'], port=redisContext['port'])
	while True:
		try:
			data = R.lpop(redisContext['key'])
			if data:
				if debug:
					logger.debug(data,'debug')
				sendSyslog(decoder(data),logger)
		except Exception as e:
			logger.error(e)

