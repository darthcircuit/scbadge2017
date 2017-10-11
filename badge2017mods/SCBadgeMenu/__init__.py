# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import PirateAnimation
import SCBadgeInfo
from SCBadgeView import SCBadgeView
import random
import pickle
import os
import threading
import time


class SCBadgeMenu(SCBadgeView):

    def __init__(self, accel, data, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)
        self.data = data

    def dynamic_font(self, text,  size, color):
        # font =
        # pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',
        # size)
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
        if font.size(text)[0] > self.screen.get_rect().width:
            return self.dynamic_font(text, size - 2, color)
        return font.render(text, True, color)

    def run(self):
        self.running = True
        self.data = SCBadgeInfo.getdata()
        if self.data['handle'] != self.btgk.player and self.data['handle'] != SCBadgeInfo.getserial():
            self.btgk.advertise(self.data['handle'])
            self.btgk.run()
        keys = [False, False]
        clock = pygame.time.Clock()
        clock.tick(60)
        if os.path.exists('settings.p'):
            lsettings = pickle.load(open("settings.p", 'rb'))
        else:
            lsettings = {'name_text': [255, 255, 255], 'credits': [
                255, 165, 60], 'background_color': 0, 'name_layout': 27, 'netowrk': [255, 165, 60]}
        self.bg_images = [
            "assets/boot-splash-pattern.jpg", "assets/BGA-1.jpg", "assets/BGA-2.jpg",
            "assets/BGA-3.jpg", "assets/BGA-4.jpg", "assets/BGA-5.jpg", "assets/BGA-6.jpg", "assets/BGA-7.jpg"]
        bg = pygame.image.load(self.bg_images[lsettings['background_color']])
        bg = pygame.transform.rotate(bg, 180).convert()
        bg.set_alpha(175)
        text_scroll = 0
        delay = 1
        next = time.time() + delay

        while self.running:
            if keys[0]:
                # pygame.event.post(pygame.event.Event(pygame.USEREVENT + 3))
                keys[0] = False
            if self.accel.orientation:
                print "ORIENTATION STOP"
                self.running = False
            if keys[1]:
                # print "STOP"
                # self.running = False
                keys[1] = False

            self.screen.fill(lsettings['background_color'])
            self.screen.blit(bg, (0, 0))

            visible = [int(x) for x in bin(lsettings['name_layout'])[2:]]
            while len(visible) < 5:
                visible.append(0)
            if visible[0]:
                name_text = self.dynamic_font(
                    self.data['name'], 36, lsettings['name_text'])
                name_text = pygame.transform.rotate(name_text, 180)
                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 200])

            if visible[1]:
                name_text = self.dynamic_font(
                    self.data['handle'], 36, lsettings['name_text'])
                name_text = pygame.transform.rotate(name_text, 180)
                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 160])

            if visible[2]:
                if "hc_score" in self.data:
                    name_text = self.dynamic_font(
                        "Score: %d" % (self.data['hc_score']), 36, lsettings['name_text'])
                else:
                    name_text = self.dynamic_font(
                        "Score: 0", 36, lsettings['name_text'])
                name_text = pygame.transform.rotate(name_text, 180)
                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 95])

            if visible[3]:
                name_text = self.dynamic_font(
                    self.data['handle'], 36, lsettings['name_text'])
                name_font = pygame.font.Font(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
                name_text = name_font.render(
                    self.data['msg'], True, lsettings['name_text'])
                name_text = pygame.transform.rotate(name_text, 180)
                w = name_text.get_width()
                if time.time() < next:
                    if text_scroll < (name_text.get_width() * 2) - 10:
                        text_scroll += 6
                    else:
                        text_scroll = 0
                    self.screen.blit(
                        name_text, [(-1 * name_text.get_width()) + text_scroll, 45])
                    next = time.time() + delay

            if visible[4]:
                name_text = self.dynamic_font(
                    self.data['handle'], 36, lsettings['name_text'])
                name_font = pygame.font.Font(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
                name_text = self.dynamic_font(
                    self.data['org'], 36, lsettings['name_text'])
                name_text = pygame.transform.rotate(name_text, 180)
                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 10])

            pygame.display.flip()
            for event in pygame.event.get():
                super(SCBadgeMenu, self).events(event)
                if event.type == pygame.USEREVENT + 2:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        keys[0] = True
                    if event.key == K_DOWN:
                        keys[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        keys[0] = False
                    if event.key == K_DOWN:
                        keys[1] = False
