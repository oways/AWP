########################################################################
# (AWP) Akamai WAF Python based Collector 
# Source: https://github.com/oways/AWP/
########################################################################

import configparser
import os
from akamai.edgegrid import EdgeRc

# Getting BaseDir
baseDir = os.path.abspath(os.getcwd())

# Read Config
config = configparser.ConfigParser()
config.read(baseDir + "/conf/collector.conf")

#[syslog]
syslogHost = config.get('syslog', 'host')
syslogPort = config.get('syslog', 'port')

#[params]
firstTS = config.get('params', 'start_timestamp')
configIds = config.get('params', 'config_id')
limit = config.get('params', 'limit')
filter = config.get('params', 'filter')

#[auth]
edgerc = EdgeRc(config.get('auth', 'edgercpath'))
section = config.get('auth', 'section')

#[redis]
redisServer = config.get('redis', 'server')
redisKey = config.get('redis', 'key')
redisPort = config.get('redis', 'port')

#[log]
logfile = config.get('log', 'logfile')
debug = config.get('log', 'debug')