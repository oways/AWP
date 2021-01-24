import os
import configparser
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

#[auth]
edgerc = EdgeRc(config.get('auth', 'edgercpath'))
section = config.get('auth', 'section')

#[offset]
offsetPath="{}/{}".format(baseDir,config.get('offset', 'path'))
offset = config.get('offset', 'value')

#[healthcheck]
healthcheckHook = config.get('healthcheck', 'webhook')
