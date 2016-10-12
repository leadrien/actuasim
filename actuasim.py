#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import random
import logging

from logging.handlers import RotatingFileHandler
from collections import OrderedDict
from PyQt5.QtWidgets import *

from knxnet import *

from actuasim.room import Room
from actuasim.ui_actuasim import Ui_MainWindow
from actuasim.knxserver import Knxserver
from actuasim.command_handler import CommandHandler


__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.2"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"


class Actuasim(QMainWindow):

    save_filename = 'saved_rooms.json'

    def __init__(self):
        super(Actuasim, self).__init__()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('actuasim.log', 'a', 10000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.info('=======================================')
        self.logger.info('           ACTUASIM START')
        self.logger.info('=======================================')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1700, 900)
        self.classrooms = []
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.file_menu = self.ui.menubar.addMenu("&File")
        self.save_action = QAction("&Save", self, triggered=self.save)
        self.file_menu.addAction(self.save_action)
        self.load_action = QAction("&Load", self, triggered=self.load)
        self.file_menu.addAction(self.load_action)
        self.command_handler = CommandHandler(self)

        # endpoints, status, id
        self.control_endpoint = ('0.0.0.0', 0)
        self.data_endpoint = ('0.0.0.0', 0)
        self.status = 0
        self.channel_id = random.randint(0, 255)  # TODO: handle multiple channel
        self.tunnel_req_data_response = None  # Store the tunneling request that contains the response for a read

        # server
        self.knxserver = Knxserver()
        self.knxserver.trigger.connect(self.frame_received)
        self.knxserver.start()

    def load_rooms(self, json_data=None):
        self._clean_rooms()
        if json_data is not None:
            data = json.loads(json_data, object_pairs_hook=OrderedDict)
            for key, val in data.items():
                room = Room.from_dict(title=key, room_dict=val)
                self.classrooms.append(room)
                self.tabs.addTab(room, key)

    def save(self):
        classrooms = OrderedDict()
        for i in range(self.tabs.count()):
            room = self.tabs.widget(i)
            classrooms[room.title] = room.get_room_dict()
        json_data = json.dumps(classrooms, indent=4)
        with open(Actuasim.save_filename, 'w') as f:
            f.write(json_data)

    def load(self):
        if os.path.isfile(Actuasim.save_filename):
            with open(Actuasim.save_filename, 'r') as f:
                json_data = f.read()
            self.load_rooms(json_data)
            return True
        else:
            m = "{0} not found".format(Actuasim.save_filename)
            print(m)
            logging.error(m)
            return False

    def load_room_template(self):
        template = """
                    {
                        "room 1": {
                            "blinds": [
                                {
                                    "value": 19,
                                    "address": "1.0.0@1/4/1"
                                },
                                {
                                    "value": 19,
                                    "address": "1.0.1@1/4/2"
                                }
                            ],
                            "valves": [
                                {
                                    "value": 19,
                                    "address": "1.0.2@0/4/1"
                                },
                                {
                                    "value": 19,
                                    "address": "1.0.3@0/4/2"
                                }
                            ]
                        },
                        "room 2": {
                            "blinds": [
                                {
                                    "value": 19,
                                    "address": "2.0.0@1/4/10"
                                },
                                {
                                    "value": 19,
                                    "address": "2.0.1@1/4/11"
                                }
                            ],
                            "valves": [
                                {
                                    "value": 19,
                                    "address": "2.0.2@0/4/10"
                                },
                                {
                                    "value": 19,
                                    "address": "2.0.3@0/4/11"
                                }
                            ]
                        }
                    }
                """
        self.load_rooms(template)

    def frame_received(self, frame):
        self.logger.info('Frame received:' + str([hex(h) for h in frame[0]]))
        decoded_frame = knxnet.decode_frame(frame[0])
        if decoded_frame.header.service_type_descriptor == knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST:
            self.logger.info('= Connection request:\n' + str(decoded_frame))
            conn_resp = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_RESPONSE,
                                            self.channel_id,
                                            self.status,
                                            self.data_endpoint)
            self.knxserver.send(conn_resp.frame)
            self.logger.info('Frame sent:' + repr(conn_resp))
            self.logger.info('= Connection response:\n' + str(conn_resp))
        elif decoded_frame.header.service_type_descriptor == knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST:
            self.logger.info('= Connection state request:\n' + str(decoded_frame))
            conn_state_resp = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_RESPONSE,
                                                  self.channel_id,
                                                  self.status)
            self.knxserver.send(conn_state_resp.frame)
            self.logger.info('Frame sent:' + repr(conn_state_resp))
            self.logger.info('= Connection state response:\n' + str(conn_state_resp))
        elif decoded_frame.header.service_type_descriptor == knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST:
            self.logger.info('= Disconnect request:\n' + str(decoded_frame))
            disconnect_resp = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_RESPONSE,
                                                  self.channel_id,
                                                  self.status)
            self.knxserver.send(disconnect_resp.frame)
            self.logger.info('Frame sent:' + repr(disconnect_resp))
            self.logger.info('= Disconnect response:\n' + str(disconnect_resp))
        elif decoded_frame.header.service_type_descriptor == knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST:
            self.logger.info('= Tunnelling request:\n' + str(decoded_frame))
            self.tunnel_req_data_response = self.command_handler.handle_tunnelling_request(decoded_frame)
            tunnel_ack = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_ACK,
                                             self.channel_id,
                                             self.status,
                                             decoded_frame.sequence_counter)
            self.knxserver.send(tunnel_ack.frame)
            self.logger.info('Frame sent:' + repr(tunnel_ack))
            self.logger.info('= Tunnelling ack:\n' + str(tunnel_ack))

            # after sending our tunnelling ack
            # we must send a tunnelling request to confirm the data
            data_service = 0x2e
            sequence_counter = 0
            tunnel_req_confirm = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST,
                                                     decoded_frame.dest_addr_group,
                                                     decoded_frame.channel_id,
                                                     decoded_frame.data,
                                                     decoded_frame.data_size,
                                                     decoded_frame.apci,
                                                     data_service,
                                                     sequence_counter)
            self.knxserver.send(tunnel_req_confirm.frame)
            self.logger.info('Frame sent:' + repr(tunnel_req_confirm))
            self.logger.info('= Tunnelling ack:\n' + str(tunnel_req_confirm))

        elif decoded_frame.header.service_type_descriptor == knxnet.ServiceTypeDescriptor.TUNNELLING_ACK:
            self.logger.info('= Tunnelling ack:\n' + str(decoded_frame))
            # Do we have a response to send?
            if self.tunnel_req_data_response:
                self.knxserver.send(self.tunnel_req_data_response.frame)
                self.logger.info('Frame sent:' + repr(self.tunnel_req_data_response))
                self.logger.info('= Tunnelling request:\n' + str(self.tunnel_req_data_response))
                self.tunnel_req_data_response = None

        else:
            self.logger.info('The frame is not supported')

    def closeEvent(self, QCloseEvent):
        self.knxserver.close_server()
        self.save()
        self.logger.info('=======================================')
        self.logger.info('    *****   ACTUASIM STOP   *****')
        self.logger.info('=======================================')

    def _clean_rooms(self):
        for i in range(len(self.tabs)):
            self.tabs.removeTab(0)
        for room in self.classrooms:
            room.deleteLater()
        self.classrooms = []

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    actuasim = Actuasim()
    if not actuasim.load():
        msg = "Error loading {0}... Load a default rooms template".format(Actuasim.save_filename)
        print(msg)
        logging.error(msg)
        actuasim.load_room_template()
    actuasim.show()
    sys.exit(app.exec_())
