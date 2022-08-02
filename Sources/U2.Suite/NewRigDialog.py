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

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from ui.Ui_NewRigDialog import Ui_NewRigDialog

class NewRigDialog(QDialog, Ui_NewRigDialog):
    __baud_rate = '57600'
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
    def debugPrint(self, msg):
        print(msg)
    
    @pyqtSlot()
    def testRig(self):
        self.debugPrint('A testRig button clicked.')
        
    def getSelectedBaudRate(self):
        return self.__baud_rate

    if __name__ == '__main__':
        from NewRigDialog import NewRigDialog
        app = QApplication(sys.argv)
        dialog = NewRigDialog()
        dialog.exec()
        sys.exit(0)