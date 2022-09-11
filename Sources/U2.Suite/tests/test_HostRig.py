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

from contracts.RigSettings import RigSettings
from helpers.FileSystemHelper import FileSystemHelper
from helpers.RigHelper import RigHelper
from rig.HostRig import HostRig

class HostRigTests(unittest.TestCase):
    def test_set_properties(self) -> None:
        path = os.path.join(FileSystemHelper.getIniFilesFolder(), 'IC-705.ini')
        self.assertTrue(os.path.isfile(path))

        commands = RigHelper.loadRigCommands(path)
        settings = RigSettings()
        rig = HostRig(1, 1, settings, commands)
        rig.Enabled = True
        
        rig.SetFreqA(1)
        self.assertEqual(1, rig.FreqA)
