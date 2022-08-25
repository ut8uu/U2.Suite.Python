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
import exceptions
from helpers.FileSystemHelper import FileSystemHelper
from helpers.RigHelper import RigHelper
from typing import List, Tuple

if os.name.lower().find('posix') > -1:
    import pty

class IC705Listener():
    @staticmethod
    def can_parse_request(buffer: str, port: str, commands: List[RigCommand]) -> bool:
        arr = bytearray(buffer)
        for cmd in commands:
            if arr == cmd.Code:
                return True
        
        return False

    @staticmethod
    def ic705_listener(port: int, commands: RigCommands):
        while 1:
            buffer = b''
            
            while 1:
                # read one byte
                buffer += os.read(port, 1)
                
                if buffer == b'exit':
                    return
                
                # try to recognize the request
                if IC705Listener.can_parse_request(buffer, port, commands):
                    break
                
    @staticmethod
    def test_listener():
        """Start the testing"""
        master,slave = pty.openpty() #open the pseudoterminal
        s_name = os.ttyname(slave) #translate the slave fd to a filename

        # load commands from the INI file
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), 'IC-705.ini')
        commands = RigHelper.loadRigCommands(path)

        #create a separate thread that listens on the master device for commands
        thread = threading.Thread(target=IC705Listener.ic705_listener, args=[master, commands])
        thread.start()
        
        #open a pySerial connection to the slave
        ser = serial.Serial(s_name, 2400, timeout=1)
        
        ser.write('exit')

    @staticmethod
    def listener(port: int, commands: RigCommands):
        #continuously listen to commands on the master device
        res = b''
        fefe = b'\xfe\xfe'
        while 1:
            res += os.read(port, 1)
            print("command: %s" % res)

            if res.endswith(fefe):
                res = fefe # reset the command
                continue # resume reading

            command_found = False

            for init_command in commands.InitCmd:
                if init_command.Code == res:
                    os.write(port, init_command.Validation.Flags)
                    command_found = True
                    break

            if res == b'exit':
                return

            if command_found:
                res = b''
                continue


    @staticmethod
    def test_serial():
        """Start the testing"""
        master,slave = pty.openpty() #open the pseudoterminal
        s_name = os.ttyname(slave) #translate the slave fd to a filename

        # load commands from the INI file
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), 'IC-705.ini')
        commands = RigHelper.loadRigCommands(path)

        #create a separate thread that listens on the master device for commands
        thread = threading.Thread(target=IC705Listener.listener, args=[master, commands])
        thread.start()

        #open a pySerial connection to the slave
        ser = serial.Serial(s_name, 2400, timeout=1)
        
        for init_command in commands.InitCmd:
            print(f'Testing command {init_command.Code}')
            ser.write(init_command.Code)
            response = ser.read(init_command.ReplyLength)
            assert response == init_command.Validation.Flags

        ser.write(b'exit')

        ser.close()
        
