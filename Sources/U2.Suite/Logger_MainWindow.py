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

import helpers.KeyBinderKeys as kbk
from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from pyqtkeybind import keybinder
from typing import List

from trainings.keybinding import WinEventFilter

class Logger_MainWindow(QMainWindow, Ui_LoggerMainWindow):
    _lastSelectedControl: QWidget
    _allControls : List[QWidget]
    _registered = False
    _win_event_filter : WinEventFilter
    _event_dispatcher : QAbstractEventDispatcher
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._allControls = [
            self.tbCallsign, self.tbRcv, self.tbSnt, self.tbName, self.tbComment,
            self.btnF1, self.btnF2, self.btnF3, self.btnF4, self.btnF5, self.btnF6,
            self.btnF7, self.btnF8, self.btnF9, self.btnF10, self.btnF11, self.btnF12,
            self.cbBand, self.cbMode, self.cbUtc, self.cbRealTime,
            self.tdDateTime,
            ]
        self.registerKeys()
    
    def __del__(self):
        '''A class' destructor'''
        self.unregisterKeys()
    
    def getSelectedControl(self) -> QWidget:
        '''
        Locates and returns the control that is focused.
        '''
        for control in self._allControls:
            if control.hasFocus():
                return control

        return None

    def handleKeySpace(self) -> None:
        '''Handles the SPACE key'''
        # Callsign
        if self.tbCallsign.hasFocus():
            self.tbName.setFocus()
        # Name
        elif self.tbName.hasFocus():
            if len(self.tbName.text()) > 0:
                self.tbName.setText(self.tbName.text() + ' ')
            else:
                self.tbComment.setFocus()
        # Comment
        elif self.tbComment.hasFocus():
            if len(self.tbComment.text()) > 0:
                self.tbComment.setText(self.tbComment.text() + ' ')
            else:
                self.tbCallsign.setFocus()

    def keyPress(self, key_string : str):
        '''Handles the key by its name'''
        match key_string:
            case kbk.KEY_SPACE:
                self.handleKeySpace()

    def keyEnterPress(self) -> None:
        self.keyPress(kbk.KEY_RETURN)

    def keyEscPress(self) -> None:
        self.keyPress(kbk.KEY_ESC)

    def keyF1Press(self) -> None:
        self.keyPress(kbk.KEY_F1)

    def keyF2Press(self) -> None:
        self.keyPress(kbk.KEY_F2)

    def keyF3Press(self) -> None:
        self.keyPress(kbk.KEY_F3)

    def keyF4Press(self) -> None:
        self.keyPress(kbk.KEY_F4)

    def keyF5Press(self) -> None:
        self.keyPress(kbk.KEY_F5)

    def keyF6Press(self) -> None:
        self.keyPress(kbk.KEY_F6)

    def keyF7Press(self) -> None:
        self.keyPress(kbk.KEY_F7)

    def keyF8Press(self) -> None:
        self.keyPress(kbk.KEY_F8)

    def keyF9Press(self) -> None:
        self.keyPress(kbk.KEY_F9)

    def keyF10Press(self) -> None:
        self.keyPress(kbk.KEY_F10)

    def keyF11Press(self) -> None:
        self.keyPress(kbk.KEY_F11)

    def keyF12Press(self) -> None:
        self.keyPress(kbk.KEY_F12)

    def keySpacePress(self) -> None:
        self.keyPress(kbk.KEY_SPACE)

    def registerKeys(self) -> None:
        '''
        Registers all hotkeys
        '''
        if self._registered:
            return

        keybinder.init()

        keybinder.register_hotkey(self.winId(), kbk.KEY_RETURN, self.keyEnterPress)
        keybinder.register_hotkey(self.winId(), kbk.KEY_SPACE, self.keySpacePress)
        keybinder.register_hotkey(self.winId(), kbk.KEY_ESC, self.keyEscPress)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F1, self.keyF1Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F2, self.keyF2Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F3, self.keyF3Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F4, self.keyF4Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F5, self.keyF5Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F6, self.keyF6Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F7, self.keyF7Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F8, self.keyF8Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F9, self.keyF9Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F10, self.keyF10Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F11, self.keyF11Press)
        keybinder.register_hotkey(self.winId(), kbk.KEY_F12, self.keyF12Press)

        self._win_event_filter = WinEventFilter(keybinder)
        self._event_dispatcher = QAbstractEventDispatcher.instance()
        self._event_dispatcher.installNativeEventFilter(self._win_event_filter)

        self._registered = True

    def unregisterKeys(self, window : QMainWindow) -> None:
        '''
        Unregisters previously registered keys
        '''
        if not self._registered:
            return
        self._registered = False
        #keybinder.unregister_hotkey(self, kbk.KEY_RETURN)
        keybinder.unregister_hotkey(self, kbk.KEY_SPACE)
        keybinder.unregister_hotkey(self, kbk.KEY_ESC)
        keybinder.unregister_hotkey(self, kbk.KEY_F1)
        keybinder.unregister_hotkey(self, kbk.KEY_F2)
        keybinder.unregister_hotkey(self, kbk.KEY_F3)
        keybinder.unregister_hotkey(self, kbk.KEY_F4)
        keybinder.unregister_hotkey(self, kbk.KEY_F5)
        keybinder.unregister_hotkey(self, kbk.KEY_F6)
        keybinder.unregister_hotkey(self, kbk.KEY_F7)
        keybinder.unregister_hotkey(self, kbk.KEY_F8)
        keybinder.unregister_hotkey(self, kbk.KEY_F9)
        keybinder.unregister_hotkey(self, kbk.KEY_F10)
        keybinder.unregister_hotkey(self, kbk.KEY_F11)
        keybinder.unregister_hotkey(self, kbk.KEY_F12)

def keyEnterPress():
    ''''''
    a = 1

if __name__ == '__main__':
    from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
    app = QApplication(sys.argv)
    window = Logger_MainWindow()

    window.show()
    #window.registerKeys()
    '''keybinder.init()
    keybinder.register_hotkey(window.winId(), "F1", keyEnterPress)
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)
'''

    app.exec()

#    window.unregisterKeys(window)

    del window