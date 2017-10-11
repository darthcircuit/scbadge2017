# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from SCBadgeView import SCBadgeView
from operator import itemgetter
import SCBadgeInfo
import requests
import threading
import datetime
import random
import json
import time
import os
import re


class SCBadgeInventoryCell(pygame.Surface):

    def __init__(self, size, data, selected):
        pygame.Surface.__init__(self, size)
        if selected:
            self.fill((247, 148, 30))
        else:
            self.fill((100, 100, 100))

        # 2017-10-11 08:30:00
        try:
            start = datetime.datetime.strptime(
                data['event_start'], '%Y-%m-%d %H:%M:%S').strftime('%A %I:%M')
        except:
            start = "TBA"
        try:
            end = datetime.datetime.strptime(
                data['event_end'], '%Y-%m-%d %H:%M:%S').strftime('%I:%M')
        except:
            end = "TBA"
        title_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
        status_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 13)
        self.time = status_font.render(
            start + " - " + end, True, (255, 255, 255))
        self.title = title_font.render(data['name'], True, (255, 255, 255))
        self.status = status_font.render(data['venue'], True, (255, 255, 255))
        # self.icon = pygame.image.load(data['icon'])
        track_font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 25)
        try:
            self.track = track_font.render(
                re.search(r'\d+', data['venue']).group(), True, (255, 255, 255))
        except Exception as e:
            if "General" in data['venue']:
                self.track = track_font.render("G", True, (255, 255, 255))
            else:
                self.track = track_font.render("V", True, (255, 255, 255))
        if 'event_subtype' in data:
            if data['event_subtype'] == 'OFFENSE':
                pygame.draw.rect(self, (221, 29, 29), (10, 7, 25, 25), 0)
            elif data['event_subtype'] == 'DEFENSE':
                pygame.draw.rect(self, (27, 168, 223), (10, 7, 25, 25), 0)
            else:
                pygame.draw.rect(self, (200, 200, 200), (10, 7, 25, 25), 0)
        else:
            if "General" in data['venue']:
                pygame.draw.rect(self, (39, 117, 18), (10, 7, 25, 25), 0)
            else:
                pygame.draw.rect(self, (136, 38, 153), (10, 7, 25, 25), 0)
        pygame.draw.line(self, (50, 50, 50), (
            0, self.get_height() - 1), (320, self.get_height() - 1), 1)
        self.blit(self.track, (13, 4))
        self.blit(self.title, (40, 4))
        self.blit(self.time, (40, 20))
        self.blit(self.status, (40, 32))


class SCBadgeScrollView(pygame.Surface):

    def __init__(self, size, data=[]):
        pygame.Surface.__init__(self, size)
        self.selected_index = 0
        self.data = data
        self.offset = 0
        self.visible = 3
        self.keys = [False, False, False, False]
        self.row_height = 50
        self.debounce = 0

    def scroll_up(self):
        if self.selected_index - 1 >= 0:
            self.selected_index -= 1

    def scroll_down(self):
        if self.selected_index + 1 < len(self.data):
            self.selected_index += 1

    def update(self):
        self.fill((0, 0, 0))
        if self.keys[0]:
            self.scroll_up()
            self.keys[0] = False
        if self.keys[1]:
            self.scroll_down()
            self.keys[1] = False

        if self.selected_index - self.offset > self.visible:
            self.offset += 1
        if self.selected_index == self.offset - 1 and self.offset != 0:
            self.offset -= 1

        if len(self.data) == 0:
            status_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 22)
            status = status_font.render("Loading... ", True, (255, 255, 255))
            self.blit(status, ((160 - status.get_width() / 2), 50))

        for i in xrange(self.offset, len(self.data)):
            if (i - self.offset) * self.row_height < self.get_height():
                cell = SCBadgeInventoryCell(
                    (320, self.row_height), self.data[i], i == self.selected_index)
                self.blit(cell, (0, self.row_height * (i - self.offset)))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
            if event.key == K_DOWN:
                self.keys[1] = True
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                self.keys[0] = False
            if event.key == K_DOWN:
                self.keys[1] = False


class SCBadgeSchedule(SCBadgeView):

    def __init__(self, accel, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)
        self.running = True
        self.table = SCBadgeScrollView((320, 200), [])

    def update_data(self):
        if SCBadgeInfo.internet():
            self.table.data = sorted(
                requests.get("https://register.saintcon.org/schedule").json(), key=itemgetter('event_start'))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        clock.tick(60)
        t = threading.Thread(target=self.update_data)
        t.daemon = True
        t.start()

        while self.running:
            self.screen.fill((0, 0, 0))

            # Titlebar
            pygame.draw.rect(self.screen, (170, 170, 170), (0, 0, 340, 20), 0)
            pygame.draw.rect(self.screen, (190, 190, 190), (0, 19, 340, 20), 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            # title_font =
            # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
            # 20)
            title = title_font.render("Schedule", True, (0, 0, 0))
            self.screen.blit(
                title, (self.screen.get_width() / 2 - title.get_width() / 2, 10))
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            # title_font =
            # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
            # 20)
            title = title_font.render("Schedule", True, (255, 255, 255))
            self.screen.blit(
                title, ((self.screen.get_width() / 2 - title.get_width() / 2) + 1, 9))
            pygame.draw.circle(self.screen, (100, 100, 100), (20, 21), 10, 0)
            pygame.draw.circle(self.screen, (255, 116, 30), (20, 20), 10, 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            # title_font =
            # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
            # 16)
            title = title_font.render("B", True, (255, 255, 255))
            self.screen.blit(title, (15, 12))

            self.table.update()
            self.screen.blit(self.table, (0, 40))
            pygame.display.flip()

            for event in pygame.event.get():
                super(SCBadgeSchedule, self).events(event)
                self.table.events(event)
                if event.type == pygame.USEREVENT + 1:
                    print "FLIP ME"
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_b:
                        self.running = False
