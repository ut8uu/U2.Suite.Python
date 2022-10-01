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

import os, unittest
import time

from contracts.RigSettings import RigSettings
from exceptions.ArgumentException import ArgumentException
from helpers.FileSystemHelper import FileSystemHelper
from helpers.RigHelper import RigHelper
from rig.HostRig import HostRig
from rig.emulators.IC705Emulator import IC705Emulator

class HostRigTests(unittest.TestCase):

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
        settings.TimeoutMs = 500
        settings.PollMs = 2000

        return settings

    def GetHostRig(self, enabled: bool, emulator : IC705Emulator) -> HostRig:
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), 'IC-705.ini')
        self.assertTrue(os.path.isfile(path))

        commands = RigHelper.loadRigCommands(path)
        settings = self.GetSettings()
        settings.Port = emulator.SerialPortName

        rig = HostRig(1, 1, settings, commands)
        rig.Enabled = enabled

        return rig

    def test_set_properties(self) -> None:
        emulator = self.GetEmulator()
        emulator.start()

        rig = self.GetHostRig(True, emulator)
        rig.SetFreqA(1)
        self.assertEqual(1, rig.FreqA)

        with self.assertRaises(ArgumentException) as ex:
            rig.SetFreq(1)

    @unittest.skipIf(os.name != 'posix', "not supported on the current platform")
    def test_CanGetFreqAViaSerialPort(self):
        emulator = IC705Emulator()
        emulator.start()
        
        rig = self.GetHostRig(True, emulator)

        freq = 14200120
        rig.FreqA = freq
        rig.FreqB = freq + 1

        time.sleep(1)  # wait for some time
        self.assertEqual(freq, emulator._rig.FreqA)
        self.assertEqual(freq + 1, emulator._rig.FreqB)

        emulator.stop()