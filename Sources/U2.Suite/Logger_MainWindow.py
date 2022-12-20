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
import os
from pathlib import Path
import sys
import time
from Logger_QsoEditorDialog import Logger_QsoEditorDialog
from helpers.FileSystemHelper import FileSystemHelper

import helpers.KeyBinderKeys as kbk
from helpers.WinEventFilter import WinEventFilter
from logger.log_database import LogDatabase
from logger.logger_constants import *
from logger.logger_main_window_keyboard import LoggerMainWindowKeyboard
from logger.logger_main_window_ui import LoggerMainWindowUiHelper
from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
from PyQt5.QtCore import QAbstractEventDispatcher, pyqtSlot, QDateTime
from PyQt5.QtCore import QDir, QTimer
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, qApp
from pyqtkeybind import keybinder
from typing import List

def load_fonts_from_dir(directory: str) -> set:
    """
    Well it loads fonts from a directory...
    """
    font_families = set()
    for _fi in QDir(directory).entryInfoList(["*.ttf", "*.woff", "*.woff2"]):
        _id = QFontDatabase.addApplicationFont(_fi.absoluteFilePath())
        font_families |= set(QFontDatabase.applicationFontFamilies(_id))
    return font_families

class Logger_MainWindow(QMainWindow, Ui_LoggerMainWindow):
    _keyboard_handler : LoggerMainWindowKeyboard
    _lastSelectedControl: QWidget
    _allControls : List[QWidget]
    _registered = False
    _win_event_filter : WinEventFilter
    _event_dispatcher : QAbstractEventDispatcher
    _db : LogDatabase

    _running : bool

    _real_timer : QTimer

    def __init__(self, parent=None):
        super().__init__(parent)

        self._running = True
        
        path = self.GetPathToDatabase()
        print(f'Path to db: {path}')
        self._db = LogDatabase(path, DATABASE_DEFAULT)

        self.setupUi(self)
        LoggerMainWindowUiHelper.update_ui(self)

        qApp.focusChanged.connect(self.on_focusChanged)
        self.listLog.itemDoubleClicked.connect(self.qso_double_clicked)
        self.cbRealtime.stateChanged.connect(self.real_time_changed)
        self.btnNow.clicked.connect(self.set_current_date_time)

        self._allControls = [
            self.tbCallsign, self.tbRcv, self.tbSnt, self.tbName, self.tbComment,
            self.btnF1, self.btnF2, self.btnF3, self.btnF4, self.btnF5, self.btnF6,
            self.btnF7, self.btnF8, self.btnF9, self.btnF10, self.btnF11, self.btnF12,
            self.cbBand, self.cbMode, self.cbUtc, 
            self.cbRealtime,
            self.tdDateTime,
            ]

        self._keyboard_handler = LoggerMainWindowKeyboard(self, self.winId())
        self._keyboard_handler.registerKeys()
        self._keyboard_handler.AddOnKeyPressHandler(self.on_keyPressed)
        self.tbCallsign.setFocus()

        self.cbMode.clear()
        self.cbMode.addItems(ALL_MODES)

        self.cbBand.clear()
        self.cbBand.addItems(ALL_BANDS)

        self._real_timer = QTimer()
        self._real_timer.timeout.connect(self.update_time)
        self._real_timer.start(1000)


        self.display_log()
    
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
            self.save_qso()
            self.display_log()
        elif key == kbk.KEY_SPACE:
            self.MoveFocus()
        else:
            print(f"Key '{key}' not supported.")

    def display_log(self):
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
            callsign = qso[callsign_index].ljust(10).upper()
            l = len(callsign)
            band = qso[band_index]
            mode = qso[mode_index]

            logline = (
                f"{str(id).rjust(3,'0')}  "
                f"{callsign}  "
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

    def save_qso(self) -> None:
        '''Saves the current session'''
        callsign = self.tbCallsign.text().lstrip().rstrip()
        if len(callsign) == 0:
            return
        data = {FIELD_CALLSIGN:callsign, FIELD_OPNAME:self.tbName.text()}
        self._db.get_or_add_callsign(data)

        if self.cbRealtime.isChecked():
            if self.cbUtc.isChecked():
                timestamp = datetime.utcnow()
            else:
                timestamp = datetime.now()
        else:
            timestamp = self.tdDateTime.dateTime().toPyDateTime()

        contact = {
            FIELD_CALLSIGN : self.tbCallsign.text().upper(),
            FIELD_OPNAME : self.tbName.text(),
            FIELD_BAND : self.cbBand.currentText(),
            FIELD_MODE : self.cbMode.currentText(),
            FIELD_TIMESTAMP : timestamp,
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

    def getSelectedControl(self) -> QWidget:
        '''Locates and returns the control that is focused.'''
        for control in self._allControls:
            if control.hasFocus():
                return control

        # in case no control found, the Callsign is concidered focused
        self.tbCallsign.setFocus()
        return self.tbCallsign

    @pyqtSlot()
    def set_current_date_time(self) -> None:
        '''Handles the clicking the Now button'''
        if self.cbUtc.isChecked():
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

    def qso_double_clicked(self) -> None:
        """
        Gets the line of the log clicked on, and passes that line to the edit dialog.
        """
        item = self.listLog.currentItem()
        contactnumber = int(item.text().split()[0])
        result = self._db.get_contact_by_id(contactnumber)
        dialog = Logger_QsoEditorDialog(self)
        dialog.setup(result, self._db)
        dialog.change.lineChanged.connect(self.qso_edited)
        self._keyboard_handler.unregisterKeys()
        dialog.open()
        self._keyboard_handler.registerKeys()

    def qso_edited(self) -> None:
        '''Handles post edit or delete event.'''
        self.display_log()

    def update_time(self) -> None:
        if self.cbUtc.isChecked():
            timestamp = datetime.utcnow()
        else:
            timestamp = datetime.now()
        self.lblTimestamp.setText(timestamp.strftime('%d.%m.%Y %H:%M:%S'))

    def real_time_changed(self) -> None:
        '''Handles the switching between real-time and manual input modes.'''
        LoggerMainWindowUiHelper.update_timestamp_controls(self)

if __name__ == '__main__':
    from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font_dir = FileSystemHelper.relpath("font")
    families = load_fonts_from_dir(os.fspath(font_dir))

    window = Logger_MainWindow()

    window.show()

    app.exec()
    window.destroy()
    del window
