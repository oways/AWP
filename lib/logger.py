########################################################################
# (AWP) Akamai WAF Python based Collector 
# Source: https://github.com/oways/AWP/
########################################################################

import base64
import time
from .conf import *
import redis

def decoder(data):
	data = data.decode('utf-8')
	return base64.b64decode(data).decode('utf-8')

def sendSyslog(data, logger, syslogger):
	syslogger.info(data)
	logger.debug('Syslog sent')
	time.sleep(0.005)

def syslog(redisContext, logger, syslogger):
	# Connect to Redis
	R = redis.Redis(host=redisContext['server'], port=redisContext['port'])
	while True:
		try:
			data = R.lpop(redisContext['key'])
			if data:
				logger.debug(data)
				sendSyslog(decoder(data), logger, syslogger)
		except Exception as e:
			logger.error(e)

