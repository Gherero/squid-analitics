#!/usr/bin/python3

__author__ = 'kiro'
import urllib3
import os
import logging
import configparser


config = configparser.ConfigParser()
config.read("/opt/kalmar/updater.conf")

server_addr= config.get('server','addr')
black_lists = config.get('server', 'lists')
black_lists = black_lists.split(',')
version_file = 'version'
#[Client]
c_folder = config.get('client','folder')
#log_folder = '/var/log/squid_updater/'
log_file = config.get('client','log_file')

logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', filename = log_file, level = logging.DEBUG )

http = urllib3.PoolManager()

for dict in black_lists :

    try:
        response = http.request('GET', 'http://' + server_addr + '/black_lists/' + dict)
        logging.info("Connect GET http://" + server_addr + '/black_lists/' + dict)

    except:

        logging.error("server not found")
        exit()

    if response.status == 404 :
        logging.warning("page not found [404]")

    else:

        with open(c_folder+dict, 'w') as f:
            f.write(response.data.decode())
        f.close()
        logging.info('Was updated dict. ' + dict)
os.system("squid3 -k reconfigure")
exit()
