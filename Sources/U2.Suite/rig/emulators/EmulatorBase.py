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

import os, serial, threading
from contracts.RigCommand import RigCommand
from contracts.RigCommands import RigCommands
from helpers.FileSystemHelper import FileSystemHelper
from helpers.RigHelper import RigHelper
from typing import List, Tuple

if os.name.lower().find('posix') > -1:
    import pty

class EmulatorBase():
    __serial_port : serial.Serial
    __started = False
    __tread : threading.Thread
    __ini_file_name : str
    __commands : RigCommands
    __prefix : str
    __freqa = 14200000
    __freqb = 145500250

    def __init__(self, ini_file_name, prefix):
        """
        Purpose: ini_file_name
        """
        
        self.__ini_file_name = ini_file_name
        self.__prefix = prefix
    # end alternate ini_file_name

    def start(self):
        if self.__started:
            return

        master,slave = pty.openpty() #open the pseudoterminal
        s_name = os.ttyname(slave) #translate the slave fd to a filename

        # load commands from the INI file
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), self.__ini_file_name)
        self.__commands = RigHelper.loadRigCommands(path)

        #create a separate thread that listens on the master device for commands
        self.__thread = threading.Thread(target=EmulatorBase.listener, args=[self, master, self.__commands])
        self.__thread.start()

        #open a pySerial connection to the slave
        self.__serial_port = serial.Serial(s_name, 2400, timeout=1)
        self.__started = True

    def stop(self):
        if self.__started:
            return

        self.__started = False
        self.__serial_port.write(b'exit')
        self.__serial_port.close()

        self.__thread.join(5)

    def listener(self, port: int, commands: RigCommands):
        #continuously listen to commands on the master device
        res = b''
        while 1:
            if not self.__started:
                return

            x = os.read(port, 0)
            if len(x) == 0:
                continue

            res += x
            print("command: %s" % res)

            if res.endswith(self.__prefix):
                res = self.__prefix # reset the command
                continue # resume reading

            command_found = False

            for init_command in self.__commands.InitCmd:
                if init_command.Code == res:
                    os.write(port, init_command.Validation.Flags)
                    command_found = True
                    break

            if not self.__started:
                return

            if res.find(b'exit') > -1:
                return

            if command_found:
                res = b''
                continue


    def test_serial(self):
        """Start the testing"""
        self.start()
        
        for init_command in self.__commands.InitCmd:
            print(f'Testing command {init_command.Code}')
            self.__serial_port.write(init_command.Code)
            response = self.__serial_port.read(init_command.ReplyLength)
            assert response == init_command.Validation.Flags

        self.stop()
        
