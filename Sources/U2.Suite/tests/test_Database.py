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

import os
from pathlib import Path
from common.contracts.AllBands import *
from common.contracts.CommandQueue import CommandQueue
from common.contracts.QueueItem import QueueItem
from common.exceptions.ArgumentMismatchException import ArgumentMismatchException
from helpers.FileSystemHelper import FileSystemHelper
from logger.logger_constants import *
from manyrig.rig.enums.CommandKind import CommandKind
from logger.log_database import LogDatabase
import unittest

UT8UU = 'UT8UU'
UT8UU_ID = 1
UT3UBR = 'UT3UBR'
UT3UBR_ID = 2
OP_NAME = 'Sergey'
OP_NAME_MOD = 'Alex'

class DatabaseTests(unittest.TestCase):
    '''A database-related unit tests'''

    _db_name : str
    _path : Path
    _full_path : Path

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self._db_name = 'test.db'
        self._path = self.GetPathToDatabase()
        self._full_path = self._path / self._db_name
        if self._path.exists():
            try:
                self._full_path.unlink()
            except:
                ''''''
                print(f'Cannot remove file {self._full_path}')

    def GetPathToDatabase(self) -> Path:
        '''Calculates the full path to the database'''
        return Path(os.path.abspath("."))

    def GetTestDatabase(self) -> LogDatabase:
        db = LogDatabase(self._path, self._db_name)
        record = db.get_or_add_callsign({FIELD_CALLSIGN : UT8UU})
        self.assertEqual(UT8UU_ID, record[FIELD_ID])
        record = db.get_or_add_callsign({FIELD_CALLSIGN: UT3UBR, FIELD_OPNAME: OP_NAME})
        self.assertEqual(UT3UBR_ID, record[FIELD_ID])
        self.assertEqual(OP_NAME, record[FIELD_OPNAME])

        return db

    def test_DatabaseCreatedAutomatically(self) -> None:
        '''A callsigns-related test'''
        self.assertFalse(self._full_path.exists())
        db = self.GetTestDatabase()
        self.assertTrue(self._full_path.exists())

    def test_CanNotAddDuplicateCallsign(self):
        '''
        This is to test how duplicate callsigns can be handled.
        An attempt to add the existing callsign returns the id of the existing record.
        '''
        db = self.GetTestDatabase()
        record = db.get_or_add_callsign({FIELD_CALLSIGN : UT8UU})
        self.assertEqual(UT8UU_ID, record[FIELD_ID])

        record = db.get_or_add_callsign({FIELD_CALLSIGN : UT8UU.lower()})
        self.assertEqual(UT8UU_ID, record[FIELD_ID])

    def test_CanUpdateCallsign(self) -> None:
        '''
        This is to test updating of the callsign info.
        '''
        db = self.GetTestDatabase()

        data = {
            FIELD_CALLSIGN : UT3UBR, 
            FIELD_OPNAME : OP_NAME_MOD,
            FIELD_EMAIL : 'EMAIL',
            FIELD_ADDRESS : 'ADDRESS',
            FIELD_HAS_DATA : 1,
            FIELD_SOURCE : 'SOURCE'
            }
        db.change_callsign(UT8UU_ID, data)
        record = db.get_callsign_by_id(UT8UU_ID)
        for key in record:
            if key == FIELD_ID:
                continue
            self.assertEqual(data[key], record[key])
