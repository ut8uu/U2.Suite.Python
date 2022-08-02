import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from ui.Ui_NewRigDialog import Ui_NewRigDialog

class NewRigDialog(QDialog, Ui_NewRigDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
    def debugPrint(self, msg):
        print(msg)
    
    @pyqtSlot()
    def testRig(self):
        self.debugPrint('A testRig button clicked.')

    if __name__ == '__main__':
        from NewRigDialog import NewRigDialog
        app = QApplication(sys.argv)
        dialog = NewRigDialog()
        dialog.exec()
        sys.exit(0)