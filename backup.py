#!/usr/bin/python

#######################
#backup running config to /home/zgochnauer/network/configs/  is currently automated
#######################

from datetime import datetime
import os
import pexpect
import devices
import time

#scp admin@172.16.152.120:startup-config /home/zgochnauer/network/

mydate =  str(datetime.now().year) +'_'+ str(datetime.now().month) +'_'+ str(datetime.now().day)
def docopy(configfolder):
    dir = '/home/zgochnauer/network/configs/' + configfolder + '/'+mydate+'/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    for device, data in devices.__dict__.iteritems():
        if isinstance(data, dict) and not device.startswith('_') and data['group']==configfolder:
            try:
                print data['location']
                child = pexpect.spawn('scp -o "StrictHostKeyChecking no" '+data['username']+'@'+data['ip']+':startup-config '+dir+device)
                child.expect('Password: ')
                print data['password']
                time.sleep(0.300)
                child.sendline(data['password'])
                child.interact()
                child.kill(0)
                #quit() #remove this to cycle through all
                pass
                raise Exception
            except Exception as err:
                if str(err)!='':
                    print data['ip'] + '   ' + str(err)


docopy('groupname')
docopy('groupname2')
#docopy('groupname3') #scp not enabled on devices


