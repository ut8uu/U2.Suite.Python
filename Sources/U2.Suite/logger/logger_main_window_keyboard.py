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

if __name__ == '__main__':
    print('This module cannot be executed directly')
    exit(0)

import helpers.KeyBinderKeys as kbk
from helpers.WinEventFilter import WinEventFilter
from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
from PyQt5.QtCore import QAbstractEventDispatcher
from pyqtkeybind import keybinder

class LoggerMainWindowKeyboard():

    _registered : bool
    _window : Ui_LoggerMainWindow

    def __init__(self) -> None:
        self._registered = False
        self._window = None

    def handleKeySpace(self) -> None:
        '''Handles the SPACE key'''
        try:
            # Callsign
            if self._window.tbCallsign.hasFocus():
                self._window.tbName.setFocus()
            # Name
            elif self._window.tbName.hasFocus():
                if len(self._window.tbName.text()) > 0:
                    self._window.tbName.setText(self._window.tbName.text() + ' ')
                else:
                    self._window.tbComment.setFocus()
            # Comment
            elif self._window.tbComment.hasFocus():
                if len(self._window.tbComment.text()) > 0:
                    self._window.tbComment.setText(self._window.tbComment.text() + ' ')
                else:
                    self._window.tbCallsign.setFocus()
        except Exception as ex:
            print(ex.args[0])

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

    def registerKeys(self, window) -> None:
        '''
        Registers all hotkeys
        '''
        if self._registered:
            return

        keybinder.init()

        win_id = window.winId()
        self._window = window

        keybinder.register_hotkey(win_id, kbk.KEY_RETURN, self.keyEnterPress)
        keybinder.register_hotkey(win_id, kbk.KEY_SPACE, self.keySpacePress)
        keybinder.register_hotkey(win_id, kbk.KEY_ESC, self.keyEscPress)
        keybinder.register_hotkey(win_id, kbk.KEY_F1, self.keyF1Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F2, self.keyF2Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F3, self.keyF3Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F4, self.keyF4Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F5, self.keyF5Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F6, self.keyF6Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F7, self.keyF7Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F8, self.keyF8Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F9, self.keyF9Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F10, self.keyF10Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F11, self.keyF11Press)
        keybinder.register_hotkey(win_id, kbk.KEY_F12, self.keyF12Press)

        self._win_event_filter = WinEventFilter(keybinder)
        self._event_dispatcher = QAbstractEventDispatcher.instance()
        self._event_dispatcher.installNativeEventFilter(self._win_event_filter)

        self._registered = True

    def unregisterKeys(self) -> None:
        '''
        Unregisters previously registered keys
        '''
        if not self._registered:
            return
        self._registered = False
        keybinder.unregister_hotkey(self, kbk.KEY_RETURN)
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

