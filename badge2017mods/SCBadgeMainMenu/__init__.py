# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import PirateAnimation
from SCBadgeView import SCBadgeView
import SCBadgeGameMenu
import SCBadgeSettings
import SCBadgeSchedule
import SCBadgeMaps
import random
import os
import threading
import time


class SCBadgeMainMenu(SCBadgeView):

    def __init__(self, accel, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)
        self.apps = [{"app": SCBadgeGameMenu.SCBadgeGameMenu(self.accel, self.screen, self.btgk), "name": "Game", "icon": "assets/icons-game"}, {"app": SCBadgeSettings.SCBadgeSettings(self.accel, self.screen, self.btgk), "name": "Settings", "icon": "assets/icons-settings"}, {
            "app": SCBadgeSchedule.SCBadgeSchedule(self.accel, self.screen, self.btgk), "name": "Schedule", "icon": "assets/icons-schedule"}] #{"app": SCBadgeMaps.SCBadgeMaps(self.accel, self.screen, self.btgk), "name": "Map", "icon": "assets/icons-maps"}]

    def run(self):
        self.running = True
        selected_index = [0, 0]
        keys = [False, False, False, False, False]
        clock = pygame.time.Clock()
        bg = pygame.image.load("assets/boot-splash-pattern.png")
        bg = bg.convert()
        bg.set_alpha(130)
        clock.tick(60)
        width, height = 320, 240
        apps = self.apps

        chunked = [apps[i:i + 3] for i in xrange(0, len(apps), 3)]

        while self.running:
            if not self.accel.orientation:
                self.running = False
            if keys[0]:
                if selected_index[1] > 0:
                    selected_index[1] -= 1
                keys[0] = False
            if keys[1]:
                if selected_index[1] < len(chunked) - 1:
                    selected_index[1] += 1
                    if selected_index[0] > len(chunked[1]) - 1:
                        selected_index[0] = len(chunked[1]) - 1
                keys[1] = False
            if keys[2]:
                if selected_index[0] > 0:
                    selected_index[0] -= 1
                keys[2] = False
            if keys[3]:
                if selected_index[0] < len(chunked[selected_index[1]]) - 1:
                    selected_index[0] += 1
                keys[3] = False

            if keys[4]:
                chunked[selected_index[1]][selected_index[0]]["app"].run()
                keys[4] = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg, (0, 0))
            for r in xrange(0, len(chunked)):
                for c in xrange(0, len(chunked[r])):
                    if r == selected_index[1] and c == selected_index[0]:
                        try:
                            # pygame.draw.circle(self.screen, (247,148,30),
                            # (65+(c*100), 70+(r*100)), 35, 0)
                            icon = pygame.image.load(
                                chunked[r][c]["icon"] + "-on.png")
                            self.screen.blit(
                                icon, (33 + (c * 100), 38 + (r * 100)))
                            # app_font =
                            # pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',
                            # 16)
                            app_font = pygame.font.Font(
                                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
                            app_title = app_font.render(
                                chunked[r][c]["name"], True, (255, 255, 255))
                            self.screen.blit(
                                app_title, (65 + (c * 100) - app_title.get_width() / 2, 110 + (r * 100)))
                        except Exception as e:
                            print e
                    else:
                        try:
                            # pygame.draw.circle(self.screen, (255,255,255),
                            # (65+(c*100), 70+(r*100)), 35, 0)
                            icon = pygame.image.load(
                                chunked[r][c]["icon"] + "-off.png")
                            self.screen.blit(
                                icon, (33 + (c * 100), 38 + (r * 100)))
                            # app_font =
                            # pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf',
                            # 16)
                            app_font = pygame.font.Font(
                                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
                            app_title = app_font.render(
                                chunked[r][c]["name"], True, (255, 255, 255))
                            self.screen.blit(
                                app_title, (65 + (c * 100) - app_title.get_width() / 2, 110 + (r * 100)))
                        except Exception as e:
                            print e

            pygame.display.flip()
            for event in pygame.event.get():
                super(SCBadgeMainMenu, self).events(event)
                if event.type == pygame.USEREVENT + 1:
                    print "FLIP ME"
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
