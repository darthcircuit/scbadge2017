# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from SCBadgeAnimations import Pirate
import SCBadgeGameResult
import random
import dataset
import os
import pickle
import json
import LEDS
import threading
import time


class SCBadgeKey(pygame.Surface):

    def __init__(self, size, key):
        pygame.Surface.__init__(self, size)
        self.fill((200, 200, 200))
        self.selected = False
        self.key = key
        print self.get_height() / 2
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
        else:
            key_font = pygame.font.Font(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
            key_text = key_font.render(
                chr(self.key).upper(), True, (255, 255, 255))
            self.blit(key_text, (self.get_width() / 2 -
                                 11, self.get_height() / 2 - 18))


class SCBadgeGameDefend(object):

    def __init__(self, data,  screen, btgk):
        self.screen = screen
        self.pirate = Pirate(self.screen)
        self.data = data
        self.btgk = btgk
        self.leds = LEDS.LEDS()
        self.db = dataset.connect('sqlite:///badges.db')

    def run(self):
        self.running = True
        keys = [False, False, False, False, False, False, False, False]
        defence_keys = []
        keyboard = [K_UP, K_DOWN, K_RIGHT, K_LEFT, K_a, K_b, K_x, K_y]
        disp = {"273": u'\u2191', "274": u'\u2193', "275": u'\u2192',
                "276": u'\u2190', "97": u"A", "98":  u"B", "120":  u"X",  "121": u"Y"}
        clock = pygame.time.Clock()
        bg = pygame.image.load("assets/boot-splash-pattern.png")
        bg = bg.convert()
        bg.set_alpha(130)
        clock.tick(60)
        flash = time.time() + 1
        password_index = 0
        password = [keyboard[random.randint(0, 7)] for x in xrange(0, 6)]
        pass_show = [SCBadgeKey((45, 45), a) for a in password]
        if os.path.exists('settings.p'):
            lsettings = pickle.load(open("settings.p", 'rb'))
        else:
            lsettings = {'name_text': [255, 255, 255], 'led_color': [255, 0, 0], 'credits': [
                255, 165, 60], 'background_color': 0, 'name_layout': 31, 'netowrk': [255, 165, 60]}

        stop = time.time() + 10
        while self.running:
            if flash < time.time():
                self.leds.colorWipe(lsettings['led_color'])
                flash = time.time() + 1
            else:
                self.leds.colorWipe((0, 0, 0))
            if stop < time.time():
                try:
                    self.leds.colorWipe((0, 0, 0))
                    self.btgk.cnx.send(json.dumps({"stop": 1}))
                except Exception as e:
                    print "SENDING ACK FAILED"
                self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg, (0, 0))
            l = 0
            for b in pass_show:
                b.update()
                self.screen.blit(b, (15 + (l * 50), 20))
                l += 1

            msg_font = pygame.font.Font(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
            msg1 = msg_font.render(
                'Type in sequence above', True, (255, 255, 255))
            msg2 = msg_font.render(
                'before time runs out', True, (255, 255, 255))
            msg3 = msg_font.render(
                'or other badge attacks.', True, (255, 255, 255))

            count_down_font = pygame.font.Font(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
            count_down = count_down_font.render(
                "%ds" % (stop - time.time()), True, (255, 255, 255))
            self.screen.blit(
                count_down, (160 - count_down.get_width() / 2, 180))
            self.screen.blit(msg1, (160 - msg1.get_width() / 2, 110))
            self.screen.blit(msg2, (160 - msg1.get_width() / 2, 130))
            self.screen.blit(msg3, (160 - msg1.get_width() / 2, 150))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == USEREVENT:
                    print event
                    if event.data['type'] == "attacked":
                        self.leds.colorWipe(lsettings['led_color'])
                        self.pirate.play(3, "You Lost!")
                        self.db['losses'].insert(dict(timestamp=time.time()))
                        self.leds.colorWipe((0, 0, 0))
                        self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == password[password_index]:
                        pass_show[password_index].selected = True
                        password_index += 1
                        if password_index == len(password):
                            self.btgk.cnx.send(json.dumps(
                                {"defend": random.randint(100, 200)}))
                            self.pirate.play(3, "You Won!")
                            self.leds.colorWipe((0, 0, 0))
                            self.db['wins'].insert(dict(timestamp=time.time()))
                            self.running = False
                    else:
                        for b in pass_show:
                            b.selected = False
                        password_index = 0
