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

from common.contracts.CommandQueue import CommandQueue
from common.contracts.QueueItem import QueueItem
from manyrig.rig.enums.CommandKind import CommandKind
import unittest

class CommandQueueTests(unittest.TestCase):

    def test_Add(self):
        queue = CommandQueue()
        queue.Add(QueueItem())
        self.assertEqual(1, len(queue))

    def test_AddBeforeStatus(self):
        queue = CommandQueue()
        item = QueueItem()
        item.Kind = CommandKind.Init
        queue.Add(item)

        new_item = QueueItem()
        new_item.Kind = CommandKind.Custom
        queue.AddBeforeStatusCommands(new_item) # should be the second

        self.assertEqual(CommandKind.Custom, queue[1].Kind)

    def test_HasStatusCommand(self):
        queue = CommandQueue()
        queue.Add(QueueItem())
        self.assertFalse(queue.HasStatusCommands)

        queue[0].Kind = CommandKind.Status
        self.assertTrue(queue.HasStatusCommands)

    def test_GetCurrentCmd(self):
        queue = CommandQueue()
        self.assertEqual(None, queue.CurrentCmd)

        queue.Add(QueueItem())
        self.assertNotEqual(None, queue.CurrentCmd)
    
    def test_IsEmpty(self):
        queue = CommandQueue()
        self.assertTrue(queue.IsEmpty)

        queue.Add(QueueItem())
        self.assertFalse(queue.IsEmpty)
