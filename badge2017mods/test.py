#!/usr/bin/python
import pygame
import BTGameKit
import SCBadgeGameInventory
import SCBadgeMainMenu
import SCBadgeGameAttack
import SCBadgeGameDiscovery
from pygame.locals import *
import LEDS
import signal
import random
import time
import json
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

pygame.init()
app = BTGameKit.BTGameKit(__name__)
width, height = 320, 240
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

try:
    app.advertise("test-badge")

    @app.route('found')
    def found():
        pass
        pygame.event.post(pygame.event.Event(pygame.USEREVENT + 3))
        # table.data = app.badges

    app.run()
except Exception as e:
    print e


class SCBadgeKey(pygame.Surface):

    def __init__(self, size, key):
        pygame.Surface.__init__(self, size)
        self.fill((200, 200, 200))
        self.selected = False
        self.key = key
        pygame.draw.circle(self, (10, 10, 10), (5, 5), 4, 0)
        pygame.draw.circle(self, (10, 10, 10),
                           (5, self.get_height() - 5), 4, 0)
        pygame.draw.circle(self, (10, 10, 10), (self.get_width() - 5, 5), 4, 0)
        pygame.draw.circle(self, (10, 10, 10),
                           (self.get_width() - 5, self.get_height() - 5), 4, 0)
        pygame.draw.circle(self, (10, 10, 10), ((self.get_width(
        ) / 2) - 1, (self.get_height() / 2) + 2), (self.get_height() / 2) - 5, 0)

    def update(self):
        if self.selected:
            pygame.draw.circle(self, (0, 200, 0), (self.get_width(
            ) / 2, self.get_height() / 2), (self.get_height() / 2) - 5, 0)
        else:
            pygame.draw.circle(self, (100, 100, 100), (self.get_width(
            ) / 2, self.get_height() / 2), (self.get_height() / 2) - 5, 0)

        if self.key == 273:  # UP
            pygame.draw.polygon(self, (255, 255, 255), [(self.get_width(
            ) / 2, 10), (self.get_width() / 2 - 10, 20), (self.get_width() / 2 + 10, 20)], 0)
            pygame.draw.rect(self, (255, 255, 255),
                             ((self.get_width() / 2) - 3, 20, 6, 15), 0)
        elif self.key == 274:  # DOWN
            pygame.draw.polygon(self, (255, 255, 255), [(self.get_width() / 2, self.get_height() - 10), (self.get_width(
            ) / 2 - 10, self.get_height() - 20), (self.get_width() / 2 + 10, self.get_height() - 20)], 0)
            pygame.draw.rect(self, (255, 255, 255), ((
                self.get_width() / 2) - 3, self.get_height() - 20 - 15, 6, 15), 0)
        elif self.key == 276:  # LEFT
            pygame.draw.polygon(self, (255, 255, 255), [(10, self.get_height(
            ) / 2), (20, self.get_height() / 2 - 10), (20, self.get_height() / 2 + 10)], 0)
            pygame.draw.rect(self, (255, 255, 255),
                             (20, self.get_height() / 2 - 3, 15, 6), 0)
        elif self.key == 275:  # RIGHT
            pygame.draw.polygon(self, (255, 255, 255), [(self.get_width() - 10, self.get_height() / 2), (self.get_width(
            ) - 20, self.get_height() / 2 - 10), (self.get_width() - 20, self.get_height() / 2 + 10)], 0)
            pygame.draw.rect(self, (255, 255, 255), (self.get_width(
            ) - 20 - 15, self.get_height() / 2 - 3, 15, 6), 0)
        elif self.key == 13 or self.key == 27:
            key_font = pygame.font.Font(
                '/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf', 30)
            key_text = key_font.render("S", True, (255, 255, 255))
            self.blit(key_text, (self.get_width() / 2 -
                                 11, self.get_height() / 2 - 18))
        else:
            key_font = pygame.font.Font(
                '/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf', 30)
            key_text = key_font.render(
                chr(self.key).upper(), True, (255, 255, 255))
            self.blit(key_text, (self.get_width() / 2 -
                                 11, self.get_height() / 2 - 18))


up = SCBadgeKey((45, 45), K_UP)
down = SCBadgeKey((45, 45), K_DOWN)
left = SCBadgeKey((45, 45), K_LEFT)
right = SCBadgeKey((45, 45), K_RIGHT)
l = SCBadgeKey((45, 45), K_l)
r = SCBadgeKey((45, 45), K_r)
a = SCBadgeKey((45, 45), K_a)
bee = SCBadgeKey((45, 45), K_b)
x = SCBadgeKey((45, 45), K_x)
y = SCBadgeKey((45, 45), K_y)
start = SCBadgeKey((45, 45), K_RETURN)
select = SCBadgeKey((45, 45), K_ESCAPE)

buttons = [up, down, left, right, l, r, a, bee, x, y, start, select]

sensor = None
try:
    from mpu6050 import mpu6050
    sensor = mpu6050(0x68)
except:
    pass

leds = LEDS.LEDS()
red = 0
green = 0
blue = 0
quit_count = 0
while True:
    screen.fill((0, 0, 0))
    screen.blit(l, (5, 30))
    screen.blit(r, (270, 30))

    if red < 250:
        red += 25
        leds.colorWipe([red, green, blue])
    else:
        red = 0
        if green < 250:
            green += 25
            leds.colorWipe([red, green, blue])
        else:
            green = 0
            if blue < 250:
                blue += 25
                leds.colorWipe([red, green, blue])
            else:
                blue = 0
                leds.colorWipe([red, green, blue])

    screen.blit(select, (110, 30))
    screen.blit(start, (165, 30))

    screen.blit(up, (55, 130))
    screen.blit(down, (55, 195))
    screen.blit(left, (5, 165))
    screen.blit(right, (105, 165))

    if sensor:
        tmp = sensor.get_accel_data()
        data = "x: %.2f, y: %.2f, z: %.2f" % (tmp['x'], tmp['y'], tmp['z'])
    else:
        data = "NO MPU FOUND!"

    key_font = pygame.font.Font(
        '/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf', 16)
    key_text = key_font.render(data, True, (255, 255, 255))
    screen.blit(key_text, (screen.get_width() /
                           2 - key_text.get_width() / 2, 100))

    screen.blit(x, (220, 130))
    screen.blit(y, (170, 165))
    screen.blit(a, (270, 165))
    screen.blit(bee, (220, 195))
    for b in buttons:
        b.update()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print event
            for k in buttons:
                if event.key == k.key:
                    if event.key == K_ESCAPE:
                        quit_count += 1
                        if quit_count == 4:
                            pygame.quit()
                    k.selected = True
