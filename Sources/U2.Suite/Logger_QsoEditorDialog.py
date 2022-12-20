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
from pathlib import Path
import sys
from helpers.FileSystemHelper import FileSystemHelper
from logger.log_database import LogDatabase
from logger.logger_constants import *
from logger.ui.Ui_QsoEditorWindow import Ui_QsoEditor
from PyQt5.QtWidgets import QApplication, QDialog

class Logger_QsoEditorDialog(QDialog, Ui_QsoEditor):

    _qso : dict
    _db : LogDatabase
    
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setupUi(self)

    def setup(self, qso : dict, db : LogDatabase) -> None:
        '''Performs an initial setup'''
        self._db = db
        self._qso = qso

        self.buttonBox.accepted.connect(self.save_changes)

        self.editBand.setCurrentText(qso[FIELD_BAND])
        self.editMode.setCurrentText(qso[FIELD_MODE])
        self.editOpName.setText(qso[FIELD_OPNAME])
        self.editFreq.setText(str(qso[FIELD_FREQUENCY]))
        self.editCallsign.setText(qso[FIELD_CALLSIGN])
        self.editRstRcvd.setText(qso[FIELD_RST_RCVD])
        self.editRstSent.setText(qso[FIELD_RST_SENT])
        self.editDateTime.setDateTime(qso[FIELD_TIMESTAMP])

    def save_changes(self) -> None:
        '''Updates a content of the contact.'''
        data = {
            FIELD_BAND : self.editBand.currentText(),
            FIELD_MODE : self.editMode.currentText(),
            FIELD_TIMESTAMP : self.editDateTime.dateTime().toPyDateTime(),
            FIELD_CALLSIGN : self.editCallsign.text(),
            FIELD_OPNAME : self.editOpName.text(),
            FIELD_RST_SENT : self.editRstSent.text(),
            FIELD_RST_RCVD : self.editRstRcvd.text()
        }
        frequency = self.editFreq.text().lstrip().rstrip()
        try:
            if len(frequency) > 0:
                data[FIELD_FREQUENCY] = int(frequency)
        except Exception as ex:
            print(ex)
            return

        db.change_contact(self._qso[FIELD_ID], data)        

if __name__ == '__main__':
    import os
    from logger.ui.Ui_QsoEditorWindow import Ui_QsoEditor
    app = QApplication(sys.argv)
    db = LogDatabase(Path(os.path.relpath('.')), 'test.sqlite')

    # an instance of the window using the default path and name of the database
    dialog = Logger_QsoEditorDialog()
    data = {
        FIELD_ID : 1,
        FIELD_IS_RUN_QSO : 0,
        FIELD_BAND : '20m',
        FIELD_FREQUENCY : 14200123,
        FIELD_MODE : MODE_SSB,
        FIELD_TIMESTAMP : datetime.datetime.utcnow(),
        FIELD_CALLSIGN : 'UT8UU',
        FIELD_OPNAME : 'Sergey',
        FIELD_RST_SENT : '59',
        FIELD_RST_RCVD : '59'
    }
    db.log_contact(data)
    record = db.load_all_contacts()
    data[FIELD_ID] = record[1][0][0]
    dialog.setup(data, db)
    dialog.open()
    app.exec()

    record = db.load_all_contacts()
    print(record)