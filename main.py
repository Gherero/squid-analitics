#!/usr/bin/python3

import subprocess
import urllib3
import logging
import time

log_file = '/var/log/kalmar/skript_updater.log'
local_versoin = '/opt/kalmar/version'
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', filename = log_file , level = logging.DEBUG)

#[server]
server = '192.168.73.58'
#[Server]
s_folder= 'black_lists'
s_list = 'porno'
version_file = 'version'
#[Client]
c_folder = '/etc/squid3/black_lists/'
log_folder = '/var/log/squid_updater/'
log_file = 'update_log.log'

try:
    f_log=open(log_file, 'a')
except:
    f_log=open(log_file, 'w')

try:
    ver_file = open(local_versoin, 'r')
except:
    ver_file = open(local_versoin, 'w')
    ver_file.writelines("0\n")
    ver_file.close()
    ver_file = open(local_versoin, 'r')


http = urllib3.PoolManager()

try:
    response = http.request('GET','http://'+server+'/main/version')
    logging.info("version")
except:
    logging.fatal("Can't connect to server")
    exit()

if response.status == 404 :
    logging.warning("Download version file is failed (File no server not found)")
else:
    new_version=int(response.data.decode())
    local_versoin = int(ver_file.readline())
    if  new_version > local_versoin :
        response = http.request('GET','http://'+server+'/main/updater.py')
        with open("/opt/kalmar/updater.py","w") as f:
            f.write(response.data.decode())
        f.close()

        response = http.request('GET', 'http://' + server + '/main/version')
        with open("/opt/kalmar/version","w") as f:
            f.write(response.data.decode())
        f.close()


subprocess.call("/opt/kalmar/updater.py", shell=True)
print ("OK")

