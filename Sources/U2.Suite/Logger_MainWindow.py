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

from PyQt5.QtWidgets import QApplication, QMainWindow
from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow

class Logger_MainWindow(QMainWindow, Ui_LoggerMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
    app = QApplication(sys.argv)
    window = Logger_MainWindow()
    window.show()
    app.exec()