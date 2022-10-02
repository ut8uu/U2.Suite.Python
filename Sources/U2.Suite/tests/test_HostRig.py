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
from contracts.RigParameter import RigParameter

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

        # SetFreq raises an exception
        with self.assertRaises(ArgumentException) as ex:
            rig.SetFreq(1)

    @unittest.skipIf(os.name != 'posix', "not supported on the current platform")
    def test_CanSetFreqAViaSerialPort(self):
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

    @unittest.skipIf(os.name != 'posix', "not supported on the current platform")
    def test_CanSetModeViaSerialPort(self):
        emulator = IC705Emulator()
        emulator.start()
        
        rig = self.GetHostRig(True, emulator)

        rig.Mode = RigParameter.fm
        self.assertEqual(RigParameter.fm.value, emulator._rig.Mode)

        rig.Mode = RigParameter.am
        self.assertEqual(RigParameter.am.value, emulator._rig.Mode)

        emulator.stop()

    def test_GanSetSplitViaSerialPort(self):
        emulator = IC705Emulator()
        emulator.start()
        
        rig = self.GetHostRig(True, emulator)

        rig.Split = RigParameter.spliton
        self.assertEqual(RigParameter.spliton.value, emulator._rig.Split)

        rig.Split = RigParameter.splitoff
        self.assertEqual(RigParameter.splitoff.value, emulator._rig.Split)

        emulator.stop()

    def test_GanSetTxViaSerialPort(self):
        emulator = IC705Emulator()
        emulator.start()
        
        rig = self.GetHostRig(True, emulator)

        rig.Tx = RigParameter.tx
        self.assertEqual(RigParameter.tx.value, emulator._rig.Tx)

        rig.Tx = RigParameter.rx
        self.assertEqual(RigParameter.rx.value, emulator._rig.Tx)

        emulator.stop()

    def test_GanSetRitViaSerialPort(self):
        emulator = IC705Emulator()
        emulator.start()
        
        rig = self.GetHostRig(True, emulator)

        rig.Rit = RigParameter.ritoff
        self.assertEqual(RigParameter.ritoff.value, emulator._rig.Rit)

        rig.Rit = RigParameter.riton
        self.assertEqual(RigParameter.riton.value, emulator._rig.Rit)

        emulator.stop()

    def test_GanSetXitViaSerialPort(self):
        emulator = IC705Emulator()
        emulator.start()
        
        rig = self.GetHostRig(True, emulator)

        rig.Xit = RigParameter.xitoff
        self.assertEqual(RigParameter.xitoff.value, emulator._rig.Xit)

        rig.Xit = RigParameter.xiton
        self.assertEqual(RigParameter.xiton.value, emulator._rig.Xit)

        emulator.stop()
