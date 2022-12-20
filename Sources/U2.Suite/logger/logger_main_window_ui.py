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

from logger.ui.Ui_LoggerMainWindow import Ui_LoggerMainWindow
from PyQt5.QtGui import QFont

class LoggerMainWindowUiHelper(object):
    
    def update_ui(window : Ui_LoggerMainWindow) -> None:
        '''Updates the UI to handle some UI-specific stuff'''
        font = window.tbCallsign.font()
        font.setCapitalization(QFont.AllUppercase)
        font.setPointSizeF(16)

        window.tbCallsign.setFont(font)
        
        LoggerMainWindowUiHelper.update_timestamp_controls(window)

    def update_timestamp_controls(window: Ui_LoggerMainWindow) -> None:
        '''Updates the timestamp-related controls'''

        if window.cbRealtime.isChecked():
            window.tdDateTime.hide()
            window.btnNow.hide()
            window.lblTimestamp.show()
            window.cbUtc.show()
        else:
            window.lblTimestamp.hide()
            window.cbUtc.hide()
            window.tdDateTime.show()
            window.btnNow.show()
