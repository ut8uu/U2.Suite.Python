import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from ui.Ui_RigSelect import Ui_RigSelector
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
 
