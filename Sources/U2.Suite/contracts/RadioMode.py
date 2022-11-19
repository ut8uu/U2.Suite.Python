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
class RadioModeType(enum.Enum):
    Unspecified = 0
    CW = 1
    SSB = 2
    PSK = 3
    RTTY = 4
    FM = 5
    DIGITALVOICE = 6
    AM = 7
    SATELLITES = 8

class RadioMode(object):
    @property
    def Type(self) -> RadioModeType:
        return self._Type

    @property
    def Name(self) -> str:
        return self._Name

    def __init__(self, type : RadioModeType, name : str):
        self.CW = 'CW'
        self.SSB = 'SSB'
        self.RTTY = 'RTTY'
        self.AM = 'AM'
        self.FM = 'FM'
        self.DIGITALVOICE = 'DIGITALVOICE'
        self.PSK = 'PSK'
        self.SATELLITES = 'SATELLITES'
        self._Type = type
        self._Name = name
        Type = type
        Name = name

    @staticmethod
    def AllModes() -> List[RadioModeType]:
        return [RadioModeType.CW, RadioModeType.PSK, RadioModeType.RTTY, RadioModeType.DIGITALVOICE, RadioModeType.SSB, RadioModeType.FM, RadioModeType.AM, RadioModeType.SATELLITES]

    @staticmethod
    def CwModes() -> List[RadioModeType]:
        return [RadioModeType.CW]

    @staticmethod
    def CwSsbModes() -> List[RadioModeType]:
        return [RadioModeType.CW, RadioModeType.SSB]

    @staticmethod
    def NarrowBandModes() -> List[RadioModeType]:
        return [RadioModeType.CW, RadioModeType.PSK, RadioModeType.RTTY]

    @staticmethod
    def NarrowBandDigitalModes() -> List[RadioModeType]:
        return [RadioModeType.PSK, RadioModeType.RTTY]

    @staticmethod
    def VoiceModes() -> List[RadioModeType]:
        return [RadioModeType.DIGITALVOICE, RadioModeType.SSB, RadioModeType.FM, RadioModeType.AM]

    @staticmethod
    def FmDigitalModes() -> List[RadioModeType]:
        return [RadioModeType.FM, RadioModeType.PSK, RadioModeType.RTTY, RadioModeType.DIGITALVOICE]

    @staticmethod
    def AmFmModes() -> List[RadioModeType]:
        return [RadioModeType.FM, RadioModeType.AM]

    @staticmethod
    def SatelliteModes() -> List[RadioModeType]:
        return [RadioModeType.SATELLITES]

class RadioModeFM(RadioMode):
    def __init__(self):
        super(RadioModeFM, self).__init__(RadioModeType.FM, RadioMode.FM)

class RadioModeCW(RadioMode):
    def __init__(self):
        super(RadioModeCW, self).__init__(RadioModeType.CW, RadioMode.CW)

class RadioModeAM(RadioMode):
    def __init__(self):
        super(RadioModeAM, self).__init__(RadioModeType.AM, RadioMode.AM)

class RadioModeSsb(RadioMode):
    def __init__(self):
        super(RadioModeSsb, self).__init__(RadioModeType.SSB, RadioMode.SSB)

class RadioModeDigitalVoice(RadioMode):
    def __init__(self):
        super(RadioModeDigitalVoice, self).__init__(RadioModeType.DIGITALVOICE, RadioMode.DIGITALVOICE)

class RadioModeRtty(RadioMode):
    def __init__(self):
        super(RadioModeRtty, self).__init__(RadioModeType.RTTY, RadioMode.RTTY)

class RadioModePsk(RadioMode):
    def __init__(self):
        super(RadioModePsk, self).__init__(RadioModeType.PSK, RadioMode.PSK)

