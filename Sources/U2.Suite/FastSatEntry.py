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
import sys
from typing import List, Tuple
from logger.ui.Ui_FastSatEntry import Ui_FastSatEntry
from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog

class FastSatEntry(QMainWindow, Ui_FastSatEntry):

    _sat_info : List[Tuple[str, str, str, str, str]] = []

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.InitDatabase()

    def InitDatabase(self) -> None:
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
    def NowClicked(self) -> None:
        '''Handles clicking the Now button'''
        self.dateTime.setDateTime(QDateTime.currentDateTimeUtc())

    @pyqtSlot()
    def ExportClicked(self) -> None:
        '''Handles clicking the Export button'''
        if len(self.tbMyCallsign.text()) == 0:
            self.DisplayErrorMessage('Please specify your callsign.')
            return
        if len(self.tbCallsigns.document().toPlainText()) == 0:
            self.DisplayErrorMessage('Please specify at least one correspondent.')
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
        qso_date = self.dateTime.dateTime().toString('MMddyyyy')
        qso_time = self.dateTime.dateTime().toString('HHmm')
        grid = self.tbGridLocator.text().lstrip().rstrip()
        (sat_name, band, mode, sat_mode) = self.GetSatInfo(self.cbSatellite.currentText())
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
            file_name += '.adif'
        fh = open(file_name, 'w')
        fh.write(adif)
        fh.close()

        self.DisplayMessage(f'ADIF was written to "{file_name}".')

    def GetSatInfo(self, sat_name : str) -> Tuple[str, str, str, str]:
        '''
        Returns the satellite information by its name.
        The following information is being returned: 
        sat_name, band, mode, sat_mode
        '''
        for sat_info in self._sat_info:
            if sat_info[0] == sat_name:
                return sat_info

        self.DisplayErrorMessage(f'Satellite {sat_name} not supported.')
        return ('', '', '', '')

    def DisplayErrorMessage(self, message : str) -> None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(message)
            msg.setWindowTitle("Error")
            msg.exec_()

    def DisplayMessage(self, message : str) -> None:
            msg = QMessageBox()
            #msg.setIcon(QMessageBox.Information)
            msg.setText(message)
            msg.setWindowTitle("Info")
            msg.exec_()


if __name__ == '__main__':
    from logger.ui.Ui_FastSatEntry import Ui_FastSatEntry
    app = QApplication(sys.argv)

    # an instance of the window using the default path and name of the database
    window = FastSatEntry()

    demo = True
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