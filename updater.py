__author__ = 'kiro'
import urllib3
import os
import logging

log_level = 'DEBUG'
logging.basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s', filename = '/var/log/squid_updater/my_log.log')

#[Server]
server= '192.168.73.114'
s_folder= 'black_lists'
s_list = 'porno'
version_file = 'version'
#[Client]
c_folder = '/etc/squid3/black_lists/'
log_folder = '/var/log/squid_updater/'
log_file = 'update_log.log'

http = urllib3.PoolManager()

try:
    f_log=open(log_folder+log_file,'a')
except:
    f_log=open(log_folder+log_file,'w')

try:
    response = http.request('GET', 'http://'+server+'/'+s_folder+'/'+s_list)
    logging.info("Connect GET http://"+server+'/'+s_folder+'/'+s_list)
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
