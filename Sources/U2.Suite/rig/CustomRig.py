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
from rig.enums.RigControlType import RigControlType
from rig.enums.RigControlStatus import RigControlStatus

class CustomRig(object):
    _application_id : str
    _rig_number = 0
    _rig_control_type = RigControlType.guest  
    _enabled = False  
    _freq = 0
    _freqA = 0
    _freqB = 0
    _pitch = 0
    _ritOffset = 0
    _vfo = RigParameter.none
    _rit = RigParameter.none
    _xit = RigParameter.none
    _tx = RigParameter.none
    _mode = RigParameter.none
    _split = RigParameter.none
    _online = None

    def __init__(self, 
        control_type: RigControlType, 
        rig_number: int,
        application_id: str):
        _rig_control_type = control_type
        _rig_number = rig_number
        _application_id = application_id

    @property
    def ApplicationId(self) -> int:
        return self._application_id
    @ApplicationId.setter
    def ApplicationId(self, value : int):
        self._application_id = value

    @property
    def RigNumber(self) -> int:
        return self._rig_number
    @RigNumber.setter
    def RigNumber(self, value : int):
        self._rig_number = value

    @property
    def Enabled(self) -> bool:
        return self._enabled
    @Enabled.setter
    def Enabled(self, value : bool):
        self._enabled = value

    @property
    def Status(self):
        return self.GetStatus()

    @property
    def Freq(self) -> int:
        return self._freq
    @Freq.setter
    def Freq(self, value : int):
        return self.SetFreq(value)

    @property
    def FreqA(self) -> int:
        return self._freqA
    @FreqA.setter
    def FreqA(self, value : int):
        return self.SetFreqA(value)
    @property
    def FreqB(self) -> int:
        return self._freqB
    @FreqB.setter
    def FreqB(self, value : int):
        return self.SetFreqB(value)

    @property
    def Pitch(self) -> int:
        return self._pitch
    @Pitch.setter
    def Pitch(self, value : int):
        return self.SetPitch(value)
    @property
    def RitOffset(self) -> int:
        return self._ritOffset
    @RitOffset.setter
    def RitOffset(self, value : int):
        return self.SetRitOffset(value)
    @property
    def Vfo(self) -> RigParameter:
        return self._vfo
    @Vfo.setter
    def Vfo(self, value : RigParameter):
        return self.SetVfo(value)
    @property
    def Split(self) -> RigParameter:
        return self.GetSplit()
    @Split.setter
    def Split(self, value : RigParameter):
        return self.SetSplit(value)
    @property
    def Rit(self) -> RigParameter:
        return self._rit
    @Rit.setter
    def Rit(self, value : RigParameter):
        return self.SetRit(value)
    @property
    def Xit(self) -> RigParameter:
        return self._xit
    @Xit.setter
    def Xit(self, value : RigParameter):
        return self.SetXit(value)
    @property
    def Tx(self) -> RigParameter:
        return self._tx
    @Tx.setter
    def Tx(self, value : RigParameter):
        return self.SetTx(value)
    @property
    def Mode(self) -> RigParameter:
        return self._mode
    @Mode.setter
    def Mode(self, value : RigParameter):
        return self.SetMode(value)

    def DisplayMessage(self, messageMode, message : str):
        if self.MessageDisplayModes.HasFlag(messageMode):
            print(message)

    def GetStatus(self) -> RigControlStatus:
        if (self._rigControlType == RigControlType.Guest):
            return self.RigControlStatus.OnLine
        if (not self.Enabled):
            return self.RigControlStatus.Disabled
        if (not self.IsConnected()):
            return self.RigControlStatus.PortBusy
        if (not self._online):
            return self.RigControlStatus.NotResponding
        return self.RigControlStatus.OnLine

    def IsConnected(self) -> bool:
        return False

    def SetFreq(self, value : int):
        self._freq = value

    def SetFreqA(self, value : int):
        self._freqA = value

    def SetFreqB(self, value : int):
        self._freqB = value

    def SetRitOffset(self, value : int):
        self._ritOffset = value

    def SetPitch(self, value : int):
        self._pitch = value

    def SetVfo(self, value : RigParameter):
        self._vfo = value

    def SetSplit(self, value : RigParameter):
        self._split = value

    def SetRit(self, value : RigParameter):
        self._rit = value

    def SetXit(self, value : RigParameter):
        self._xit = value

    def SetTx(self, value : RigParameter):
        self._tx = value

    def SetMode(self, value : RigParameter):
        self._mode = value

    def GetSplit(self) -> RigParameter:
        if (self._split != RigParameter.none):
            return self._split
        if [RigParameter.VfoAA, RigParameter.VfoBB].Contains(self.Vfo):
            self._split = RigParameter.SplitOff
        elif [RigParameter.VfoAB, RigParameter.VfoBA].Contains(self.Vfo):
            self._split = RigParameter.SplitOn
        return self._split

