import pygame
import time
from pygame.locals import *
import itertools


class Pirate(object):

    def __init__(self, screen):
        self.screen = screen
        self.playing = True
        self.ptime = time.time()
        self.loop = 3
        self.index = 0
        path = ["/home/pi/badge2017/PirateAnimation/images/p" + "%02d" %
                (num) + ".tiff" for num in range(1, 30)]
        self.images = []
        for p in path:
            self.images.append(pygame.image.load(p))
        self.animation = itertools.cycle(self.images)

    def play(self, loop):
        self.loop = loop
        self.playing = True
        self.index = 0
        while self.playing:
            self.screen.blit(self.images[self.index], (-26, -13))
            pygame.display.flip()

            if self.index < len(self.images) - 1:
                if time.time() - self.ptime > 0.1:
                    self.index += 1
                    self.ptime = time.time()
            else:
                self.index = 0
                self.loop -= 1
                if self.loop == 0:
                    self.playing = False
