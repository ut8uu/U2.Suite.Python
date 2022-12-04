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

from pathlib import Path
import sys
from helpers.FileSystemHelper import FileSystemHelper
from logger.log_database import LogDatabase
from logger.logger_constants import DATABASE_DEFAULT
from logger.ui.Ui_LogContentWindow import Ui_LogContentWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget

class Logger_ContentWindow(QMainWindow, Ui_LogContentWindow):

    _path_to_db : Path
    _db : LogDatabase
    
    def __init__(self, path_to_db : Path = None, db_name : str = DATABASE_DEFAULT, parent = None):
        super().__init__(parent)

        if path_to_db == None:
            path_to_db = self.GetPathToDatabase()
        self._path_to_db = path_to_db
        self._db = LogDatabase(self._path_to_db, db_name)
        self.setupUi(self)
        self.UpdateTableView(self.tableMain)
        self.UpdateTableView(self.tableFiltered)

    def GetPathToDatabase(self) -> Path:
        '''Calculates the full path to the database'''
        return FileSystemHelper.get_appdata_path(Path('U2.Suite') / 'Logger' / 'Database', create_if_not_exists=True)

    def UpdateTableView(self, table : QTableWidget) -> None:
        table.setColumnWidth(2, 64)
        table.setColumnWidth(3, 40)
        table.setColumnWidth(4, 40)

    def Refresh(self) -> None:
        '''Refreshes a content of the tables'''
        

if __name__ == '__main__':
    from logger.ui.Ui_LogContentWindow import Ui_LogContentWindow
    app = QApplication(sys.argv)

    # an instance of the window using the default path and name of the database
    db_name = DATABASE_DEFAULT
    if len(sys.argv) > 0:
        db_name = sys.argv[0]
    window = Logger_ContentWindow(db_name=db_name)
    window.show()

    app.exec()
    window.destroy()
    del window