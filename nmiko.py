#!/usr/bin/python

import threading
from netmiko import ConnectHandler
import devices
import sys

threaded = 1 #run on all devices at once (1) or one at a time (0)
groups = ['all'] #can enter a group name location/device name, all, or multiple groups sepearted by commmas
config_commands = ['command1, command2']

if len(sys.argv)> 1:
    groups = (sys.argv[1]).replace(" ","").split(',')

if len(sys.argv)>3:
    config_commands = (sys.argv[3]).replace("","").split(',')

def worker(data):
    try:
        net_connect = ConnectHandler(device_type=data['device_type'],ip=data['ip'],username=data['username'],password=data['password'],secret=data['secret'])
        rstring =  '\x1b[0;32;1m'+data['location'] + '   ' + data['ip']+'\x1b[0m'
        if data['secret']:
            net_connect.enable()
        rstring += "        \n" + '\x1b[0;30;47m' +net_connect.find_prompt() + '\x1b[0m'
        rstring += "   \n"
        if len(sys.argv)>2:
            if str(sys.argv[2]) == '-c':
		rstring += net_connect.config_mode()
		rstring += net_connect.send_config_set(config_commands)
	    elif str(sys.argv[2]) == '-e':
		rstring += net_connect.send_command_expect(str(sys.argv[3]))
	    else:
		rstring += net_connect.send_command(str(sys.argv[2]))
	else:
            #rstring += net_connect.send_command_expect('write mem')
            #rstring += net_connect.send_command('clear counters', expect_string=']')
            #rstring += net_connect.config_mode()
            rstring += net_connect.send_config_set(config_commands)
            #raw_input ('press enter to continue') # only use this if threading is turned off!
        print rstring
        pass
        raise Exception
    except Exception as err:
        if str(err)!='':
            print data['ip'] + '   ' + str(err)

threads = []
for device, data in devices.__dict__.iteritems():
    if isinstance(data, dict) and not device.startswith('_'):
        if data['group'] in groups or 'all' in groups or data['location'] in groups:
            if threaded:
                t = threading.Thread(target=worker, args=(data,))
                threads.append(t)
                t.start()
            else:
                worker(data)



