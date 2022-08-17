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

import unittest
from contracts.RigCommands import RigCommands
from contracts.RigParameter import RigParameter
from helpers.FileSystemHelper import FileSystemHelper as fsh
from helpers.RigHelper import RigHelper as rh
from os.path import join

class RigHelperTests(unittest.TestCase):
    def test_LoadIC705(self):
        folder = fsh.getIniFilesFolder()
        ini_file_path = join(folder, 'IC-705.ini')
        rig_commands = rh.loadRigCommands(ini_file_path)
        self.assertEqual(3, len(rig_commands.InitCmd))
        self.assertEqual(9, len(rig_commands.StatusCmd))
        
        parameters = [
            RigParameter.freqa, RigParameter.freqb, RigParameter.rit0, RigParameter.pitch,
            RigParameter.spliton, RigParameter.splitoff, RigParameter.vfoa, RigParameter.vfob,
            RigParameter.vfoequal, RigParameter.vfoswap, RigParameter.vfoaa, RigParameter.vfoab,
            RigParameter.vfoba, RigParameter.vfobb, RigParameter.riton, RigParameter.ritoff,
            RigParameter.xiton, RigParameter.xitoff, RigParameter.rx, RigParameter.tx,
            RigParameter.cw_u, RigParameter.cw_l, RigParameter.ssb_u, RigParameter.ssb_l,
            RigParameter.dig_u, RigParameter.dig_l, RigParameter.am, RigParameter.fm,
        ]
        self.assertEqual(len(parameters), len(rig_commands.WriteCmd));

        
    def test_are_equal(self):
        assert rh.AreEqual('a', 'a')
        assert not rh.AreEqual('a', 'b')
        
