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

import os
import unittest
from contracts.RigParameter import RigParameter
from contracts.RigSettings import RigSettings
from helpers.RigHelper import RigHelper
from rig.RigSerialPort import RigSerialPort

from rig.emulators.IC705Emulator import IC705Emulator

class SerialPortTests(unittest.TestCase):
    '''To test the abilities of the RigSerialPort class'''

    def GetEmulator(self) -> IC705Emulator:
        emulator = IC705Emulator()
        return emulator

    def GetSettings(self) -> RigSettings:
        settings = RigSettings()
        settings.BaudRate = 9600
        settings.DataBits = 8
        settings.DtrMode = False
        settings.RtsMode = False
        settings.Parity = 'None'
        settings.StopBits = 1
        settings.TimeoutMs = 2000
        settings.PollMs = 500

        return settings

    def GetRigSerialPort(self, port: str) -> RigSerialPort:
        settings = self.GetSettings()
        settings.Port = port
        serial_port = RigSerialPort(settings)
        return serial_port

    def test_CanSendCommandsUnderWindows(self) -> None:
        '''
        In case of running under Windows, ensure you have the com0com installed and configured.
        Please specify the name of the port in the com0com in the 
        WINDOWS_MASTER_COM_PORT constant in the EmulatorBase.py
        '''
        emulator = self.GetEmulator()
        emulator.start()
        serial_port = self.GetRigSerialPort(emulator.SerialPortName)

        serial_port.Connect()
        self.assertTrue(serial_port.IsConnected)

        command = emulator.get_status_command(RigParameter.freqa)
        reply = serial_port.SendMessageAndReadBytes(command.Code, command.ReplyLength)
        self.assertEqual(len(reply), command.ReplyLength)
        RigHelper.validate_reply(reply, command.Validation)

        command = emulator._commands.InitCmd[0]
        serial_port.SendMessage(command.Code)

        emulator.stop()

    @unittest.skipIf(True, 'Comment this when working with real ports.')
    def test_GetSerialPortInfo(self) -> None:
        '''This test cannot find any COM port created by com0com'''
        from serial_device2 import SerialDevice, find_serial_device_ports
        ports = find_serial_device_ports() # Returns list of available serial ports
        dev = SerialDevice() # Might automatically find device if one available
        info = dev.get_device_info()
        x = info[0]
