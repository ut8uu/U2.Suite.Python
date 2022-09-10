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

class RigSettings(object):
    DataBits = [ 5, 6, 7, 8]
    BaudRates = [ 110, 300, 600, 1200, 2400, 
                 4800, 9600, 14400, 19200, 38400, 56000,
                 57600, 115200, 128000, 256000 ]
    StopBits = [ 1.0, 1.5, 2.0 ]
    
    def __init__(self):
        self._RigNumber = ''
        self._Enabled = False
        self._RigType = ''
        self._Port = ''
        self._BaudRate = 9600
        self._DataBits = 8
        self._Parity = 0
        self._StopBits = 1.0
        self._RtsMode = False
        self._DtrMode = False
        self._PollMs = 500
        self._TimeoutMs = 3000
        
    @property
    def RigId(self) -> int:
        return self._RigId
    @RigId.setter
    def RigId(self, value):
        self._RigId = value
    @property
    def Enabled(self) -> bool:
        return self._Enabled
    @Enabled.setter
    def Enabled(self, value):
        self._Enabled = value
    @property
    def RigType(self) -> str:
        return self._RigType
    @RigType.setter
    def RigType(self, value):
        self._RigType = value
    @property
    def Port(self) -> str:
        return self._Port
    @Port.setter
    def Port(self, value):
        self._Port = value
    @property
    def BaudRate(self) -> int:
        return self._BaudRate
    @BaudRate.setter
    def BaudRate(self, value):
        self._BaudRate = value
    @property
    def DataBits(self) -> int:
        return self._DataBits
    @DataBits.setter
    def DataBits(self, value):
        self._DataBits = value
    @property
    def Parity(self) -> int:
        return self._Parity
    @Parity.setter
    def Parity(self, value):
        self._Parity = value
    @property
    def StopBits(self) -> int:
        return self._StopBits
    @StopBits.setter
    def StopBits(self, value) -> float:
        self._StopBits = value
    @property
    def RtsMode(self):
        return self._RtsMode
    @RtsMode.setter
    def RtsMode(self, value):
        self._RtsMode = value
    @property
    def DtrMode(self):
        return self._DtrMode
    @DtrMode.setter
    def DtrMode(self, value):
        self._DtrMode = value
    @property
    def PollMs(self) -> int:
        return self._PollMs
    @PollMs.setter
    def PollMs(self, value):
        self._PollMs = value
    @property
    def TimeoutMs(self) -> int:
        return self._TimeoutMs
    @TimeoutMs.setter
    def TimeoutMs(self, value):
        self._TimeoutMs = value
