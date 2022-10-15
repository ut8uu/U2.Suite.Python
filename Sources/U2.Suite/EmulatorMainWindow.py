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


from math import floor
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from ui.Ui_EmulatorMainWindow import Ui_EmulatorMainWindow

class EmulatorMainWindow(QDialog, Ui_EmulatorMainWindow):
    _last_dial_position : int

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._last_dial_position = 0

    @pyqtSlot()
    def tuningValueChanged(self):
        ''''''
        clearHertzes = lambda x : floor(x/self.dial.maximum()) * self.dial.maximum()

        #tuningValue = value
        current_position = self.dial.value()
        if current_position == 100:
            current_position = 0
        dial_max = self.dial.maximum()
        if abs(current_position - self._last_dial_position) > dial_max/2:
            # the change is too big, we crossed the zero point
            if current_position < self._last_dial_position:
                # moved clockwise, increase the value
                new_value = clearHertzes(self.lcdFreqA.intValue() + dial_max) + current_position
                self.lcdFreqA.display(new_value)
            else:
                # moved counterclockwise, decrease the value
                new_value = clearHertzes(self.lcdFreqA.intValue() - dial_max) + current_position
                self.lcdFreqA.display(new_value)
        else:
            new_value = clearHertzes(self.lcdFreqA.intValue()) + current_position
            self.lcdFreqA.display(new_value)

        self._last_dial_position = current_position
        
    @pyqtSlot()
    def vfoASwitched(self, value : bool):
        ''''''

    @pyqtSlot()
    def vfoBSwitched(self, value : bool):
        ''''''

    @pyqtSlot()
    def rxSwitched(self, value : bool):
        ''''''

    @pyqtSlot()
    def txSwitched(self, value : bool):
        ''''''

    @pyqtSlot()
    def bandChanged(self):
        ''''''

    @pyqtSlot()
    def modeChanged(self):
        ''''''

    @pyqtSlot()
    def splitChanged(self):
        ''''''

    @pyqtSlot()
    def pitchChanged(self):
        ''''''

    @pyqtSlot()
    def xitChanged(self):
        ''''''

    @pyqtSlot()
    def xitOffsetChanged(self):
        ''''''

    @pyqtSlot()
    def ritChanged(self):
        ''''''

    @pyqtSlot()
    def ritOffsetChanged(self):
        ''''''

app = QApplication(sys.argv)
window = EmulatorMainWindow()
window.exec()
sys.exit(0)