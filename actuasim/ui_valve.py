# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_valve.ui'
#
# Created: Mon Mar  9 11:48:33 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Valve(object):
    def setupUi(self, Valve):
        Valve.setObjectName("Valve")
        Valve.resize(274, 233)
        self.labelValveAddress = QtWidgets.QLabel(Valve)
        self.labelValveAddress.setGeometry(QtCore.QRect(71, 10, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelValveAddress.setFont(font)
        self.labelValveAddress.setObjectName("labelValveAddress")
        self.buttonUp = QtWidgets.QPushButton(Valve)
        self.buttonUp.setGeometry(QtCore.QRect(130, 180, 61, 23))
        self.buttonUp.setObjectName("buttonUp")
        self.buttonDown = QtWidgets.QPushButton(Valve)
        self.buttonDown.setGeometry(QtCore.QRect(70, 180, 61, 23))
        self.buttonDown.setObjectName("buttonDown")
        self.labelPositionValue = QtWidgets.QLabel(Valve)
        self.labelPositionValue.setGeometry(QtCore.QRect(90, 40, 75, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelPositionValue.setFont(font)
        self.labelPositionValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPositionValue.setObjectName("labelPositionValue")
        self.imageOrigin = QtWidgets.QLabel(Valve)
        self.imageOrigin.setGeometry(QtCore.QRect(50, 70, 16, 16))
        self.imageOrigin.setText("")
        self.imageOrigin.setObjectName("imageOrigin")

        self.retranslateUi(Valve)
        QtCore.QMetaObject.connectSlotsByName(Valve)

    def retranslateUi(self, Valve):
        _translate = QtCore.QCoreApplication.translate
        Valve.setWindowTitle(_translate("Valve", "Form"))
        self.labelValveAddress.setText(_translate("Valve", "5.0.5@0/5/26"))
        self.buttonUp.setText(_translate("Valve", "+"))
        self.buttonDown.setText(_translate("Valve", "-"))
        self.labelPositionValue.setText(_translate("Valve", "1"))

