# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from SCBadgeView import SCBadgeView
import random
import os


class SCBadgeInventoryCell(pygame.Surface):

    def __init__(self, size, data, selected):
        pygame.Surface.__init__(self, size)
        if selected:
            # self.fill((0,0,255))
            self.fill((247, 148, 30))
        else:
            self.fill((100, 100, 100))
        title_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
        status_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
        self.title = title_font.render(data['title'], True, (255, 255, 255))
        self.status = status_font.render(data['status'], True, (255, 255, 255))
        # self.icon = pygame.image.load(data['icon'])
        pygame.draw.rect(self, (200, 200, 200), (10, 7, 25, 25), 0)
        pygame.draw.line(self, (50, 50, 50), (0, 39), (320, 39), 1)
        self.blit(self.title, (40, 5))
        self.blit(self.status, (40, 20))


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

        # print self.offset

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


class SCBadgeGameResearch(SCBadgeView):

    def __init__(self, accel, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)
        self.running = True
        self.data = [{"title": "Title Text", "status": "Ready!"}, {"title": "Title Text 2", "status": "Ready!"}, {"title": "Title Text 3", "status": "Ready!"}, {
            "title": "Title Text 4", "status": "Ready!"}, {"title": "Title Text 5", "status": "Ready!"}, {"title": "Title Text 6", "status": "Ready!"}]
        self.table = SCBadgeScrollView((320, 200), self.data)

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        clock.tick(60)

        while self.running:
            self.screen.fill((0, 0, 0))

            # Titlebar
            pygame.draw.rect(self.screen, (170, 170, 170), (0, 0, 340, 20), 0)
            pygame.draw.rect(self.screen, (190, 190, 190), (0, 19, 340, 20), 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            title = title_font.render("Research", True, (0, 0, 0))
            self.screen.blit(
                title, (self.screen.get_width() / 2 - title.get_width() / 2, 10))
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            title = title_font.render("Research", True, (255, 255, 255))
            self.screen.blit(
                title, ((self.screen.get_width() / 2 - title.get_width() / 2) + 1, 9))
            pygame.draw.circle(self.screen, (247, 148, 30), (20, 20), 10, 0)
            # pygame.draw.circle(self.screen, (120,120,120), (300, 20), 10, 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            title = title_font.render("B", True, (255, 255, 255))
            self.screen.blit(title, (15, 12))

            self.table.update()
            self.screen.blit(self.table, (0, 40))
            pygame.display.flip()

            for event in pygame.event.get():
                super(SCBadgeGameResearch, self).events(event)
                self.table.events(event)
                if event.type == pygame.USEREVENT + 1:
                    print "FLIP ME"
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_RIGHT:
                        pygame.event.post(
                            pygame.event.Event(pygame.USEREVENT + 3))
                    if event.key == K_b:
                        self.running = False
