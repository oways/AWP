########################################################################
# (AWP) Akamai WAF Python based Collector 
# Source: https://github.com/oways/AWP/
########################################################################

import requests
from akamai.edgegrid import EdgeGridAuth
from datetime import datetime
import json
import base64
import urllib.parse
import time
from .conf import *
import redis
from .logger import log

def decoder(data):
	return str(base64.b64decode(urllib.parse.unquote(data)))

def encoder(message):
	return base64.b64encode(str(message).encode()).decode()

def urldecoder(data):
	return str(urllib.parse.unquote(data))

# Decoding base64 values
def decodeData(j):
	j['attackData']['rules'] =  decoder(j['attackData']['rules'])
	j['attackData']['ruleVersions'] =  decoder(j['attackData']['ruleVersions'])
	j['attackData']['ruleMessages'] =  decoder(j['attackData']['ruleMessages'])
	j['attackData']['ruleTags'] =  decoder(j['attackData']['ruleTags'])
	j['attackData']['ruleData'] =  decoder(j['attackData']['ruleData'])
	j['attackData']['ruleSelectors'] =  decoder(j['attackData']['ruleSelectors'])
	j['attackData']['ruleActions'] =  decoder(j['attackData']['ruleActions'])
	j['httpMessage']['requestHeaders'] =  urldecoder(j['httpMessage']['requestHeaders'])
	j['httpMessage']['responseHeaders'] =  urldecoder(j['httpMessage']['responseHeaders'])
	return j

def collect(redisContext):
	# Updating current timestamp
	currentTS = str(round(datetime.now().timestamp()))
	# Connect to Redis
	R = redis.Redis(host=redisContext['server'], port=redisContext['port'])
	# Akamai auth
	s = requests.Session()
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	while True:
		try:
			# continue from last fetch
			offset = R.get('offset')
			if offset:
				offset = offset.decode("utf-8")
			url = 'https://{}/siem/v1/configs/{}?offset={}&from={}&to={}&limit={}'.format(edgerc.get(section, 'host'),configIds,offset,firstTS,currentTS,limit)
			result = s.get(url)
			content = result.content.decode("utf-8")
			data = []
			lines = content.splitlines()
			lastLine =  json.loads(lines[len(lines)-1])
			for l in lines[:-1]:
				j = json.loads(l)
				tags = decoder(j['attackData']['ruleTags'])
				# Filtering logs for only builtin Akamai web attacks and polices (ex. sqli, xss & rce)
				for f in filter:
					if f in tags:
						data.append(decodeData(j))
						break
			# update new offset in redis
			R.set('offset', lastLine['offset'])
			# Store in redis
			for d in data:
				if debug:
					log(f"Added to redis: {d['httpMessage']['requestId']}", 'debug')
				R.rpush(redisContext['key'], encoder(d))
			time.sleep(5)
		except Exception as e:
				log(e)
				
