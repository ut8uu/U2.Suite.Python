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

import sys
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog

from logger.log_database import LogDatabase
from logger.logger_options import LoggerOptions
from logger.ui.Ui_StationInfoDialog import Ui_StationInfoDialog

class StationInfoDialogEvent(QtCore.QObject):
    """
    Custom qt event signal used when something in station info was updated.
    """
    changed = QtCore.pyqtSignal()

class Logger_StationInfoDialog(QDialog, Ui_StationInfoDialog):
    '''Represents a station info dialog.'''

    _options : LoggerOptions
    _change_event : StationInfoDialogEvent

    '''---------------------------------------------------------------------------'''
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setupUi(self)

        font = self.tbCallsign.font()
        font.setCapitalization(QFont.AllUppercase)
        font.setPointSizeF(16)
        self.tbCallsign.setFont(font)

    '''---------------------------------------------------------------------------'''
    def setup(self, options: LoggerOptions) -> None:
        '''Initiates the dialog with data.'''
        self._change_event = StationInfoDialogEvent()

        self.buttonBox.accepted.connect(self.save_changes)

        self._options = options
        self.tbCallsign.setText(self._options.StationCallsign)
        self.tbOoperatorName.setText(self._options.OperatorName)

    '''---------------------------------------------------------------------------'''
    def save_changes(self) -> None:
        '''Saves all the changes and closes the dialog box'''
        self._options.OperatorName = self.tbOoperatorName.text()
        self._options.StationCallsign = self.tbCallsign.text()

        self._change_event.changed.emit()
        self.close()

if __name__ == '__main__':
    import os
    from logger.ui.Ui_StationInfoDialog import Ui_StationInfoDialog
    app = QApplication(sys.argv)
    db = LogDatabase(Path(os.path.relpath('.')), 'test.sqlite')
    options = LoggerOptions(db._db)

    # an instance of the window using the default path and name of the database
    dialog = Logger_StationInfoDialog()
    dialog.setup(options)
    dialog.open()
    app.exec()

    record = db.load_all_contacts()
    print(record)
