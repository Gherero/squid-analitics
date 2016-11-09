#!/usr/bin/python3

__author__ = 'kiro'
import urllib3
import os
import logging
import configparser

log_level = 'DEBUG'
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', filename = '/var/log/squid_updater/list-updater.log')

config = configparser.ConfigParser()
config.read("/opt/kalmar/updater.py")

server_addr= config.get('server','addr')
s_folder= 'black_lists'
s_list = 'porno'
version_file = 'version'
#[Client]
c_folder = config.get('client','folder')
#log_folder = '/var/log/squid_updater/'
log_file = config.get('client','log_file')

http = urllib3.PoolManager()

try:
    f_log=open(log_file,'a')
except:
    f_log=open(log_file,'w')

try:
    response = http.request('GET', 'http://' + server_addr + '/black_lists/' + s_list)
    logging.info("Connect GET http://" + server_addr + '/black_lists/' + s_list)
except:
    logging.error("server not found")
    exit()

if response.status == 404 :
    logging.warning("page not found [404]")
    exit()

with open(c_folder+s_list,'w') as f:
    f.write(response.data.decode())
f.close()

os.system("squid3 -k reconfigure")
exit()
