########################################################################
# (AWP) Akamai WAF Python based Collector 
# Source: https://github.com/oways/AWP/
########################################################################

from multiprocessing import Process
from lib.conf import *
from lib.collector import collect
from lib.logger import syslog
import logging

if __name__ == "__main__":

	# logger init
	logger = logging.getLogger("AWP")
	if debug == 'On':
		logger.setLevel(logging.DEBUG)
	else:
		logger.setLevel(logging.ERROR)
	handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=(1048576*5), backupCount=1)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# redis connection
	redisContext = {"server": redisServer, "port": redisPort, "key": redisKey}

	# Start Query Process
	collector_process = Process(target=collect, args=(redisContext,logger))
	collector_process.daemon = True
	collector_process.start()

	# Start Query Process
	logger_process = Process(target=syslog, args=(redisContext,logger))
	logger_process.daemon = True
	logger_process.start()

	# Join
	collector_process.join()
	logger_process.join()

