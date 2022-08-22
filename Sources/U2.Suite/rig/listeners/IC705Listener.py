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
    def ic705_listener(port):
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), 'IC705.ini')
        commands = RigHelper.loadRigCommands(path)
        while 1:
            buffer = b''
            
            while 1:
                # read one byte
                buffer += os.read(port, 1)
                
                if buffer == b'exit':
                    return
                
                # try to recognize the request
                if IC705Listener.IC705Listener.can_parse_request(buffer, port, commands):
                    break
                
    @staticmethod
    def test_listener():
        """Start the testing"""
        master,slave = pty.openpty() #open the pseudoterminal
        s_name = os.ttyname(slave) #translate the slave fd to a filename

        #create a separate thread that listens on the master device for commands
        thread = threading.Thread(target=IC705Listener.IC705Listener.ic705_listener, args=[master])
        thread.start()
        
        #open a pySerial connection to the slave
        ser = serial.Serial(s_name, 2400, timeout=1)
        
        ser.write('exit')
                
    if __name__ == '__main__':
        if os.name.lower().find('posix') == -1:
            raise exceptions.OsNotSupportedException()
        test_listener()
                
        