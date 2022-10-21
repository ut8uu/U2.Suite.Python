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
from rig.emulators.EmulatorBase import EmulatorBase
from rig.emulators.IC705Emulator import IC705Emulator
from ui.Ui_EmulatorMainWindow import Ui_EmulatorMainWindow

class EmulatorMainWindow(QDialog, Ui_EmulatorMainWindow):
    _last_dial_position : int
    _dial_step : int
    _current_frequency : int
    _emulator : EmulatorBase

    def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        self._last_dial_position = 0
        self._dial_step = 1
        self._current_frequency = 1810000
        self.lcdFreqA.display(self._current_frequency)
        self.lcdFreqB.display(self._current_frequency)

        self._emulator = IC705Emulator()
        self._emulator.start()

    def UpdateVfoValue(self, original_value: int, dial_value: int, \
            modifier: int, mult : int) -> int:
        '''
        Updates the given original value:
        - original_value - a value to be updated
        - dial_value - a value taken from the dial
        - modifier - contains 0 if change is regular, 
            -100 or 100 in case of zero traversal
        - mult - a multiplier according to the dial_step
        '''
        rest = original_value % mult
        if mult == 1:
            rest = 0
        left_part = floor(original_value / (100 * mult)) + modifier
        result = (left_part * 100 + dial_value) * mult + rest
        if result < 0:
            result = original_value
        return result

    def UpdateLcdDisplay(self, new_value : int) -> None:
        if self.rbVfoA.isChecked():
            self.lcdFreqA.display(new_value)
        else:
            self.lcdFreqB.display(new_value)

    def UpdateDial(self):
        ''''''
        left_part = int(floor(self._current_frequency / self._dial_step))
        value = int(left_part % 100)
        if self.dial.value() != value:
            try:
                self.dial.setValue(value)
            except Exception as ex:
                s = ex.args

    @pyqtSlot()
    def tuningValueChanged(self):
        ''''''
        #tuningValue = value
        current_position = self.dial.value()
        if current_position == 100:
            current_position = 0
        dial_max = self.dial.maximum()
        new_value = self._current_frequency
        if abs(current_position - self._last_dial_position) > dial_max/2:
            # the change is too big, we crossed the zero point
            if current_position < self._last_dial_position:
                # moved clockwise, increase the value
                new_value = self.UpdateVfoValue(self._current_frequency, current_position, 1, self._dial_step)
            else:
                # moved counterclockwise, decrease the value
                new_value = self.UpdateVfoValue(self._current_frequency, current_position, -1, self._dial_step)
        else:
            new_value = self.UpdateVfoValue(self._current_frequency, current_position, 0, self._dial_step)

        self._current_frequency = new_value
        self.UpdateLcdDisplay(new_value)
        self._last_dial_position = current_position
        
    @pyqtSlot()
    def dialStepChanged(self):
        '''Reflects the change of the dial step'''
        new_value = self.cbDialStep.currentText()
        if new_value == '1 Hz':
            self._dial_step = 1
        elif new_value == '10 Hz':
            self._dial_step = 10
        elif new_value == '100 Hz':
            self._dial_step = 100
        elif new_value == '1 kHz':
            self._dial_step = 1000
        elif new_value == '10 kHz':
            self._dial_step = 10000
        elif new_value == '100 kHz':
            self._dial_step = 100000
        elif new_value == '1 MHz':
            self._dial_step = 1000000

        self.UpdateDial()       

    @pyqtSlot()
    def vfoASwitched(self):
        ''''''
        if self.rbVfoA.isChecked(): 
            self.rbVfoB.setChecked(False)
            self._current_frequency = self.lcdFreqA.intValue()
            self.UpdateDial()

    @pyqtSlot()
    def vfoBSwitched(self):
        ''''''
        if self.rbVfoB.isChecked(): 
            self.rbVfoA.setChecked(False)
            self._current_frequency = self.lcdFreqB.intValue()
            self.UpdateDial()

    @pyqtSlot()
    def rxSwitched(self):
        ''''''

    @pyqtSlot()
    def txSwitched(self):
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