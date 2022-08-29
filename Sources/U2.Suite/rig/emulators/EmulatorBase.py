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
from contracts.RigCommand import RigCommand
from contracts.RigCommands import RigCommands
from helpers.RigHelper import RigHelper
from helpers.FileSystemHelper import FileSystemHelper
from serial import Serial
from typing import Tuple

class EmulatorBase():
    __prefix = b''
    __started = False
    __ini_file_name = ''
    __thread : threading.Thread
    __serial_port_name = ''
    __commands : RigCommands
    __freqa = 14200000
    __freqb = 145500250

    def __init__(self, ini_file_name, prefix) -> None:
        self.__ini_file_name = ini_file_name
        self.__prefix = prefix
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), self.__ini_file_name)
        self.__commands = RigHelper.loadRigCommands(path)

    @property
    def SerialPortName(self) -> int:
        return self.__serial_port_name

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

        init0 = self.__commands.InitCmd[0]

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
        if len(command) == 0:
            return False

        for init_cmd in self.__commands.InitCmd:
            if bytes(init_cmd.Code) == command:
                return (True, init_cmd)

        return (False, None)

    def listener(self, port):
        #continuously listen to commands on the master device
        while 1:
            res = b''
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
                (rig_command_parsed, rig_command) = self.parse_rig_command(res)
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
                    os.write(port, rig_command.Validation.Flags)

    def read_from_serial(self, ser : Serial, count: int) -> str:
        res = b''
        while len(res) < count:
            #read the response
            res += ser.read()
        print("result: %s" % res.strip())

    def send_receive(self, ser : Serial, data: bytes, count: int):
        if not data.startswith(self.__prefix):
            ser.write(self.__prefix)
        ser.write(data)
        self.read_from_serial(ser, count)

    def test_serial(self):
        #an emulator is expected to be started by the moment 

        #open a pySerial connection to the slave
        ser = Serial(self.__serial_port_name, 2400, timeout=1)
        self.send_receive(ser, b'cmd1', 5)
        self.send_receive(ser, b'cmd2', 5)

        for cmd in self.__commands.InitCmd:
            self.send_receive(ser, cmd.Code, cmd.ReplyLength)

        ser.close()

if __name__=='__main__':
    x = EmulatorBase('IC-705.ini', b'\xfe\xfe')
    x.start()
    x.test_serial()
    x.stop()