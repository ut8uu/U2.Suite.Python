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

import logging
from contracts.BitMask import BitMask
from contracts.RigCommands import RigCommands
from contracts.RigParameter import RigParameter
from contracts.RigSettings import RigSettings
from exceptions.ArgumentOutOfRangeException import ArgumentOutOfRangeException
from exceptions.ValueValidationException import ValueValidationException
from helpers.ConversionHelper import ConversionHelper
from helpers.RigHelper import RigHelper
from rig.enums.MessageDisplayModes import MessageDisplayModes
from rig.enums.RigControlType import RigControlType
from rig.Rig import Rig
from typing import List, Tuple

class HostRig(Rig):
    __application_id: int
    __rig_commands: RigCommands
    __rig_number: int
    __rig_settings: RigSettings
    __changed_params : List[RigParameter]

    def __init__(self, rig_number:int, application_id:int, 
                 rig_settings:RigSettings, rig_commands:RigCommands):
        __rig_number = rig_number
        __application_id = application_id
        __rig_settings = rig_settings
        __rig_commands = rig_commands
        super().__init__(RigControlType.host, rig_number, application_id)
        
    def ValidateReply(self, inputData : bytes, mask : BitMask):
        if len(inputData) != len(mask.Flags):
            raise ValueValidationException(f"Incorrect input data length. Expected {len(mask.Flags)}, actual {len(inputData)}.")

        data = ConversionHelper.BytesAnd(inputData, mask.Mask)
        if data == mask.Flags:
            return

        expectedString = ConversionHelper.BytesToHexStr(mask.Flags)
        actualString = ConversionHelper.BytesToHexStr(inputData)
        raise ValueValidationException(f"Invalid input data. Expected {expectedString}, actual {actualString}.")

    def ProcessStatusReply(self, statusCommandIndex : int, data : bytes) -> Tuple[bool, int]:
        #validate reply
        cmd = self.__rig_commands.StatusCmd[statusCommandIndex];

        reply = ConversionHelper.BytesToHexStr(data)
        self.DisplayMessage(MessageDisplayModes.Diagnostics3,
            f"Processing the Status ({cmd.Value.Param}) reply: {reply}")

        self.ValidateReply(data, cmd.Validation);

        #extract numeric values
        for index in range(0, len(cmd.Values)):
            try:
                value = ConversionHelper.UnformatValue(data, cmd.Values[index]);
                self.StoreParam(cmd.Values[index].Param, value);
            except (Exception) as ex:
                logging.Error(ex.Message);

        #extract bit flags
        for index in range(0, len(cmd.Flags)):
            if len(data) != len(cmd.Flags[index].Mask) or \
                len(data) != len(cmd.Flags[index].Flags):
                self.DisplayMessage(MessageDisplayModes.Error, f"RIG{self._rig_number}: incorrect reply length")
            elif cmd.Flags[index].Flags == ConversionHelper.BytesAnd(data, cmd.Flags[index].Mask):
                parameter = cmd.Flags[index].Param
                if self.StoreParam(parameter):
                    self.DisplayMessage(MessageDisplayModes.Diagnostics2, 
                        f"Found changed parameter: {parameter}")
                    self.__changed_params.append(parameter);

        self.ReportChangedParameters(self.__changed_params)
        self.__changed_params.clear()

        #tell clients
        #if len(self.__changed_params) > 0:
        #    packet = UdpPacketFactory.CreateMultipleParametersReportingPacket(RigNumber,
        #        senderId: ApplicationId, receiverId: KnownIdentifiers.MultiCast, _changedParams);
        #    UdpMessenger.SendMultiCastMessage(packet);
        #    logging.debug(f"Multiple parameters changed. A multicast message sent: {ConversionHelper.BytesToHexStr(packet.GetBytes())}");
        
        return True

    def StoreParam(self, parameter):
        if RigHelper.VfoParams.Contains(parameter):
            if (Vfo == parameter):
                return False
            Vfo = parameter
        elif RigHelper.SplitParams.Contains(parameter):
            if (Split == parameter):
                return False
            Split = parameter
        elif RigHelper.RitOnParams.Contains(parameter):
            if (Rit == parameter):
                return False
            Rit = parameter
        elif RigHelper.XitOnParams.Contains(parameter):
            if (Xit == parameter):
                return False
            Xit = parameter
            return False
        elif RigHelper.TxParams.Contains(parameter):
            if (Tx == parameter):
                return False
            Tx = parameter
        elif RigHelper.ModeParams.Contains(parameter):
            if (Mode == parameter):
                return False
            Mode = parameter
        else:
            return False
        self.ReportChangedParameters([parameter])
        if (RigHelper.ModeParams.Contains(parameter) and (parameter != LastWrittenMode)):
            LastWrittenMode = RigParameter.none
        logging.debug(f"RIG{self._rig_number} status changed: {parameter} enabled")
        return True

    def StoreParam(self, parameter : RigParameter, parameter_value : int):
        changed = False
        if parameter == RigParameter.freqa and self.FreqA != parameter_value:
            self.FreqA = parameter_value
            changed = True
        elif parameter == RigParameter.freqb:
            self.FreqB = parameter_value
            changed = True
        elif parameter == RigParameter.freq:
            self.Freq = parameter_value
            changed = True
        elif parameter == RigParameter.pitch:
            self.Pitch = parameter_value
            changed = True
        elif parameter == RigParameter.ritoffset:
            self.RitOffset = parameter_value
            changed = True
        else:
            raise ArgumentOutOfRangeException(f"Parameter {parameter} not supported.")

        if changed:
            self.__changed_params.append(parameter)
            #DisplayMessage(MessageDisplayModes.Debug, "RIG{} status changed: {} = {}".format(RigNumber, parameter.ToString(), Convert.ToString(parameterValue)))
            #packet = UdpPacketFactory.CreateSingleParameterReportingPacket(RigNumber, senderId = ApplicationId, receiverId = KnownIdentifiers.MultiCast, parameter, parameterValue)
            #UdpMessenger.SendMultiCastMessage(packet)

    def ReportChangedParameters(self, parameters):
        for parameter in parameters:
            if parameter == RigParameter.FreqA:
                parameterValue = self.FreqA
            elif parameter == RigParameter.none:
                parameterValue = 0
            elif parameter == RigParameter.Freq:
                parameterValue = self.Freq
            elif parameter == RigParameter.FreqB:
                parameterValue = self.FreqB
            elif parameter == RigParameter.Pitch:
                parameterValue = self.Pitch
            elif parameter == RigParameter.RitOffset:
                parameterValue = self.RitOffset
            elif parameter == RigParameter.Rit0:
                parameterValue = self.Rit
            elif parameter == RigParameter.VfoAA \
                or parameter == RigParameter.VfoAB \
                or parameter == RigParameter.VfoBA \
                or parameter == RigParameter.VfoBB \
                or parameter == RigParameter.VfoA \
                or parameter == RigParameter.VfoB \
                or parameter == RigParameter.VfoEqual \
                or parameter == RigParameter.VfoSwap:
                parameterValue = 0
            elif parameter == RigParameter.spliton:
                parameterValue = 1
            elif parameter == RigParameter.splitoff:
                parameterValue = 0
            elif parameter == RigParameter.riton:
                parameterValue = 1
            elif parameter == RigParameter.ritoff:
                parameterValue = 0
            elif parameter == RigParameter.xiton:
                parameterValue = 1
            elif parameter == RigParameter.xitoff:
                parameterValue = 0
            elif parameter == RigParameter.rx:
                parameterValue = "RX"
            elif parameter == RigParameter.tx:
                parameterValue = "TX"
            elif parameter == RigParameter.cw_u or parameter == RigParameter.cw_l:
                parameterValue = "CW"
            elif parameter == RigParameter.ssb_u:
                parameterValue = "USB"
            elif parameter == RigParameter.ssb_l:
                parameterValue = "LSB"
            elif parameter == RigParameter.dig_u:
                parameterValue = "DIGI-U"
            elif parameter == RigParameter.dig_l:
                parameterValue = "DIGI-L"
            elif parameter == RigParameter.am:
                parameterValue = "AM"
            elif parameter == RigParameter.fm:
                parameterValue = "FM"
            else:
                parameterValue = 0
            #OnRigParameterChanged(RigNumber, parameter, parameterValue)
