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
import sched
import threading
import time
from contracts.BitMask import BitMask
from contracts.CommandQueue import CommandQueue
from contracts.RigCommand import RigCommand
from contracts.RigCommands import RigCommands
from contracts.RigParameter import RigParameter
from contracts.RigSettings import RigSettings
from contracts.QueueItem import QueueItem
from contracts.ValueFormat import ValueFormat
from exceptions.ArgumentException import ArgumentException
from exceptions.ArgumentOutOfRangeException import ArgumentOutOfRangeException
from exceptions.TimeoutException import TimeoutException
from exceptions.ValueValidationException import ValueValidationException
from helpers.ConversionHelper import ConversionHelper
from helpers.DebugHelper import DebugHelper
from helpers.RigHelper import RigHelper
from rig.RigSerialPort import RigSerialPort
from rig.enums.CommandKind import CommandKind
from rig.enums.ExchangePhase import ExchangePhase
from rig.enums.MessageDisplayModes import MessageDisplayModes
from rig.enums.RigControlType import RigControlType
from rig.events.OnRigParameterChangedEvent import OnRigParameterChangedEvent
from rig.Rig import Rig
from typing import List, Tuple

from rig.events.SerialPortMessageReceivedEvent import SerialPortMessageReceivedEvent

class HostRig(Rig):

    _rig_commands : RigCommands
    _rig_settings : RigSettings
    _serial_port : RigSerialPort
    _queue : CommandQueue = CommandQueue()
    _poll_scheduler : sched.scheduler
    _changed_params : List[RigParameter]

    def __init__(self, rig_number:int, application_id:int, 
                 rig_settings:RigSettings, rig_commands:RigCommands):
        self._rig_number = rig_number
        self._application_id = application_id
        self._rig_settings = rig_settings
        self._rig_commands = rig_commands
        self._changed_params = []
        self.OnRigParameterChanged = OnRigParameterChangedEvent()
        super(Rig, self).__init__(RigControlType.host, rig_number, application_id)
        self._serial_port = RigSerialPort(rig_settings)
        self._serial_port.Connect()

        self._poll_scheduler = sched.scheduler(time.monotonic, time.sleep)

        self._poll_scheduler.enter(self._rig_settings.PollMs / 1000, 1, self.PollQueue, argument=(self._poll_scheduler,))
        self._poll_scheduler.run(False)
        
    def PollQueue(self, scheduler): 
        print("Polling the RIG...")

        if not self._queue.HasStatusCommands:
            self.AddCommands(self._rig_commands.StatusCmd, CommandKind.Status)
        self.CheckQueue()

        scheduler.enter(self._rig_settings.PollMs / 1000, 1, self.PollQueue, argument=(scheduler,))

    def AddCommands(self, commands : List[RigCommand], kind : CommandKind) -> None:
        index = 0
        for command in commands:
            item = QueueItem()
            item.Code = command.Code
            item.Number = index
            item.ReplyLength = command.ReplyLength
            item.ReplyEnd = ConversionHelper.BytesToHexStr(command.ReplyEnd)
            item.Kind = kind
            self.AddCommand(item)
            index += 1

    def AddCommand(self, item : QueueItem) -> None:
        self._queue.Add(item)

    def ValidateReply(self, inputData : bytes, mask : BitMask):
        if len(inputData) != len(mask.Flags):
            raise ValueValidationException(f"Incorrect input data length. Expected {len(mask.Flags)}, actual {len(inputData)}.")

        data = ConversionHelper.BytesAnd(inputData, mask.Mask)
        if data == mask.Flags:
            return

        expectedString = ConversionHelper.BytesToHexStr(mask.Flags)
        actualString = ConversionHelper.BytesToHexStr(inputData)
        raise ValueValidationException(f"Invalid input data. Expected {expectedString}, actual {actualString}.")

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
        pname = parameter.name
        if parameter == RigParameter.freqa:
            if self.FreqA != parameter_value:
                self._freqA = parameter_value
                changed = True
        if pname == RigParameter.freqa.name:
            if self.FreqA != parameter_value:
                self._freqA = parameter_value
                changed = True
        elif pname == RigParameter.freqb.name:
            if self.FreqB != parameter_value:
                self.FreqB = parameter_value
                changed = True
        elif pname == RigParameter.freq.name:
            if self.Freq != parameter_value:
                self.Freq = parameter_value
                changed = True
        elif pname == RigParameter.pitch.name:
            if self.FreqA != parameter_value:
                self.Pitch = parameter_value
                changed = True
        elif pname == RigParameter.ritoffset.name:
            if self.RitOffset != parameter_value:
                self.RitOffset = parameter_value
                changed = True
        else:
            raise ArgumentOutOfRangeException(f"Parameter {parameter.name} not supported.")

        if changed:
            self._changed_params.append(parameter)
            DebugHelper.DisplayMessage(MessageDisplayModes.Debug, 
                "RIG{} status changed: {} = {}".format(self._rig_number, parameter.name, parameter_value))
            #packet = UdpPacketFactory.CreateSingleParameterReportingPacket(RigNumber, senderId = ApplicationId, receiverId = KnownIdentifiers.MultiCast, parameter, parameterValue)
            #UdpMessenger.SendMultiCastMessage(packet)

    def ReportChangedParameters(self, parameters : List[RigParameter]):
        for parameter in parameters:
            if parameter == RigParameter.freqa:
                parameterValue = self.FreqA
            elif parameter == RigParameter.none:
                parameterValue = 0
            elif parameter == RigParameter.freq:
                parameterValue = self.Freq
            elif parameter == RigParameter.freqb:
                parameterValue = self.FreqB
            elif parameter == RigParameter.pitch:
                parameterValue = self.Pitch
            elif parameter == RigParameter.ritoffset:
                parameterValue = self.RitOffset
            elif parameter == RigParameter.rit0:
                parameterValue = self.Rit
            elif parameter == RigParameter.vfoaa \
                or parameter == RigParameter.vfoab \
                or parameter == RigParameter.vfoba \
                or parameter == RigParameter.vfobb \
                or parameter == RigParameter.vfoa \
                or parameter == RigParameter.vfob \
                or parameter == RigParameter.vfoequal \
                or parameter == RigParameter.vfoswap:
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
            self.OnRigParameterChanged(self._rig_number, parameter, parameterValue)

    def SetFreq(self, value):
        if not self.Enabled or self.Freq == value:
            return
        super(HostRig, self).SetFreq(value)
        self.AddWriteCommand(RigParameter.freq, value)

    def SetFreqA(self, value):
        if not self.Enabled or value == self.FreqA:
            return
        super(HostRig, self).SetFreqA(value)
        self.AddWriteCommand(RigParameter.freqa, value)

    def SetFreqB(self, value):
        if not self.Enabled or value == self.FreqB:
            return
        super(HostRig, self).SetFreqB(value)
        self.AddWriteCommand(RigParameter.freqb, value)

    def SetPitch(self, value):
        if not self.Enabled or self.Pitch == value:
            return
        if not RigHelper.CollectionContainsValue(self._rig_commands.ReadableParams, RigParameter.Pitch):
            super(HostRig, self).SetPitch(value)
        self.AddWriteCommand(RigParameter.pitch, value)

    def SetRitOffset(self, value):
        if not self.Enabled or self.RitOffset == value:
            return
        super(HostRig, self).SetRitOffset(value)
        self.AddWriteCommand(RigParameter.ritoffset, value)

    def SetVfo(self, value):
        if not self.Enabled \
            or self.Vfo == value \
            or not RigHelper.CollectionContainsValue(RigHelper.VfoParams, value):
            return
        super(HostRig, self).SetVfo(value)
        self.AddWriteCommand(value)

    def SetRit(self, value):
        if not self.Enabled or value == self.Rit \
            or not RigHelper.CollectionContainsValue(RigHelper.RitOnParams, value):
            return
        super(HostRig, self).SetRit(value)
        self.AddWriteCommand(value)

    def SetXit(self, value):
        if not self.Enabled \
            or not RigHelper.CollectionContainsValue(RigHelper.XitOnParams, value) \
            or (value == self.Xit):
            return
        super(HostRig, self).SetXit(value)
        self.AddWriteCommand(value)

    def SetTx(self, value):
        if not self.Enabled \
            or not RigHelper.CollectionContainsValue(RigHelper.TxParams, value):
            return
        super(HostRig, self).SetTx(value)
        self.AddWriteCommand(value)

    def SetMode(self, value):
        if not self.Enabled \
            or not RigHelper.CollectionContainsValue(RigHelper.ModeParams, value):
            return
        super(HostRig, self).SetMode(value)
        self.AddWriteCommand(value)

    def SetSplit(self, value):
        if not self.Enabled \
            and not RigHelper.CollectionContainsValue(RigHelper.SplitParams, value):
            return
        if RigHelper.CollectionContainsValue(self._rig_commands.WriteableParams, value) \
            and (value != self.Split):
            self.AddWriteCommand(value)
        elif (value == RigParameter.spliton):
            if self.Vfo == RigParameter.vfoaa:
                self.SetVfo(RigParameter.vfoab)
            elif self.Vfo == RigParameter.vfobb:
                self.SetVfo(RigParameter.vfoba)
            else:
                # consider unknown value as vfoaa
                self.SetVfo(RigParameter.vfoab)
        else:
            if self.Vfo == RigParameter.vfoab:
                self.SetVfo(RigParameter.vfoaa)
            elif self.Vfo == RigParameter.vfoba:
                self.SetVfo(RigParameter.vfobb)
            else:
                # consider unknown value as vfoaa
                self.SetVfo(RigParameter.vfoaa)
        super(HostRig, self).SetSplit(value)

    def AddWriteCommand(self, param : RigParameter, value : int = 0):
        if (self._rig_commands == None):
            return

        cmd_id = next((c for c in self._rig_commands.WriteCmd if c == param.value), None)
        if cmd_id == None:
            raise ArgumentException(f"A parameter {param} does not support writing to the RIG.")

        cmd = self._rig_commands.WriteCmd[param.value]
        if (cmd.Code == None):
            logging.Error(f"RIG{self._rig_number} Write command not supported for {param}")
            return

        newCode = cmd.Code.copy()
        if cmd.Value.Format != ValueFormat.none:
            try:
                fmtValue = ConversionHelper.FormatValue(value, cmd.Value)
                if (cmd.Value.Start + cmd.Value.Len) > len(newCode):
                    raise ValueValidationException("Value {} too long".format(ConversionHelper.BytesToHexStr(cmd.Code)))
                for index in range(0, cmd.Value.Len):
                    newCode[cmd.Value.Start + index] = fmtValue[index]
            except Exception as e:
                logging.Error("RIG{0}: Generating command: {1}", self._rig_number, e.args[0])
        
        queueItem = QueueItem()
        queueItem.Code = newCode
        queueItem.Param = param
        queueItem.Kind = CommandKind.Write
        queueItem.ReplyLength = cmd.ReplyLength
        queueItem.ReplyEnd = ConversionHelper.BytesToHexStr(cmd.ReplyEnd)
        self._queue.AddBeforeStatusCommands(queueItem)
        self.CheckQueue()

    def CheckQueue(self):
        if self._queue.IsEmpty:
            return

        if not self.Enabled \
            or not self._serial_port.IsConnected \
            or self._queue.Phase != ExchangePhase.Idle \
            or self._queue.IsEmpty:
            return

        while self._queue.CurrentCmd != None:
            response = []
            try:
                cmd = self._queue.CurrentCmd
                if cmd.NeedsReply:
                    response = self._serial_port.SendMessageAndReadBytes(cmd.Code, cmd.ReplyLength)
                    if len(response) == cmd.ReplyLength:
                        self.OnSerialPortMessageReceived(response)
                else:
                    self._serial_port.SendMessage(cmd.Code)
            except TimeoutException as ex:
                logging.error(ex.args[0])
            except Exception as ex:
                logging.error(ex.args[0])

            # a command is sent and response is received (if any)
            self._queue.remove(self._queue.CurrentCmd)

    def ProcessReceivedData(self, cmd: QueueItem, data: bytes) -> None:
        '''Processes a reply for the given command'''
        if not cmd.NeedsReply or cmd.ReplyLength != len(data):
            return
        if cmd.Kind == CommandKind.Init:
            self.ProcessInitReply(cmd, data)
        elif cmd.Kind == CommandKind.Status:
            self.ProcessStatusReply(cmd.Number, data)
        elif cmd.Kind == CommandKind.Write:
            self.ProcessWriteReply(cmd, data)
        elif cmd.Kind == CommandKind.Custom:
            self.ProcessCustomReply(cmd, data)

    def ProcessInitReply(self, cmd: QueueItem, data: bytes):
        '''Processes a reply for the Init command'''
        DebugHelper.DisplayMessage(MessageDisplayModes.Diagnostics3, f'Processing the Init command: {ConversionHelper.BytesToHexStr(data)}')
        self.ValidateReply(data, self._rig_commands.InitCmd[cmd.Number].Validation)

    def ProcessWriteReply(self, cmd: QueueItem, data: bytes):
        '''Processes a reply for the Write command'''
        DebugHelper.DisplayMessage(MessageDisplayModes.Diagnostics3, f'Processing the Write command: {ConversionHelper.BytesToHexStr(data)}')
        self.ValidateReply(data, self._rig_commands.WriteCmd[cmd.Number].Validation)

    def ProcessStatusReply(self, statusCommandIndex : int, data : bytes) -> Tuple[bool, int]:
        #validate reply
        cmd = self._rig_commands.StatusCmd[statusCommandIndex]

        #reply = ConversionHelper.BytesToHexStr(data)
        #self.DisplayMessage(MessageDisplayModes.Diagnostics3,
        #    f"Processing the Status ({cmd.Value.Param}) reply: {reply}")

        RigHelper.validate_reply(data, cmd.Validation)

        #extract numeric values
        for index in range(0, len(cmd.Values)):
            try:
                value = ConversionHelper.UnformatValue(data, cmd.Values[index]);
                self.StoreParam(cmd.Values[index].Param, value);
            except (Exception) as ex:
                logging.Error(ex.args[0]);

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
                    self._changed_params.append(parameter);

        self.ReportChangedParameters(self._changed_params)
        self._changed_params.clear()

        #tell clients
        #if len(self._changed_params) > 0:
        #    packet = UdpPacketFactory.CreateMultipleParametersReportingPacket(RigNumber,
        #        senderId: ApplicationId, receiverId: KnownIdentifiers.MultiCast, _changedParams);
        #    UdpMessenger.SendMultiCastMessage(packet);
        #    logging.debug(f"Multiple parameters changed. A multicast message sent: {ConversionHelper.BytesToHexStr(packet.GetBytes())}");
        
        return True

    def OnSerialPortMessageReceived(self, data: bytes):
        """A handler for the MessageReceived"""
        if len(data) == 0:
            return

        if len(self._queue) == 0:
            return
            
        if not self._queue.CurrentCmd.NeedsReply:
            return

        if self._queue.CurrentCmd.ReplyLength != len(data):
            DebugHelper.DisplayMessage(MessageDisplayModes.Error, f'Serial port message length mismatch. Expected {self._queue.CurrentCmd.ReplyLength} bytes, received {len(data)} bytes.')
            return

        self.ProcessReceivedData(self._queue.CurrentCmd, data)

