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

from common.exceptions.ArgumentException import ArgumentException
from database.database_core import DatabaseCore
from database.database_options import DatabaseOptions
import hashlib
from logger.logger_constants import *
from logger.logger_options import LoggerOptions
import logging
from pathlib import Path
import sqlite3
from typing import Any, List, Tuple
import uuid
import semver

class LogDatabase(object):
    """Class handles all requests to the database"""

    _db : DatabaseCore
    _db_version : str = '1.0.0'

    _options : DatabaseOptions
    _logger_options : LoggerOptions

    def __init__(self, path : Path, db_name : str = DATABASE_DEFAULT) -> None:
        self._db_name = db_name
        if not path.exists():
            path.mkdir()
        self._db_full_path = path / db_name
        self._db = DatabaseCore(path, db_name)
        #options-related stuff must be created before using it
        self._options = DatabaseOptions(self._db)
        self._options.create_table()

        self._logger_options = LoggerOptions(self._db)

        # TODO consider collecting fields from the database
        self._db._table_descriptions[TABLE_CALLS] = ( FIELD_ID, FIELD_CALLSIGN, FIELD_OPNAME, 
                            FIELD_EMAIL, FIELD_ADDRESS, FIELD_SOURCE, FIELD_HAS_DATA)
        self._db._table_descriptions[TABLE_CONTACTS] = ( 
                            FIELD_ID, 
                            FIELD_CHECKSUM,
                            FIELD_CALLSIGN, 
                            FIELD_TIMESTAMP, 
                            FIELD_FREQUENCY,
                            FIELD_BAND, 
                            FIELD_MODE, 
                            FIELD_OPNAME, 
                            FIELD_RST_SENT, 
                            FIELD_RST_RCVD,
                            FIELD_IS_RUN_QSO, 
                            FIELD_UNIQUE_ID, 
                            FIELD_DIRTY
                            )

        self.__check_db()
        pass

    @property
    def LoggerOptions(self) -> LoggerOptions:
        return self._logger_options

    def __check_db(self) -> None:
        try:
            self._options.create_table()
            version = semver.VersionInfo.parse(self._db_version)
            self._options.get_or_insert_version(version)

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
            self._db.execute_non_query(sql)

            # create a table for QSO
            sql = (
                f"CREATE TABLE IF NOT EXISTS {TABLE_CONTACTS} "
                f"({FIELD_ID} INTEGER PRIMARY KEY, "
                f"{FIELD_CHECKSUM} TEXT NOT NULL, "
                f"{FIELD_CALLSIGN} TEXT NOT NULL, "
                f"{FIELD_TIMESTAMP} TIMESTAMP NOT NULL, "
                f"{FIELD_FREQUENCY} INTEGER DEFAULT 0, "
                f"{FIELD_BAND} text NOT NULL, "
                f"{FIELD_MODE} text NOT NULL, "
                # this optional field can contain an overriden name of the operator
                f"{FIELD_OPNAME} text DEFAULT ''," 
                f"{FIELD_RST_SENT} text NULL, "
                f"{FIELD_RST_RCVD} text NULL, "
                f"{FIELD_IS_RUN_QSO} INTEGER DEFAULT 0, "
                f"{FIELD_UNIQUE_ID} text NOT NULL, "
                f"{FIELD_DIRTY} INTEGER DEFAULT 1);"
            )
            self._db.execute_non_query(sql)
        except sqlite3.Error as error:
            print("Error while connecting to the database.", error)

    def get_callsign(self, callsign : str) -> dict:
        """
        Looks for a given callsign in the database.
        Returns the dictionary containing all the info about the callsign, if one is found.
        The keys of the dictionary are names of the table columns.
        The values are the actual values from the table.
        Returns 0 if callsign is absent in the database.

        """
        sql = f'SELECT * FROM {TABLE_CALLS} WHERE {FIELD_CALLSIGN}=? COLLATE NOCASE'
        with sqlite3.connect(self._db_full_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (callsign,))
            data = cursor.fetchone()
            cursor.close()

        result = dict()
        if data == None:
            return None

        for index, col_name in enumerate(self._db._table_descriptions[TABLE_CALLS]):
            result[col_name] = data[index]

        return result

    def __insert_callsign(self, input_data : dict) -> dict:
        """
        Inserts given callsign in the database.
        A duplicate check is not performed.
        """

        data = self._db.filter_dictionary(input_data, CALLSIGN_FIELDS)
        self._db.insert_in_table(TABLE_CALLS, data)
        return self.get_callsign(data[FIELD_CALLSIGN])

    def get_callsign_by_id(self, i_id : int) -> dict:
        """
        Retrieves the callsign and operator name by the given id.
        Returns a dictionary having all the record data.
        """
        sql = f'SELECT * FROM {TABLE_CALLS} WHERE {FIELD_ID}=?'
        with sqlite3.connect(self._db_full_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (i_id,))
            data = cursor.fetchone()
            cursor.close()

        if data == None:
            return None

        result = dict()

        for index, col_name in enumerate(self._db._table_descriptions[TABLE_CALLS]):
            result[col_name] = data[index]

        return result

    def get_or_add_callsign(self, input_data : dict) -> dict:
        """
        Looks for a given callsign (case insensitive) and returns one found.
        Creates a new record if callsign was not found.

        `data` - a dictionary containing the callsign data.
        """

        data = self._db.filter_dictionary(input_data, CALLSIGN_FIELDS)
        print(data)

        callsign = input_data[FIELD_CALLSIGN]
        if callsign == None or len(callsign.lstrip().rstrip()) == 0:
            raise ArgumentException('Callsign is a mandatory parameter.')

        result = self.get_callsign(callsign)
        if result != None:
            print(f'Callsign {callsign} is already in the database.')
            return result

        data[FIELD_CALLSIGN] = data[FIELD_CALLSIGN].upper()

        result = self.__insert_callsign(data) 
        print(f'Callsign {callsign} added.')
        return result

    def change_callsign(self, id : int, data : dict) -> dict:
        """
        Updates callsign data by its identifier.
        The `data` parameter is a dictionary containing the following values:
        - callsign
        - opname
        - email
        - address
        - source
        - has_data
        """

        if len(data[FIELD_CALLSIGN].lstrip().rstrip()) == 0:
            raise ArgumentException('Callsign is a mandatory parameter.')

        self._db.change_row_in_table(TABLE_CALLS, id, data)

    def delete_callsign_by_id(self, id : int) -> None:
        """
        Deletes a callsign by its identifier.
        Does nothing if identifier not found.
        """
        sql = f'DELETE FROM {TABLE_CALLS} WHERE {FIELD_ID}={id}'
        self._db.execute_non_query(sql)
        
    def delete_callsign_by_callsign(self, callsign : str) -> None:
        """
        Deletes a callsign by its identifier.
        Does nothing if identifier not found.
        """
        sql = f'DELETE FROM {TABLE_CALLS} WHERE {FIELD_CALLSIGN}=?'
        self._db.execute_non_query(sql, (callsign,))  

    def load_all_contacts(self, order_by_field : str = '') -> tuple[tuple, List[tuple]]:
        """
        Loads all contacts from the database.
        Returns a tuple containing all the fields
        and a list of tuples containing all the fetched rows.
        """

        sql = f'SELECT * FROM {TABLE_CONTACTS}'
        order_by = order_by_field.lstrip().rstrip()
        if len(order_by) > 0:
            sql += f' ORDER BY {order_by}'

        with sqlite3.connect(self._db_full_path,
                detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            result = (self._db._table_descriptions[TABLE_CONTACTS], cursor.fetchall())
            cursor.close()
            return result

    def calculate_checksum(self, data : dict) -> str:
        """Calculates checksum based on the values from the given dictionary."""
        content = f'{data[FIELD_CALLSIGN]}{data[FIELD_BAND]}{data[FIELD_MODE]}{data[FIELD_TIMESTAMP]}'
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def is_duplicate(self, data : dict) -> bool:
        """
        Checks whether the contact is a duplicate one.
        
        """
        checksum = self.calculate_checksum(data)
        sql = f'SELECT count(id) FROM {TABLE_CONTACTS} WHERE {FIELD_CHECKSUM}=?'
        count = self._db.execute_scalar(sql, (checksum,))
        return count != 0

    def log_contact(self, input_data : dict) -> None:
        """
        Inserts a contact into the db.
        A provided callsign is looked up in the database and callsign_id is stored.

        The contact will be ignored if it is considered a duplicate QSO.

        The following values can be present in the dictionary:
        - callsign (mandatory)
        - timestamp (mandatory)
        - frequency (or band)
        - band (or frequency)
        - mode (mandatory)
        - opname (optional)
        - rst_rcvd (optional)
        - rst_sent (optional)
        - is_run_qso (optional, `0` is inserted if omitted)
        The following fields are being filled automatically:
        - unique_id
        - dirty
        """

        if self.is_duplicate(input_data):
            return

        data = self._db.filter_dictionary(input_data, CONTACT_FIELDS)
        data[FIELD_CHECKSUM] = self.calculate_checksum(data)
        print(data)

        call_data = self.get_or_add_callsign(input_data)
        print(call_data)

        data[FIELD_UNIQUE_ID] = uuid.uuid4().hex
        data[FIELD_DIRTY] = 1
        data[FIELD_CALLSIGN] = data[FIELD_CALLSIGN].upper()
        self._db.insert_in_table(TABLE_CONTACTS, data)

    def get_contact_by_id(self, id : int) -> dict:
        """
        Retrieves a contact from the database.
        Returns a dictionary with column names as keys.
        Returns empty dictionary if no record is found.
        """
        sql = f'SELECT * FROM {TABLE_CONTACTS} WHERE id=?'

        with sqlite3.connect(self._db_full_path,
                detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id,))
            data = cursor.fetchall()
            cursor.close()

            result = dict()
            if len(data) == 0:
                return result

            row = data[0]
            for i in range(len(self._db._table_descriptions[TABLE_CONTACTS])):
                key = self._db._table_descriptions[TABLE_CONTACTS][i]
                result[key] = row[i]
            return result        

    def delete_contact_by_id(self, id : int) -> None:
        """Deletes a contact from the db."""
        if id:
            try:
                sql = f"delete from {TABLE_CONTACTS} where id=?"
                self._db.execute_non_query(sql, (id,))
            except sqlite3.Error as exception:
                logging.info("DataBase delete_contact: %s", exception)

    def delete_all_contacts(self) -> None:
        """Deletes all contacts from the database."""
        self._db.execute_non_query(f'DELETE FROM {TABLE_CONTACTS}')

    def change_contact(self, id: int, input_data : dict) -> None:
        """
        Changes a contact in the db by the given id.
        The following values can be present in the dictionary:
        - callsign
        - timestamp
        - frequency
        - band
        - mode
        - rst_rcvd
        - rst_sent
        - id
        """

        callsign_data = self.get_or_add_callsign(input_data)
        print(callsign_data)

        data = self._db.filter_dictionary(input_data, CONTACT_CHANGE_FIELDS)

        data[FIELD_CALLSIGN] = data[FIELD_CALLSIGN].upper()
        self._db.change_row_in_table(TABLE_CONTACTS, id, data)

