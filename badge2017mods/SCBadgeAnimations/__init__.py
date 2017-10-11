import pygame
import os
import time
from pygame.locals import *
import itertools
from random import randint


class Pirate(object):

    def __init__(self, screen):
        self.screen = screen
        self.playing = True
        self.ptime = time.time()
        self.images = []
        self.loop = 10
        self.index = 0

    def load(self):
        self.images = []
        i = len(
            [name for name in os.listdir('/home/pi/badge2017/Animations/hack/')]) - 1
        x = randint(0, i)
        size = len(
            [name for name in os.listdir('/home/pi/badge2017/Animations/hack/%d/' % (x))])
        path = ["/home/pi/badge2017/Animations/hack/" +
                str(x) + "/" + "%02d" % (num) + ".png" for num in range(0, size)]
        for p in path:
            self.images.append(pygame.image.load(p))
        self.animation = itertools.cycle(self.images)

    def play(self, loop, msg=""):
        self.load()
        # self.loop = loop
        self.loop = time.time() + 8
        self.playing = True
        self.index = 0
        while self.playing:
            for event in pygame.event.get():
                pass
            self.screen.blit(self.images[self.index], (0, 0))

            if msg != "":
                pygame.draw.rect(self.screen, (70, 70, 70), (0, 0, 320, 35))
                name_font = pygame.font.Font(
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
                name_text = name_font.render(msg, 36, (255, 255, 255))

                half = name_text.get_width() / 2
                self.screen.blit(name_text, [160 - half, 5])

            pygame.display.flip()

            if self.index < len(self.images) - 1:
                if time.time() - self.ptime > 0.08:
                    self.index += 1
                    self.ptime = time.time()
            else:
                self.index = 0
                if self.loop < time.time():
                    self.playing = False
