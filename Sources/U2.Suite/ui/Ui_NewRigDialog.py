# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Projects\Git\U2.Suite.Python\Sources\U2.Suite\ui\NewRigDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewRigDialog(object):
    def setupUi(self, NewRigDialog):
        NewRigDialog.setObjectName("NewRigDialog")
        NewRigDialog.resize(305, 387)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewRigDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblRigType = QtWidgets.QLabel(NewRigDialog)
        self.lblRigType.setObjectName("lblRigType")
        self.gridLayout.addWidget(self.lblRigType, 0, 0, 1, 1)
        self.cbRigType = QtWidgets.QComboBox(NewRigDialog)
        self.cbRigType.setObjectName("cbRigType")
        self.gridLayout.addWidget(self.cbRigType, 0, 1, 1, 1)
        self.lblPort = QtWidgets.QLabel(NewRigDialog)
        self.lblPort.setObjectName("lblPort")
        self.gridLayout.addWidget(self.lblPort, 1, 0, 1, 1)
        self.cbPort = QtWidgets.QComboBox(NewRigDialog)
        self.cbPort.setObjectName("cbPort")
        self.gridLayout.addWidget(self.cbPort, 1, 1, 1, 1)
        self.lblBaudRate = QtWidgets.QLabel(NewRigDialog)
        self.lblBaudRate.setObjectName("lblBaudRate")
        self.gridLayout.addWidget(self.lblBaudRate, 2, 0, 1, 1)
        self.cbBaudRate = QtWidgets.QComboBox(NewRigDialog)
        self.cbBaudRate.setObjectName("cbBaudRate")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.gridLayout.addWidget(self.cbBaudRate, 2, 1, 1, 1)
        self.lblDataBits = QtWidgets.QLabel(NewRigDialog)
        self.lblDataBits.setObjectName("lblDataBits")
        self.gridLayout.addWidget(self.lblDataBits, 3, 0, 1, 1)
        self.cbDataBits = QtWidgets.QComboBox(NewRigDialog)
        self.cbDataBits.setObjectName("cbDataBits")
        self.cbDataBits.addItem("")
        self.cbDataBits.addItem("")
        self.cbDataBits.addItem("")
        self.cbDataBits.addItem("")
        self.gridLayout.addWidget(self.cbDataBits, 3, 1, 1, 1)
        self.lblParity = QtWidgets.QLabel(NewRigDialog)
        self.lblParity.setObjectName("lblParity")
        self.gridLayout.addWidget(self.lblParity, 4, 0, 1, 1)
        self.cbParity = QtWidgets.QComboBox(NewRigDialog)
        self.cbParity.setObjectName("cbParity")
        self.cbParity.addItem("")
        self.cbParity.addItem("")
        self.cbParity.addItem("")
        self.cbParity.addItem("")
        self.cbParity.addItem("")
        self.gridLayout.addWidget(self.cbParity, 4, 1, 1, 1)
        self.lblStopBits = QtWidgets.QLabel(NewRigDialog)
        self.lblStopBits.setObjectName("lblStopBits")
        self.gridLayout.addWidget(self.lblStopBits, 5, 0, 1, 1)
        self.cbStopBits = QtWidgets.QComboBox(NewRigDialog)
        self.cbStopBits.setObjectName("cbStopBits")
        self.cbStopBits.addItem("")
        self.cbStopBits.addItem("")
        self.cbStopBits.addItem("")
        self.gridLayout.addWidget(self.cbStopBits, 5, 1, 1, 1)
        self.lblRts = QtWidgets.QLabel(NewRigDialog)
        self.lblRts.setObjectName("lblRts")
        self.gridLayout.addWidget(self.lblRts, 6, 0, 1, 1)
        self.lblDtr = QtWidgets.QLabel(NewRigDialog)
        self.lblDtr.setObjectName("lblDtr")
        self.gridLayout.addWidget(self.lblDtr, 7, 0, 1, 1)
        self.lblDtr_2 = QtWidgets.QLabel(NewRigDialog)
        self.lblDtr_2.setObjectName("lblDtr_2")
        self.gridLayout.addWidget(self.lblDtr_2, 8, 0, 1, 1)
        self.udPollInterval = QtWidgets.QSpinBox(NewRigDialog)
        self.udPollInterval.setMinimum(100)
        self.udPollInterval.setMaximum(9999)
        self.udPollInterval.setProperty("value", 2000)
        self.udPollInterval.setObjectName("udPollInterval")
        self.gridLayout.addWidget(self.udPollInterval, 8, 1, 1, 1)
        self.lblDtr_3 = QtWidgets.QLabel(NewRigDialog)
        self.lblDtr_3.setObjectName("lblDtr_3")
        self.gridLayout.addWidget(self.lblDtr_3, 9, 0, 1, 1)
        self.udTimeout = QtWidgets.QSpinBox(NewRigDialog)
        self.udTimeout.setMinimum(100)
        self.udTimeout.setMaximum(9999)
        self.udTimeout.setProperty("value", 500)
        self.udTimeout.setObjectName("udTimeout")
        self.gridLayout.addWidget(self.udTimeout, 9, 1, 1, 1)
        self.cbRts = QtWidgets.QCheckBox(NewRigDialog)
        self.cbRts.setText("")
        self.cbRts.setObjectName("cbRts")
        self.gridLayout.addWidget(self.cbRts, 6, 1, 1, 1)
        self.cbDtr = QtWidgets.QCheckBox(NewRigDialog)
        self.cbDtr.setText("")
        self.cbDtr.setObjectName("cbDtr")
        self.gridLayout.addWidget(self.cbDtr, 7, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnTest = QtWidgets.QPushButton(NewRigDialog)
        self.btnTest.setObjectName("btnTest")
        self.horizontalLayout.addWidget(self.btnTest)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnOk = QtWidgets.QPushButton(NewRigDialog)
        self.btnOk.setObjectName("btnOk")
        self.horizontalLayout_2.addWidget(self.btnOk)
        self.btnCancel = QtWidgets.QPushButton(NewRigDialog)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(NewRigDialog)
        self.cbBaudRate.setCurrentIndex(11)
        self.cbDataBits.setCurrentIndex(3)
        self.btnOk.pressed.connect(NewRigDialog.accept) # type: ignore
        self.btnCancel.pressed.connect(NewRigDialog.reject) # type: ignore
        self.btnTest.pressed.connect(NewRigDialog.testRig) # type: ignore
        self.cbRigType.currentIndexChanged['QString'].connect(NewRigDialog.rigTypeChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(NewRigDialog)

    def retranslateUi(self, NewRigDialog):
        _translate = QtCore.QCoreApplication.translate
        NewRigDialog.setWindowTitle(_translate("NewRigDialog", "New Rig"))
        self.lblRigType.setText(_translate("NewRigDialog", "Rig Type"))
        self.lblPort.setText(_translate("NewRigDialog", "Port"))
        self.lblBaudRate.setText(_translate("NewRigDialog", "Baud Rate"))
        self.cbBaudRate.setItemText(0, _translate("NewRigDialog", "110"))
        self.cbBaudRate.setItemText(1, _translate("NewRigDialog", "300"))
        self.cbBaudRate.setItemText(2, _translate("NewRigDialog", "600"))
        self.cbBaudRate.setItemText(3, _translate("NewRigDialog", "1200"))
        self.cbBaudRate.setItemText(4, _translate("NewRigDialog", "2400"))
        self.cbBaudRate.setItemText(5, _translate("NewRigDialog", "4800"))
        self.cbBaudRate.setItemText(6, _translate("NewRigDialog", "9600"))
        self.cbBaudRate.setItemText(7, _translate("NewRigDialog", "14400"))
        self.cbBaudRate.setItemText(8, _translate("NewRigDialog", "19200"))
        self.cbBaudRate.setItemText(9, _translate("NewRigDialog", "38400"))
        self.cbBaudRate.setItemText(10, _translate("NewRigDialog", "56000"))
        self.cbBaudRate.setItemText(11, _translate("NewRigDialog", "57600"))
        self.cbBaudRate.setItemText(12, _translate("NewRigDialog", "115200"))
        self.cbBaudRate.setItemText(13, _translate("NewRigDialog", "128000"))
        self.cbBaudRate.setItemText(14, _translate("NewRigDialog", "256000"))
        self.lblDataBits.setText(_translate("NewRigDialog", "Data Bits"))
        self.cbDataBits.setItemText(0, _translate("NewRigDialog", "5"))
        self.cbDataBits.setItemText(1, _translate("NewRigDialog", "6"))
        self.cbDataBits.setItemText(2, _translate("NewRigDialog", "7"))
        self.cbDataBits.setItemText(3, _translate("NewRigDialog", "8"))
        self.lblParity.setText(_translate("NewRigDialog", "Parity"))
        self.cbParity.setItemText(0, _translate("NewRigDialog", "None"))
        self.cbParity.setItemText(1, _translate("NewRigDialog", "Odd"))
        self.cbParity.setItemText(2, _translate("NewRigDialog", "Even"))
        self.cbParity.setItemText(3, _translate("NewRigDialog", "Mark"))
        self.cbParity.setItemText(4, _translate("NewRigDialog", "Space"))
        self.lblStopBits.setText(_translate("NewRigDialog", "Stop Bits"))
        self.cbStopBits.setItemText(0, _translate("NewRigDialog", "1"))
        self.cbStopBits.setItemText(1, _translate("NewRigDialog", "1.5"))
        self.cbStopBits.setItemText(2, _translate("NewRigDialog", "2"))
        self.lblRts.setText(_translate("NewRigDialog", "RTS"))
        self.lblDtr.setText(_translate("NewRigDialog", "DTR"))
        self.lblDtr_2.setText(_translate("NewRigDialog", "Poll interval, ms."))
        self.lblDtr_3.setText(_translate("NewRigDialog", "Timeout, ms"))
        self.btnTest.setText(_translate("NewRigDialog", "Test"))
        self.btnOk.setText(_translate("NewRigDialog", "OK"))
        self.btnCancel.setText(_translate("NewRigDialog", "Cancel"))
