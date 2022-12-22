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

import datetime
import os
from pathlib import Path
from common.contracts.AllBands import *
from common.contracts.CommandQueue import CommandQueue
from common.contracts.QueueItem import QueueItem
from common.exceptions.ArgumentMismatchException import ArgumentMismatchException
from helpers.FileSystemHelper import FileSystemHelper
from logger.logger_constants import *
from logger.logger_options import LoggerOptions
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

    def test_UpperCaseCallsign(self) -> None:
        '''Tests how callsign case is converted to upper.'''
        db = self.GetTestDatabase()
        db.get_or_add_callsign({FIELD_CALLSIGN : 'a1a'})
        record = db.get_callsign('a1a')
        self.assertEqual('A1A', record[FIELD_CALLSIGN])

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

    def test_CanDeleteCallsignById(self) -> None:
        db = self.GetTestDatabase()

        record = db.get_callsign_by_id(UT8UU_ID)
        self.assertIsNotNone(record)
        
        db.delete_callsign_by_id(UT8UU_ID)
        
        record = db.get_callsign_by_id(UT8UU_ID)
        self.assertIsNone(record)

    def test_CanDeleteCallsignByCallsign(self) -> None:
        db = self.GetTestDatabase()

        record = db.get_callsign(UT8UU)
        self.assertIsNotNone(record)
        
        db.delete_callsign_by_callsign(UT8UU)
        
        record = db.get_callsign(UT8UU)
        self.assertIsNone(record)

    def test_CanWorkWithContacts(self) -> None:
        db = self.GetTestDatabase()

        data = {
            FIELD_IS_RUN_QSO : 0,
            FIELD_BAND : '20m',
            FIELD_FREQUENCY : 14200123,
            FIELD_MODE : MODE_SSB,
            FIELD_TIMESTAMP : datetime.datetime.utcnow(),
            FIELD_CALLSIGN : UT8UU.lower(),
            FIELD_OPNAME : 'Sergey'
        }
        db.log_contact(data)

        result1 = db.load_all_contacts()
        self.assertEqual(1, len(result1[1]))
        data = result1[1]
        callsign_index = result1[0].index(FIELD_CALLSIGN)
        self.assertEqual(UT8UU, data[0][callsign_index])

        record1 = db.get_callsign_by_id(1)
        self.assertEqual(1, record1[FIELD_ID])
        self.assertEqual(UT8UU, record1[FIELD_CALLSIGN])

        data_updated = {
            FIELD_BAND : '40m',
            FIELD_FREQUENCY : 7200123,
            FIELD_MODE : MODE_CW,
            FIELD_TIMESTAMP : datetime.datetime.utcnow(),
            FIELD_CALLSIGN : UT3UBR.lower(),
            FIELD_OPNAME : 'Alex'
        }
        db.change_contact(1, data_updated)

        data_updated[FIELD_CALLSIGN] = data_updated[FIELD_CALLSIGN].upper()

        result2 = db.load_all_contacts()
        self.assertEqual(1, len(result2[1]))
        all_values = result2[1]
        for key in data_updated:
            expected = data_updated[key]
            actual_index = result2[0].index(key)
            actual = all_values[0][actual_index]
            self.assertEqual(expected, actual)
            
    def test_CanDeleteContact(self) -> None:
        '''Tests how to delete the contact'''
        db = self.GetTestDatabase()
        db.delete_contact_by_id(UT8UU_ID)
        record = db.get_contact_by_id(UT8UU_ID)
        self.assertEqual(0, len(record))

    def test_CanWorkWithOptions(self) -> None:
        '''Tests how options can be accessed.'''
        db = self.GetTestDatabase()

        options = LoggerOptions(db._db)

        self.assertEqual('', options.StationCallsign)
        self.assertEqual('', options.OperatorName)

        options.StationCallsign = UT8UU
        options.OperatorName = 'Sergey'

        # reopen the database to test the setters
        db = self.GetTestDatabase()
        options = LoggerOptions(db._db)
        self.assertEqual(UT8UU, options.StationCallsign)
        self.assertEqual('Sergey', options.OperatorName)
        