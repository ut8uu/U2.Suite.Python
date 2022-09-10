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
import unittest

class CommandQueueTests(unittest.TestCase):

    def test_Add(self):
        queue = CommandQueue()
        queue.Add()
        self.assertEqual(1, len(queue))

    def test_AddBeforeStatus(self):
        queue = CommandQueue()
        item = queue.Add()
        item.Kind = CommandKind.Init

        new_item = QueueItem()
        new_item.Kind = CommandKind.Custom
        queue.AddBeforeStatusCommands(new_item) # should be the second

        self.assertEqual(CommandKind.Custom, queue[1].Kind)

    def test_HasStatusCommand(self):
        queue = CommandQueue()
        item = queue.Add()
        self.assertFalse(queue.HasStatusCommands)

        queue[0].Kind = CommandKind.Status
        self.assertTrue(queue.HasStatusCommands)

    def test_GetCurrentCmd(self):
        queue = CommandQueue()
        self.assertEqual(None, queue.CurrentCmd)

        queue.Add()
        self.assertNotEqual(None, queue.CurrentCmd)
        