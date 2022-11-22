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

from common.contracts.QueueItem import QueueItem
from manyrig.rig.enums.CommandKind import CommandKind
from manyrig.rig.enums.ExchangePhase import ExchangePhase
from typing import List

class CommandQueue(List[QueueItem]):

    def __init__(self):
        self._Phase = ExchangePhase.Idle
        super(CommandQueue, self).__init__()

    @property
    def Phase(self) -> ExchangePhase:
        return self._Phase

    @Phase.setter
    def Phase(self, value):
        self._Phase = value

    def Add(self):
        item = QueueItem()
        self.append(item)
        return item

    def Add(self, item: QueueItem) -> None:
        self.append(item)

    def AddBeforeStatusCommands(self, item):
        if len(self) == 0:
            self.append(item)
            return

        firstStatusItem = next((c for c in self if c.Kind == CommandKind.Status), None)
        if (firstStatusItem == None):
            self.append(item)
            return
        
        index = self.index(firstStatusItem)
        if index == 0 and len(self) > 1:
            index += 1
        self.insert(index, item)

    @property
    def HasStatusCommands(self):
        firstStatusItem = next((c for c in self if c.Kind == CommandKind.Status), None)
        return firstStatusItem != None

    @property
    def CurrentCmd(self) -> QueueItem:
        if len(self) > 0:
            item = self[0]
            return item
        return None

    @property
    def IsEmpty(self):
        return len(self) == 0
        