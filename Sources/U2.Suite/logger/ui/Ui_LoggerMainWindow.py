# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Projects\Git\U2.Suite.Python\U2.Suite.Python\Sources\U2.Suite\logger\ui\LoggerMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoggerMainWindow(object):
    def setupUi(self, LoggerMainWindow):
        LoggerMainWindow.setObjectName("LoggerMainWindow")
        LoggerMainWindow.resize(569, 552)
        LoggerMainWindow.setStyleSheet("background-color: rgb(46, 52, 54); color: rgb(211, 215, 207);")
        self.centralwidget = QtWidgets.QWidget(LoggerMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lblCallsign = QtWidgets.QLabel(self.centralwidget)
        self.lblCallsign.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.lblCallsign.setObjectName("lblCallsign")
        self.tbCallsign = QtWidgets.QLineEdit(self.centralwidget)
        self.tbCallsign.setGeometry(QtCore.QRect(10, 30, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tbCallsign.setFont(font)
        self.tbCallsign.setText("")
        self.tbCallsign.setObjectName("tbCallsign")
        self.lblSent = QtWidgets.QLabel(self.centralwidget)
        self.lblSent.setGeometry(QtCore.QRect(190, 10, 47, 13))
        self.lblSent.setObjectName("lblSent")
        self.tbSnt = QtWidgets.QLineEdit(self.centralwidget)
        self.tbSnt.setGeometry(QtCore.QRect(190, 30, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tbSnt.setFont(font)
        self.tbSnt.setObjectName("tbSnt")
        self.lblRcvd = QtWidgets.QLabel(self.centralwidget)
        self.lblRcvd.setGeometry(QtCore.QRect(250, 10, 47, 13))
        self.lblRcvd.setObjectName("lblRcvd")
        self.tbRcv = QtWidgets.QLineEdit(self.centralwidget)
        self.tbRcv.setGeometry(QtCore.QRect(250, 30, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tbRcv.setFont(font)
        self.tbRcv.setObjectName("tbRcv")
        self.lblName = QtWidgets.QLabel(self.centralwidget)
        self.lblName.setGeometry(QtCore.QRect(310, 10, 47, 13))
        self.lblName.setObjectName("lblName")
        self.tbName = QtWidgets.QLineEdit(self.centralwidget)
        self.tbName.setGeometry(QtCore.QRect(310, 30, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tbName.setFont(font)
        self.tbName.setText("")
        self.tbName.setObjectName("tbName")
        self.lblComment = QtWidgets.QLabel(self.centralwidget)
        self.lblComment.setGeometry(QtCore.QRect(420, 10, 47, 13))
        self.lblComment.setObjectName("lblComment")
        self.tbComment = QtWidgets.QLineEdit(self.centralwidget)
        self.tbComment.setGeometry(QtCore.QRect(420, 30, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tbComment.setFont(font)
        self.tbComment.setText("")
        self.tbComment.setObjectName("tbComment")
        self.lblBand = QtWidgets.QLabel(self.centralwidget)
        self.lblBand.setGeometry(QtCore.QRect(10, 130, 47, 13))
        self.lblBand.setObjectName("lblBand")
        self.lblMode = QtWidgets.QLabel(self.centralwidget)
        self.lblMode.setGeometry(QtCore.QRect(120, 130, 47, 13))
        self.lblMode.setObjectName("lblMode")
        self.cbBand = QtWidgets.QComboBox(self.centralwidget)
        self.cbBand.setGeometry(QtCore.QRect(10, 150, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cbBand.setFont(font)
        self.cbBand.setObjectName("cbBand")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbBand.addItem("")
        self.cbMode = QtWidgets.QComboBox(self.centralwidget)
        self.cbMode.setGeometry(QtCore.QRect(120, 150, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cbMode.setFont(font)
        self.cbMode.setObjectName("cbMode")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.cbMode.addItem("")
        self.lblDateTime = QtWidgets.QLabel(self.centralwidget)
        self.lblDateTime.setGeometry(QtCore.QRect(10, 70, 60, 13))
        self.lblDateTime.setObjectName("lblDateTime")
        self.cbUtc = QtWidgets.QCheckBox(self.centralwidget)
        self.cbUtc.setGeometry(QtCore.QRect(160, 70, 51, 17))
        self.cbUtc.setChecked(True)
        self.cbUtc.setObjectName("cbUtc")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 200, 551, 54))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btnF1 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF1.setObjectName("btnF1")
        self.gridLayout.addWidget(self.btnF1, 0, 0, 1, 1)
        self.btnF2 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF2.setObjectName("btnF2")
        self.gridLayout.addWidget(self.btnF2, 0, 1, 1, 1)
        self.btnF3 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF3.setObjectName("btnF3")
        self.gridLayout.addWidget(self.btnF3, 0, 2, 1, 1)
        self.btnF4 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF4.setObjectName("btnF4")
        self.gridLayout.addWidget(self.btnF4, 0, 3, 1, 1)
        self.btnF5 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF5.setObjectName("btnF5")
        self.gridLayout.addWidget(self.btnF5, 0, 4, 1, 1)
        self.btnF6 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF6.setObjectName("btnF6")
        self.gridLayout.addWidget(self.btnF6, 0, 5, 1, 1)
        self.btnF7 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF7.setObjectName("btnF7")
        self.gridLayout.addWidget(self.btnF7, 1, 0, 1, 1)
        self.btnF8 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF8.setObjectName("btnF8")
        self.gridLayout.addWidget(self.btnF8, 1, 1, 1, 1)
        self.btnF9 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF9.setObjectName("btnF9")
        self.gridLayout.addWidget(self.btnF9, 1, 2, 1, 1)
        self.btnF10 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF10.setObjectName("btnF10")
        self.gridLayout.addWidget(self.btnF10, 1, 3, 1, 1)
        self.btnF11 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF11.setObjectName("btnF11")
        self.gridLayout.addWidget(self.btnF11, 1, 4, 1, 1)
        self.btnF12 = QtWidgets.QPushButton(self.layoutWidget)
        self.btnF12.setObjectName("btnF12")
        self.gridLayout.addWidget(self.btnF12, 1, 5, 1, 1)
        self.cbPropagation = QtWidgets.QComboBox(self.centralwidget)
        self.cbPropagation.setGeometry(QtCore.QRect(270, 150, 230, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cbPropagation.setFont(font)
        self.cbPropagation.setObjectName("cbPropagation")
        self.cbPropagation.addItem("")
        self.cbPropagation.setItemText(0, "")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.cbPropagation.addItem("")
        self.lblPropagation = QtWidgets.QLabel(self.centralwidget)
        self.lblPropagation.setGeometry(QtCore.QRect(270, 130, 70, 13))
        self.lblPropagation.setObjectName("lblPropagation")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 260, 550, 240))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.listLog = QtWidgets.QListWidget(self.frame_2)
        self.listLog.setGeometry(QtCore.QRect(5, 11, 540, 220))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.listLog.setFont(font)
        self.listLog.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listLog.setStyleSheet("alternate-background-color: rgb(66, 66, 66);\n"
"")
        self.listLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listLog.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listLog.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.listLog.setProperty("showDropIndicator", False)
        self.listLog.setAlternatingRowColors(True)
        self.listLog.setObjectName("listLog")
        self.cbRealtime = QtWidgets.QCheckBox(self.centralwidget)
        self.cbRealtime.setGeometry(QtCore.QRect(80, 70, 71, 17))
        self.cbRealtime.setChecked(True)
        self.cbRealtime.setObjectName("cbRealtime")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 90, 496, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTimestamp = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lblTimestamp.setFont(font)
        self.lblTimestamp.setObjectName("lblTimestamp")
        self.horizontalLayout.addWidget(self.lblTimestamp)
        self.tdDateTime = QtWidgets.QDateTimeEdit(self.layoutWidget1)
        self.tdDateTime.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tdDateTime.setFont(font)
        self.tdDateTime.setWrapping(False)
        self.tdDateTime.setFrame(True)
        self.tdDateTime.setAccelerated(False)
        self.tdDateTime.setProperty("showGroupSeparator", False)
        self.tdDateTime.setCalendarPopup(True)
        self.tdDateTime.setCurrentSectionIndex(0)
        self.tdDateTime.setTimeSpec(QtCore.Qt.LocalTime)
        self.tdDateTime.setObjectName("tdDateTime")
        self.horizontalLayout.addWidget(self.tdDateTime)
        self.btnNow = QtWidgets.QPushButton(self.layoutWidget1)
        self.btnNow.setObjectName("btnNow")
        self.horizontalLayout.addWidget(self.btnNow)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        LoggerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LoggerMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 569, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuImport = QtWidgets.QMenu(self.menuFile)
        self.menuImport.setObjectName("menuImport")
        LoggerMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LoggerMainWindow)
        self.statusbar.setObjectName("statusbar")
        LoggerMainWindow.setStatusBar(self.statusbar)
        self.actionStation_info = QtWidgets.QAction(LoggerMainWindow)
        self.actionStation_info.setObjectName("actionStation_info")
        self.actionNewLog = QtWidgets.QAction(LoggerMainWindow)
        self.actionNewLog.setVisible(False)
        self.actionNewLog.setObjectName("actionNewLog")
        self.actionOpenLog = QtWidgets.QAction(LoggerMainWindow)
        self.actionOpenLog.setVisible(False)
        self.actionOpenLog.setObjectName("actionOpenLog")
        self.actionExit = QtWidgets.QAction(LoggerMainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionImportFrom_ADIF_file = QtWidgets.QAction(LoggerMainWindow)
        self.actionImportFrom_ADIF_file.setObjectName("actionImportFrom_ADIF_file")
        self.menuImport.addAction(self.actionImportFrom_ADIF_file)
        self.menuFile.addAction(self.actionStation_info)
        self.menuFile.addAction(self.actionNewLog)
        self.menuFile.addAction(self.actionOpenLog)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(LoggerMainWindow)
        self.cbMode.currentIndexChanged['QString'].connect(LoggerMainWindow.modeChanged) # type: ignore
        self.cbBand.currentIndexChanged['QString'].connect(LoggerMainWindow.bandChanged) # type: ignore
        self.cbUtc.stateChanged['int'].connect(LoggerMainWindow.dateTimeCheckBoxChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(LoggerMainWindow)
        LoggerMainWindow.setTabOrder(self.tbCallsign, self.tbSnt)
        LoggerMainWindow.setTabOrder(self.tbSnt, self.tbRcv)
        LoggerMainWindow.setTabOrder(self.tbRcv, self.tbName)
        LoggerMainWindow.setTabOrder(self.tbName, self.tbComment)
        LoggerMainWindow.setTabOrder(self.tbComment, self.tdDateTime)
        LoggerMainWindow.setTabOrder(self.tdDateTime, self.cbUtc)
        LoggerMainWindow.setTabOrder(self.cbUtc, self.cbBand)
        LoggerMainWindow.setTabOrder(self.cbBand, self.cbMode)
        LoggerMainWindow.setTabOrder(self.cbMode, self.btnF12)
        LoggerMainWindow.setTabOrder(self.btnF12, self.btnF1)
        LoggerMainWindow.setTabOrder(self.btnF1, self.btnF2)
        LoggerMainWindow.setTabOrder(self.btnF2, self.btnF3)
        LoggerMainWindow.setTabOrder(self.btnF3, self.btnF4)
        LoggerMainWindow.setTabOrder(self.btnF4, self.btnF5)
        LoggerMainWindow.setTabOrder(self.btnF5, self.btnF6)
        LoggerMainWindow.setTabOrder(self.btnF6, self.btnF11)
        LoggerMainWindow.setTabOrder(self.btnF11, self.btnF7)
        LoggerMainWindow.setTabOrder(self.btnF7, self.btnF8)
        LoggerMainWindow.setTabOrder(self.btnF8, self.btnF9)
        LoggerMainWindow.setTabOrder(self.btnF9, self.btnF10)

    def retranslateUi(self, LoggerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        LoggerMainWindow.setWindowTitle(_translate("LoggerMainWindow", "U2.Suite Logger by UT8UU"))
        self.lblCallsign.setText(_translate("LoggerMainWindow", "Callsign"))
        self.lblSent.setText(_translate("LoggerMainWindow", "Snt"))
        self.tbSnt.setText(_translate("LoggerMainWindow", "599"))
        self.lblRcvd.setText(_translate("LoggerMainWindow", "Rcvd"))
        self.tbRcv.setText(_translate("LoggerMainWindow", "599"))
        self.lblName.setText(_translate("LoggerMainWindow", "Name"))
        self.lblComment.setText(_translate("LoggerMainWindow", "Comment"))
        self.lblBand.setText(_translate("LoggerMainWindow", "Band"))
        self.lblMode.setText(_translate("LoggerMainWindow", "Mode"))
        self.cbBand.setItemText(0, _translate("LoggerMainWindow", "160m"))
        self.cbBand.setItemText(1, _translate("LoggerMainWindow", "80m"))
        self.cbBand.setItemText(2, _translate("LoggerMainWindow", "60m"))
        self.cbBand.setItemText(3, _translate("LoggerMainWindow", "40m"))
        self.cbBand.setItemText(4, _translate("LoggerMainWindow", "30m"))
        self.cbBand.setItemText(5, _translate("LoggerMainWindow", "20m"))
        self.cbBand.setItemText(6, _translate("LoggerMainWindow", "17m"))
        self.cbBand.setItemText(7, _translate("LoggerMainWindow", "15m"))
        self.cbBand.setItemText(8, _translate("LoggerMainWindow", "12m"))
        self.cbBand.setItemText(9, _translate("LoggerMainWindow", "10m"))
        self.cbBand.setItemText(10, _translate("LoggerMainWindow", "6m"))
        self.cbBand.setItemText(11, _translate("LoggerMainWindow", "4m"))
        self.cbBand.setItemText(12, _translate("LoggerMainWindow", "2m"))
        self.cbBand.setItemText(13, _translate("LoggerMainWindow", "70cm"))
        self.cbMode.setItemText(0, _translate("LoggerMainWindow", "AM"))
        self.cbMode.setItemText(1, _translate("LoggerMainWindow", "CW"))
        self.cbMode.setItemText(2, _translate("LoggerMainWindow", "DIGITALVOICE"))
        self.cbMode.setItemText(3, _translate("LoggerMainWindow", "FM"))
        self.cbMode.setItemText(4, _translate("LoggerMainWindow", "RTTY"))
        self.cbMode.setItemText(5, _translate("LoggerMainWindow", "SSB"))
        self.cbMode.setItemText(6, _translate("LoggerMainWindow", "THOR"))
        self.lblDateTime.setText(_translate("LoggerMainWindow", "Date/Time"))
        self.cbUtc.setText(_translate("LoggerMainWindow", "UTC"))
        self.btnF1.setText(_translate("LoggerMainWindow", "F1 Spare"))
        self.btnF2.setText(_translate("LoggerMainWindow", "F2 Spare"))
        self.btnF3.setText(_translate("LoggerMainWindow", "F3 Spare"))
        self.btnF4.setText(_translate("LoggerMainWindow", "F4 Spare"))
        self.btnF5.setText(_translate("LoggerMainWindow", "F5 Spare"))
        self.btnF6.setText(_translate("LoggerMainWindow", "F6 Spare"))
        self.btnF7.setText(_translate("LoggerMainWindow", "F7 Spare"))
        self.btnF8.setText(_translate("LoggerMainWindow", "F8 Spare"))
        self.btnF9.setText(_translate("LoggerMainWindow", "F9 Spare"))
        self.btnF10.setText(_translate("LoggerMainWindow", "F10 Spare"))
        self.btnF11.setText(_translate("LoggerMainWindow", "F11 Spare"))
        self.btnF12.setText(_translate("LoggerMainWindow", "F12 Wipe"))
        self.cbPropagation.setItemText(1, _translate("LoggerMainWindow", "Aurora"))
        self.cbPropagation.setItemText(2, _translate("LoggerMainWindow", "Aurora E"))
        self.cbPropagation.setItemText(3, _translate("LoggerMainWindow", "Back scatter"))
        self.cbPropagation.setItemText(4, _translate("LoggerMainWindow", "EchoLink"))
        self.cbPropagation.setItemText(5, _translate("LoggerMainWindow", "EME"))
        self.cbPropagation.setItemText(6, _translate("LoggerMainWindow", "F2"))
        self.cbPropagation.setItemText(7, _translate("LoggerMainWindow", "Ionoscatter"))
        self.cbPropagation.setItemText(8, _translate("LoggerMainWindow", "Meteor scatter"))
        self.cbPropagation.setItemText(9, _translate("LoggerMainWindow", "Rain scatter"))
        self.cbPropagation.setItemText(10, _translate("LoggerMainWindow", "Satellite"))
        self.cbPropagation.setItemText(11, _translate("LoggerMainWindow", "Sporadic E"))
        self.cbPropagation.setItemText(12, _translate("LoggerMainWindow", "Terrestrial repeater"))
        self.cbPropagation.setItemText(13, _translate("LoggerMainWindow", "Tropospheric ducting"))
        self.cbPropagation.setItemText(14, _translate("LoggerMainWindow", "Trans-equatorial"))
        self.lblPropagation.setText(_translate("LoggerMainWindow", "Propagation"))
        self.cbRealtime.setText(_translate("LoggerMainWindow", "Real-time"))
        self.lblTimestamp.setText(_translate("LoggerMainWindow", "01.01.2022 11:22:33"))
        self.tdDateTime.setDisplayFormat(_translate("LoggerMainWindow", "dd.MM.yyyy hh:mm:ss"))
        self.btnNow.setText(_translate("LoggerMainWindow", "< now"))
        self.menuFile.setTitle(_translate("LoggerMainWindow", "File"))
        self.menuImport.setTitle(_translate("LoggerMainWindow", "Import"))
        self.actionStation_info.setText(_translate("LoggerMainWindow", "Station info"))
        self.actionNewLog.setText(_translate("LoggerMainWindow", "New log"))
        self.actionOpenLog.setText(_translate("LoggerMainWindow", "Open log"))
        self.actionExit.setText(_translate("LoggerMainWindow", "Exit"))
        self.actionImportFrom_ADIF_file.setText(_translate("LoggerMainWindow", "From ADIF file"))
