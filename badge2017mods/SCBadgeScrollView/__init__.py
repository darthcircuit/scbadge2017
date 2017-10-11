# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from SCBadgeView import SCBadgeView
import random
import os


class SCBadgeScrollView(SCBadgeView):

    def __init__(self, data, screen):
        SCBadgeView.__init__(self, screen)
        self.selected_index = 0
        self.data = data
        self.offset = 0
        self.visible = self.screen.get_height() / 25
        self.keys = [False, False]
        self.row_height = 45

    def scroll_up(self):
        if self.selected_index - 1 >= 0:
            self.selected_index -= 1

    def scroll_down(self):
        if self.selected_index + 1 < len(self.data):
            self.selected_index += 1

    def list_item(self, text, name, size, color, selected):
        if text in self.owned:
            text = u'\u2605 ' + text
        else:
            text = u'\u2606 ' + text
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)
        if font.size(text)[0] > self.screen.get_rect().width:
            return dynamic_font(text, name, size - 2, color)
        if selected:
            return font.render(text, True, (0, 0, 0), color)
        return font.render(text, True, color)

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

        for i in xrange(self.offset, len(self.data)):
            if self.selected_index == i:
                pygame.draw.rect(self.screen, (0, 255, 0), [
                                 0, ((i - self.offset) * self.row_height + 45), self.screen.get_rect().width - 2,  self.row_height], 0)
            li = self.list_item(
                self.data[i]['name'], "", 22, (0, 255, 255), False)
            li_rect = li.get_rect()
            li_rect.topleft = [20, ((i - self.offset) * self.row_height + 45)]
            pygame.draw.line(self.screen, (100, 100, 100), [0, ((i - self.offset) * self.row_height + 45 + self.row_height) - 1], [
                             self.screen.get_rect().width - 2, ((i - self.offset) * self.row_height + 45 + self.row_height) - 1], 1)
            # pygame.draw.line(self.screen, (255,255,255), [0,((i -
            # self.offset) * self.row_height + 45+self.row_height)],
            # [self.screen.get_rect().width-2, ((i - self.offset) *
            # self.row_height + 45+self.row_height )], 1)
            pygame.draw.line(self.screen, (100, 100, 100), [0, ((i - self.offset) * self.row_height + 45 + self.row_height) + 1], [
                             self.screen.get_rect().width - 2, ((i - self.offset) * self.row_height + 45 + self.row_height) + 1], 1)
            if (i - self.offset) * 25 < self.screen.get_height():
                self.screen.blit(li, li_rect)

    def events(self, event):
        super(SCBadgeScrollView, self).events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
            if event.key == K_DOWN:
                self.keys[1] = True
