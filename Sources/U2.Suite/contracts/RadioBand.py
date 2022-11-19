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

import enum
from typing import List

@enum.unique
class RadioBandType(enum.Enum):
    Unspecified = 0
    B160m = 1
    B80m = 2
    B60m = 3
    B50m = 4
    B40m = 5
    B30m = 6
    B20m = 7
    B17m = 8
    B15m = 9
    B12m = 10
    B11m = 11
    B10m = 12
    B6m = 13
    B4m = 14
    B2m = 15
    B70cm = 16
    B23cm = 17

@enum.unique
class RadioBandGroup(enum.Enum):
    Unspecified = 0
    MW = 1
    LW = 2
    HF = 3
    VHF = 4
    UHF = 5

@enum.unique
class RadioModeType(enum.Enum):
    CW = 1
    SSB = 2
    PSK = 3
    RTTY = 4
    FM = 5
    DIGITALVOICE = 6
    AM = 7
    SATELLITES = 8

class SubBand(object):
    def __init__(self, begin : int, end : int, modes : List[RadioModeType]):
        self._BeginMhz = begin
        self._EndMhz = end
        self._Modes = modes

    @property
    def BeginMhz(self) -> int:
        return self._BeginMhz
    @BeginMhz.setter
    def BeginMhz(self, value):
        self._BeginMhz = value

    @property
    def EndMhz(self) -> int:
        return self._EndMhz
    @EndMhz.setter
    def EndMhz(self, value):
        self._EndMhz = value

    @property
    def Modes(self) -> List[RadioModeType]:
        return self._Modes
    @Modes.setter
    def Modes(self, value):
        self._Modes = value

class RadioBand(object):
    _BeginMhz : int
    _EndMhz : int
    _Group : RadioBandGroup
    _Type : RadioBandType
    _Name : str
    _SubBands : List[SubBand]

    def __init__(self):
        self._Name = ''
        self._Group = RadioBandGroup.Unspecified
        self._BeginMhz = 0
        self._EndMhz = 0
        self._Type = RadioBandType.Unspecified
        self._SubBands = []
    @property
    def Name(self) -> str:
        return self._Name
    @Name.setter
    def Name(self, value):
        self._Name = value
    @property
    def Group(self) -> RadioBandGroup:
        return self._Group
    @Group.setter
    def Group(self, value):
        self._Group = value

    @property
    def BeginMhz(self) -> int:
        return self._BeginMhz
    @BeginMhz.setter
    def BeginMhz(self, value):
        self._BeginMhz = value

    @property
    def Type(self) -> RadioBandType:
        return self._Type
    @Type.setter
    def Type(self, value):
        self._Type = value
    
    @property
    def EndMhz(self) -> int:
        return self._EndMhz
    @EndMhz.setter
    def EndMhz(self, value):
        self._EndMhz = value

    @property
    def SubBands(self) -> List[SubBand]:
        return self._SubBands
    @SubBands.setter
    def SubBands(self, value):
        self._SubBands = value

class RadioBandName(object):
    B160m : str
    B80m : str
    B60m : str
    B40m : str
    B30m : str
    B20m : str
    B17m : str
    B15m : str
    B12m : str
    B10m : str
    B6m : str
    B4m : str
    B2m : str
    B70cm : str

    def __init__(self):
        self.B160m = "160m"
        self.B80m = "80m"
        self.B60m = "60m"
        self.B40m = "40m"
        self.B30m = "30m"
        self.B20m = "20m"
        self.B17m = "17m"
        self.B15m = "15m"
        self.B12m = "12m"
        self.B10m = "10m"
        self.B6m = "6m"
        self.B4m = "4m"
        self.B2m = "2m"
        self.B70cm = "70cm"
