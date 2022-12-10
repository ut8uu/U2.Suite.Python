# This file is part of the U2.Suite.Python distribution
# (https://github.com/ut8uu/U2.Suite.Python).
# 
# Copyright (c) 2022 Sergey Usmanov, UT8UU.
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import sys
from threading import Thread
import time

import helpers.KeyBinderKeys as kbk
from helpers.WinEventFilter import WinEventFilter
from logger.logger_constants import *
from logger.logger_main_window_keyboard import LoggerMainWindowKeyboard
from PyQt5.QtCore import QAbstractEventDispatcher, pyqtSlot, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget
from typing import List

class Logger_MainWindow(LoggerMainWindowKeyboard):
    _lastSelectedControl: QWidget
    _allControls : List[QWidget]
    _registered = False
    _win_event_filter : WinEventFilter
    _event_dispatcher : QAbstractEventDispatcher

    _running : bool

    _datetime_utc : bool
    _datetime_24h : bool
    _datetime_realtime : bool

    _realtime_thread : Thread
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self._running = True
        
        # datetime stuff
        self._datetime_utc = True
        self._datetime_24h = True
        self._datetime_realtime = True

        self.setupUi(self)
        self._allControls = [
            self.tbCallsign, self.tbRcv, self.tbSnt, self.tbName, self.tbComment,
            self.btnF1, self.btnF2, self.btnF3, self.btnF4, self.btnF5, self.btnF6,
            self.btnF7, self.btnF8, self.btnF9, self.btnF10, self.btnF11, self.btnF12,
            self.cbBand, self.cbMode, self.cbUtc, 
            #self.cbRealTime,
            self.tdDateTime,
            ]
        self.registerKeys()
        self.tbCallsign.setFocus()
        self.SetCurrentDateTime()

        #self._realtime_thread = Thread(target = self.realTimeThread)
        #self._realtime_thread.start()
    
    def __del__(self):
        '''A class' destructor'''
        self._running = False
        self.unregisterKeys()

    def destroy(self) -> None:
        self._running = False

    def realTimeThread(self) -> None:
        '''A code inside the realtime timer'''
        while self._running:
            try:
                if self._datetime_realtime:
                    focused_control = self.getSelectedControl()
                    if self._datetime_utc:
                        self.tdDateTime.setDateTime(QDateTime.currentDateTimeUtc())
                    else:
                        self.tdDateTime.setDateTime(QDateTime.currentDateTime())
                    focused_control.setFocus()
            except Exception as ex:
                print(ex.args[0])
            time.sleep(1)

    def getSelectedControl(self) -> QWidget:
        '''Locates and returns the control that is focused.'''
        for control in self._allControls:
            if control.hasFocus():
                return control

        # in case no control found, the Callsign is concidered focused
        self.tbCallsign.setFocus()
        return self.tbCallsign

    @pyqtSlot()
    def SetCurrentDateTime(self) -> None:
        '''Handles the clicking the Now button'''
        if self._datetime_utc:
            self.tdDateTime.setDateTime(QDateTime.currentDateTimeUtc())
        else:
            self.tdDateTime.setDateTime(QDateTime.currentDateTime())

    @pyqtSlot()
    def dateTimeCheckBoxChanged(self):
        '''Handles changing of the date and time related checkboxes'''
        '''
        if self.cb24hour.isChecked():
            self.tdDateTime.setDisplayFormat(DISPLAY_FORMAT_DDMMYY_HHMMSS)
        else:
            self.tdDateTime.setDisplayFormat(DISPLAY_FORMAT_MMDDYY_HHMMSS_AP)
        self._datetime_realtime = self.cbRealTime.isChecked()
        if self._datetime_realtime and self.tdDateTime.hasFocus():
            self.tbCallsign.setFocus()
        self.tdDateTime.setEnabled(not self._datetime_realtime)
        '''
        self._datetime_utc = self.cbUtc.isChecked()

    @pyqtSlot()
    def bandChanged(self):
        '''Handles changing of the band'''

    @pyqtSlot()
    def modeChanged(self):
        '''Handles changing of the mode'''
        current_text = self.cbMode.currentText()
        report = '599'
        if current_text == MODE_CW:
            report = '599'
        elif current_text == MODE_DIGITALVOICE:
            report = '59'
        elif current_text == MODE_SSB:
            report = '59'

        self.tbRcv.setText(report)
        self.tbSnt.setText(report)

if __name__ == '__main__':
    from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
    app = QApplication(sys.argv)
    window = Logger_MainWindow()

    window.show()

    app.exec()
    window.destroy()
    del window