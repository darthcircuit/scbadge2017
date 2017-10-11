# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import PirateAnimation
from SCBadgeView import SCBadgeView
import random
import dataset
import os
import threading
import time


class SCBadgeGameHelp(SCBadgeView):

    def __init__(self, accel,  screen, btgk):
        SCBadgeView.__init__(self, accel,  screen, btgk)

    def run(self):
        self.running = True
        keys = [False, False, False, False]
        clock = pygame.time.Clock()
        bg = pygame.image.load("assets/boot-splash-pattern.png")
        bg = bg.convert()
        bg.set_alpha(130)
        clock.tick(60)
        selected_index = 0

        while self.running:
            if not self.accel.orientation:
                print "ORIENTATION STOP"
                self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                super(SCBadgeGameHelp, self).events(event)
                if event.type == pygame.USEREVENT + 1:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_b:
                        self.running = False
