import subprocess
import urllib3
import logging

log_level = 'DEBUG'
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', filename = '/var/log/squid_updater/my_log.log')
subprocess.call("/tmp/main.py", shell=True)
print ("OK")