# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import random
import os
import json
import threading
import time
import dataset


class SCBadgeGameResult(object):

    def __init__(self, data,  screen, btgk):
        self.screen = screen
        self.data = data
        self.btgk = btgk

    def dynamic_font(self, text,  size, color):
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
        if font.size(text)[0] > self.screen.get_rect().width:
            return self.dynamic_font(text, size - 2, color)
        return font.render(text, True, color)

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        # bg = pygame.image.load("splash.png")
        clock.tick(60)
        stop = time.time() + 10
        while self.running:
            if stop < time.time():
                self.running = False

            self.screen.fill((0, 0, 0))
            # self.screen.blit(bg, (0,0))

            if self.data == "win":
                name_font = pygame.font.Font(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
                name_text = name_font.render(
                    "Winner Winner", True, (255, 255, 255))
                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 10])

            else:
                name_font = pygame.font.Font(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
                name_text = name_font.render(
                    "Loser Loser", True, (255, 255, 255))
                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 10])

            # count_down_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
            # count_down = count_down_font.render("%ds" % (stop - time.time()), True, (255,255,255))
            # self.screen.blit(count_down, (80,80))

            pygame.display.flip()

            for event in pygame.event.get():
                pass
