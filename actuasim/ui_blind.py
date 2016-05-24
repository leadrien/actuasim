# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_blind.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Blind(object):
    def setupUi(self, Blind):
        Blind.setObjectName("Blind")
        Blind.resize(275, 294)
        self.buttonDown = QtWidgets.QPushButton(Blind)
        self.buttonDown.setGeometry(QtCore.QRect(49, 248, 61, 22))
        self.buttonDown.setObjectName("buttonDown")
        self.progressBar = QtWidgets.QProgressBar(Blind)
        self.progressBar.setGeometry(QtCore.QRect(50, 50, 61, 161))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setObjectName("progressBar")
        self.labelPositionValue = QtWidgets.QLabel(Blind)
        self.labelPositionValue.setGeometry(QtCore.QRect(11, 25, 141, 17))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelPositionValue.setFont(font)
        self.labelPositionValue.setText("")
        self.labelPositionValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPositionValue.setObjectName("labelPositionValue")
        self.labelBlindAddress = QtWidgets.QLabel(Blind)
        self.labelBlindAddress.setGeometry(QtCore.QRect(30, 0, 141, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelBlindAddress.setFont(font)
        self.labelBlindAddress.setObjectName("labelBlindAddress")
        self.buttonUp = QtWidgets.QPushButton(Blind)
        self.buttonUp.setGeometry(QtCore.QRect(50, 220, 61, 22))
        self.buttonUp.setObjectName("buttonUp")

        self.retranslateUi(Blind)
        QtCore.QMetaObject.connectSlotsByName(Blind)

    def retranslateUi(self, Blind):
        _translate = QtCore.QCoreApplication.translate
        Blind.setWindowTitle(_translate("Blind", "Form"))
        self.buttonDown.setText(_translate("Blind", "v"))
        self.labelBlindAddress.setText(_translate("Blind", "5.11.5@1/5/26"))
        self.buttonUp.setText(_translate("Blind", "^"))

