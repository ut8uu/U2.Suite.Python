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

from contracts.RigCommand import RigCommand
from contracts.RigParameter import RigParameter
from typing import List

class RigCommands(object):
    def __init__(self):
        self._RigType = None
        self._InitCmd : List[RigCommand] = []
        self._WriteCmd = []
        self._StatusCmd : List[RigCommand] = []
        self._ReadableParams : List[RigParameter] = []
        self._WriteableParams : List[RigParameter] = []
        self._Title = str
    @property
    def RigType(self):
        return self._RigType
    @RigType.setter
    def RigType(self, value):
        self._RigType = value
    @property
    def InitCmd(self) -> List[RigCommand]:
        return self._InitCmd
    @InitCmd.setter
    def InitCmd(self, value):
        self._InitCmd = value
    @property
    def WriteCmd(self) -> List[RigCommand]:
        return self._WriteCmd
    @WriteCmd.setter
    def WriteCmd(self, value):
        self._WriteCmd = value
    @property
    def StatusCmd(self) -> List[RigCommand]:
        return self._StatusCmd
    @StatusCmd.setter
    def StatusCmd(self, value):
        self._StatusCmd = value
    @property
    def ReadableParams(self):
        return self._ReadableParams
    @ReadableParams.setter
    def ReadableParams(self, value):
        self._ReadableParams = value
    @property
    def WriteableParams(self):
        return self._WriteableParams
    @WriteableParams.setter
    def WriteableParams(self, value):
        self._WriteableParams = value
    @property
    def Title(self):
        return self._Title
    @Title.setter
    def Title(self, value):
        self._Title = value
