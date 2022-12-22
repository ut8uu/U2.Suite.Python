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

if __name__ == '__main__':
    print('This module cannot be executed directly')
    exit(0)

import logging

from database.database_core import DatabaseCore

from logger.logger_constants import FIELD_KEY, FIELD_VALUE, OPTION_VERSION, TABLE_OPTIONS
import semver

class DatabaseOptions(object):
    '''Represents options-related activities in the database.'''

    #from logger.log_database import LogDatabase
    #_db : LogDatabase
    _db : DatabaseCore

    def __init__(self, db : DatabaseCore) -> None:
        self._db = db

    def create_table(self) -> None:
        '''Creates the OPTIONS table if it does not exist'''
        # create a table for options
        sql = (
            f'CREATE TABLE IF NOT EXISTS "{TABLE_OPTIONS}" ('
            f'    {FIELD_KEY} TEXT,'
            f'    {FIELD_VALUE} TEXT'
            '    );'
            )
        self._db.execute_non_query(sql)

    def get_option(self, key : str) -> str:
        '''
        Retrieves an option by the given key.
        Returns the stored value or `None` if option not found.
        '''
        sql = f'SELECT {FIELD_VALUE} FROM {TABLE_OPTIONS} WHERE key=?'
        return self._db.execute_scalar(sql, (key,))

    def delete_option(self, key: str) -> None:
        '''Deletes an option with given key.'''
        sql = f'DELETE FROM {TABLE_OPTIONS} WHERE {FIELD_KEY}=?'
        self._db.execute_non_query(sql, (key,))

    def get_or_insert_option(self, key : str, value : str = '') -> str:
        '''
        Fetches an option by given key.
        If option is not found, it is created using the passed value.
        '''
        existing_value = self.get_option(key)
        if existing_value == None:
            # option not found, it's time to insert it
            sql = f'INSERT INTO {TABLE_OPTIONS} ({FIELD_KEY}, {FIELD_VALUE}) VALUES (?, ?)'
            self._db.execute_non_query(sql, (key, value,))
            return value

        return existing_value

    def update_or_insert_option(self, key: str, value: str) -> None:
        '''
        Updates existing option or inserts new one if given key is not present.
        '''
        existing_value = self.get_option(key)
        if existing_value == None:
            # option not found, it's time to insert it
            sql = f'INSERT INTO {TABLE_OPTIONS} ({FIELD_KEY}, {FIELD_VALUE}) VALUES (?, ?)'
            self._db.execute_non_query(sql, (key, value,))
        else:
            sql = f'UPDATE {TABLE_OPTIONS} SET {FIELD_VALUE}=? WHERE {FIELD_KEY}=?'
            self._db.execute_non_query(sql, (value, key,))

    def get_or_insert_version(self, version : semver.VersionInfo) -> semver:
        ''''''
        return self.get_or_insert_option(OPTION_VERSION, str(version))
