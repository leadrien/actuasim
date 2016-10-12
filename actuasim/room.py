# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from actuasim.blind import BlindWidget
from actuasim.valve import ValveWidget
from knxnet.utils import *

__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.2"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"


class Room(QWidget):
    def __init__(self, parent=None, title=None, blind_list=None, valve_list=None):
        super(Room, self).__init__(parent)
        self.blind_list = []
        self.valve_list = []
        main_layout = QVBoxLayout()
        self.blind_list = blind_list
        self.valve_list = valve_list
        # blinds
        blind_box = QGroupBox("Blinds")
        blind_box.setFixedWidth(1670)
        blind_box.setFixedHeight(380)
        blind_layout = QHBoxLayout()
        blind_box.setLayout(blind_layout)
        blind_scroll = QScrollArea(self)
        blind_scroll.setWidget(blind_box)
        for blind in blind_list:
            blind_layout.addWidget(blind)
        blind_layout.addStretch()
        blind_layout.setSpacing(0)
        # valves
        valve_box = QGroupBox("Valves")
        valve_box.setFixedWidth(1670)
        valve_box.setFixedHeight(380)
        valve_layout = QHBoxLayout()
        valve_box.setLayout(valve_layout)
        valve_scroll = QScrollArea(self)
        valve_scroll.setWidget(valve_box)
        for valve in valve_list:
            valve_layout.addWidget(valve)
        valve_layout.addStretch()
        valve_layout.setSpacing(0)
        # room
        main_layout.addWidget(blind_scroll)
        main_layout.addWidget(valve_scroll)
        self.setLayout(main_layout)
        self.setWindowTitle(title)
        self.title = title

    @classmethod
    def from_dict(cls, title='title', room_dict=None):
        blind_list = []
        valve_list = []
        if room_dict is not None:
            for blind in room_dict['blinds']:
                addr = blind['address'].split('@')
                value = blind['value']
                blind_list.append(BlindWidget(IndividualAddress.from_str(addr[0]),
                                              GroupAddress.from_str(addr[1]),
                                              value))
            for valve in room_dict['valves']:
                addr = valve['address'].split('@')
                value = valve['value']
                valve_list.append(ValveWidget(IndividualAddress.from_str(addr[0]),
                                              GroupAddress.from_str(addr[1]),
                                              value))
        return cls(None, title, blind_list, valve_list)

    def get_room_dict(self):
        blinds = [{'address': blind.address_str, 'value': blind.position} for blind in self.blind_list]
        valves = [{'address': valve.address_str, 'value': valve.position} for valve in self.valve_list]
        return {'blinds': blinds, 'valves': valves}


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    room = Room()
    room.show()
    sys.exit(app.exec_())