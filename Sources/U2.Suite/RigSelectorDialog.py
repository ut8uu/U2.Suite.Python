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
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from ui.Ui_RigSelectDialog import Ui_RigSelector
from NewRigDialog import NewRigDialog

class RigSelectorDialog(QDialog, Ui_RigSelector):
    __selected_rig = 0
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
    def getSelectedRig(self):
        return self.__selected_rig
    
    def debugPrint(self, msg):
        print(msg)
        
    @pyqtSlot()
    def selectRig(self, widget_item: QTableWidgetItem):
        self.debugPrint('A new rig selected.')
        widget_item.data.toString()
 
    @pyqtSlot()
    def addNewRig(self):
        self.debugPrint('A new rig button clicked.')
        newRigDialog = NewRigDialog()
        newRigDialog.exec()
 
