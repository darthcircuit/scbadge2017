from cryptography.fernet import Fernet
# from mpu6050 import mpu6050
import SCBadgeGameDefend
import pygame
import threading
import signal
import bluetooth
import time
import random
import json
import sys
import os

request = threading.local()

# Need to work out the hand shake of building connections between the badges
# Who is the server and who is the client and how that will work.
# will need to add run to its own thread.


class BTGameKit():

    def __init__(self, import_name):
        os.system("hciconfig hci0 piscan")
        self.gen_key = Fernet.generate_key()
        key = "oYJQ9Ro-0Dr0G57zxvM8fVjuuP9HDvAWxe9fF6zrsqI="
        self.cipher = Fernet(key)
        self.threads = []
        self.listening = None
        self.badges = []
        self.rules = {}
        self.player = ""
        self.s = False
        self.searching = False
        self.cnx = None
        self.display_mode = True
        self.uuid = "8286E00D-755B-4EA1-8BA9-2A4C6BACDB34"

    def advertise(self, player):
        print player
        print "Start Advertising..."
        try:
            self.socket.close()
        except Exception as e:
            print e
        self.player = player
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.bind(("", bluetooth.PORT_ANY))
        self.socket.listen(1)
        bluetooth.advertise_service(
            self.socket, player, description="PASSWORD:6YABSX71B8EVFA8S", service_id=self.uuid,
            service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])

    def stop_search(self):
        self.searching = False

    def search(self):
        if not self.s:
            self.s = True
            self.searching = True
            print "Start Searching..."
            t = threading.Thread(target=self.__find_badges)
            t.daemon = True
            t.start()

    def __find_badges(self):
        try:
            self.badges = bluetooth.find_service(uuid=self.uuid)
            print self.badges
            if len(self.badges) < 1 and self.searching:
                self.__find_badges()
            else:
                print "Stop Searching..."
                self.s = False
                self.searching = False
                self.rules['found']()
        except bluetooth.BluetoothError as e:
            self.s = False
            self.searching = False
            print e

    def connect(self, badge_id):
        try:
            badge = (self.badges[badge_id][
                     'host'], self.badges[badge_id]['port'])
            self.cnx = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.cnx.connect(badge)
            thread = threading.Thread(target=self.__read_data_from_client)
            thread.daemon = True
            thread.start()
            return True
        except Exception as e:
            print e
            return False

    def run(self):
        try:
            self.listening = threading.Thread(target=self.__listen)
            self.listening.daemon = True
            self.listening.start()
        except Exception as e:
            print "Error"

    def __handle_data(self, data):
        if data['handler'] in self.rules:
            request.data = data
            self.rules[data['handler']]()

    def __listen(self):
        self.cnx, addr = self.socket.accept()
        pygame.event.post(pygame.event.Event(pygame.USEREVENT + 3))
        self.__read_data_from_client()

    def __read_data_from_client(self):
        try:
            print "Waiting for data..."
            listening = True
            while listening:
                data = self.cnx.recv(1024)
                print data
                try:
                    packet = json.loads(data)
                    if "attack" in packet:
                        if "user" in packet:
                            pygame.event.post(
                                pygame.event.Event(pygame.USEREVENT, data={"type": "attacked", "user" : packet['user']}))
                        else:
                            pygame.event.post(
                                pygame.event.Event(pygame.USEREVENT, data={"type": "attacked"}))
                        self.cnx.send(json.dumps({"stop": 1}))
                        print packet['attack']
                        listening = False
                    if "defend" in packet:
                        pygame.event.post(
                            pygame.event.Event(pygame.USEREVENT, data={"type": "defended"}))
                        self.cnx.send(json.dumps({"stop": 1}))
                        print packet['defend']
                        listening = False
                    if "stop" in packet:
                        print "STOP PACKET"
                        listening = False
                except Exception as e:
                    print "BAD PACKET"

        except Exception as e:
            print "LISTEN PROBLEM"
            print e
            self.run()
        print "STOP"
        self.run()

    def route(self, rule, **options):
        def decorator(f):
            self.rules[rule] = f
            return f
        return decorator


if __name__ == "__main__":
    # driver example/tester
    app = BTGameKit(__name__)
    app.search()
    app.advertise("atticus88")

    @app.route('found')
    def found():
        print "FOUND"
        app.connect(0)

    @app.route('connection_established')
    def found():
        pass

    app.run()

    # SIMULAT PYGAME LOOP
    while True:
        pass
