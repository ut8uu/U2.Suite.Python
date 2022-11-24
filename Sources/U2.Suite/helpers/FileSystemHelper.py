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

import pathlib
import sys
import os
from os import listdir, getcwd, path
from os.path import isfile, join
from typing import List

class FileSystemHelper():
    @staticmethod
    def enumerateDirectory(path:str, ext:str) -> List[str]:
        return [f for f in listdir(path) if isfile(join(path, f)) & f.endswith(ext)]
    
    @staticmethod
    def enumerateRigs() -> List[str]:
        result = []
        iniDirectory = FileSystemHelper.getIniFilesFolder()
        files = FileSystemHelper.enumerateDirectory(iniDirectory, '.ini')
        result = [f.removesuffix('.ini') for f in files]
        return result
    
    @staticmethod
    def readFile(path:str) -> List[str]:
        with open(path) as f: lines = f.readlines()
        return lines
    
    @staticmethod
    def getLocalFolder():
        # we are in ./helpers directory
        dir = path.dirname(path.dirname(path.abspath(__file__)))
        assert not dir.endswith('helpers')
        return getcwd()
    
    @staticmethod
    def getIniFilesFolder() -> str:
        return join(FileSystemHelper.getLocalFolder(), 'manyrig', 'ini')

    @staticmethod
    def get_appdata_path(folder : str, create_if_not_exists : bool = False) -> pathlib.Path:
        '''
        Returns a path to the given folder in the application 
        data folder depending on the OS.

        folder - a name of the folder inside the shared folder
        create_if_not_exists - indicates whether the folder must be created if it is absent
        '''
        home = pathlib.Path.home()
        path : pathlib.Path

        if sys.platform == "win32":
            path = home / "AppData/Roaming" / folder
        elif sys.platform == "linux":
            path = home / ".local/share" / folder
        elif sys.platform == "darwin":
            path = home / "Library/Application Support" / folder

        if create_if_not_exists and not os.path.exists(path):
            os.mkdir(path)

        return path
    