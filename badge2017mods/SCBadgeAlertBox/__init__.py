# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from SCBadgeAnimations import Pirate
import SCBadgeGameResult
import random
import os
import json
import LEDS
import threading
import time


class SCBadgeAlertBox(object):

    def __init__(self, data,  screen, btgk):
        self.screen = screen
        self.data = data
        self.btgk = btgk
        self.leds = LEDS.LEDS()

    def drawText(self, surface, text, color, rect, font, aa=True, bkg=None):
        rect = Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        clock.tick(60)
        flash = time.time() + 1
        stop = time.time() + 5
        dimmer = True

        while self.running:
            if stop < time.time():
                self.running = False

            if dimmer:
                s = pygame.Surface((320, 240))
                s.set_alpha(100)
                s.fill((0, 0, 0))
                self.screen.blit(s, (0, 0))
                dimmer = False

            pygame.draw.rect(
                self.screen, (100, 100, 100), (10, 20, 300, 150), 0)
            pygame.draw.rect(self.screen, (60, 60, 60), (10, 20, 300, 30), 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
            title = title_font.render("Alert Message", True, (255, 255, 255))
            self.screen.blit(title, (160 - title.get_width() / 2, 25))

            message_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            # message = message_font.render(self.data['msg'], True, (255,255,255))
            # self.screen.blit(message, (15,55))
            box_content = pygame.Surface((300, 110))
            self.drawText(self.screen, self.data['msg'], (
                255, 255, 255), (15, 55, 290, 110), message_font)

            # count_down_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
            # count_down = count_down_font.render("%ds" % (stop - time.time()), True, (255,255,255))
            # self.screen.blit(count_down, (80,80))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.running = False
