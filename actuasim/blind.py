# -*- coding: utf-8 -*-

import logging

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import *

from actuasim.ui_blind import Ui_Blind


__author__ = "Adrien Lescourt"
__copyright__ = "HES-SO 2015, Project EMG4B"
__credits__ = ["Adrien Lescourt"]
__version__ = "1.0.2"
__email__ = "adrien.lescourt@gmail.com"
__status__ = "Prototype"


class BlindWidget(QWidget):

    MAX_PROGRESS_BAR = 255

    def __init__(self, individual_address, group_address, blind_position=0, animation_speed_ms=1500):
        super(BlindWidget, self).__init__()

        self.ui = Ui_Blind()
        self.ui.setupUi(self)

        self.logger = logging.getLogger()

        self.individual_address = individual_address
        self.group_address = group_address

        # Progressbar init
        self.is_moving = False
        self.animation_speed = animation_speed_ms
        self.animate_progress = QPropertyAnimation(self.ui.progressBar, QByteArray(bytes('value', 'utf-8')))
        self.ui.progressBar.setMaximum(BlindWidget.MAX_PROGRESS_BAR)
        self.ui.progressBar.setValue(0)
        self.position = blind_position
        self.setFixedWidth(220)
        self.update_position_value()
        self.ui.progressBar.valueChanged.connect(self.update_position_value)
        self.animate_progress.finished.connect(self.animation_finished)

        # Other stuff init
        self.ui.labelBlindAddress.setText(self.address_str)
        self.ui.buttonDown.clicked.connect(self.button_down_clicked)
        self.ui.buttonUp.clicked.connect(self.button_up_clicked)

    @property
    def address_str(self):
        return str(self.individual_address) + '@' + str(self.group_address)

    @property
    def position(self):
        return self.ui.progressBar.value()

    @position.setter
    def position(self, value):
        if value < 0:
            value = 0
        if value > BlindWidget.MAX_PROGRESS_BAR:
            value = BlindWidget.MAX_PROGRESS_BAR
        self.animate_progressbar(value)

    def update_position_value(self):
        self.ui.labelPositionValue.setText(str(self.ui.progressBar.value()))

    def button_down_clicked(self):
        if self.is_moving:
            self.animation_finished()
            return
        self.move_down()

    def button_up_clicked(self):
        if self.is_moving:
            self.animation_finished()
            return
        self.move_up()

    def move_down(self):
        self.logger.info('Blind ' + self.address_str + ' DOWN')
        self.animation_finished()
        self.animate_progressbar(0)

    def move_up(self):
        self.logger.info('Blind ' + self.address_str + ' UP')
        self.animation_finished()
        self.animate_progressbar(BlindWidget.MAX_PROGRESS_BAR)

    def move_to(self, value):
        self.logger.info('Blind ' + self.address_str + ' MOVE TO %s' % value)
        self.animation_finished()
        self.animate_progressbar(value)

    def animate_progressbar(self, end_value):
        if end_value == self.ui.progressBar.value():
            return
        blind_move_speed_ratio = abs(self.ui.progressBar.value()-end_value)/BlindWidget.MAX_PROGRESS_BAR
        self.animate_progress.setDuration(self.animation_speed*blind_move_speed_ratio)
        self.animate_progress.setStartValue(self.ui.progressBar.value())
        self.animate_progress.setEndValue(end_value)
        self.is_moving = True
        self.animate_progress.start()

    def animation_finished(self):
        self.animate_progress.stop()
        self.is_moving = False
