########################################################################
# (AWP) Akamai WAF Python based Collector 
# Author: https://github.com/oways 
########################################################################

import requests
from akamai.edgegrid import EdgeGridAuth
from datetime import datetime
import json
import base64
import urllib.parse
import logging
import time
from os import path
from logging.handlers import SysLogHandler
from conf import syslogHost, syslogPort, firstTS, configIds, limit, edgerc, section, offset, offsetPath, healthcheckHook

# Updating current timestamp
currentTS = str(round(datetime.now().timestamp()))

# Continue from last offset
if path.exists(offsetPath):
	with open(offsetPath,"r+") as f:
		offset = f.readline()

def healthCheck():
	if healthcheckHook:
		try:
			requests.get(healthcheckHook,verify=False)
		except Exception as e:
			print(e)

def decoder(data):
	return str(base64.b64decode(urllib.parse.unquote(data)))

def urldecoder(data):
	return str(urllib.parse.unquote(data))

def sendSyslog(data):
	mylogger = logging.getLogger('AWP_Collector')
	mylogger.setLevel(logging.INFO)
	handler = SysLogHandler(address = (syslogHost,syslogPort), facility=SysLogHandler.LOG_LOCAL5)
	# Log format
	formatter = logging.Formatter('%(message)r')
	handler.setFormatter(formatter)
	mylogger.addHandler(handler)
	for message in data:
		mylogger.info(message)
		time.sleep(0.005)

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

def main():
	s = requests.Session()
	# Akamai auth
	s.auth = EdgeGridAuth.from_edgerc(edgerc, section)
	url = 'https://{}/siem/v1/configs/{}?offset={}&from={}&to={}&limit={}'.format(edgerc.get(section, 'host'),configIds,offset,firstTS,currentTS,limit)
	result = s.get(url)
	content = result.content.decode("utf-8")
	data = []
	lines = content.splitlines()
	lastLine =  json.loads(lines[len(lines)-1])
	for l in lines[:-1]:
		try:
			j = json.loads(l)
			tags = decoder(j['attackData']['ruleTags'])
			# Filtering logs for only builtin Akamai web attacks and polices (ex. sqli, xss & rce)
			if "WEB_ATTACK" in tags or "/POLICY/" in tags:
				data.append(decodeData(j))
		except Exception as e:
			print(e)

	with open(offsetPath,"w+") as f:
		f.write(lastLine['offset'])

	# Send data to syslog server
	sendSyslog(data)
	# Checking if every thing went will
	healthCheck()

if __name__ == "__main__":
	main()
