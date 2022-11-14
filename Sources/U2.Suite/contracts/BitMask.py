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

class BitMask:
    def __init__(self):
        self._Mask = b''
        self._Flags = b''
        self._Param = RigParameter.none
    @property
    def Mask(self) -> bytearray:
        return self._Mask
    @Mask.setter
    def Mask(self, value):
        self._Mask = value
    @property
    def Flags(self) -> bytearray:
        return self._Flags
    @Flags.setter
    def Flags(self, value):
        self._Flags = value
    @property
    def Param(self) -> RigParameter:
        return self._Param
    @Param.setter
    def Param(self, value):
        self._Param = value
