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

from pathlib import Path
import pathlib
import shutil

import helpers.FileSystemHelper as fsh
import logger.log_database
import os
import unittest

class LogDatabaseTests(unittest.TestCase):
    '''This is to test the LogDatabase class'''

    def get_test_data_path(self) -> Path:
        return Path(fsh.FileSystemHelper.getLocalFolder()) / '.test_data'

    def cleanup_test_data(self):
        '''Cleans the test data folder. Required to launch before each test.'''
        path = self.get_test_data_path()
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def test_CreateNewDatabase(self) -> None:
        '''This is to test how the new database can be created'''
        self.cleanup_test_data()

        path = self.get_test_data_path()
        file_name = 'create_new_db.sqlite'
        full_path = path / file_name
        db = logger.log_database.LogDatabase(path, file_name)

        self.assertTrue(os.path.exists(full_path))

        
