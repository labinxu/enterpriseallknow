# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'site_slect_dlg.ui'
#
# Created: Mon Sep 15 13:15:52 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(737, 361)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tw_sites = QtWidgets.QTableWidget(self.groupBox)
        self.tw_sites.setObjectName("tw_sites")
        self.tw_sites.setColumnCount(0)
        self.tw_sites.setRowCount(0)
        self.verticalLayout.addWidget(self.tw_sites)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        self.tw_sites.cellClicked['int','int'].connect(Dialog.onCellClicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "站点选择"))

