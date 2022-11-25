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

from typing import Tuple
from common.exceptions.ArgumentException import ArgumentException
import os
from pathlib import Path
import sqlite3
from common.exceptions.logger.CallsignNotFoundException import CallsignNotFoundException

from helpers.FileSystemHelper import FileSystemHelper

class LogDatabase(object):
    '''Class handles all requests to the database'''

    DB_VERSION_MAJOR : int = 1
    DB_VERSION_MINOR : int = 0

    _db_name : str
    _db_full_path : Path
    _connection : sqlite3.Connection

    def __init__(self, db_name : str) -> None:
        self._db_name = db_name
        self._db_full_path = FileSystemHelper.get_appdata_path('U2.Suite', create_if_not_exists=True) / db_name
        self.open_db(self._db_full_path)
        pass

    def __init__(self, path : Path, db_name : str) -> None:
        self._db_name = db_name
        self._db_full_path = path / db_name
        self.open_db(self._db_full_path)
        pass

    def open_db(self, path : Path) -> None:
        '''Opens the database. Creates the database if it does not exist.'''
        self.check_db(path)
        self._connection = sqlite3.connect(path)

    def check_db(self, path : Path) -> None:
        '''Check the presence of the database and creates it if it does not exist.'''
        if not os.path.exists(path):
            # a database does not exist. We have to create it first.
            self.create_db(path)

    def create_db(self, path : Path) -> None:
        '''Creates a database by the given path'''
        if os.path.exists(path):
            return

        try:
            p = str(path)
            sqlite_connection = sqlite3.connect(p)   

            # create a table for version
            sql = '''
CREATE TABLE "version" (
    "major" INTEGER,
    "minor" INTEGER
    );
'''
            self.execute_non_query(sqlite_connection, sql)
            sql = 'INSERT INTO version (major, minor) VALUES (?, ?)'
            self.execute_non_query(sqlite_connection, sql, (self.DB_VERSION_MAJOR, self.DB_VERSION_MINOR))

            # create a table for callsigns 
            sql = '''
CREATE TABLE "calls" (
	"id"	INTEGER,
	"callsign"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
            self.execute_non_query(sqlite_connection, sql)

            # create a table for QSO
            sql = '''
CREATE TABLE "qso" (
	"id"	INTEGER,
	"callsign_id"	INTEGER,
	"date"	INTEGER,
	"timestamp_utc"	INTEGER,
	"rcv"	TEXT,
	"snt"	TEXT,
	"comment"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''
            self.execute_non_query(sqlite_connection, sql)
        except sqlite3.Error as error:
            print("Error while connecting to the database.", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def execute_non_query(self, sqlite_connection : sqlite3.Connection, sql : str, params = ()) -> None:
        '''Executes given SQL against the database'''
        cursor = sqlite_connection.cursor()
        cursor.execute(sql, params)
        sqlite_connection.commit()
        cursor.close()

    def get_callsign(self, callsign : str) -> Tuple[int, str]:
        '''
        Looks for a given callsign in the database.
        Returns the callsign id if one is found.
        Returns 0 if callsign is absent in the database.

        '''
        cursor = self._connection.cursor()

        sql = 'SELECT id, name FROM calls WHERE callsign=? COLLATE NOCASE'
        cursor.execute(sql, (callsign,))
        data = cursor.fetchone()
        cursor.close()

        if data == None:
            return (0, '')

        return (data[0], data[1])

    def insert_callsign(self, callsign : str, name : str = '') -> Tuple[int, str]:
        '''
        Inserts given callsign in the database.
        A duplicate check is not performed.
        '''

        sql = 'INSERT INTO calls (callsign, name) VALUES (?, ?)'
        self.execute_non_query(self._connection, sql, (callsign, name))

        return self.get_callsign(callsign)

    def get_or_add_callsign(self, i_callsign : str, i_name : str = '') -> int:
        '''
        Looks for a given callsign (case insensitive) and returns one found.
        Creates a new record if callsign was not found.

        callsign - a callsign to be looked up (mandatory)
        name - a name of the operator (optional)
        '''

        if len(i_callsign.lstrip()) == 0:
            raise ArgumentException('Callsign is a mandatory parameter.')

        (id, name) = self.get_callsign(i_callsign)
        if id > 0:
            return (id, name)

        return self.insert_callsign(i_callsign, i_name) 

    def update_callsign(self, i_id : int, i_callsign : str, i_name : str) -> None:
        if len(i_callsign.lstrip()) == 0:
            raise ArgumentException('Callsign is a mandatory parameter.')

        sql = 'UPDATE calls SET callsign=?, name=? WHERE id=?'
        self.execute_non_query(self._connection, sql, (i_callsign, i_name, i_id))

