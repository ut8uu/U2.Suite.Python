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

from common.exceptions.ArgumentException import ArgumentException
from common.exceptions.logger.CallsignNotFoundException import CallsignNotFoundException
import helpers.FileSystemHelper as fsh
import logger.log_database
import os
from pathlib import Path
import shutil
import unittest

class LogDatabaseTests(unittest.TestCase):
    '''This is to test the LogDatabase class'''

    TEST_CALLSIGN = 'UT8UU'
    TEST_NAME = 'Sergey'

    def get_test_data_path(self) -> Path:
        return Path(fsh.FileSystemHelper.getLocalFolder()) / '.test_data'

    def cleanup_test_data(self):
        '''Cleans the test data folder. Required to launch before each test.'''
        path = self.get_test_data_path()
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def get_database(self, file_name : str) -> logger.log_database.LogDatabase:
        '''This is creates an empty database with given name.'''
        path = self.get_test_data_path()
        return logger.log_database.LogDatabase(path, file_name)

    def insert_test_data(self, db : logger.log_database.LogDatabase) -> None:
        db.insert_callsign(self.TEST_CALLSIGN, self.TEST_NAME)

    def test_CreateNewDatabase(self) -> None:
        '''This is to test how the new database can be created'''
        self.cleanup_test_data()
        path = self.get_test_data_path()

        file_name = 'create_new_db.sqlite'
        full_path = path / file_name
        self.get_database(file_name)

        self.assertTrue(os.path.exists(full_path))

    def test_GetAddCallsigns(self) -> None:
        '''This is to test how database can handle callsign-related CRUD operations'''
        self.cleanup_test_data()
        db = self.get_database('test_callsigns.sqlite')

        # at this point there is no records yet
        (id, name) = db.get_or_add_callsign('UT8UU', 'Sergey')
        self.assertEqual(1, id)

        # here we should get the same id
        (id, name) = db.get_or_add_callsign('UT8UU')
        self.assertEqual(1, id)

        # here we try to add the same callsign in lower case
        # the result must be the same
        (id, name) = db.get_or_add_callsign('ut8uu')
        self.assertEqual(1, id)
        self.assertEqual('Sergey', name)

    def test_UpdateCallsign(self):
        '''This is to test how the callsign can be updated'''
        self.cleanup_test_data()
        db = self.get_database('test_callsigns.sqlite')

        # at this point there is no records yet
        (id, name) = db.get_or_add_callsign('UT8UU', 'Sergey')
        self.assertEqual(1, id)

        db.update_callsign(1, 'UT8UU-1', 'Updated')
        (id, name) = db.get_or_add_callsign('UT8UU-1')
        self.assertEqual(1, id)
        self.assertEqual('Updated', name)

        with self.assertRaises(ArgumentException) as ex:
            db.update_callsign(0, '', '')
        
    def test_GetCallsignById(self):
        '''This is to test how the callsign can be found by ID'''
        self.cleanup_test_data()
        db = self.get_database('test_callsigns.sqlite')
        self.insert_test_data(db)

        with self.assertRaises(CallsignNotFoundException) as ex:
            db.get_callsign_by_id(0)

        (id, callsign, name) = db.get_callsign_by_id(1)
        self.assertEqual(1, id)
        self.assertEqual(self.TEST_CALLSIGN, callsign)
        self.assertEqual(self.TEST_NAME, name)
        
