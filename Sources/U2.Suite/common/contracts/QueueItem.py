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

from common.contracts.RigParameter import RigParameter
from helpers.ConversionHelper import ConversionHelper
from manyrig.rig.enums.CommandKind import CommandKind

class QueueItem(object):
    def __init__(self):
        self._Code : bytearray = None
        self._Kind : CommandKind = CommandKind.Custom
        self._Param : RigParameter = RigParameter.none
        self._Number : int = 0
        self._CustSender = None
        self._ReplyLength = 0
        self._ReplyEnd : str = ''

    @property
    def Code(self) -> bytearray:
        return self._Code
    @Code.setter
    def Code(self, value):
        self._Code = value

    @property
    def Kind(self):
        return self._Kind
    @Kind.setter
    def Kind(self, value) -> CommandKind:
        self._Kind = value

    @property
    def Param(self):
        return self._Param
    @Param.setter
    def Param(self, value) -> RigParameter:
        self._Param = value

    @property
    def Number(self) -> int:
        return self._Number
    @Number.setter
    def Number(self, value):
        self._Number = value

    @property
    def CustSender(self):
        return self._CustSender
    @CustSender.setter
    def CustSender(self, value):
        self._CustSender = value

    @property
    def ReplyLength(self) -> str:
        return self._ReplyLength
    @ReplyLength.setter
    def ReplyLength(self, value):
        self._ReplyLength = value

    @property
    def ReplyEnd(self):
        return self._ReplyEnd
    @ReplyEnd.setter
    def ReplyEnd(self, value):
        self._ReplyEnd = value
        
    @property
    def NeedsReply(self):
        return ((self.ReplyLength > 0) or (self.ReplyEnd != str.Empty))
    def ToString(self):
        reply = ("Reply" if self.NeedsReply else "NoReply")
        return "{} : {} : {} : {}".format(ConversionHelper.BytesToHexStr(self.Code), self.Kind, self.Param, reply)
