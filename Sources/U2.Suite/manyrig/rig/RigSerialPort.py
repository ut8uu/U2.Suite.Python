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
from common.contracts.RigSettings import RigSettings
from common.exceptions.TimeoutException import TimeoutException
from helpers.ConversionHelper import ConversionHelper
from manyrig.rig.events.SerialPortMessageReceivedEvent import SerialPortMessageReceivedEvent

class RigSerialPort():
    _rig_settings: RigSettings
    _serial_port: serial.Serial
    _serial_port_initialized : bool = False
    _connected : bool = False
    OnSerialPortMessageReceived : SerialPortMessageReceivedEvent
    
    def __init__(self, settings : RigSettings) -> None:
        self._rig_settings = settings
        self.OnSerialPortMessageReceivedEvent = SerialPortMessageReceivedEvent()
        pass

    def AddSubscriberForSerialPortMessageReceived(self, method):
        self.OnSerialPortMessageReceived += method
    
    @property
    def IsConnected(self) -> bool:
        if not self._connected or self._serial_port == None:
            return False
        self._connected = self._serial_port.isOpen
        return self._connected
    
    def Connect(self):
        self._connected = False # reset the flag first

        if self._serial_port_initialized and self._serial_port.is_open:
            return
        
        self._serial_port = serial.Serial(
            port = self._rig_settings.Port,
            baudrate = self._rig_settings.BaudRate,
            parity = ConversionHelper.string_to_parity(self._rig_settings.Parity),
            bytesize = ConversionHelper.int_to_databits(self._rig_settings.DataBits),
            stopbits = ConversionHelper.float_to_stopbits(self._rig_settings.StopBits))
        self._serial_port.timeout = self._rig_settings.TimeoutMs / 1000
        self._serial_port.write_timeout = self._rig_settings.TimeoutMs / 1000

        self._serial_port_initialized = True
        self._connected = self._serial_port.isOpen()
        
    def SendMessage(self, data: bytearray) -> None:
        """sends data to the port"""
        try:
            self._serial_port.write(data)
        except serial.SerialTimeoutException:
            raise TimeoutException(f'Timeout occured while sending data to {self._rig_settings.Port}')

    def SendMessageAndReadBytes(self, data: bytearray, expected_bytes: int) -> bytes:
        """sends data to the port"""
        outputCharacters = bytearray(b'')
        try:
            self._serial_port.write(data)
            while 1:
                ch = self._serial_port.read()
                if len(ch) == 0:
                    break
                outputCharacters += ch
                if outputCharacters[-expected_bytes:] == expected_bytes:
                    break

        except serial.SerialTimeoutException:
            """Do nothing in case of the timeout, just return what was fetched"""
        return bytes(outputCharacters)

def test_serial():
    """Start the testing"""
    master,slave = pty.openpty() #open the pseudoterminal
    s_name = os.ttyname(slave) #translate the slave fd to a filename

    #create a separate thread that listens on the master device for commands
    thread = threading.Thread(target=listener, args=[master])
    thread.start()

    #open a pySerial connection to the slave
    ser = serial.Serial(s_name, 2400, timeout=1)
    ser.write(b'test2\r\n') #write the first command
    res = b""
    while not res.endswith(b'\r\n'):
        #read the response
        res +=ser.read()
    print("result: %s" % res)
    ser.write(b'QPGS\r\n') #write a second command
    res = b""
    while not res.endswith(b'\r\n'):
        #read the response
        res +=ser.read()
    print("result: %s" % res)
    
if __name__ == '__main__':
    a = 1
        