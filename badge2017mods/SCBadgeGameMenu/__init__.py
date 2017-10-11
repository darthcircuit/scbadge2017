# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import PirateAnimation
from SCBadgeView import SCBadgeView
import SCBadgeGameResearch
import SCBadgeGameDiscovery
import SCBadgeGameInventory
import SCBadgeGameHelp
import random
import dataset
import os
import threading
import time


class SCBadgeGameMenu(SCBadgeView):

    def __init__(self, accel,  screen, btgk):
        SCBadgeView.__init__(self, accel,  screen, btgk)
        self.db = dataset.connect('sqlite:///badges.db')
        self.apps = [SCBadgeGameDiscovery.SCBadgeGameDiscovery(self.accel, self.screen, self.btgk), SCBadgeGameInventory.SCBadgeGameInventory(
            self.accel, self.screen, self.btgk), SCBadgeGameHelp.SCBadgeGameHelp(self.accel, self.screen, self.btgk)]

    def run(self):
        self.running = True
        keys = [False, False, False, False]
        clock = pygame.time.Clock()
        bg = pygame.image.load("assets/boot-splash-pattern.png")
        bg = bg.convert()
        bg.set_alpha(130)

        clock.tick(60)
        buttons = ["ATTACK", "DISCOVERED"]
        selected_index = 0
        padding = 10
        bwidth = 130
        bheight = 50
        tmp = self.db['badges']
        if tmp:
            discovered = [b for b in self.db['badges']]
        else:
            discovered = []

        w = self.db['wins']
        if w:
            wins = [a for a in w]
        else:
            wins = []
        while self.running:
            if keys[0]:
                # pygame.event.post(pygame.event.Event(pygame.USEREVENT + 3))
                if selected_index > 0:
                    selected_index -= 1
                keys[0] = False
            if not self.accel.orientation:
                print "ORIENTATION STOP"
                self.running = False
            if keys[1]:
                if selected_index < len(buttons) - 1:
                    selected_index += 1
                keys[1] = False
            if keys[2]:
                self.running = False
                keys[2] = False
            if keys[3]:
                self.apps[selected_index].run()
                keys[3] = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(bg, (0, 0))
            # pygame.draw.rect(self.screen, (200,200,200), (165, 10, 130, 130),
            # 0)
            logo = pygame.image.load("assets/badgepwn.png")
            self.screen.blit(logo, (160, 10))
            font = pygame.font.Font(
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
            text = font.render("BadgePwn", True, (255, 255, 255))
            self.screen.blit(text, [160, 150])
            # lvl = font.render("lvl. 1", True, (255,255,255))
            # self.screen.blit(lvl, [185, 120])
            row = 0
            bfont = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)

            discov_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            discov_text = discov_font.render(
                "Badges Discovered: %d" % len(discovered), True, (255, 255, 255))
            self.screen.blit(discov_text, [20, 200])

            score_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            score_text = score_font.render(
                "Score: %d" % (len(discovered) * 10 + len(wins) * 15), True, (255, 255, 255))
            self.screen.blit(score_text, [20, 220])

            for i in buttons:
                if row == selected_index:
                    pygame.draw.rect(self.screen, (247, 148, 30), (
                        10, padding + (bheight * row + padding * row), 130, 50), 0)
                    text = bfont.render(i, True, (0, 0, 0))
                    self.screen.blit(
                        text, [15, padding + (bheight * row + padding * row)])
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), (
                        10, padding + (bheight * row + padding * row), 130, 50), 0)
                    text = bfont.render(i, True, (0, 0, 0))
                    self.screen.blit(
                        text, [15, padding + (bheight * row + padding * row)])
                row += 1
            pygame.display.flip()

            for event in pygame.event.get():
                super(SCBadgeGameMenu, self).events(event)
                if event.type == pygame.USEREVENT + 1:
                    print "FLIP ME"
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        keys[0] = True
                    if event.key == K_DOWN:
                        keys[1] = True
                    if event.key == K_b:
                        keys[2] = True
                    if event.key == K_a:
                        keys[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        keys[0] = False
                    if event.key == K_DOWN:
                        keys[1] = False
                    if event.key == K_b:
                        keys[2] = False
                    if event.key == K_a:
                        keys[3] = False
