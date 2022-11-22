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
from threading import Timer
import time
from common.contracts.RigParameter import RigParameter

from common.contracts.RigSettings import RigSettings
from common.exceptions.ArgumentException import ArgumentException
from helpers.FileSystemHelper import FileSystemHelper
from helpers.RigHelper import RigHelper
from manyrig.rig.HostRig import HostRig
from manyrig.rig.emulators.IC705Emulator import IC705Emulator

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

        # SetFreq raises an exception
        with self.assertRaises(ArgumentException) as ex:
            rig.SetFreq(1)

        freq = 14200120
        rig.FreqA = freq
        rig.FreqB = freq + 1

        self.assertEqual(freq, emulator._rig.FreqA)
        self.assertEqual(freq + 1, emulator._rig.FreqB)

        '''Set Mode'''
        rig.Mode = RigParameter.fm
        time.sleep(1)
        self.assertEqual(RigParameter.fm, emulator._rig.Mode)

        rig.Mode = RigParameter.am
        time.sleep(1)
        self.assertEqual(RigParameter.am, emulator._rig.Mode)

        '''Set Split'''
        rig.Split = RigParameter.spliton
        time.sleep(1)
        self.assertEqual(RigParameter.spliton, emulator._rig.Split)

        rig.Split = RigParameter.splitoff
        time.sleep(1)
        self.assertEqual(RigParameter.splitoff, emulator._rig.Split)

        '''Set Tx'''
        rig.Tx = RigParameter.tx
        time.sleep(1)
        self.assertEqual(RigParameter.tx, emulator._rig.Tx)

        rig.Tx = RigParameter.rx
        time.sleep(1)
        self.assertEqual(RigParameter.rx, emulator._rig.Tx)

        '''Set Rit'''
        rig.Rit = RigParameter.ritoff
        time.sleep(1)
        self.assertEqual(RigParameter.ritoff, emulator._rig.Rit)

        rig.Rit = RigParameter.riton
        time.sleep(1)
        self.assertEqual(RigParameter.riton, emulator._rig.Rit)

        '''Set Xit'''
        rig.Xit = RigParameter.xitoff
        time.sleep(1)
        self.assertEqual(RigParameter.xitoff, emulator._rig.Xit)

        rig.Xit = RigParameter.xiton
        time.sleep(1)
        self.assertEqual(RigParameter.xiton, emulator._rig.Xit)

        rig.Enabled = False
        emulator.stop()

    def test_GetFreqAViaSerialPort(self) -> None:
        '''to test how the FreqA can be retrieved using the STATUS command'''
        emulator = IC705Emulator()
        emulator.start()
        emulator._rig.FreqA = 14232000

        rig = self.GetHostRig(True, emulator)

        time.sleep(5) # need to completely finish polling the rig
        rig.Enabled = False
        emulator.stop()
        
        self.assertEqual(14232000, rig.FreqA)

