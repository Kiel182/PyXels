# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyXels.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PyXels(object):
    def setupUi(self, PyXels):
        PyXels.setObjectName("PyXels")
        PyXels.resize(921, 700)
        self.centralwidget = QtWidgets.QWidget(PyXels)
        self.centralwidget.setObjectName("centralwidget")
        self.GLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.GLWidget.setGeometry(QtCore.QRect(9, 9, 800, 637))
        self.GLWidget.setMinimumSize(QtCore.QSize(800, 600))
        self.GLWidget.setObjectName("GLWidget")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(860, 10, 46, 27))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(860, 90, 46, 27))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_3 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_3.setGeometry(QtCore.QRect(860, 50, 46, 27))
        self.spinBox_3.setObjectName("spinBox_3")
        PyXels.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PyXels)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 921, 23))
        self.menubar.setObjectName("menubar")
        PyXels.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PyXels)
        self.statusbar.setObjectName("statusbar")
        PyXels.setStatusBar(self.statusbar)

        self.retranslateUi(PyXels)
        QtCore.QMetaObject.connectSlotsByName(PyXels)

    def retranslateUi(self, PyXels):
        _translate = QtCore.QCoreApplication.translate
        PyXels.setWindowTitle(_translate("PyXels", "PyXels"))

