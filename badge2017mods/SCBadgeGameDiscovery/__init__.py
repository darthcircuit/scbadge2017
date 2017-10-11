# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from SCBadgeView import SCBadgeView
import SCBadgeGameAttack
import BTGameKit
import dataset
import time
import random
import os


class SCBadgeInventoryCell(pygame.Surface):

    def __init__(self, size, data, selected):
        pygame.Surface.__init__(self, size)
        if selected:
            self.fill((247, 148, 30))
            # self.fill((0,0,255))
        else:
            self.fill((100, 100, 100))
        title_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
        status_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
        self.title = title_font.render(data['name'], True, (255, 255, 255))
        # self.status = status_font.render(data['host'], True, (255,255,255))
        self.icon = pygame.image.load("assets/icons-badge-attack.png")
        pygame.draw.rect(self, (200, 200, 200), (10, 7, 25, 25), 0)
        pygame.draw.line(self, (50, 50, 50), (0, 39), (320, 39), 1)
        self.blit(self.title, (40, 10))
        self.blit(self.icon, (10, 7))
        # self.blit(self.status, (40, 20))


class SCBadgeScrollView(pygame.Surface):

    def __init__(self, size, data=[]):
        pygame.Surface.__init__(self, size)
        self.selected_index = 0
        self.data = data
        self.offset = 0
        self.visible = 4
        self.keys = [False, False, False, False]
        self.row_height = 40

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
            status = status_font.render("Scanning...", True, (255, 255, 255))
            self.blit(
                status, ((self.get_width() / 2 - status.get_width() / 2), 50))

        for i in xrange(self.offset, len(self.data)):
            if (i - self.offset) * 40 < self.get_height():
                cell = SCBadgeInventoryCell(
                    (320, 40), self.data[i], i == self.selected_index)
                self.blit(cell, (0, 40 * (i - self.offset)))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
            if event.key == K_DOWN:
                self.keys[1] = True


class SCBadgeGameDiscovery(SCBadgeView):

    def __init__(self, accel, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)
        self.running = True
        self.data = []
        self.table = SCBadgeScrollView((320, 200), self.data)
        self.db = dataset.connect('sqlite:///badges.db')

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        clock.tick(60)

        @self.btgk.route('found')
        def found():
            self.table.data = self.btgk.badges
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 5))
        try:
            self.btgk.search()
        except Exception as e:
            print e

        x_rotate = 0
        x_rect = pygame.Rect((295, 12, 10, 17))

        while self.running:
            self.screen.fill((0, 0, 0))
            if self.btgk.searching:
                x_rotate += 5
                if x_rotate > 360:
                    x_rotate = 0
            else:
                x_rotate = 0 

            # Titlebar
            pygame.draw.rect(self.screen, (170, 170, 170), (0, 0, 340, 20), 0)
            pygame.draw.rect(self.screen, (190, 190, 190), (0, 19, 340, 20), 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            title = title_font.render("Devices", True, (0, 0, 0))
            self.screen.blit(
                title, (self.screen.get_width() / 2 - title.get_width() / 2, 10))
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            title = title_font.render("Devices", True, (255, 255, 255))
            self.screen.blit(
                title, ((self.screen.get_width() / 2 - title.get_width() / 2) + 1, 9))
            pygame.draw.circle(self.screen, (247, 148, 30), (20, 20), 10, 0)

            pygame.draw.circle(self.screen, (247, 148, 30), (300, 20), 10, 0)
            #title_font = pygame.font.Font(
            #    '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            #title = title_font.render("X", True, (255, 255, 255))
            x_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            x_title = x_font.render("X", True, (255, 255, 255))
            x_title = pygame.transform.rotate(x_title, x_rotate)
            tmp_rect = x_title.get_rect(center=x_rect.center)
            self.screen.blit(x_title, tmp_rect)
            #self.screen.blit(tmp, (tmp.get_rect().x, tmp.get_rect().y))
    
            # pygame.draw.circle(self.screen, (120,120,120), (300, 20), 10, 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            title = title_font.render("B", True, (255, 255, 255))
            self.screen.blit(title, (15, 12))

            self.table.update()
            self.screen.blit(self.table, (0, 40))
            pygame.display.flip()

            for event in pygame.event.get():
                super(SCBadgeGameDiscovery, self).events(event)
                self.table.events(event)
                if event.type == pygame.USEREVENT + 1:
                    self.btgk.stop_search()
                    self.running = False
                if event.type == pygame.USEREVENT + 5:
                    for t in self.btgk.badges:
                        self.db['badges'].upsert(
                            dict(host=t['host'], name=t['name']), ['host'])
                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        for t in self.btgk.badges:
                            self.db['badges'].upsert(
                                dict(host=t['host'], name=t['name']), ['host'])
                        if len(self.btgk.badges) > 0:
                            b = self.btgk.badges[self.table.selected_index]
                            r = self.db['badges'].find_one(host=b['host'])
                            print r
                            if r is None or 'timeout' not in r or time.time() > r['timeout'] or time.time()+300 < r['timeout']:
                                status = self.btgk.connect(
                                    self.table.selected_index)
                                if status:
                                    b['timeout'] = time.time() + 300 # REAL 600
                                    self.db['badges'].upsert(
                                        dict(host=b['host'], name=b['name'], timeout=b['timeout']), ['host'])
                                    SCBadgeGameAttack.SCBadgeGameAttack(
                                        [],  self.screen, self.btgk).run()
                                else:
                                    super(SCBadgeGameDiscovery, self).alert(
                                        {"msg": "A error occured while trying to connect to another badge, try again in a few seconds."})
                            else:
                                super(SCBadgeGameDiscovery, self).alert(
                                    {"msg": "You have already attacked this badge there is a 5 min cool down before you can attack this badge again."})
                                print "LOCK OUT"
                    if event.key == K_x:
                        if not self.btgk.searching:
                            self.btgk.search()
                    if event.key == K_b:
                        self.btgk.stop_search()
                        self.running = False
