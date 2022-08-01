import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from RigSelectorDialog import RigSelectorDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    rig_selector = RigSelectorDialog()
    rig_selector.show()
    
    app.exec_()