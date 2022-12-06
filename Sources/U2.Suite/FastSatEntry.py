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

import datetime
from json import dumps, loads
import logging
import os
import sys
from logger.logger_constants import *
from logger.ui.Ui_FastSatEntry import Ui_FastSatEntry
from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from typing import List, Tuple

class FastSatEntry(QMainWindow, Ui_FastSatEntry):

    _sat_info : List[Tuple[str, str, str, str, str]] = []

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_database()

        self.preferences = {
            KEY_MYCALLSIGN: "",
            KEY_MYGRID: "",
            KEY_DEFAULT_MODE: "",
            KEY_DEFAULT_SATELLITE: ""
            }
        self.reference_preference = self.preferences.copy()
        self.read_preferences()

    def init_database(self) -> None:
        '''
        Initializes a database of satellites
        List contains the following values: sat_name, band, mode, sat_mode
        '''
        self._sat_info.append(('SO-50', '2m', 'FM', 'VU'))
        self._sat_info.append(('ISS', '2m', 'FM', 'VU'))
        self._sat_info.append(('AO-27', '2m', 'FM', 'VU'))
        self._sat_info.append(('AO-85', '70cm', 'FM', 'UV'))
        self._sat_info.append(('AO-91', '70cm', 'FM', 'UV'))
        self._sat_info.append(('AO-92', '70cm', 'FM', 'UV'))

    @pyqtSlot()
    def now_clicked(self) -> None:
        '''Handles clicking the Now button'''
        self.dateTime.setDateTime(QDateTime.currentDateTimeUtc())

    @pyqtSlot()
    def save_clicked(self) -> None:
        '''Handles clicking the Save button'''
        self.preferences[KEY_DEFAULT_MODE] = self.cbMode.currentText()
        self.preferences[KEY_DEFAULT_SATELLITE] = self.cbSatellite.currentText()
        self.preferences[KEY_MYCALLSIGN] = self.tbMyCallsign.text()
        self.preferences[KEY_MYGRID] = self.tbGridLocator.text()
        self.reference_preference = self.preferences.copy()
        self.write_preferences()

    @pyqtSlot()
    def export_clicked(self) -> None:
        '''Handles clicking the Export button'''
        if len(self.tbMyCallsign.text()) == 0:
            self.display_error_message('Please specify your callsign.')
            return
        if len(self.tbCallsigns.document().toPlainText()) == 0:
            self.display_error_message('Please specify at least one correspondent.')
            return
        
        now = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        adif = f'''
#++
#
#   Fast Sat Entry version 1.0, Copyright © 2022 Sergey Usmanov, UT8UU
#   http://www.hamstudio.net
#
#   Created:  {now}
#
#--

<ADIF_VERS:3>2.2
<PROGRAMID:12>FastSatEntry
<PROGRAMVERSION:11>Version 1.0
<EOH>

'''
        my_call = self.tbMyCallsign.text().lstrip().rstrip()
        qso_date = self.dateTime.dateTime().toString('yyyyMMdd')
        qso_time = self.dateTime.dateTime().toString('HHmm')
        grid = self.tbGridLocator.text().lstrip().rstrip()
        (sat_name, band, mode, sat_mode) = self.get_sat_info(self.cbSatellite.currentText())
        if len(sat_name) == 0:
            return
        num = self.tbCallsigns.document().blockCount()
        block = self.tbCallsigns.document().firstBlock()
        index = 0
        while index < num:
            index += 1
            call = block.text().rstrip().lstrip()
            if len(call) == 0:
                continue
            adif += f'''
<STATION_CALLSIGN:{len(my_call)}>{my_call} <CALL:{len(call)}>{call} 
<QSO_DATE:8>{qso_date} <TIME_ON:4>{qso_time} <BAND:{len(band)}>{band} <MODE:{len(mode)}>{mode} 
<OPERATOR:{len(my_call)}>{my_call} <MY_GRIDSQUARE:{len(grid)}>{grid} 
<PROP_MODE:3>SAT <SAT_MODE:{len(sat_mode)}>{sat_mode} <SAT_NAME:{len(sat_name)}>{sat_name}
<EOR>

'''
            block = block.next()
        
        name = QFileDialog.getSaveFileName(self, 'Save File')
        if len(name[0]) == 0:
            return
        file_name = name[0]
        if file_name.lower().find('.adi') == -1:
            file_name += '.adi'
        fh = open(file_name, 'w')
        fh.write(adif)
        fh.close()

        self.display_message(f'ADIF was written to "{file_name}".')

    def get_sat_info(self, sat_name : str) -> Tuple[str, str, str, str]:
        '''
        Returns the satellite information by its name.
        The following information is being returned: 
        sat_name, band, mode, sat_mode
        '''
        for sat_info in self._sat_info:
            if sat_info[0] == sat_name:
                return sat_info

        self.display_error_message(f'Satellite {sat_name} not supported.')
        return ('', '', '', '')

    def display_error_message(self, message : str) -> None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(message)
            msg.setWindowTitle("Error")
            msg.exec_()

    def display_message(self, message : str) -> None:
            msg = QMessageBox()
            #msg.setIcon(QMessageBox.Information)
            msg.setText(message)
            msg.setWindowTitle("Info")
            msg.exec_()

    def get_preference(self, key : str, default_value : str = '') -> str:
        '''
        Performs an attempt to get the preference by the given name.
        If preference not found, a default value will be returned.
        '''
        try:
            return self.preferences.get(key)
        except KeyError:
            return default_value

    def write_preferences(self):
        '''Writes the preferences file'''
        with open(f'./{PREFERENCES_FILE}', "wt", encoding="utf-8") as file_descriptor:
            self.preferences = self.reference_preference.copy()
            file_descriptor.write(dumps(self.preferences, indent=4))
            logging.info("%s", self.preferences)

    def read_preferences(self):
        '''Reads preferences from existing file or creates a new one'''
        try:
            preferences_file_name = f'./{PREFERENCES_FILE}'
            if os.path.exists(preferences_file_name):
                with open(preferences_file_name, "rt", encoding="utf-8") as file_descriptor:
                    content = file_descriptor.read()
                    if len(content) == 0:
                        self.write_preferences()
                    else:
                        self.preferences = loads(content)
                        logging.info("%s", self.preferences)
            else:
                logging.info("No preference file. Writing preference.")
                self.write_preferences()
        except IOError as exception:
            logging.critical("Error: %s", exception)

        try:
            self.tbMyCallsign.setText(self.get_preference(KEY_MYCALLSIGN))
            self.tbGridLocator.setText(self.get_preference(KEY_MYGRID))
            default_mode = self.get_preference(KEY_DEFAULT_MODE)
            if len(default_mode) > 0 and self.cbMode.findText(default_mode) > -1:
                self.cbMode.setCurrentText(default_mode)
            default_sat = self.get_preference(KEY_DEFAULT_SATELLITE)
            if len(default_sat) > 0 and self.cbSatellite.findText(default_sat) > -1:
                self.cbSatellite.setCurrentText(default_sat)
            

        except KeyError as exception:
            logging.critical('Error: %s', exception)

if __name__ == '__main__':
    from logger.ui.Ui_FastSatEntry import Ui_FastSatEntry
    app = QApplication(sys.argv)

    # an instance of the window using the default path and name of the database
    window = FastSatEntry()

    demo = False
    if demo:
        window.tbMyCallsign.setText('UT8UU')
        window.tbCallsigns.setText('''UT2UB
UR8US
4O/UT3UBR''')
        window.tbGridLocator.setText('KO50aa')
        window.dateTime.setDateTime(QDateTime.currentDateTimeUtc())

    window.show()

    app.exec()
    window.destroy()
    del window