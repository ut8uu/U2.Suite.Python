import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from Ui_RigSelect import Ui_RigSelector

class RigSelectorDialog(QDialog, Ui_RigSelector):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #self.connectSignalsSlots()
    
    def debugPrint(self, msg):
        print(msg)
        
    @pyqtSlot()
    def selectRig(self):
        self.debugPrint('A new rig selected.')
 
    @pyqtSlot()
    def addNewRig(self):
        self.debugPrint('A new rig button clicked.')
 
