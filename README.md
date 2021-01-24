## AWP

### What's Akamai WAF Python based Collector (AWP):

Connector shipping logs from Akamai WAF to SEIM solutions using syslog.

## How to use AWP?

```

git clone https://github.com/oways/AWP.git

pip3 install -r ruquirements.txt

# Modify the configuration file details
vim /path/conf/collector.cof

crontab -e

# Add run.py path, it will fetch the api every 1 min
* * * * * /usr/bin/python3 /path/run.py

```

Note: AWP work only with python v3
