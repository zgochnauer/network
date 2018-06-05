#!/usr/bin/python

#################
#traces mac address
#################

import threading
from netmiko import ConnectHandler
import devices
import sys


threaded = 1 #run on all devices at once (1) or one at a time (0)
groups = ['groupname'] #can enter all, groupname, or multiple groupnames seperated by commas

if len(sys.argv)> 1:
    groups = [str(sys.argv[1])]

rawmac = raw_input('enter a full MAC or an ending of a MAC in any format \n')
rawmac = (''.join(e for e in rawmac if e.isalnum())).lower()
mac = ''
if len(rawmac) <= 4:
    mac = rawmac
elif len(rawmac) == 12:
    for i in range(0, len(rawmac)):
        if i == 4 or i == 8:
            mac += '.'
        mac += rawmac[i]
else:
    print 'you did not enter a full MAC or an ending of a MAC (last 4, 3, 2, or 1 digits) \nexiting now'
    quit()

def worker(data):
    try:
        net_connect = ConnectHandler(device_type=data['device_type'],ip=data['ip'],username=data['username'],password=data['password'],secret=data['secret'])

        rstring =  '\x1b[0;32;1m'+data['location'] + '   ' + data['ip']+'\x1b[0m'
        if data['secret']:
            net_connect.enable()
        rstring += "        \n" + '\x1b[0;30;47m' +net_connect.find_prompt() + '\x1b[0m'

        rstring += '\n' + net_connect.send_command('show mac address | inc '+ mac) 
        print rstring
        #quit() #remove this to cycle through all
        pass
        raise Exception
    except Exception as err:
        if str(err)!='':
            print data['ip'] + '   ' + str(err)
 

threads = []
for device, data in devices.__dict__.iteritems():
    if isinstance(data, dict) and not device.startswith('_'):
        if data['group'] in groups or 'all' in groups:
            if threaded:
                t = threading.Thread(target=worker, args=(data,))
                threads.append(t)
                t.start()
            else:
                worker(data)

