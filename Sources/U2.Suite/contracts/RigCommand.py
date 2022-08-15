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

from typing import List
from contracts.BitMask import BitMask
from contracts.ParameterValue import ParameterValue

class RigCommand(object):
    def __init__(self):
        self._Code = None
        self._Value = None
        self._ReplyLength = None
        self._ReplyEnd = None
        self._Validation = None
        self._Values = None
        self._Flags = None

    @property
    def Code(self) -> bytearray:
        return self._Code
    @Code.setter
    def Code(self, value):
        self._Code = value

    @property
    def Value(self) -> ParameterValue:
        return self._Value
    @Value.setter
    def Value(self, value):
        self._Value = value

    @property
    def ReplyLength(self) -> int:
        return self._ReplyLength
    @ReplyLength.setter
    def ReplyLength(self, value):
        self._ReplyLength = value

    @property
    def ReplyEnd(self) -> bytearray:
        return self._ReplyEnd
    @ReplyEnd.setter
    def ReplyEnd(self, value):
        self._ReplyEnd = value

    @property
    def Validation(self) -> BitMask:
        return self._Validation
    @Validation.setter
    def Validation(self, value):
        self._Validation = value

    @property
    def Values(self) -> List[ParameterValue]:
        return self._Values
    @Values.setter
    def Values(self, value):
        self._Values = value

    @property
    def Flags(self) -> List[BitMask]:
        return self._Flags
    @Flags.setter
    def Flags(self, value):
        self._Flags = value
