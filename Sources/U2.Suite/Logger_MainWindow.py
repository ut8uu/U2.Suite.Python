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
from pathlib import Path
import sys
from threading import Thread
import time
from helpers.FileSystemHelper import FileSystemHelper

import helpers.KeyBinderKeys as kbk
from helpers.WinEventFilter import WinEventFilter
from logger.log_database import LogDatabase
from logger.logger_constants import *
from logger.logger_main_window_keyboard import LoggerMainWindowKeyboard
from logger.logger_main_window_ui import LoggerMainWindowUiHelper
from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
from PyQt5.QtCore import QAbstractEventDispatcher, pyqtSlot, QDateTime, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, qApp
from pyqtkeybind import keybinder
from typing import List

class Logger_MainWindow(QMainWindow, Ui_LoggerMainWindow):
    _keyboard_handler : LoggerMainWindowKeyboard
    _lastSelectedControl: QWidget
    _allControls : List[QWidget]
    _registered = False
    _win_event_filter : WinEventFilter
    _event_dispatcher : QAbstractEventDispatcher
    _db : LogDatabase

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

        path = self.GetPathToDatabase()
        print(f'Path to db: {path}')
        self._db = LogDatabase(path, DATABASE_DEFAULT)

        self.setupUi(self)
        LoggerMainWindowUiHelper.update_ui(self)

        qApp.focusChanged.connect(self.on_focusChanged)
        
        self._allControls = [
            self.tbCallsign, self.tbRcv, self.tbSnt, self.tbName, self.tbComment,
            self.btnF1, self.btnF2, self.btnF3, self.btnF4, self.btnF5, self.btnF6,
            self.btnF7, self.btnF8, self.btnF9, self.btnF10, self.btnF11, self.btnF12,
            self.cbBand, self.cbMode, self.cbUtc, 
            #self.cbRealTime,
            self.tdDateTime,
            ]

        self._keyboard_handler = LoggerMainWindowKeyboard(self, self.winId())
        self._keyboard_handler.registerKeys()
        self._keyboard_handler.AddOnKeyPressHandler(self.on_keyPressed)
        self.tbCallsign.setFocus()
        self.SetCurrentDateTime()

        #self._realtime_thread = Thread(target = self.realTimeThread)
        #self._realtime_thread.start()

        self.DisplayLog()
    
    def __del__(self):
        '''A class' destructor'''
        self._running = False
        self._keyboard_handler.unregisterKeys()
        self._keyboard_handler.RemoveOnKeyPressHandler(self.on_keyPressed)

    def destroy(self) -> None:
        self._running = False

    def on_keyPressed(self, key: str) -> None:
        '''Handles the key_pressed event'''
        if key == kbk.KEY_RETURN:
            self.SaveQSO()
            self.DisplayLog()
        elif key == kbk.KEY_SPACE:
            self.MoveFocus()
        else:
            print(f"Key '{key}' not supported.")

    def DisplayLog(self):
        '''Displays the entire log.'''
        contacts = self._db.load_all_contacts(FIELD_TIMESTAMP)
        self.listLog.clear()

        fields = contacts[0]
        data = contacts[1]
        id_index = fields.index(FIELD_ID)
        callsign_index = fields.index(FIELD_CALLSIGN)
        timestamp_index = fields.index(FIELD_TIMESTAMP)
        mode_index = fields.index(FIELD_MODE)
        band_index = fields.index(FIELD_BAND)
        for qso in data:
            id = qso[id_index]
            timestamp = qso[timestamp_index].strftime('%Y-%m-%d %H:%M:%S')
            callsign = qso[callsign_index]
            band = qso[band_index]
            mode = qso[mode_index]

            logline = (
                f"{str(id).rjust(3,'0')}  "
                f"{callsign.ljust(10).upper()}  "
                f"{timestamp.ljust(16)}  "
                f"{band.rjust(5)}  "
                f"{mode} "
            )
            self.listLog.addItem(logline)

    def MoveFocus(self) -> None:
        '''
        Circularly moves focus among Callsign, Name, and Comment.
        Does nothing if none of the controls mentioned above is selected.
        '''
        try:
            # Callsign
            if self.tbCallsign.hasFocus():
                self.tbName.setFocus()
            # Name
            elif self.tbName.hasFocus():
                if len(self.tbName.text()) > 0:
                    self.tbName.setText(self.tbName.text() + ' ')
                else:
                    self.tbComment.setFocus()
            # Comment
            elif self.tbComment.hasFocus():
                if len(self.tbComment.text()) > 0:
                    self.tbComment.setText(self.tbComment.text() + ' ')
                else:
                    self.tbCallsign.setFocus()
            else:
                print(f'Focus remains on the "{self.getSelectedControl().objectName()}" control.')
        except Exception as ex:
            print(ex.args[0])

    def GetPathToDatabase(self) -> Path:
        '''Calculates the full path to the database'''
        return FileSystemHelper.get_appdata_path(Path('U2.Suite') / 'Logger' / 'Database', create_if_not_exists=True)

    def SaveQSO(self) -> None:
        '''Saves the current session'''
        callsign = self.tbCallsign.text().lstrip().rstrip()
        if len(callsign) == 0:
            return
        data = {FIELD_CALLSIGN:callsign, FIELD_OPNAME:self.tbName.text()}
        self._db.get_or_add_callsign(data)
        
        contact = {
            FIELD_CALLSIGN : self.tbCallsign.text().upper(),
            FIELD_OPNAME : self.tbName.text(),
            FIELD_BAND : self.cbBand.currentText(),
            FIELD_MODE : self.cbMode.currentText(),
            FIELD_TIMESTAMP : datetime.utcnow(),
            FIELD_RST_SENT : self.tbSnt.text().lstrip().rstrip(),
            FIELD_RST_RCVD : self.tbRcv.text().lstrip().rstrip()
        }
        self._db.log_contact(contact)

    @pyqtSlot("QWidget*", "QWidget*")
    def on_focusChanged(self, old, new) -> None:
        '''Handles obtaining the focus'''

        if new == None:
            try:
                self._keyboard_handler.unregisterKeys()
            except Exception as ex:
                print(ex)
        else:
            self._keyboard_handler.registerKeys()

    def focusOut(self) -> None:
        '''Handles losing the focus'''
        self._keyboard_handler.unregisterKeys()

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