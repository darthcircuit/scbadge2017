import requests
import pygame
import hashlib
import pickle
import socket
import threading
import os
from uuid import getnode as get_mac


def network(host="8.8.8.8", port=53, timeout=2):
    status = "Not Connected!"
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        status = True
        mac = get_mac()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        ip  = s.getsockname()[0]
        s.close()
    except Exception as e:
        print e
        status = False 
        mac = hex(get_mac())
        ip  = socket.getsockname()[0]
    print "HELLO" 
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, data={"type": "network", "status" : status, "mac" : mac, "ip" : ip}))    
    

def internet(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print e
        return False


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    m = hashlib.md5()
    m.update(cpuserial[0:8])
    m.update("saintcon2017")
    m.update(cpuserial[8:16])
    print m.hexdigest()
    return m.hexdigest()[0:10]

    return cpuserial


def update():
    try:
        if internet():
            r = requests.get(
                'https://www.hackerschallenge.org/badge?badge_id=' + getserial(), timeout=2)
            data = r.json()['badge_info']
            if 'first_name' in data and 'last_name' in data:
                data['name'] = "%s %s" % (data['first_name'], data['last_name'])
            else:
                raise Exception('No Name Registred')
            if 'org' not in data:
                data['org'] = ""
            if 'handle' not in data:
                data['handle'] = 'n00b-' + getserial()[0:4]
            pickle.dump(data, open("info.p", "wb"))
            return r.json()
    except Exception as e:
        print e
        print "ERROR HERE"


def getdata():
    t = threading.Thread(target=update)
    t.daemon = True
    t.start()

    if os.path.exists("info.p"):
        print "MY DATA LOAD"
        try:
            return pickle.load(open("info.p", "rb"))
        except Exception as e:
            print e

    return {"name": "Register:", "handle": getserial(), "org": "", "msg": "Register your badge @ https://www.hackerschallenge.org"}
