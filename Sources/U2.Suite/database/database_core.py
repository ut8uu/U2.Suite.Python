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
from logger.logger_constants import *
from typing import Any, List, Tuple
import os
from pathlib import Path
import sqlite3

class DatabaseCore(object):
    '''Class handles all requests to the database'''

    DB_VERSION_MAJOR : int = 1
    DB_VERSION_MINOR : int = 0

    _db_name : str
    _db_full_path : Path
    _table_descriptions : dict[str, tuple]

    def __init__(self, path : Path, db_name : str = DATABASE_DEFAULT) -> None:
        self._db_name = db_name
        self._db_full_path = path / db_name
        # TODO consider collecting fields from the database
        self._table_descriptions = {
            TABLE_VERSION : (FIELD_VERSION_MAJOR, FIELD_VERSION_MINOR)
        }
        self.__check_db()
        pass

    def __check_db(self) -> None:
        '''Check the presence of the database and creates it if it does not exist.'''
        if not os.path.exists(self._db_full_path):
            # a database does not exist. We have to create it first.
            self.__create_db()

    def __create_db(self) -> None:
        '''Creates a database by the given path'''
        try:
            # create a table for version
            sql = (
                f'CREATE TABLE IF NOT EXISTS "{TABLE_VERSION}" ('
                '    "major" INTEGER,'
                '    "minor" INTEGER'
                '    );'
                )
            self.execute_non_query(sql)
            sql = f'INSERT INTO {TABLE_VERSION} (major, minor) VALUES (?, ?)'
            self.execute_non_query(sql, (self.DB_VERSION_MAJOR, self.DB_VERSION_MINOR))
        except sqlite3.Error as error:
            print("Error while connecting to the database.", error)

    def execute_scalar(self, sql : str, params = ()) -> Any:
        '''
        Executes given query and returns the first column of the first row.
        Returns the value of the very first column in the first row.
        Returns `None` if query has brough no results.
        '''
        try:
            with sqlite3.connect(self._db_full_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                data = cursor.fetchone()
                cursor.close()

            if data == None:
                return None

            return data[0]
        except sqlite3.Error as error:
            print('Error during executing scalar query.', error)

    def execute_non_query(self, sql : str, params = ()) -> None:
        '''Executes given SQL against the database'''
        try:
            with sqlite3.connect(self._db_full_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
                cursor.close()
        except sqlite3.Error as ex:
            logging.exception(f'SqLite error: {ex}')
        logging.debug(f'Query {sql} executed successfully.')

    def insert_in_table(self, table : str, data : dict) -> None:
        '''Inserts a record in the given table'''
        sql_fields = ', '.join(data)
        sql_values = ', '.join(['?' for key in data])
        values = tuple(data.values())

        sql = f'INSERT INTO {table} ({sql_fields}) VALUES ({sql_values})'
        self.execute_non_query(sql, values)

    def change_row_in_table(self, table : str, id : int, data : dict) -> None:
        '''Updates row in the given table by its identifier.'''
        sql_fields = ', '.join([f'{key}=?' for key in data])
        sql_values = [data[key] for key in data]

        sql = f'UPDATE {table} SET {sql_fields} WHERE {FIELD_ID}={id}'
        self.execute_non_query(sql, sql_values)

    def filter_dictionary(self, input : dict, allowed_keys : tuple) -> dict:
        '''Creates new dictionary containing only allowed keys.'''
        result = dict()
        all_keys = input.keys()
        for key in allowed_keys:
            if key in all_keys:
                result[key] = input[key]
        return result

