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

from exceptions.OsNotSupportedException import OsNotSupportedException
from helpers.RigHelper import RigHelper
from rig.listeners.IC705Listener import IC705Listener
import os, unittest

class test_IC705Listener(unittest.TestCase):
    
    def test_001(self):
        #RigHelper.loadAllRigCommands()
        self.assertNotEqual('nt', os.name, 'This test cannot be run under the Windows')
        IC705Listener.test_serial()