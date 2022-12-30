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

import os
from pathlib import Path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.FileSystemHelper import FileSystemHelper
from logger.logger_preferences import LoggerApplicationPreferences
from logger.ui.Ui_LoggerPreferencesDialog import Ui_LoggerPreferencesDialog

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog

class PreferencesDialogEvent(QObject):
    """
    Custom qt event signal used when something in station info was updated.
    """
    changed = pyqtSignal()
    dialogClosed = pyqtSignal()


class Logger_PreferencesDialog(QDialog, Ui_LoggerPreferencesDialog):
    '''Represents Preferences dialog.'''
    
    _preferences : LoggerApplicationPreferences
    change_event : PreferencesDialogEvent
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        
        self.setupUi(self)

        self.change_event = PreferencesDialogEvent()

        self.buttonBox.accepted.connect(self.save_changes)
        self.buttonBox.rejected.connect(self.close_dialog)

        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(FileSystemHelper.relpath('icon/edit_file-32.png')))
    
    '''---------------------------------------------------------------------------'''
    def setup(self, preferences : LoggerApplicationPreferences) -> None:
        '''Initiates the dialog with data.'''

        self._preferences = preferences
        self.cbAcceptWsjtPackets.setChecked(preferences.AcceptWsjtPackets)
        
        # Station Info stuff
        self.tbCall.setText(preferences.Callsign)
        self.tbGridSquare.setText(preferences.GridSquare)
        self.tbOperatorName.setText(preferences.OperatorName)
        
    def close_dialog(self) -> None:
        self.close()

    def save_changes(self) -> None:
        '''Saves changes to preferences file.'''
        self._preferences.AcceptWsjtPackets = self.cbAcceptWsjtPackets.isChecked()
        #Station Info stuff
        self._preferences.OperatorName = self.tbOperatorName.text()
        self._preferences.Callsign = self.tbCall.text()
        self._preferences.GridSquare = self.tbGridSquare.text()
        
        self._preferences.write_preferences()
        self.change_event.changed.emit()
        self.close()
        
if __name__ == '__main__':
    '''Launched directly. Consider a test run.'''
    import os
    from logger.ui.Ui_StationInfoDialog import Ui_StationInfoDialog
    app = QApplication(sys.argv)
    preferences = LoggerApplicationPreferences()
    preferences.Callsign = 'UT8UU'
    preferences.GridSquare = 'KO50'
    preferences.OperatorName = 'Sergey'
    
    preferences.AcceptWsjtPackets = True

    # an instance of the window using the default path and name of the database
    dialog = Logger_PreferencesDialog()
    dialog.setup(preferences)
    dialog.open()
    app.exec()
