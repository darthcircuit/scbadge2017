#!/usr/bin/python

import pygame
import BTGameKit
import SCBadgeMotion
import SCBadgeMenu
import SCBadgeMainMenu
import SCBadgeInfo
import requests
import pickle 
import signal
import json
from pygame.locals import *
import random
import os


def handler(signum, frame):
    """Why is systemd sending sighups? I DON'T KNOW."""
    print "EXIT: " + str(signum)
    if signum == 15:
        pygame.quit()

signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGCONT, handler)

os.environ['SDL_FBDEV'] = '/dev/fb1'
try:
    with open('/sys/class/backlight/fb_ili9341/bl_power', 'w') as bl:
        bl.write('0')
except Exception as e:
    print e

pygame.init()
accel = SCBadgeMotion.SCBadgeMotion()
app = BTGameKit.BTGameKit(__name__)
width, height = 320, 240
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
data = SCBadgeInfo.getdata()

if os.path.exists('settings.p'):
    lsettings = pickle.load(open("settings.p", 'rb'))
else:
   lsettings = {'name_text': [255, 255, 255], 'credits': [ 255, 165, 60], 'background_color': 0, 'name_layout': 31, 'netowrk': [255, 165, 60], 'hdmi' : 0}

if 'hdmi' in lsettings:
    if lsettings['hdmi'] == 0:
        os.system('/usr/bin/tvservice -o')
    else:
        os.system('/usr/bin/tvservice -p')
else:
    os.system('/usr/bin/tvservice -o')


try:
    if data['handle'] == SCBadgeInfo.getserial():
        print "GOOD"
        app.advertise("n00b-" + data['handle'][0:4])
    else:
        print "BAD"
        app.advertise(data['handle'])
    app.run()
except Exception as e:
    print e


main_menu = SCBadgeMainMenu.SCBadgeMainMenu(accel, screen, app)
while True:
    SCBadgeMenu.SCBadgeMenu(accel, data, screen, app).run()
    main_menu.run()
