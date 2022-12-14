# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Projects\Git\U2.Suite.Python\Sources\U2.Suite\ui\RigSelectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RigSelector(object):
    def setupUi(self, RigSelector):
        RigSelector.setObjectName("RigSelector")
        RigSelector.resize(650, 295)
        RigSelector.setSizeGripEnabled(True)
        RigSelector.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(RigSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(RigSelector)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnNew = QtWidgets.QPushButton(RigSelector)
        self.btnNew.setObjectName("btnNew")
        self.horizontalLayout.addWidget(self.btnNew)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnOk = QtWidgets.QPushButton(RigSelector)
        self.btnOk.setObjectName("btnOk")
        self.horizontalLayout.addWidget(self.btnOk)
        self.btnCancel = QtWidgets.QPushButton(RigSelector)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RigSelector)
        self.btnOk.pressed.connect(RigSelector.accept) # type: ignore
        self.btnCancel.pressed.connect(RigSelector.reject) # type: ignore
        self.tableWidget.cellPressed['int','int'].connect(RigSelector.selectRig) # type: ignore
        self.btnNew.pressed.connect(RigSelector.addNewRig) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RigSelector)

    def retranslateUi(self, RigSelector):
        _translate = QtCore.QCoreApplication.translate
        RigSelector.setWindowTitle(_translate("RigSelector", "Rig Selector"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("RigSelector", "Company"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("RigSelector", "Radio"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("RigSelector", "Port"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("RigSelector", "Speed"))
        self.btnNew.setText(_translate("RigSelector", "New..."))
        self.btnOk.setText(_translate("RigSelector", "OK"))
        self.btnCancel.setText(_translate("RigSelector", "Cancel"))
