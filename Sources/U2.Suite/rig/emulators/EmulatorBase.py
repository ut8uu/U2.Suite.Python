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
    __prefix = b''
    __started = False
    __ini_file_name = ''
    __thread : threading.Thread
    __serial_port_name = ''
    _commands : RigCommands
    __rig : CustomRig

    def __init__(self, ini_file_name, prefix) -> None:
        self.__ini_file_name = ini_file_name
        self.__prefix = prefix
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), self.__ini_file_name)
        self._commands = RigHelper.loadRigCommands(path)
        self.init_rig()

    @property
    def SerialPortName(self) -> int:
        return self.__serial_port_name

    def init_rig(self):
        self.__rig = CustomRig(RigControlType.emulator, 1, KnownIdentifiers.U2RigEmulator)
        self.__rig.Enabled = True
        self.__rig.FreqA = 14150400
        self.__rig.FreqB = 432800000
        self.__rig.Mode = RigParameter.ssb_u
        self.__rig.Tx = RigParameter.rx
        self.__rig.Pitch = 0
        self.__rig.Split = RigParameter.splitoff
        self.__rig.Vfo = RigParameter.vfoaa # no split

    def try_prepare_response(self, command : RigCommand) -> bytearray:
        response = command.Validation.Flags

        rig = self.__rig
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
        if self.__started:
            return

        self.start_listener()
        self.__started = True

    def stop(self):
        if not self.__started:
            return
        self.__started = False
        self.__thread.join(1)

    def start_listener(self):
        """Start the testing"""
        master,slave = pty.openpty() #open the pseudoterminal
        self.__serial_port_name = os.ttyname(slave) #translate the slave fd to a filename

        #create a separate thread that listens on the master device for commands
        self.__thread = threading.Thread(target=self.listener, args=[master])
        self.__thread.start()

    def parse_custom_command(self, command : bytearray) -> Tuple[bool, str]:
        cmd = command.removeprefix(self.__prefix)
        if len(cmd) == 0:
            return False

        init0 = self._commands.InitCmd[0]

        #custom commands
        match cmd:
            case b'cmd1':
                return (True, cmd)
            case b'cmd2':
                return (True, cmd)
            case b'exit':
                return (True, cmd)

        return (False, b'')

    def parse_rig_command(self, command : bytearray) -> Tuple[bool, RigCommand]:
        if len(command) < 3:
            return (False, None, 'none')

        for init_cmd in self._commands.InitCmd:
            if bytes(init_cmd.Code) == command:
                return (True, init_cmd, 'init')

        for status_cmd in self._commands.StatusCmd:
            if bytes(status_cmd.Code) == command:
                return (True, status_cmd, 'status')

        for write_cmd_id in self._commands.WriteCmd:
            write_cmd = self._commands.WriteCmd[write_cmd_id]
            if bytes(write_cmd.Code) == command:
                return (True, write_cmd, 'write')

        return (False, None, 'unknown')

    def listener(self, port):
        #continuously listen to commands on the master device
        while True:
            res = b''
            try:
                while True:
                    res += os.read(port, 1)
                    if res == self.__prefix:
                        continue
                    if res.endswith(self.__prefix):
                        if len(res) > 2:
                            print('command reset')
                        res = self.__prefix
                        continue
                    (parsed, command) = self.parse_custom_command(res)
                    if parsed:
                        break
                    (rig_command_parsed, rig_command, rig_command_type) = self.parse_rig_command(res)
                    if rig_command_parsed:
                        break
                print("command: %s" % res.removeprefix(self.__prefix))

                if parsed:
                    match command:
                        case b'cmd1':
                            os.write(port, b'resp1')
                        case b'cmd2':
                            os.write(port, b'resp2')
                        case b'exit':
                            os.write(port, b'exiting')
                            break
                        case _:
                            os.write(port, b"I dont understand\r\n")

                elif rig_command_parsed:
                    if rig_command.ReplyLength > 0:
                        match rig_command_type:
                            case 'init':
                                os.write(port, rig_command.Validation.Flags)
                            case 'status':
                                response = self.try_prepare_response(rig_command)
                                if response != None:
                                    os.write(port, response)
                            case 'write':
                                raise NotImplementedError()
            except:
                continue

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
        if not data.startswith(self.__prefix):
            ser.write(self.__prefix)
        ser.write(data)
        return self.read_from_serial(ser, count)

    def test_self(self):
        #an emulator is expected to be started by the moment 

        #open a pySerial connection to the slave
        ser = Serial(self.__serial_port_name, 2400, timeout=1)

        #self.send_receive(ser, b'cmd1', 5)
        #self.send_receive(ser, b'cmd2', 5)

        #for cmd in self._commands.InitCmd:
        #    self.send_receive(ser, cmd)

        freqa_command = self.get_status_command(RigParameter.freqa)
        assert freqa_command != None
        response = self.send_receive_command(ser, freqa_command)
        assert freq_a == self.__rig.FreqA

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