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

class ParameterValue(object):
    def __init__(self):
        self._Start = None
        self._Len = None
        self._Format = None
        self._Mult = None
        self._Add = None
        self._Param = None
    @property
    def Start(self):
        return self._Start
    @Start.setter
    def Start(self, value):
        self._Start = value
    @property
    def Len(self):
        return self._Len
    @Len.setter
    def Len(self, value):
        self._Len = value
    @property
    def Format(self):
        return self._Format
    @Format.setter
    def Format(self, value):
        self._Format = value
    @property
    def Mult(self):
        return self._Mult
    @Mult.setter
    def Mult(self, value):
        self._Mult = value
    @property
    def Add(self):
        return self._Add
    @Add.setter
    def Add(self, value):
        self._Add = value
    @property
    def Param(self):
        return self._Param
    @Param.setter
    def Param(self, value):
        self._Param = value
