# -*- coding: utf-8 -*-

from math import cos, sin, radians
import os
import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from actuasim.ui_valve import Ui_Valve


__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.2"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"


class ValveWidget(QWidget):

    MAX_PROGRESS_BAR = 255

    def __init__(self, individual_address, group_address, valve_position=45, animation_speed_ms=1500):
        super(ValveWidget, self).__init__()
        self.ui = Ui_Valve()
        self.ui.setupUi(self)

        self.logger = logging.getLogger()

        self.individual_address = individual_address
        self.group_address = group_address
        self._position = 0
        self.position = valve_position
        self.setFixedWidth(220)

        self.temperature_bar_image = QImage(os.getcwd() + '/res/temperature_bar.png')
        self.temperature_bar_rect = QRect(self.ui.imageOrigin.x(),
                                          self.ui.imageOrigin.y(),
                                          150, 85)
        self.line_origin = QPoint(self.ui.imageOrigin.x()+75, 135)
        self.line_length = 60

        self.ui.labelValveAddress.setText(self.address_str)
        self.ui.labelPositionValue.setText(str(self._position))
        self.ui.buttonDown.clicked.connect(self.button_down_pressed)
        self.ui.buttonUp.clicked.connect(self.button_up_pressed)

    @property
    def address_str(self):
        return str(self.individual_address) + '@' + str(self.group_address)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        if self._position < 0:
            self._position = 0
        if self._position > ValveWidget.MAX_PROGRESS_BAR:
            self._position = ValveWidget.MAX_PROGRESS_BAR
        self.logger.info('Valve ' + self.address_str + ' = ' + str(self._position))
        self.ui.labelPositionValue.setText(str(self._position))
        self.repaint()

    def button_down_pressed(self):
        self.position -= 1

    def button_up_pressed(self):
        self.position += 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(int(QPainter.SmoothPixmapTransform) | int(QPainter.Antialiasing))
        painter.drawImage(self.temperature_bar_rect, self.temperature_bar_image)
        to_180_degree = 180 / ValveWidget.MAX_PROGRESS_BAR
        angle = (ValveWidget.MAX_PROGRESS_BAR - self.position) * to_180_degree + 90
        x = self.line_origin.x() + self.line_length * sin(radians(angle))
        y = self.line_origin.y() + self.line_length * cos(radians(angle))
        painter.drawLine(self.line_origin, QPoint(x, y))
