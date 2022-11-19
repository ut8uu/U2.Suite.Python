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

from contracts.CommandQueue import CommandQueue
from contracts.QueueItem import QueueItem
from rig.enums.CommandKind import CommandKind
from contracts.AllBands import *
import unittest

class AllBandsTests(unittest.TestCase):

    def test_Band70CM(self):
        band = Band70CM()
        self.assertEqual(430000000, band.BeginMhz)
        self.assertEqual(440000000, band.EndMhz)
        self.assertEqual(8, len(band.SubBands))
