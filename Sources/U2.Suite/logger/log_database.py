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
from typing import Any, List, Tuple
import uuid
from common.exceptions.ArgumentException import ArgumentException
import os
from pathlib import Path
import sqlite3
from common.exceptions.ArgumentMismatchException import ArgumentMismatchException
from common.exceptions.logger.CallsignNotFoundException import CallsignNotFoundException

from helpers.FileSystemHelper import FileSystemHelper
from logger.logger_constants import *

class LogDatabase(object):
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
            TABLE_CALLS : ( FIELD_ID, FIELD_CALLSIGN, FIELD_OPNAME, 
                            FIELD_EMAIL, FIELD_ADDRESS, FIELD_SOURCE, FIELD_HAS_DATA),
            TABLE_CONTACTS : ( 
                            FIELD_ID, FIELD_CALLSIGN, FIELD_TIMESTAMP, FIELD_FREQUENCY,
                            FIELD_BAND, FIELD_MODE, FIELD_OPNAME, FIELD_IS_RUN_QSO,
                            FIELD_UNIQUE_ID, FIELD_DIRTY
                            ),
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
            self.__execute_non_query(sql)
            sql = f'INSERT INTO {TABLE_VERSION} (major, minor) VALUES (?, ?)'
            self.__execute_non_query(sql, (self.DB_VERSION_MAJOR, self.DB_VERSION_MINOR))

            # create a table for calls
            sql = (
                f'CREATE TABLE IF NOT EXISTS "{TABLE_CALLS}" ('
	            f'"{FIELD_ID}"	INTEGER PRIMARY KEY,'
                f'"{FIELD_CALLSIGN}"	TEXT,'
                f'"{FIELD_OPNAME}"	TEXT,'
                f'"{FIELD_EMAIL}"     TEXT,'
                f'"{FIELD_ADDRESS}"   TEXT,'
                f'"{FIELD_SOURCE}"    TEXT,'
                f'"{FIELD_HAS_DATA}"  INTEGER DEFAULT 0);'
            )
            self.__execute_non_query(sql)

            # create a table for QSO
            sql = (
                f"CREATE TABLE IF NOT EXISTS {TABLE_CONTACTS} "
                f"({FIELD_ID} INTEGER PRIMARY KEY, "
                f"{FIELD_CALLSIGN} text NOT NULL, "
                f"{FIELD_TIMESTAMP} TIMESTAMP NOT NULL, "
                f"{FIELD_FREQUENCY} INTEGER DEFAULT 0, "
                f"{FIELD_BAND} text NOT NULL, "
                f"{FIELD_MODE} text NOT NULL, "
                f"{FIELD_OPNAME} text NOT NULL,"
                f"{FIELD_IS_RUN_QSO} INTEGER DEFAULT 0,"
                f"{FIELD_UNIQUE_ID} text NOT NULL, "
                f"{FIELD_DIRTY} INTEGER DEFAULT 1);"
            )
            self.__execute_non_query(sql)
        except sqlite3.Error as error:
            print("Error while connecting to the database.", error)

    def __execute_scalar(self, sql : str, params = ()) -> Any:
        '''Executes given query and returns the first column of the first row.'''
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

    def __execute_non_query(self, sql : str, params = ()) -> None:
        '''Executes given SQL against the database'''
        with sqlite3.connect(self._db_full_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            cursor.close()

    def get_callsign(self, callsign : str) -> dict:
        '''
        Looks for a given callsign in the database.
        Returns the callsign id if one is found.
        Returns 0 if callsign is absent in the database.

        '''
        sql = f'SELECT * FROM {TABLE_CALLS} WHERE {FIELD_CALLSIGN}=? COLLATE NOCASE'
        with sqlite3.connect(self._db_full_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (callsign,))
            data = cursor.fetchone()
            cursor.close()

        result = dict()
        if data == None:
            return None

        for index, col_name in enumerate(self._table_descriptions[TABLE_CALLS]):
            result[col_name] = data[index]

        return result

    def __insert_in_table(self, table : str, data : dict) -> None:
        '''Inserts a record in the given table'''
        sql_fields = ', '.join(data)
        sql_values = ', '.join(['?' for key in data])
        values = tuple(data.values())

        sql = f'INSERT INTO {table} ({sql_fields}) VALUES ({sql_values})'
        self.__execute_non_query(sql, values)

    def __change_row_in_table(self, table : str, id : int, data : dict) -> None:
        '''Updates row in the given table by its identifier.'''
        sql_fields = ', '.join([f'{key}=?' for key in data])
        sql_values = [data[key] for key in data]

        sql = f'UPDATE {table} SET {sql_fields} WHERE {FIELD_ID}={id}'
        self.__execute_non_query(sql, sql_values)

    def __insert_callsign(self, data : dict) -> dict:
        '''
        Inserts given callsign in the database.
        A duplicate check is not performed.
        '''

        self.__insert_in_table(TABLE_CALLS, data)
        return self.get_callsign(data[FIELD_CALLSIGN])

    def get_callsign_by_id(self, i_id : int) -> dict:
        '''
        Retrieves the callsign and operator name by the given id.
        Returns a dictionary having all the record data.
        '''
        sql = f'SELECT * FROM {TABLE_CALLS} WHERE {FIELD_ID}=?'
        with sqlite3.connect(self._db_full_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (i_id,))
            data = cursor.fetchone()
            cursor.close()

        if data == None:
            return None

        result = dict()

        for index, col_name in enumerate(self._table_descriptions[TABLE_CALLS]):
            result[col_name] = data[index]

        return result

    def get_or_add_callsign(self, data : dict) -> dict:
        '''
        Looks for a given callsign (case insensitive) and returns one found.
        Creates a new record if callsign was not found.

        `data` - a dictionary containing the callsign data.
        '''

        callsign = data[FIELD_CALLSIGN]
        if callsign == None or len(callsign.lstrip().rstrip()) == 0:
            raise ArgumentException('Callsign is a mandatory parameter.')

        result = self.get_callsign(callsign)
        if result != None:
            return result

        return self.__insert_callsign(data) 

    def change_callsign(self, id : int, data : dict) -> dict:
        '''
        Updates callsign data by its identifier.
        The `data` parameter is a dictionary containing the following values:
        - callsign
        - opname
        - email
        - address
        - source
        - has_data
        '''

        if len(data[FIELD_CALLSIGN].lstrip().rstrip()) == 0:
            raise ArgumentException('Callsign is a mandatory parameter.')

        self.__change_row_in_table(TABLE_CALLS, id, data)

    def delete_callsign_by_id(self, id : int) -> None:
        '''
        Deletes a callsign by its identifier.
        Does nothing if identifier not found.
        '''
        sql = f'DELETE FROM {TABLE_CALLS} WHERE {FIELD_ID}={id}'
        self.__execute_non_query(sql)
        
    def delete_callsign_by_callsign(self, callsign : str) -> None:
        '''
        Deletes a callsign by its identifier.
        Does nothing if identifier not found.
        '''
        sql = f'DELETE FROM {TABLE_CALLS} WHERE {FIELD_CALLSIGN}=?'
        self.__execute_non_query(sql, (callsign,))  

    def load_all_contacts(self, order_by_field : str = '') -> tuple[tuple, List[tuple]]:
        '''
        Loads all contacts from the database.
        Returns a tuple containing all the fields
        and a list of tuples containing all the fetched rows.
        '''
        sql = f'SELECT * FROM {TABLE_CONTACTS}'
        if len(order_by_field.lstrip().rstrip()) > 0:
            sql += f' ORDER BY {order_by_field}'

        with sqlite3.connect(self._db_full_path,
                detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            result = (self._table_descriptions[TABLE_CONTACTS], cursor.fetchall())
            cursor.close()
            return result


    def log_contact(self, data : dict) -> None:
        """
        Inserts a contact into the db.
        The following values can be present in the dictionary:
        - callsign
        - timestamp
        - frequency
        - band
        - mode, 
        - opname
        - is_run_qso
        The following fields are being filled automatically:
        - unique_id
        - dirty
        """
        data[FIELD_UNIQUE_ID] = uuid.uuid4().hex
        data[FIELD_DIRTY] = 1
        self.__insert_in_table(TABLE_CONTACTS, data)

    def delete_contact(self, contact : int) -> None:
        """Deletes a contact from the db."""
        if contact:
            try:
                sql = f"delete from {TABLE_CONTACTS} where id={contact};"
                self.__execute_non_query(sql)
            except sqlite3.Error as exception:
                logging.info("DataBase delete_contact: %s", exception)

    def change_contact(self, id: int, data : dict) -> None:
        '''
        Changes a contact in the db by the given id.
        The following values can be present in the dictionary:
        - callsign
        - timestamp
        - frequency
        - band
        - mode
        - id
        '''
        self.__change_row_in_table(TABLE_CONTACTS, id, data)

