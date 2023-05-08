########################################################################
# (AWP) Akamai WAF Python based Collector 
# Source: https://github.com/oways/AWP/
########################################################################

from multiprocessing import Process
from lib.conf import *
from lib.collector import collect
from lib.logger import syslog
				
if __name__ == "__main__":

	# redis connection
	redisContext = {"server": redisServer, "port": redisPort, "key": redisKey}

	# Start Query Process
	collector_process = Process(target=collect, args=(redisContext,))
	collector_process.daemon = True
	collector_process.start()

	# Start Query Process
	logger_process = Process(target=syslog, args=(redisContext,))
	logger_process.daemon = True
	logger_process.start()

	# Join
	collector_process.join()
	logger_process.join()

