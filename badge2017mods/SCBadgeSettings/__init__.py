# -*- coding: utf-8 -*-
from __future__ import division
import pygame
from pygame.locals import *
import threading
from SCBadgeView import SCBadgeView
import SCBadgeInfo
import LEDS
import random
import pickle
import os


class SCBadgeUpdate(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.internet = False
        self.check = True
        self.running = False
        self.color = []

    def dynamic_font(self, text,  size, color):
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
        if font.size(text)[0] > self.get_rect().width:
            return self.dynamic_font(text, size - 2, color)
        return font.render(text, True, color)

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

    def update(self):
        self.fill((0, 0, 0))
        if self.running:
            pygame.draw.rect(self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 14)
        self.drawText(
            self, "Updating your badge will result in losing your badge settings.",
            (255, 255, 255), (5, 5, 130, 195), font)

        if self.running and  self.check:
            self.internet = SCBadgeInfo.internet()  
            self.check = False

        if self.running and self.internet:
            pygame.draw.rect(self, (247, 148, 30), (16, 100, 100, 40), 0)
        else:
            pygame.draw.rect(self, (200, 200, 200), (16, 100, 100, 40), 0)
        status_text = self.dynamic_font("UPDATE", 16, (255, 255, 255))
        self.blit(status_text, [16+50 - status_text.get_width()/2, 110])

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                if SCBadgeInfo.internet():
                    try:
                        os.system('/home/pi/update.sh')    
                    except Excpetion as e:
                        print "UPDATE FAILED"
                        print e
                else:
                    self.internet = False
            if event.key == K_x:
                self.check = True

class SCBadgeHDMI(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.running = False
        self.color = 0

    def dynamic_font(self, text,  size, color):
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
        if font.size(text)[0] > self.get_rect().width:
            return self.dynamic_font(text, size - 2, color)
        return font.render(text, True, color)

    def update(self):
        self.fill((0, 0, 0))
        name_text = self.dynamic_font("HDMI Power", 16, (255, 255, 255))
        half = name_text.get_width() / 2
        self.blit(name_text, [self.get_width() / 2 - half, 10])


        if self.running:
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)

        if self.color == 0:
            pygame.draw.rect(self, (100, 100, 100), (16, 100, 100, 40), 0)
            pygame.draw.rect(self, (200, 200, 200), (16, 100, 40, 40), 0)
            status_text = self.dynamic_font("OFF", 16, (255, 255, 255))
            self.blit(status_text, [16+40+30 - status_text.get_width()/2, 110])
        else:
            pygame.draw.rect(self, (0, 200, 0), (16, 100, 100, 40), 0)
            pygame.draw.rect(self, (200, 200, 200), (116-40, 100, 40, 40), 0)
            status_text = self.dynamic_font("ON", 16, (255, 255, 255))
            self.blit(status_text, [16+30 - status_text.get_width()/2, 110])

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_DOWN:
                if self.color == 1:
                    os.system('/usr/bin/tvservice -o')
                self.color = 0
            if event.key == K_LEFT:
                if self.color == 1:
                    os.system('/usr/bin/tvservice -o')
                self.color = 0
            if event.key == K_UP:
                if self.color == 1:
                    os.system('/usr/bin/tvservice -p')
                self.color = 1
            if event.key == K_RIGHT:
                if self.color == 1:
                    os.system('/usr/bin/tvservice -p')
                self.color = 1

class SCBadgeLayout(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.running = False
        self.color = 0

    def dynamic_font(self, text,  size, color):
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size)
        if font.size(text)[0] > self.get_rect().width:
            return self.dynamic_font(text, size - 2, color)
        return font.render(text, True, color)

    def update(self):
        self.fill((0, 0, 0))
        if self.running:
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)
        visible = [int(x) for x in bin(self.color)[2:]]
        while len(visible) < 5:
            visible.append(0)
        if visible[0] == 1:
            name_text = self.dynamic_font("Name", 20, (255, 255, 255))
            half = name_text.get_width() / 2
            self.blit(name_text, [self.get_width() / 2 - half, 10])
        if visible[1] == 1:
            name_text = self.dynamic_font("Handle", 20, (255, 255, 255))
            half = name_text.get_width() / 2
            self.blit(name_text, [self.get_width() / 2 - half, 35])
        if visible[2] == 1:
            name_text = self.dynamic_font("HC Score", 20, (255, 255, 255))
            half = name_text.get_width() / 2
            self.blit(name_text, [self.get_width() / 2 - half, 90])
        if visible[3] == 1:
            name_text = self.dynamic_font("Message", 20, (255, 255, 255))
            half = name_text.get_width() / 2
            self.blit(name_text, [self.get_width() / 2 - half, 145])
        if visible[4] == 1:
            name_text = self.dynamic_font("Org.", 20, (255, 255, 255))
            half = name_text.get_width() / 2
            self.blit(name_text, [self.get_width() / 2 - half, 170])

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_DOWN:
                if self.color > 0:
                    self.color -= 1
            if event.key == K_LEFT:
                if self.color > 0:
                    self.color -= 1
            if event.key == K_UP:
                if self.color < 32:
                    self.color += 1
            if event.key == K_RIGHT:
                if self.color < 32:
                    self.color += 1


class SCBadgeCredits(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.running = False
        self.color = []

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

    def update(self):
        self.fill((0, 0, 0))
        if self.running:
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)
        font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
        self.drawText(
            self, "Badge Team:    Luke Jenkins, Jonathan Karras, Klint Holmes, Dustin Woodard                      THANKS:          Troy Jessup    UtahSAINT Board, SAINTCON Committee.                        Eben Upton,    Mike Buffham                                                 RIP Trevor",
            (255, 255, 255), (5, 5, 130, 195), font)

    def events(self, event):
        pass


class SCBadgeNetworkStatus(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.running = False
        self.color = []
        self.status = False
        self.mac = 0
        self.ip = "00:00:00:00:00"
        self.x_count = 0
        self.y_count = 0
        self.check = True

    def update(self):
        self.fill((0, 0, 0))
        if self.check:
            t = threading.Thread(target=SCBadgeInfo.network)
            t.daemon = True
            t.start()
            self.check = False

        if self.running:
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)

        if self.status:
            status = pygame.image.load("assets/network-status-on.png")
            status_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 15)
            status_text = status_font.render("Connected", True, (0, 200, 0))
            self.blit(status_text, (10, 180))
        else:
            status = pygame.image.load("assets/network-status-off.png")
            status_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 15)
            status_text = status_font.render("Not Connected", True, (200, 0, 0))
            self.blit(status_text, (10, 180))

        if self.x_count > 2 and self.y_count > 2:
            status_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 10)
            status_text = status_font.render(self.ip, True, (200, 200, 200))
            self.blit(status_text, (10, 150))
            status_font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 10)
            status_text = status_font.render(':'.join(("%012X" % self.mac)[i:i+2] for i in range(0, 12, 2)), True, (200, 200, 200))
            self.blit(status_text, (10, 165))

        self.blit(status, (-5, 10))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_x:
                self.x_count += 1
            if event.key == K_y:
                self.y_count += 1


class SCBadgeBackgroundColorPicker(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.running = False
        self.keys = [False, False]
        self.selected_index = 0
        self.bg_images = [
            "assets/boot-splash-pattern.jpg", "assets/BGA-1.jpg", "assets/BGA-2.jpg",
            "assets/BGA-3.jpg", "assets/BGA-4.jpg", "assets/BGA-5.jpg", "assets/BGA-6.jpg", "assets/BGA-7.jpg"]
        self.color = 0

    def update(self):
        bg = pygame.image.load(self.bg_images[self.color])
        self.blit(bg, (-100, 0))
        if self.running:
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                if self.color > 0:
                    self.color -= 1
            if event.key == K_RIGHT:
                if self.color < 7:
                    self.color += 1
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                self.keys[0] = False
            if event.key == K_DOWN:
                self.keys[1] = False


class SCBadgeLEDColorPicker(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.running = False
        self.keys = [False, False]
        self.selected_index = 0
        self.color = [15, 100, 255]
        self.leds = LEDS.LEDS()

    def update(self):
        if self.keys[0]:
            if self.color[self.selected_index] < 255:
                self.color[self.selected_index] += 5
        if self.keys[1]:
            if self.color[self.selected_index] > 5:
                self.color[self.selected_index] -= 5

        self.fill((0, 0, 0))
        if self.running:
            self.leds.colorWipe(self.color)
            pygame.draw.rect(self, (247, 148, 30), (
                8 + (45 * self.selected_index), 8, 34, 124), 0)
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)
        else:
            self.leds.colorWipe([0, 0, 0])

        pygame.draw.rect(self, (100, 100, 100), (10, 10, 30, 120), 0)
        pygame.draw.rect(self, (100, 100, 100), (55, 10, 30, 120), 0)
        pygame.draw.rect(self, (100, 100, 100), (100, 10, 30, 120), 0)

        pygame.draw.rect(
            self, (255, 0, 0), (10 + 2, 10 + 2 + (116 - self.color[0] / 255 * 116), 26, ((self.color[0] / 255) * 116)), 0)
        pygame.draw.rect(
            self, (0, 255, 0), (55 + 2, 10 + 2 + (116 - self.color[1] / 255 * 116), 26, ((self.color[1] / 255) * 116)), 0)
        pygame.draw.rect(
            self, (0, 0, 255), (100 + 2, 10 + 2 + (116 - self.color[2] / 255 * 116), 26, ((self.color[2] / 255) * 116)), 0)

        pygame.draw.rect(
            self, (self.color[0], self.color[1], self.color[2]), (8, 160, 123, 30), 0)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
                # if self.color[self.selected_index] < 255:
                #    self.color[self.selected_index] += 5
            if event.key == K_DOWN:
                self.keys[1] = True
                # if self.color[self.selected_index] > 5:
                #     self.color[self.selected_index] -= 5
            if event.key == K_LEFT:
                if self.selected_index > 0:
                    self.selected_index -= 1
            if event.key == K_RIGHT:
                if self.selected_index < 2:
                    self.selected_index += 1
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                self.keys[0] = False
            if event.key == K_DOWN:
                self.keys[1] = False


class SCBadgeColorPicker(pygame.Surface):

    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.keys = [False, False]
        self.running = False
        self.selected_index = 0
        self.color = [15, 100, 255]

    def update(self):
        if self.keys[0]:
            if self.color[self.selected_index] < 255:
                self.color[self.selected_index] += 5
        if self.keys[1]:
            if self.color[self.selected_index] > 5:
                self.color[self.selected_index] -= 5

        self.fill((0, 0, 0))
        if self.running:
            pygame.draw.rect(self, (247, 148, 30), (
                8 + (45 * self.selected_index), 8, 34, 124), 0)
            pygame.draw.rect(
                self, (247, 148, 30), (0, 0, 139, self.get_height()), 3)

        pygame.draw.rect(self, (100, 100, 100), (10, 10, 30, 120), 0)
        pygame.draw.rect(self, (100, 100, 100), (55, 10, 30, 120), 0)
        pygame.draw.rect(self, (100, 100, 100), (100, 10, 30, 120), 0)

        pygame.draw.rect(
            self, (255, 0, 0), (10 + 2, 10 + 2 + (116 - self.color[0] / 255 * 116), 26, ((self.color[0] / 255) * 116)), 0)
        pygame.draw.rect(
            self, (0, 255, 0), (55 + 2, 10 + 2 + (116 - self.color[1] / 255 * 116), 26, ((self.color[1] / 255) * 116)), 0)
        pygame.draw.rect(
            self, (0, 0, 255), (100 + 2, 10 + 2 + (116 - self.color[2] / 255 * 116), 26, ((self.color[2] / 255) * 116)), 0)

        title_font = pygame.font.Font(
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
        title = title_font.render(
            "Sample", True, (self.color[0], self.color[1], self.color[2]))
        self.blit(title, (self.get_width() / 2 - title.get_width() / 2, 160))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
                # if self.color[self.selected_index] < 255:
                #    self.color[self.selected_index] += 5
            if event.key == K_DOWN:
                self.keys[1] = True
                # if self.color[self.selected_index] > 5:
                #     self.color[self.selected_index] -= 5
            if event.key == K_LEFT:
                if self.selected_index > 0:
                    self.selected_index -= 1
            if event.key == K_RIGHT:
                if self.selected_index < 2:
                    self.selected_index += 1
        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                self.keys[0] = False
            if event.key == K_DOWN:
                self.keys[1] = False


class SCBadgeInventoryCell(pygame.Surface):

    def __init__(self, size, data, selected):
        pygame.Surface.__init__(self, size)
        if selected:
            self.fill((247, 148, 30))
        else:
            self.fill((100, 100, 100))
        title_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
        status_font = pygame.font.Font(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
        # title_font = pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf', 16)
        # status_font =
        # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
        # 12)
        self.title = title_font.render(data['title'], True, (255, 255, 255))
        self.status = status_font.render(data['status'], True, (255, 255, 255))
        self.icon = pygame.image.load(data['icon'])
        pygame.draw.rect(self, (200, 200, 200), (10, 7, 25, 25), 0)
        pygame.draw.line(self, (50, 50, 50), (0, 39), (320, 39), 1)
        self.blit(self.icon, (10, 7))
        self.blit(self.title, (40, 5))
        self.blit(self.status, (40, 20))


class SCBadgeScrollView(pygame.Surface):

    def __init__(self, size, data=[]):
        pygame.Surface.__init__(self, size)
        self.selected_index = 0
        self.data = data
        self.offset = 0
        self.visible = 4
        self.keys = [False, False, False, False]
        self.row_height = 40

    def scroll_up(self):
        if self.selected_index - 1 >= 0:
            self.selected_index -= 1

    def scroll_down(self):
        if self.selected_index + 1 < len(self.data):
            self.selected_index += 1

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
            if (i - self.offset) * 40 < self.get_height():
                cell = SCBadgeInventoryCell(
                    (320, 40), self.data[i], i == self.selected_index)
                self.blit(cell, (0, 40 * (i - self.offset)))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.keys[0] = True
            if event.key == K_DOWN:
                self.keys[1] = True


class SCBadgeSettings(SCBadgeView):

    def __init__(self, accel, screen, btgk):
        SCBadgeView.__init__(self, accel, screen, btgk)
        self.running = True
        text_color_picker = SCBadgeColorPicker((149, 200))
        bg_color_picker = SCBadgeBackgroundColorPicker((149, 200))
        led_color_picker = SCBadgeLEDColorPicker((149, 200))
        self.network_status = SCBadgeNetworkStatus((149, 200))
        credits = SCBadgeCredits((149, 200))
        menu_layout = SCBadgeLayout((149, 200))
        hdmi_setting = SCBadgeHDMI((149,200))
        update_setting = SCBadgeUpdate((149,200))
        self.data = [
            {"id": "name_text", "title": "Name Badge", "status": "Text Color",
                "icon": "assets/settings-text.png", "app": text_color_picker},
            {"id": "name_layout", "title": "Name Badge", "status": "Layout",
             "icon": "assets/settings-layout.png", "app": menu_layout},
            {"id": "background_color", "title": "Background", "status": "Image",
             "icon": "assets/settings-background.png", "app": bg_color_picker},
            {"id": "led_color", "title": "LED Alert", "status": "Color",
             "icon": "assets/settings-led.png", "app": led_color_picker},
            {"id": "netowrk", "title": "Network", "status": "Status",
             "icon": "assets/settings-network.png", "app": self.network_status},
            {"id": "hdmi", "title": "HDMI", "status": "Power",
             "icon": "assets/settings-background.png", "app": hdmi_setting},
            {"id": "credits", "title": "Credits", "status": "Thanks", "icon": "assets/settings-credits.png", "app": credits},
            {"id": "credits", "title": "Update", "status": "Badge Code", "icon": "assets/settings-layout.png", "app": update_setting}]
        self.table = SCBadgeScrollView((180, 200), self.data)

    def run(self):

        if os.path.exists('settings.p'):
            lsettings = pickle.load(open("settings.p", 'rb'))
        else:
            lsettings = {'name_text': [255, 255, 255], 'led_color': [255, 0, 0], 'credits': [
                255, 165, 60], 'background_color': 0, 'name_layout': 27, 'netowrk': [255, 165, 60]}

        for s in self.data:
            try:
                s['app'].color = lsettings[s['id']]
            except:
                print s['id']
                s['app'].color = [255, 255, 255]

        self.running = True
        clock = pygame.time.Clock()
        clock.tick(60)

        while self.running:

            self.screen.fill((0, 0, 0))

            # Titlebar
            pygame.draw.rect(self.screen, (170, 170, 170), (0, 0, 340, 20), 0)
            pygame.draw.rect(self.screen, (190, 190, 190), (0, 19, 340, 20), 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            # title_font =
            # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
            # 20)
            title = title_font.render("Settings", True, (0, 0, 0))
            self.screen.blit(
                title, (self.screen.get_width() / 2 - title.get_width() / 2, 10))
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
            # title_font =
            # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
            # 20)
            title = title_font.render("Settings", True, (255, 255, 255))
            self.screen.blit(
                title, ((self.screen.get_width() / 2 - title.get_width() / 2) + 1, 9))
            pygame.draw.circle(self.screen, (100, 100, 100), (20, 21), 10, 0)
            pygame.draw.circle(self.screen, (255, 116, 30), (20, 20), 10, 0)
            title_font = pygame.font.Font(
                '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
            # title_font =
            # pygame.font.Font('/usr/share/fonts/truetype/droid/DroidSans-Bold.ttf',
            # 16)
            title = title_font.render("B", True, (255, 255, 255))
            self.screen.blit(title, (15, 12))

            self.table.update()
            # self.color_picker.update()
            self.screen.blit(self.table, (0, 40))

            self.data[self.table.selected_index]['app'].update()
            self.screen.blit(
                self.data[self.table.selected_index]['app'], (181, 40))
            pygame.display.flip()

            for event in pygame.event.get():
                if self.data[self.table.selected_index]['app'].running:
                    self.data[self.table.selected_index]['app'].events(event)
                else:
                    self.table.events(event)
                super(SCBadgeSettings, self).events(event)
                if event.type == USEREVENT:
                    print event
                    if event.data['type'] == 'network':
                        self.network_status.status = event.data['status']
                        self.network_status.mac = event.data['mac']
                        self.network_status.ip = event.data['ip']
                if event.type == pygame.USEREVENT + 1:
                    settings = {}
                    for s in self.data:
                        settings[s['id']] = s['app'].color
                    pickle.dump(settings, open("settings.p", "wb"))
                    if self.data[self.table.selected_index]['id'] == 'led_color':
                        self.data[self.table.selected_index]['app'].running = False
                        self.data[self.table.selected_index]['app'].leds.colorWipe([0,0,0])
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_a:
                        self.data[self.table.selected_index][
                            'app'].running = True
                    if event.key == K_b:
                        if self.data[self.table.selected_index]['app'].running:
                            self.data[self.table.selected_index][
                                'app'].running = False
                        else:
                            settings = {}
                            self.network_status.check = True
                            for s in self.data:
                                settings[s['id']] = s['app'].color
                            print settings
                            pickle.dump(settings, open("settings.p", "wb"))
                            self.running = False
