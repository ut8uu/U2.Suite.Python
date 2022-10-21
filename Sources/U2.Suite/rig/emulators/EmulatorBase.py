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

import os, pty, threading
from contracts.KnownIdentifiers import KnownIdentifiers
from contracts.RigCommand import RigCommand
from contracts.RigCommands import RigCommands
from contracts.RigParameter import RigParameter
from exceptions.ParameterNotSupported import ParameterNotSupported
from helpers.ConversionHelper import ConversionHelper
from helpers.RigHelper import RigHelper
from helpers.FileSystemHelper import FileSystemHelper
from rig.CustomRig import CustomRig
from serial import Serial
from typing import Tuple
from rig.enums.MessageDisplayModes import MessageDisplayModes

from rig.enums.RigControlType import RigControlType

class EmulatorBase():
    _prefix = b''
    _started = False
    _ini_file_name = ''
    _thread : threading.Thread
    _serial_port_name = ''
    _commands : RigCommands
    _rig : CustomRig
    _lock : threading.Lock

    def __init__(self, ini_file_name, prefix) -> None:
        self._lock = threading.Lock()
        self._started = False
        self._ini_file_name = ini_file_name
        self._prefix = prefix
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), self._ini_file_name)
        self._commands = RigHelper.loadRigCommands(path)
        self.init_rig()

    @property
    def SerialPortName(self) -> str:
        return self._serial_port_name

    def init_rig(self):
        self._rig = CustomRig(RigControlType.emulator, 1, KnownIdentifiers.U2RigEmulator)
        self._rig.Enabled = True
        self._rig.FreqA = 14150400
        self._rig.FreqB = 432800000
        self._rig.Mode = RigParameter.ssb_u
        self._rig.Tx = RigParameter.rx
        self._rig.Pitch = 0
        self._rig.Split = RigParameter.splitoff
        self._rig.Vfo = RigParameter.vfoaa # no split

    def try_prepare_response(self, command : RigCommand) -> bytearray:
        response = command.Validation.Flags

        rig = self._rig
        match command.Values[0].Param:
            case RigParameter.freq:
                return self.try_inject_value(command, rig.Freq)
            case RigParameter.freqa:
                return self.try_inject_value(command, rig.FreqA)
            case RigParameter.freqb:
                return self.try_inject_value(command, rig.FreqB)
            case RigParameter.pitch:
                return self.try_inject_value(command, rig.Pitch)
            case RigParameter.ritoffset:
                return self.try_inject_value(command, rig.RitOffset)

        all_parameters = { rig.Mode, rig.Vfo, rig.Rit, rig.Xit, rig.Tx, rig.Split }

        for parameter in all_parameters:
            if parameter == RigParameter.none:
                continue

            for mode_flag in command.Flags:
                if mode_flag.Param == parameter:
                    return ConversionHelper.BytesOr(command.Validation.Flags, mode_flag)

        raise ParameterNotSupported(f"Parameter {command.Value.Param} not supported.");

    def try_inject_value(self, command: RigCommand, value: int) -> bytearray:
        response = command.Validation.Flags

        info = command.Values[0]
        bytes = ConversionHelper.FormatValue(value, info)
        if (len(bytes) == 0):
            return False

        assert len(bytes) == info.Len
        for i in range(0, info.Len):
            response[info.Start + i] = bytes[i]
        # end for
        return response

    def start(self):
        if self._started:
            return

        self._started = True
        self.start_listener()

    def stop(self):
        if not self._started:
            return
        self._started = False
        self._thread.join(1)

    def start_listener(self):
        self._master_port,slave = pty.openpty() #open the pseudoterminal
        self._serial_port_name = os.ttyname(slave) #translate the slave fd to a filename

        #create a separate thread that listens on the master device for commands
        self._thread = threading.Thread(target=self.EmulatorListener, args=[self._master_port])
        self._thread.start()

    def parse_rig_command(self, command : bytearray) -> Tuple[bool, RigCommand]:
        if len(command) < 3:
            return (False, None, 'none')

        cmd_len = len(command)

        for init_cmd in self._commands.InitCmd:
            if cmd_len != len(init_cmd.Code):
                continue
            if bytes(init_cmd.Code) == command:
                with self._lock:
                    print(f'Found init command: {ConversionHelper.BytesToHexStr(command)}')
                return (True, init_cmd, 'init')

        for status_cmd in self._commands.StatusCmd:
            if cmd_len != len(status_cmd.Code):
                continue
            if bytes(status_cmd.Code) == command:
                with self._lock:
                    print(f'Found status command: {ConversionHelper.BytesToHexStr(command)}')
                return (True, status_cmd, 'status')

        for write_cmd_id in self._commands.WriteCmd:
            write_cmd = self._commands.WriteCmd[write_cmd_id]
            if cmd_len != len(write_cmd.Code):
                continue
            command_empty = bytearray(command)
            v = write_cmd.Value
            for index in range(0, v.Len):
                command_empty[v.Start + index] = 0x00
            if bytes(write_cmd.Code) == command_empty:
                with self._lock:
                    print(f'Found write command: {ConversionHelper.BytesToHexStr(command)}')
                return (True, write_cmd, 'write')

        return (False, None, 'unknown')

    def EmulatorListener(self, port):
        #continuously listen to commands on the master device
        while True:
            res = b''
            try:
                while True:
                    if not self._started:
                        print('Exiting the thread')
                        return
                    chars = os.read(port, 1)
                    if len(chars) == 0:
                        continue
                    res += chars
                    if res == self._prefix:
                        continue
                    if res.endswith(self._prefix):
                        if len(res) > 2:
                            print('command reset')
                        res = self._prefix
                        continue
                    (rig_command_parsed, rig_command, rig_command_type) = self.parse_rig_command(res)
                    if rig_command_parsed:
                        break
                #print("command: %s" % res.removeprefix(self._prefix))

                if rig_command_parsed:
                    if rig_command.ReplyLength > 0:
                        match rig_command_type:
                            case 'init':
                                os.write(port, rig_command.Validation.Flags)
                            case 'status':
                                response = self.try_prepare_response(rig_command)
                                if response != None:
                                    os.write(port, response)
                            case 'write':
                                v = rig_command.Value
                                value = ConversionHelper.UnformatValue(bytearray(res), rig_command.Value)
                                self.SetValue(v.Param, value)
                                formatted_value = ConversionHelper.FormatValue(value, v)
                                response = bytearray(rig_command.Validation.Flags)
                                for index in range(0, v.Len):
                                    response[v.Start + index] = formatted_value[index]
                                os.write(port, response)
            except Exception as ex:
                continue

    def SetValue(self, param: RigParameter, value: int):
        match param:
            case RigParameter.freqa:
                self._rig.FreqA = value
            case RigParameter.freqb:
                self._rig.FreqB = value
            case RigParameter.freq:
                self._rig.Freq = value
            case RigParameter.pitch:
                self._rig.Pitch = value
        
        if RigHelper.CollectionContainsValue(RigHelper.ModeParams, param):
            self._rig.Mode = param
        elif RigHelper.CollectionContainsValue(RigHelper.SplitParams, param):
            self._rig.Split = param
        elif RigHelper.CollectionContainsValue(RigHelper.RitOnParams, param):
            self._rig.Rit = param
        elif RigHelper.CollectionContainsValue(RigHelper.XitOnParams, param):
            self._rig.Xit = param
        elif RigHelper.CollectionContainsValue(RigHelper.TxParams, param):
            self._rig.Tx = param
        elif RigHelper.CollectionContainsValue(RigHelper.VfoParams, param):
            self._rig.Vfo = param

    def read_from_serial(self, ser : Serial, count: int) -> bytes:
        res = b''
        while len(res) < count:
            #read the response
            res += ser.read()
        print("result: %s" % res.strip())
        return res

    def send_receive_command(self, ser: Serial, command : RigCommand) -> bytes:
        return self.send_receive(ser, command.Code, command.ReplyLength)

    def send_receive(self, ser : Serial, data: bytes, count: int) -> bytes:
        if not data.startswith(self._prefix):
            ser.write(self._prefix)
        ser.write(data)
        return self.read_from_serial(ser, count)

    def test_self(self):
        #an emulator is expected to be started by the moment 

        #open a pySerial connection to the slave
        ser = Serial(self._serial_port_name, 2400, timeout=1)

        #self.send_receive(ser, b'cmd1', 5)
        #self.send_receive(ser, b'cmd2', 5)

        #for cmd in self._commands.InitCmd:
        #    self.send_receive(ser, cmd)

        freqa_command = self.get_status_command(RigParameter.freqa)
        assert freqa_command != None
        response = self.send_receive_command(ser, freqa_command)
        #assert freq_a == self._rig.FreqA

        ser.close()

    def get_status_command(self, command_parameter : RigParameter) -> RigCommand:
        for command in self._commands.StatusCmd:
            if command.Value != None and command.Value.Param == command_parameter:
                return command
            for value in command.Values:
                if value.Param == command_parameter:
                    return command

if __name__=='__main__':
    x = EmulatorBase('IC-705.ini', b'\xfe\xfe')
    x.start()
    x.test_self()
    x.stop()