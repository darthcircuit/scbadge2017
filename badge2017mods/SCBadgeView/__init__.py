# -*- coding: utf-8 -*-
import pygame
import math
from pygame.locals import *
from SCBadgeAnimations import Pirate
import SCBadgeGameDefend
import SCBadgeAlertBox
import random
import os
import threading
import time


class SCBadgeView(object):

    def __init__(self, accel, screen, btgk):
        self.running = True
        self.screen = screen
        self.backlight = True
        self.btgk = btgk
        self.accel = accel
        self.orientation = True
        self.pirate = Pirate(self.screen)
        self.konami = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT,
                       K_RIGHT, K_LEFT, K_RIGHT, K_b, K_a, K_ESCAPE, K_RETURN]
        self.konami_index = 0

    def alert(self,  data):
        alert = SCBadgeAlertBox.SCBadgeAlertBox(
            data, self.screen, self.btgk).run()

    def events(self, event):
        if event.type == pygame.USEREVENT + 4:
            self.pirate.play(3)
        if event.type == pygame.USEREVENT + 3:
            SCBadgeGameDefend.SCBadgeGameDefend(
                [], self.screen, self.btgk).run()
        if event.type == pygame.KEYDOWN:
            if event.key == self.konami[self.konami_index]:
                self.konami_index += 1
                if self.konami_index == len(self.konami):
                    self.konami_index = 0
                    self.alert(
                        {"msg": "Good work! Here is a Hackers Challenge Code: EXEIOHA4ABXDO7A7"})
            else:
                self.konami_index = 0

            #if event.key == K_ESCAPE and self.konami_index != 11:
            #    pygame.quit()
            #    exit(0)
