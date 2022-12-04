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
from helpers.FileSystemHelper import FileSystemHelper
from logger.ui.Ui_FastSatEntry import Ui_FastSatEntry
from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow

class FastSatEntry(QMainWindow, Ui_FastSatEntry):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def NowClicked(self) -> None:
        '''Handles clicking the Now button'''
        self.dateTime.setDateTime(QDateTime.currentDateTimeUtc())

    @pyqtSlot()
    def ExportClicked(self) -> None:
        '''Handles clicking the Export button'''

if __name__ == '__main__':
    from logger.ui.Ui_FastSatEntry import Ui_FastSatEntry
    app = QApplication(sys.argv)

    # an instance of the window using the default path and name of the database
    window = FastSatEntry()
    window.show()

    app.exec()
    window.destroy()
    del window