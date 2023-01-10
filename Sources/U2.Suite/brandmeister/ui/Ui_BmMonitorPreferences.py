# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Projects\Git\_U2\U2.Suite.Python\Sources\U2.Suite\brandmeister\ui\BmMonitorPreferences.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BmPreferencesDialog(object):
    def setupUi(self, BmPreferencesDialog):
        BmPreferencesDialog.setObjectName("BmPreferencesDialog")
        BmPreferencesDialog.resize(525, 392)
        BmPreferencesDialog.setStyleSheet("background-color: rgb(46, 52, 54); color: rgb(211, 215, 207);")
        self.buttonBox = QtWidgets.QDialogButtonBox(BmPreferencesDialog)
        self.buttonBox.setGeometry(QtCore.QRect(430, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(BmPreferencesDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 411, 371))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tabFilter = QtWidgets.QWidget()
        self.tabFilter.setObjectName("tabFilter")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tabFilter)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 10, 381, 331))
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabOptions = QtWidgets.QWidget()
        self.tabOptions.setObjectName("tabOptions")
        self.label = QtWidgets.QLabel(self.tabOptions)
        self.label.setGeometry(QtCore.QRect(30, 30, 210, 16))
        self.label.setObjectName("label")
        self.udTransmissionDuration = QtWidgets.QSpinBox(self.tabOptions)
        self.udTransmissionDuration.setGeometry(QtCore.QRect(240, 30, 91, 22))
        self.udTransmissionDuration.setMaximum(100)
        self.udTransmissionDuration.setProperty("value", 0)
        self.udTransmissionDuration.setObjectName("udTransmissionDuration")
        self.udSilenceDuration = QtWidgets.QSpinBox(self.tabOptions)
        self.udSilenceDuration.setGeometry(QtCore.QRect(240, 60, 91, 22))
        self.udSilenceDuration.setMaximum(999)
        self.udSilenceDuration.setProperty("value", 0)
        self.udSilenceDuration.setObjectName("udSilenceDuration")
        self.label_2 = QtWidgets.QLabel(self.tabOptions)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 200, 16))
        self.label_2.setObjectName("label_2")
        self.tabWidget_2.addTab(self.tabOptions, "")
        self.tabTG = QtWidgets.QWidget()
        self.tabTG.setObjectName("tabTG")
        self.lbGroups = QtWidgets.QListView(self.tabTG)
        self.lbGroups.setGeometry(QtCore.QRect(10, 40, 350, 260))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.lbGroups.setFont(font)
        self.lbGroups.setObjectName("lbGroups")
        self.cbFilterByTG = QtWidgets.QCheckBox(self.tabTG)
        self.cbFilterByTG.setGeometry(QtCore.QRect(10, 10, 190, 20))
        self.cbFilterByTG.setObjectName("cbFilterByTG")
        self.tabWidget_2.addTab(self.tabTG, "")
        self.tabDxcc = QtWidgets.QWidget()
        self.tabDxcc.setObjectName("tabDxcc")
        self.cbFilterByDxcc = QtWidgets.QCheckBox(self.tabDxcc)
        self.cbFilterByDxcc.setGeometry(QtCore.QRect(10, 10, 190, 20))
        self.cbFilterByDxcc.setObjectName("cbFilterByDxcc")
        self.lbCountries = QtWidgets.QListView(self.tabDxcc)
        self.lbCountries.setGeometry(QtCore.QRect(10, 40, 350, 260))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.lbCountries.setFont(font)
        self.lbCountries.setObjectName("lbCountries")
        self.tabWidget_2.addTab(self.tabDxcc, "")
        self.tabCalls = QtWidgets.QWidget()
        self.tabCalls.setObjectName("tabCalls")
        self.cbFilterByCallsigns = QtWidgets.QCheckBox(self.tabCalls)
        self.cbFilterByCallsigns.setGeometry(QtCore.QRect(10, 10, 250, 20))
        self.cbFilterByCallsigns.setObjectName("cbFilterByCallsigns")
        self.tbCallsigns = QtWidgets.QPlainTextEdit(self.tabCalls)
        self.tbCallsigns.setEnabled(False)
        self.tbCallsigns.setGeometry(QtCore.QRect(10, 40, 350, 260))
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.tbCallsigns.setFont(font)
        self.tbCallsigns.setObjectName("tbCallsigns")
        self.tabWidget_2.addTab(self.tabCalls, "")
        self.tabWidget.addTab(self.tabFilter, "")
        self.tabStorage = QtWidgets.QWidget()
        self.tabStorage.setObjectName("tabStorage")
        self.cbSaveToDb = QtWidgets.QCheckBox(self.tabStorage)
        self.cbSaveToDb.setGeometry(QtCore.QRect(20, 20, 351, 20))
        self.cbSaveToDb.setChecked(True)
        self.cbSaveToDb.setObjectName("cbSaveToDb")
        self.lblPathToDb = QtWidgets.QLabel(self.tabStorage)
        self.lblPathToDb.setGeometry(QtCore.QRect(20, 50, 331, 16))
        self.lblPathToDb.setObjectName("lblPathToDb")
        self.tbPathToDb = QtWidgets.QLineEdit(self.tabStorage)
        self.tbPathToDb.setGeometry(QtCore.QRect(20, 70, 321, 30))
        self.tbPathToDb.setObjectName("tbPathToDb")
        self.btnSelectPathToDb = QtWidgets.QPushButton(self.tabStorage)
        self.btnSelectPathToDb.setGeometry(QtCore.QRect(350, 70, 41, 28))
        self.btnSelectPathToDb.setObjectName("btnSelectPathToDb")
        self.cbDbStorageLimit = QtWidgets.QComboBox(self.tabStorage)
        self.cbDbStorageLimit.setGeometry(QtCore.QRect(20, 140, 181, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cbDbStorageLimit.setFont(font)
        self.cbDbStorageLimit.setObjectName("cbDbStorageLimit")
        self.lblDatabaseStorageLimit = QtWidgets.QLabel(self.tabStorage)
        self.lblDatabaseStorageLimit.setGeometry(QtCore.QRect(20, 120, 271, 16))
        self.lblDatabaseStorageLimit.setObjectName("lblDatabaseStorageLimit")
        self.tabWidget.addTab(self.tabStorage, "")
        self.tabReporting = QtWidgets.QWidget()
        self.tabReporting.setObjectName("tabReporting")
        self.tabWidget.addTab(self.tabReporting, "")

        self.retranslateUi(BmPreferencesDialog)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.buttonBox.accepted.connect(BmPreferencesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(BmPreferencesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(BmPreferencesDialog)

    def retranslateUi(self, BmPreferencesDialog):
        _translate = QtCore.QCoreApplication.translate
        BmPreferencesDialog.setWindowTitle(_translate("BmPreferencesDialog", "Brandmeister Preferences"))
        self.label.setText(_translate("BmPreferencesDialog", "Min. duration of transmission (sec)"))
        self.label_2.setText(_translate("BmPreferencesDialog", "Min. duration of silence (sec)"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabOptions), _translate("BmPreferencesDialog", "Options"))
        self.cbFilterByTG.setText(_translate("BmPreferencesDialog", "Filter by groups"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabTG), _translate("BmPreferencesDialog", "TG"))
        self.cbFilterByDxcc.setText(_translate("BmPreferencesDialog", "Filter by DXCC"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabDxcc), _translate("BmPreferencesDialog", "DXCC"))
        self.cbFilterByCallsigns.setText(_translate("BmPreferencesDialog", "Filter by callsigns"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabCalls), _translate("BmPreferencesDialog", "Calls"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFilter), _translate("BmPreferencesDialog", "Filter"))
        self.cbSaveToDb.setText(_translate("BmPreferencesDialog", "Save to database"))
        self.lblPathToDb.setText(_translate("BmPreferencesDialog", "Path to database"))
        self.btnSelectPathToDb.setText(_translate("BmPreferencesDialog", "..."))
        self.lblDatabaseStorageLimit.setText(_translate("BmPreferencesDialog", "Database storage limit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStorage), _translate("BmPreferencesDialog", "Storage"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabReporting), _translate("BmPreferencesDialog", "Reporting"))
