# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Sat Aug 23 19:56:03 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.WindowModal)
        Form.resize(840, 652)
        Form.setMinimumSize(QtCore.QSize(1, 1))
        Form.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 10, 821, 541))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.gdlyMain = QtWidgets.QGridLayout(self.horizontalLayoutWidget_4)
        self.gdlyMain.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gdlyMain.setContentsMargins(5, 5, 5, 5)
        self.gdlyMain.setObjectName("gdlyMain")
        self.groupBox = QtWidgets.QGroupBox(self.horizontalLayoutWidget_4)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(240, 10, 551, 501))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.hzlyTbwResult = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.hzlyTbwResult.setContentsMargins(5, 5, 5, 5)
        self.hzlyTbwResult.setObjectName("hzlyTbwResult")
        self.tbwResult = QtWidgets.QTableWidget(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbwResult.sizePolicy().hasHeightForWidth())
        self.tbwResult.setSizePolicy(sizePolicy)
        self.tbwResult.setAutoFillBackground(True)
        self.tbwResult.setLineWidth(2)
        self.tbwResult.setMidLineWidth(1)
        self.tbwResult.setWordWrap(False)
        self.tbwResult.setRowCount(0)
        self.tbwResult.setColumnCount(10)
        self.tbwResult.setObjectName("tbwResult")
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbwResult.setHorizontalHeaderItem(8, item)
        self.hzlyTbwResult.addWidget(self.tbwResult)
        self.hzlyTbwResult.setStretch(0, 1)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 221, 501))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabTasks = QtWidgets.QTabWidget(self.horizontalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabTasks.sizePolicy().hasHeightForWidth())
        self.tabTasks.setSizePolicy(sizePolicy)
        self.tabTasks.setObjectName("tabTasks")
        self.tabTaskRuning = QtWidgets.QWidget()
        self.tabTaskRuning.setAutoFillBackground(False)
        self.tabTaskRuning.setObjectName("tabTaskRuning")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tabTaskRuning)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 201, 461))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.hzlyRunningTask = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.hzlyRunningTask.setContentsMargins(5, 5, 5, 5)
        self.hzlyRunningTask.setObjectName("hzlyRunningTask")
        self.listRunningTasks = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.listRunningTasks.setObjectName("listRunningTasks")
        self.hzlyRunningTask.addWidget(self.listRunningTasks)
        self.tabTasks.addTab(self.tabTaskRuning, "")
        self.tabTaskCompleted = QtWidgets.QWidget()
        self.tabTaskCompleted.setObjectName("tabTaskCompleted")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tabTaskCompleted)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 201, 461))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.hzlyCompletedTask = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.hzlyCompletedTask.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.hzlyCompletedTask.setContentsMargins(5, 5, 5, 5)
        self.hzlyCompletedTask.setObjectName("hzlyCompletedTask")
        self.listCompletedTasks = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.listCompletedTasks.setObjectName("listCompletedTasks")
        self.hzlyCompletedTask.addWidget(self.listCompletedTasks)
        self.tabTasks.addTab(self.tabTaskCompleted, "")
        self.horizontalLayout.addWidget(self.tabTasks)
        self.gdlyMain.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gdlyMain.setRowStretch(0, 1)
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(10, 560, 821, 75))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ltOutput = QtWidgets.QListWidget(self.horizontalLayoutWidget_6)
        self.ltOutput.setObjectName("ltOutput")
        self.horizontalLayout_2.addWidget(self.ltOutput)

        self.retranslateUi(Form)
        self.tabTasks.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.tbwResult.horizontalHeaderItem(0)
        item.setText(_translate("Form", "公司"))
        item = self.tbwResult.horizontalHeaderItem(1)
        item.setText(_translate("Form", "联系人"))
        item = self.tbwResult.horizontalHeaderItem(2)
        item.setText(_translate("Form", "联系电话"))
        item = self.tbwResult.horizontalHeaderItem(3)
        item.setText(_translate("Form", "手机"))
        item = self.tbwResult.horizontalHeaderItem(4)
        item.setText(_translate("Form", "传真"))
        item = self.tbwResult.horizontalHeaderItem(5)
        item.setText(_translate("Form", "邮编"))
        item = self.tbwResult.horizontalHeaderItem(6)
        item.setText(_translate("Form", "公司主页"))
        item = self.tbwResult.horizontalHeaderItem(7)
        item.setText(_translate("Form", "公司地址"))
        item = self.tbwResult.horizontalHeaderItem(8)
        item.setText(_translate("Form", "备注"))
        self.tabTaskRuning.setStatusTip(_translate("Form", "Task is running"))
        self.tabTasks.setTabText(self.tabTasks.indexOf(self.tabTaskRuning), _translate("Form", "未完成"))
        self.tabTasks.setTabText(self.tabTasks.indexOf(self.tabTaskCompleted), _translate("Form", "已完成"))

