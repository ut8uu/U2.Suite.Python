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

from contracts.RigCommands import RigCommands
from contracts.RigCommand import RigCommand
from exceptions.IniFileLoadException import IniFileLoadException
from helpers.FileSystemHelper import readFile, getLocalFolder, enumerateDirectory
from os import join

class RigHelper():
    
    @staticmethod
    def LoadRigCommands(path):
        return 0
    
    @staticmethod
    def LoadAllRigCommands(path):
        list = []
        iniDirectory = join(getLocalFolder, "ini")
        files = enumerateDirectory(iniDirectory, ".ini")
        for file in files:
            try:
                list.Add(RigHelper.LoadRigCommands(file))
            except IniFileLoadException as ex:
                print('Error loading ini file {}. {}'.format(file, ex.Message))
        return list        
    