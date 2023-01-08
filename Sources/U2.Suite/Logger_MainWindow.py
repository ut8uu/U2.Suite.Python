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

from common.ui.DialogAbout import DialogAbout

from logger.Logger_QsoEditorDialog import Logger_QsoEditorDialog
from logger.Logger_StationInfoDialog import Logger_StationInfoDialog
from helpers.AdifHelper import ADIF_BAND, ADIF_CALL, ADIF_MODE, ADIF_OPERATOR, ADIF_QSO_DATE, ADIF_TIME_OFF, ADIF_TIME_ON, ADIF_log, AdifHelper
from helpers.FileSystemHelper import FileSystemHelper
from logger.Logger_PreferencesDialog import Logger_PreferencesDialog
from logger.listeners.wsjt_listener import WsjtListener

from logger.log_database import LogDatabase
from logger.logger_constants import *
from logger.logger_main_window_ui import LoggerMainWindowUiHelper
from logger.logger_preferences import LoggerApplicationPreferences
from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
from PyQt5.QtCore import QAbstractEventDispatcher, pyqtSlot, QDateTime
from PyQt5.QtCore import QDir, QTimer, Qt, QEvent
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, qApp, QFileDialog
from typing import List

class Logger_MainWindow(QMainWindow, Ui_LoggerMainWindow):
    DESCRIPTION = 'A small logging application.'
    VERSION = '1.0.0'
    
    _lastSelectedControl: QWidget
    _allControls : List[QWidget]
    _registered = False
    _event_dispatcher : QAbstractEventDispatcher
    _db : LogDatabase
    _preferences : LoggerApplicationPreferences
    
    _wsjt_listener : WsjtListener

    _running : bool

    _real_timer : QTimer

    def __init__(self, parent=None):
        super().__init__(parent)

        self._running = True

        self._preferences = LoggerApplicationPreferences()

        path = self.GetPathToDatabase()
        print(f'Path to db: {path}')
        self._db = LogDatabase(path, DATABASE_DEFAULT)

        self.setupUi(self)
        LoggerMainWindowUiHelper.update_ui(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(FileSystemHelper.relpath('icon/edit_file-32.png')))

        self.listLog.itemDoubleClicked.connect(self.qso_double_clicked)
        self.cbRealtime.stateChanged.connect(self.real_time_changed)
        self.btnNow.clicked.connect(self.set_current_date_time)

        self.actionImportFrom_ADIF_file.triggered.connect(self.import_from_file)
        self.actionExportToADIFfile.triggered.connect(self.export_to_adif)
        self.actionExportToADXfile.triggered.connect(self.export_to_adx)
        self.actionPreferences.triggered.connect(self.display_preferences_dialog)
        self.actionExit.triggered.connect(self.close_window)
        self.actionAbout.triggered.connect(self.display_about_dialog)

        # install event handler for main input controls
        self.tbCallsign.installEventFilter(self)
        self.tbName.installEventFilter(self)
        self.tbComment.installEventFilter(self)

        self.actionStation_info.triggered.connect(self.display_station_info_dialog)

        self._allControls = [
            self.tbCallsign, self.tbRcv, self.tbSnt, self.tbName, self.tbComment,
            self.btnF1, self.btnF2, self.btnF3, self.btnF4, self.btnF5, self.btnF6,
            self.btnF7, self.btnF8, self.btnF9, self.btnF10, self.btnF11, self.btnF12,
            self.cbBand, self.cbMode, self.cbUtc, 
            self.cbRealtime, self.btnNow,
            self.tdDateTime,
            ]

        self.tbCallsign.setFocus()

        self.cbMode.clear()
        self.cbMode.addItems(ALL_MODES)

        self.cbBand.clear()
        self.cbBand.addItems(ALL_BANDS)

        self._real_timer = QTimer()
        self._real_timer.timeout.connect(self.update_time)
        self._real_timer.start(1000)

        self.display_log()

        self.cbRealtime.setChecked(self._preferences.Realtime)
        self.cbUtc.setChecked(self._preferences.Utc)
        self.cbMode.setCurrentText(self._preferences.DefaultMode)
        self.cbBand.setCurrentText(self._preferences.DefaultBand)

        if len(self._db.LoggerOptions.StationCallsign) == 0:
            self.display_station_info_dialog()
            
        # WSHT-X related stuff
        self._wsjt_listener = WsjtListener()
        self._wsjt_listener.setup('127.0.0.1')
        self._wsjt_listener.ListenerEvent.adif_received.connect(self.adif_received)
        if self._preferences.AcceptWsjtPackets:
            self._wsjt_listener.start()
            
        self._preferences.PreferencesChanged.changed.connect(self.preferences_changed)

    
    def __del__(self):
        '''A class' destructor'''
        self._running = False
        
    '''==========================================================================='''
    def close_window(self):
        ''''''
        
        self.close()

    '''==========================================================================='''
    def closeEvent(self, a0) -> None:
        self.save_current_qso_state()
        self._wsjt_listener.stop()
        return super().closeEvent(a0)

    '''==========================================================================='''
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress):
            if source in [self.tbCallsign, self.tbName, self.tbComment]:
                print('key press:', (event.key(), event.text()))
                key = event.key()
                if key in [Qt.Key.Key_Space, Qt.Key.Key_Tab]:
                    if self.MoveFocus(key):
                        '''A focus has been moved. Drop the input.'''
                        return True
        return super(Logger_MainWindow, self).eventFilter(source, event)

    '''==========================================================================='''
    def destroy(self) -> None:
        self._running = False

    '''==========================================================================='''
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

    '''==========================================================================='''
    def MoveFocus(self, key: Qt.Key = Qt.Key.Key_Space) -> bool:
        '''
        Circularly moves focus among Callsign, Name, and Comment.
        Does nothing if none of the controls mentioned above is selected.
        '''
        try:
            selected_control = self.getSelectedControl()
            # Callsign
            if selected_control is self.tbCallsign:
                self.tbName.setFocus()
                return True
            # Name
            elif selected_control is self.tbName:
                if key == Qt.Key.Key_Space:
                    if len(self.tbName.text()) > 0:
                        self.tbName.setText(self.tbName.text() + ' ')
                    else:
                        self.tbComment.setFocus()
                elif key == Qt.Key.Key_Tab:
                    self.tbComment.setFocus()
                return True
            # Comment
            elif selected_control is self.tbComment:
                if key == Qt.Key.Key_Space:
                    if len(self.tbComment.text()) > 0:
                        self.tbComment.setText(self.tbComment.text() + ' ')
                    else:
                        self.tbCallsign.setFocus()
                elif key == Qt.Key.Key_Tab:
                    self.tbCallsign.setFocus()
                return True
            else:
                print(f'Focus remains on the "{selected_control.objectName()}" control.')
        except Exception as ex:
            print(ex.args[0])

        return False

    '''==========================================================================='''
    def GetPathToDatabase(self) -> Path:
        '''Calculates the full path to the database'''
        return FileSystemHelper.get_appdata_path(Path('U2.Suite') / 'Logger' / 'Database', create_if_not_exists=True)

    '''==========================================================================='''
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
        self.save_current_qso_state()

    '''==========================================================================='''
    def save_current_qso_state(self) -> None:
        '''Stores current state of controls to the preferences.'''
        self._preferences.DefaultMode = self.cbMode.currentText()
        self._preferences.DefaultBand = self.cbBand.currentText()
        self._preferences.Utc = self.cbUtc.isChecked()
        self._preferences.Realtime = self.cbRealtime.isChecked()
        self._preferences.write_preferences()

    '''==========================================================================='''
    def clear_fields(self) -> None:
        '''Removes all information from inputs'''
        self.tbCallsign.setText('')
        self.tbName.setText('')
        self.tbComment.setText('')

    '''==========================================================================='''
    def getSelectedControl(self) -> QWidget:
        '''Locates and returns the control that is focused.'''
        for control in self._allControls:
            if control.hasFocus():
                return control

        # in case no control found, the Callsign is concidered focused
        self.tbCallsign.setFocus()
        return self.tbCallsign

    '''==========================================================================='''
    @pyqtSlot()
    def set_current_date_time(self) -> None:
        '''Handles the clicking the Now button'''
        if self.cbUtc.isChecked():
            self.tdDateTime.setDateTime(QDateTime.currentDateTimeUtc())
        else:
            self.tdDateTime.setDateTime(QDateTime.currentDateTime())

    '''==========================================================================='''
    @pyqtSlot()
    def dateTimeCheckBoxChanged(self):
        '''Handles changing of the date and time related checkboxes'''
        self._datetime_utc = self.cbUtc.isChecked()

    '''==========================================================================='''
    @pyqtSlot()
    def bandChanged(self):
        '''Handles changing of the band'''


    '''==========================================================================='''
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

    '''==========================================================================='''
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
        dialog.change.dialogClosed.connect(self.edit_qso_dialog_closed)
        dialog.open()

    '''==========================================================================='''
    def qso_edited(self) -> None:
        '''Handles post edit or delete event.'''
        self.display_log()

    '''==========================================================================='''
    def edit_qso_dialog_closed(self) -> None:
        '''Handles closing of the EditQSO dialog'''

    '''==========================================================================='''
    def update_time(self) -> None:
        if self.cbUtc.isChecked():
            timestamp = datetime.utcnow()
        else:
            timestamp = datetime.now()
        self.lblTimestamp.setText(timestamp.strftime('%d.%m.%Y %H:%M:%S'))

    '''==========================================================================='''
    def real_time_changed(self) -> None:
        '''Handles the switching between real-time and manual input modes.'''
        LoggerMainWindowUiHelper.update_timestamp_controls(self)

    '''==========================================================================='''
    def display_station_info_dialog(self) -> None:
        '''Handles clicking the `Show Station Info` menu'''
        dialog = Logger_StationInfoDialog(self)
        # get values from application preferences, if any
        if len(self._db.LoggerOptions.StationCallsign) == 0:
            self._db.LoggerOptions.StationCallsign = self._preferences.Callsign
        if len(self._db.LoggerOptions.OperatorName) == 0:
            self._db.LoggerOptions.OperatorName = self._preferences.OperatorName
        dialog.setup(self._db.LoggerOptions)
        dialog.change_event.dialogClosed.connect(self.station_info_dialog_closed)
        dialog.open()

    '''==========================================================================='''
    def station_info_dialog_closed(self) -> None:
        '''Handles closing of the Station Info dialog'''

    '''=========================================================================='''
    def keyPressEvent(self, event):
        """This overrides Qt key event."""
        modifier = event.modifiers()
        is_ctrl = modifier == Qt.ControlModifier
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.clear_fields()
            self.tbCallsign.setFocus()
        elif key in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            self.save_qso()
            self.clear_fields()
            self.tbCallsign.setFocus()
            self.display_log()
        elif key == Qt.Key.Key_Delete:
            self.delete_qso()
        elif key == Qt.Key.Key_Space:
            if self.MoveFocus():
                event.accept()

    '''=========================================================================='''
    def delete_qso(self) -> None:
        '''Deletes a selected QSO, if any.'''
        item = self.listLog.currentItem()
        contactnumber = int(item.text().split()[0])
        result = self._db.get_contact_by_id(contactnumber)
        if result != None:
            self._db.delete_contact_by_id(result['id'])
            self.display_log()

    '''=========================================================================='''
    def import_from_file(self) -> None:
        '''Handles click on the `Import from ADIF file` action'''
        filename, filetype = QFileDialog.getOpenFileName(self, 'Select ADIF file', '.',
                filter="ADIF files (*.adi;*.adx)")

        if len(filename) == 0:
            return
        log = AdifHelper.ImportFromFile(filename)
        
        self._db.delete_all_contacts()
        self.import_from_adif_log(log)
        
    def import_from_adif_log(self, log : ADIF_log):
        for entry in log:
            date = f'{entry[ADIF_QSO_DATE]}{entry[ADIF_TIME_ON]}'
            timestamp = datetime.strptime(date, '%Y%m%d%H%M%S')
            data = {
                FIELD_CALLSIGN : str(entry[ADIF_CALL]),
                FIELD_BAND : str(entry[ADIF_BAND]),
                FIELD_MODE : str(entry[ADIF_MODE]),
                FIELD_TIMESTAMP : timestamp
            }
            self._db.log_contact(data)
        
        self.display_log()

    '''==========================================================================='''
    def export_to_adx(self) -> None:
        '''Handles clicking the `Export to ADX file` menu item.'''
        filename, filetype = QFileDialog.getSaveFileName(self, 'Select ADX file', '.',
                filter="ADX files (*.adx)")
        self.export_to_adif_file(filename, filetype)

    '''==========================================================================='''
    def export_to_adif(self) -> None:
        '''Handles clicking the `Export to ADIF file` menu item.'''
        filename, filetype = QFileDialog.getSaveFileName(self, 'Select ADIF file', '.',
                filter="ADIF files (*.adi)")
        self.export_to_adif_file(filename, filetype)

    '''=========================================================================='''
    def export_to_adif_file(self, filename : str, filetype : str) -> None:
        if len(filename) == 0:
            return

        log = ADIF_log()
        contacts = self._db.load_all_contacts()
        
        fields = contacts[0]
        data = contacts[1]
        callsign_index = fields.index(FIELD_CALLSIGN)
        timestamp_index = fields.index(FIELD_TIMESTAMP)
        mode_index = fields.index(FIELD_MODE)
        band_index = fields.index(FIELD_BAND)

        operator = self._db.LoggerOptions.StationCallsign
        for qso in data:
            qso_date = qso[timestamp_index].strftime('%Y%m%d')
            time_on = qso[timestamp_index].strftime('%H%M')
            callsign = qso[callsign_index].upper()
            band = qso[band_index]
            mode = qso[mode_index]

            entry = log.newEntry()
            entry[ADIF_BAND] = band
            entry[ADIF_MODE] = mode
            entry[ADIF_CALL] = callsign
            entry[ADIF_QSO_DATE] = qso_date
            entry[ADIF_TIME_ON] = time_on
            entry[ADIF_TIME_OFF] = time_on
            entry[ADIF_OPERATOR] = operator

        if filetype.find('adi') > -1:
            AdifHelper.ExportAdif(filename, log)
        elif filetype.find('adx') > -1:
            AdifHelper.ExportAdx(filename, log)

    '''=========================================================================='''
    def display_preferences_dialog(self) -> None:
        '''Displays the application preferences dialog.'''
        dialog = Logger_PreferencesDialog(self)
        #dialog.change_event.changed.connect(self.preferences_changed)
        dialog.setup(self._preferences)
        dialog.open()
        
    '''=========================================================================='''
    def preferences_changed(self) -> None:
        '''Handles changing the application preferences.'''
        if self._preferences.AcceptWsjtPackets:
            self._wsjt_listener.start()
        else:
            self._wsjt_listener.stop()
        
    '''=========================================================================='''
    def adif_received(self, log : ADIF_log) -> None:
        '''Handles receiving of the ADIF log.'''
        self.import_from_adif_log(log)
        self.display_log()
        
    '''=========================================================================='''
    def display_about_dialog(self) -> None:
        dialog = DialogAbout()
        dialog.Title = 'About Logger'
        dialog.DisplayImage('logger.png')
        dialog.AppName = 'Logger'
        dialog.AppDescription = self.DESCRIPTION
        dialog.Version = f'version {self.VERSION}'
        year = datetime.utcnow().strftime('%Y')
        dialog.Copyright = f'© {year} Sergey Usmanov, UT8UU'
        dialog.exec()

'''==========================================================================='''
if __name__ == '__main__':
    from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font_dir = FileSystemHelper.relpath("font")
    families = FileSystemHelper.load_fonts_from_dir(os.fspath(font_dir))

    window = Logger_MainWindow()

    window.show()

    app.exec()
    window.destroy()
    del window
