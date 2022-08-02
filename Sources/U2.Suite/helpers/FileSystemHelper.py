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
from os import listdir, getcwd
from os.path import isfile, join, open

class FileSystemHelper():
    @staticmethod
    def enumerateDirectory(path, ext):
        return [f for f in listdir(path) if isfile(join(path, f)) & f.endswith(ext)]
    
    @staticmethod
    def readFile(path):
        with open(path) as f: lines = f.readlines()
        return lines
    
    @staticmethod
    def getLocalFolder():
        return getcwd()