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

import os
import sys
from brandmeister.bm_monitor_core import BrandmeisterMonitorCore
from brandmeister.ui.Ui_BmMonitorMainWindow import Ui_BmMonitorMainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui

from helpers.FileSystemHelper import FileSystemHelper

class BrandmeisterMonitor(QMainWindow, Ui_BmMonitorMainWindow):
    '''Represents a brandmeister monitor application.'''
    
    _monitor_core : BrandmeisterMonitorCore
    
    '''==============================================================='''    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.setupUi(self)
        
        self.actionExit.triggered.connect(self.close_window)
        self.actionStart.triggered.connect(self.start_monitor)
        self.actionStop.triggered.connect(self.stop_monitor)
        
        self._monitor_core = BrandmeisterMonitorCore()
        self.start_monitor()
        
    '''==============================================================='''    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._monitor_core.Stop()
        return super().closeEvent(a0)

    '''==============================================================='''    
    def start_monitor(self):
        if not self.actionStart.isEnabled():
            return

        self.actionStart.setEnabled(False)
        self.actionStop.setEnabled(True)
        self._monitor_core.Start()
    
    '''==============================================================='''    
    def stop_monitor(self):
        if not self.actionStop.isEnabled():
            return

        self.actionStart.setEnabled(True)
        self.actionStop.setEnabled(False)
        self._monitor_core.Stop()
    
    '''==============================================================='''    
    def close_window(self):
        self.close()
    
'''==============================================================='''    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font_dir = FileSystemHelper.relpath("font")
    families = FileSystemHelper.load_fonts_from_dir(os.fspath(font_dir))

    window = BrandmeisterMonitor()

    window.show()

    app.exec()
    window.destroy()
    del window
