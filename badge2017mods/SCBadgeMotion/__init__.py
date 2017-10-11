import pygame
import time
import math
import threading


class SCBadgeMotion():

    def __init__(self):
        self.running = True
        self.backlight = True
        self.orientation = True
        try:
            from mpu6050 import mpu6050
            self.sensor = mpu6050(0x68)
            accel = threading.Thread(target=self.__motion)
            accel.daemon = True
            accel.start()
        except Exception as e:
            print "MPU6050 Not Found"
            self.sensor = None

    def __motion(self):
        print "TRACK MOTION"
        last_step_time = time.time()
        while self.running:
            data = self.sensor.get_accel_data()
            motion = math.sqrt(
                data['x'] ** 2 + data['y'] ** 2 + data['z'] ** 2)
            if motion > 11.5:
                last_step_time = time.time()
                if not self.backlight:
                    with open('/sys/class/backlight/fb_ili9341/bl_power', 'w') as bl:
                        bl.write('0')
                    self.backlight = True

            if time.time() > last_step_time + 60:
                if self.backlight and not self.orientation:
                    self.backlight = False
                    with open('/sys/class/backlight/fb_ili9341/bl_power', 'w') as bl:
                        bl.write('1')

            if data['y'] > 1:
                #print data['y']
                #print self.orientation
                if self.orientation:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
                    if not self.backlight:
                        self.backlight = True
                        with open('/sys/class/backlight/fb_ili9341/bl_power', 'w') as bl:
                            bl.write('0')
                        last_step_time = time.time()
                    self.orientation = False
            elif data['y'] < -1:
                #print data['y']
                #print self.orientation
                if not self.orientation:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))
                    if not self.backlight:
                        self.backlight = True
                        with open('/sys/class/backlight/fb_ili9341/bl_power', 'w') as bl:
                            bl.write('0')
                        last_step_time = time.time()
                    self.orientation = True
            time.sleep(0.1)
        print "STOP STOP STOP"
