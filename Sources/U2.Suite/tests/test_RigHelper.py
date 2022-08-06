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

import imp
from os.path import join
from helpers.FileSystemHelper import FileSystemHelper as fsh
from helpers.RigHelper import RigHelper as rh
from contracts.RigCommands import RigCommands

def test_LoadIC705():
    folder = fsh.getIniFilesFolder()
    ini_file_path = join(folder, 'IC-705.ini')
    rig_commands = rh.loadRigCommands(ini_file_path)
    assert len(rig_commands.InitCmd) == 3
    
def test_are_equal():
    assert rh.AreEqual('a', 'a')
    assert not rh.AreEqual('a', 'b')
    
