import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from Ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
