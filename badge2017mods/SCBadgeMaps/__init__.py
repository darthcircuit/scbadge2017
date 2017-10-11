# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import PirateAnimation
from SCBadgeView import SCBadgeView
import random
import os
import threading
import time


class SCBadgeMaps(SCBadgeView):

    def __init__(self, accel, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)

    def run(self):
        self.running = True
        selected_index = [0, 0]
        keys = [False, False, False, False, False]
        clock = pygame.time.Clock()
        bg = pygame.image.load("splash.png")
        bg = bg.convert()
        bg.set_alpha(85)
        clock.tick(60)

        while self.running:
            if not self.accel.orientation:
                self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                super(SCBadgeMaps, self).events(event)
                if event.type == pygame.USEREVENT + 1:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        keys[0] = True
                    if event.key == K_DOWN:
                        keys[1] = True
                    if event.key == K_LEFT:
                        keys[2] = True
                    if event.key == K_RIGHT:
                        keys[3] = True
                    if event.key == K_a:
                        keys[4] = True
                    if event.key == K_b:
                        self.running = False
