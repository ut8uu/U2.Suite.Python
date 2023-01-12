# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Projects\Git\_U2\U2.Suite.Python\Sources\U2.Suite\brandmeister\ui\BmMonitorMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BmMonitorMainWindow(object):
    def setupUi(self, BmMonitorMainWindow):
        BmMonitorMainWindow.setObjectName("BmMonitorMainWindow")
        BmMonitorMainWindow.resize(952, 600)
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        BmMonitorMainWindow.setFont(font)
        BmMonitorMainWindow.setStyleSheet("background-color: rgb(46, 52, 54); color: rgb(211, 215, 207);")
        self.centralwidget = QtWidgets.QWidget(BmMonitorMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cbTimestampFilter = QtWidgets.QComboBox(self.centralwidget)
        self.cbTimestampFilter.setGeometry(QtCore.QRect(450, 0, 151, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cbTimestampFilter.setFont(font)
        self.cbTimestampFilter.setObjectName("cbTimestampFilter")
        self.cbTimestampFilter.addItem("")
        self.cbTimestampFilter.addItem("")
        self.cbTimestampFilter.addItem("")
        self.cbTimestampFilter.addItem("")
        self.cbTimestampFilter.addItem("")
        self.cbTimestampFilter.addItem("")
        self.monitoringList = QtWidgets.QListView(self.centralwidget)
        self.monitoringList.setGeometry(QtCore.QRect(309, 50, 630, 480))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.monitoringList.setFont(font)
        self.monitoringList.setObjectName("monitoringList")
        self.lblDisplay = QtWidgets.QLabel(self.centralwidget)
        self.lblDisplay.setGeometry(QtCore.QRect(310, 10, 130, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblDisplay.setFont(font)
        self.lblDisplay.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblDisplay.setObjectName("lblDisplay")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 290, 520))
        self.scrollArea.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 288, 518))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblFilterByTG = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFilterByTG.sizePolicy().hasHeightForWidth())
        self.lblFilterByTG.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblFilterByTG.setFont(font)
        self.lblFilterByTG.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblFilterByTG.setObjectName("lblFilterByTG")
        self.verticalLayout.addWidget(self.lblFilterByTG)
        self.lvFilterByTG = QtWidgets.QListView(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lvFilterByTG.sizePolicy().hasHeightForWidth())
        self.lvFilterByTG.setSizePolicy(sizePolicy)
        self.lvFilterByTG.setObjectName("lvFilterByTG")
        self.verticalLayout.addWidget(self.lvFilterByTG)
        self.lblFilterByDxcc = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFilterByDxcc.sizePolicy().hasHeightForWidth())
        self.lblFilterByDxcc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblFilterByDxcc.setFont(font)
        self.lblFilterByDxcc.setObjectName("lblFilterByDxcc")
        self.verticalLayout.addWidget(self.lblFilterByDxcc)
        self.lvFilterByDxcc = QtWidgets.QListView(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lvFilterByDxcc.sizePolicy().hasHeightForWidth())
        self.lvFilterByDxcc.setSizePolicy(sizePolicy)
        self.lvFilterByDxcc.setObjectName("lvFilterByDxcc")
        self.verticalLayout.addWidget(self.lvFilterByDxcc)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        BmMonitorMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BmMonitorMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 952, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        BmMonitorMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BmMonitorMainWindow)
        self.statusbar.setObjectName("statusbar")
        BmMonitorMainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(BmMonitorMainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(BmMonitorMainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionStart = QtWidgets.QAction(BmMonitorMainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(BmMonitorMainWindow)
        self.actionStop.setEnabled(False)
        self.actionStop.setObjectName("actionStop")
        self.actionPreferences = QtWidgets.QAction(BmMonitorMainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuFile.addAction(self.actionStart)
        self.menuFile.addAction(self.actionStop)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPreferences)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(BmMonitorMainWindow)
        QtCore.QMetaObject.connectSlotsByName(BmMonitorMainWindow)

    def retranslateUi(self, BmMonitorMainWindow):
        _translate = QtCore.QCoreApplication.translate
        BmMonitorMainWindow.setWindowTitle(_translate("BmMonitorMainWindow", "Brandmeister Monitor by UT8UU"))
        self.cbTimestampFilter.setItemText(0, _translate("BmMonitorMainWindow", "Last hour"))
        self.cbTimestampFilter.setItemText(1, _translate("BmMonitorMainWindow", "Last 6 hours"))
        self.cbTimestampFilter.setItemText(2, _translate("BmMonitorMainWindow", "Last 12 hours"))
        self.cbTimestampFilter.setItemText(3, _translate("BmMonitorMainWindow", "Last 24 hours"))
        self.cbTimestampFilter.setItemText(4, _translate("BmMonitorMainWindow", "Last week"))
        self.cbTimestampFilter.setItemText(5, _translate("BmMonitorMainWindow", "All"))
        self.lblDisplay.setText(_translate("BmMonitorMainWindow", "Display period:"))
        self.lblFilterByTG.setText(_translate("BmMonitorMainWindow", "Filter by TG"))
        self.lblFilterByDxcc.setText(_translate("BmMonitorMainWindow", "Filter by DXCC"))
        self.menuFile.setTitle(_translate("BmMonitorMainWindow", "File"))
        self.menuHelp.setTitle(_translate("BmMonitorMainWindow", "Help"))
        self.actionExit.setText(_translate("BmMonitorMainWindow", "Exit"))
        self.actionAbout.setText(_translate("BmMonitorMainWindow", "About"))
        self.actionStart.setText(_translate("BmMonitorMainWindow", "Start"))
        self.actionStop.setText(_translate("BmMonitorMainWindow", "Stop"))
        self.actionPreferences.setText(_translate("BmMonitorMainWindow", "Preferences"))
