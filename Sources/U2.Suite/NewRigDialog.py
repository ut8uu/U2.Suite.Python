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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog

from helpers.FileSystemHelper import FileSystemHelper
from typing import List
from ui.Ui_NewRigDialog import Ui_NewRigDialog

class NewRigDialog(QDialog, Ui_NewRigDialog):
    __all_rigs = FileSystemHelper.enumerateRigs()
    __rig_type = __all_rigs[0]
    __baud_rate = '57600'
    __port = ''
    __parity = 'None'
    __data_bits = '8'
    __stop_bits = '1'
    __dtr = 'High'
    __rts = 'High'
    __poll_interval = 500
    __timeout = 2000
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        rigs = FileSystemHelper.enumerateRigs()
        self.cbRigType.addItems(rigs)
        self.cbRigType.setCurrentIndex(0)
        
    def debugPrint(self, msg:str):
        print(msg)
    
    @pyqtSlot()
    def rigTypeChanged(self):
        self.__rig_type = self.cbRigType.currentText
        self.debugPrint(f'Rig type {self.__rig_type} selected')
    
    @pyqtSlot()
    def testRig(self):
        self.debugPrint('A testRig button clicked.')
        
    def getSelectedRigType(self):
        return self.__rig_type

    def getSelectedBaudRate(self):
        return self.__baud_rate

    def getSelectedPort(self):
        return self.__port

    def getSelectedParity(self):
        return self.__parity

    def getSelectedDataBits(self) -> str:
        return self.__data_bits

    def getSelectedStopBits(self):
        return self.__stop_bits

    def getSelectedRts(self):
        return self.__rts

    def getSelectedDtr(self):
        return self.__dtr

    def getSelectedPollInterval(self) -> int:
        return self.__poll_interval

    def getSelectedTimeout(self):
        return self.__timeout
    
    def setRigs(self, rigs:List[str]):
        self.__all_rigs = rigs

    if __name__ == '__main__':
        from NewRigDialog import NewRigDialog
        app = QApplication(sys.argv)
        dialog = NewRigDialog()
        
        assert dialog.getSelectedBaudRate() == '57600'
        assert dialog.getSelectedDataBits() == '8'
        assert dialog.getSelectedStopBits() == '1'
        assert dialog.getSelectedDtr() == 'High'
        assert dialog.getSelectedRts() == 'High'
        assert dialog.getSelectedTimeout() == 2000
        assert dialog.getSelectedPollInterval() == 500
        
        dialog.exec()
        sys.exit(0)