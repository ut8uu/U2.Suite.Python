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

from contracts.RigParameter import RigParameter
from contracts.ValueFormat import ValueFormat

class ParameterValue(object):
    def __init__(self):
        self._Start = 0
        self._Len = 0
        self._Format = ValueFormat.none
        self._Mult = 1
        self._Add = 0
        self._Param = RigParameter.none
    @property
    def Start(self) -> int:
        return self._Start
    @Start.setter
    def Start(self, value):
        self._Start = value
    @property
    def Len(self) -> int:
        return self._Len
    @Len.setter
    def Len(self, value):
        self._Len = value
    @property
    def Format(self) -> ValueFormat:
        return self._Format
    @Format.setter
    def Format(self, value):
        self._Format = value
    @property
    def Mult(self) -> float:
        return self._Mult
    @Mult.setter
    def Mult(self, value):
        self._Mult = value
    @property
    def Add(self) -> float:
        return self._Add
    @Add.setter
    def Add(self, value):
        self._Add = value
    @property
    def Param(self) -> RigParameter:
        return self._Param
    @Param.setter
    def Param(self, value):
        self._Param = value
