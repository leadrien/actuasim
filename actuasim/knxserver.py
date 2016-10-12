# -*- coding: utf-8 -*-

import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal

__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.2"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"


class Knxserver(QObject, threading.Thread):

    udp_port = 3671
    trigger = pyqtSignal([list])

    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_running = True
        self.addr = None

    def run(self):
        try:
            self.socket.bind(('', self.udp_port))
            while self.server_running:
                data, self.addr = self.socket.recvfrom(1024)
                if data:
                    if len(data) > len(b'exit'):
                        self.trigger.emit([data])
        finally:
            self.socket.close()

    def send(self, frame):
        if self.server_running:
            if self.addr is not None:
                self.socket.sendto(frame, self.addr)

    def close_server(self):
        self.server_running = False
        self.socket.sendto(b'exit', ('localhost', self.udp_port))

if __name__ == '__main__':
    serv = Knxserver()
    serv.start()