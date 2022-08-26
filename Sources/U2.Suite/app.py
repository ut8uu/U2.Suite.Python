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

from PyQt5.QtWidgets import QApplication

from RigSelectorDialog import RigSelectorDialog
from MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    rig_selector = RigSelectorDialog()
    dialog_code = rig_selector.exec()
    print(dialog_code)
    
    print('Rig selected')
    
    selected_rig = rig_selector.getSelectedRig()
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())
