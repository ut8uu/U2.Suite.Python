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

import logging
import os
from pathlib import Path
import sys

from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtWidgets import QApplication, QDialog, QSizePolicy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), f'..{os.path.sep}..')))

from common.ui.Ui_AboutDialog import Ui_AboutDialog
from helpers.FileSystemHelper import FileSystemHelper

class DialogAbout(QDialog, Ui_AboutDialog):
    """
    Represents an universal About Dialog.
    """
    
    _image_file : str
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self._image_file = ''
        
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

    @property
    def Title(self) -> str:
        return self.windowTitle()
    @Title.setter
    def Title(self, value : str) -> None:
        self.setWindowTitle(value)

    @property
    def AppName(self) -> str:
        return self.lblAppName.text()
    @AppName.setter
    def AppName(self, value : str) -> None:
        self.lblAppName.setText(value)

    @property
    def AppDescription(self) -> str:
        return self.lblAppDescription.text()
    @AppDescription.setter
    def AppDescription(self, value : str) -> None:
        self.lblAppDescription.setText(value)

    @property
    def Version(self) -> str:
        return self.lblVersion.text()
    @Version.setter
    def Version(self, value : str) -> None:
        self.lblVersion.setText(value)

    @property
    def Copyright(self) -> str:
        return self.lblCopyright.text()
    @Copyright.setter
    def Copyright(self, value : str) -> None:
        self.lblCopyright.setText(value)

    def DisplayImage(self, file : str) -> None:
        """
        Displays given image on the dialog surface.
        
        File - a name of the file inside of the /icon/about folder.
        A file itself must be 250x250 pixels.
        """
        path = Path('.') / 'icon' / 'about' / file
        spath = FileSystemHelper.relpath(str(path))
        assert os.path.exists(spath)
        if not os.path.exists(spath):
            logging.error(f'Image /icon/about/{file} not found.')
            return
        
        image = QImage(spath)
        if image.isNull():
            return
        
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.scaleFactor = 1.0
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DialogAbout()
    dialog.Title = 'About the Main'
    dialog.DisplayImage('demo.png')
    dialog.AppName = 'A Demo About Dialog'
    dialog.AppDescription = 'A small dialog to show how the About dialog can be shown without launching the main application. This text is long and therefore should be displayed in multiple lines.'
    dialog.Version = 'version 2.3.5'
    dialog.Copyright = '(c) 2023 Sergey Usmanov, UT8UU'
    dialog.exec()
    sys.exit(0)
    