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

from datetime import datetime
import logging
import sqlite3
import semver

import brandmeister.bm_monitor_constants as const
from brandmeister.bm_monitor_core import MonitorReportData
from database.database_core import DatabaseCore
from database.database_options import DatabaseOptions
from pathlib import Path

BM_MONITOR_DEFAULT_DB_NAME = 'bm_monitor.sqlite'
TABLE_BM_MONITOR_REPORTS = 'bm_monitor_reports'
FIELD_BM_MONITOR_ID = 'id'
FIELD_BM_MONITOR_TIMESTAMP = 'timestamp'
FIELD_BM_MONITOR_TG = 'tg'
FIELD_BM_MONITOR_CALLSIGN = 'callsign'
FIELD_BM_MONITOR_DURATION = 'duration'

class BmMonitorDatabase:
    '''Represents a persistent storage for Brandmeister Monitor.'''
    
    _db : DatabaseCore
    _db_name : str
    _db_full_path : Path
    _db_version : str
    
    def __init__(self, path : Path, db_name : str = BM_MONITOR_DEFAULT_DB_NAME) -> None:
        self._db_version = '1.0.0'
        
        self._db_name = db_name
        if not path.exists():
            path.mkdir()
        self._db_full_path = path / db_name
        self._db = DatabaseCore(path, db_name)
        #options-related stuff must be created before using it
        self._options = DatabaseOptions(self._db)
        self._options.create_table()

        self._options.create_table()
        version = semver.VersionInfo.parse(self._db_version)
        self._options.get_or_insert_version(version)

        self._db._table_descriptions[TABLE_BM_MONITOR_REPORTS] = ( 
            FIELD_BM_MONITOR_ID,
            FIELD_BM_MONITOR_TIMESTAMP,
            FIELD_BM_MONITOR_CALLSIGN,
            FIELD_BM_MONITOR_TG,
            FIELD_BM_MONITOR_DURATION
            )

        # create a table for calls
        sql = (
            f'CREATE TABLE IF NOT EXISTS "{TABLE_BM_MONITOR_REPORTS}" ('
            f'"{FIELD_BM_MONITOR_ID}"	INTEGER PRIMARY KEY, '
            f'"{FIELD_BM_MONITOR_TIMESTAMP}"	TIMESTAMP, '
            f'"{FIELD_BM_MONITOR_CALLSIGN}"	TEXT, '
            f'"{FIELD_BM_MONITOR_TG}"     INT, '
            f'"{FIELD_BM_MONITOR_DURATION}"  INT'
            f');'
        )
        self._db.execute_non_query(sql)
        pass
    
    '''======================================================================'''
    def insert_report(self, data : MonitorReportData) -> int:
        '''
        Inserts a report in the database.
        
        Returns an identifier of the newly added record.
        '''
        values = {
            FIELD_BM_MONITOR_TIMESTAMP : datetime.utcnow(),
            FIELD_BM_MONITOR_CALLSIGN : data.Callsign,
            FIELD_BM_MONITOR_DURATION : data.Duration,
            FIELD_BM_MONITOR_TG : int(data.TG),
        }
        self._db.insert_in_table(TABLE_BM_MONITOR_REPORTS, values)
        return self._db.execute_scalar(f'SELECT max({FIELD_BM_MONITOR_ID}) FROM {TABLE_BM_MONITOR_REPORTS}')
    
    '''======================================================================'''
    def get_reports(self, filter : dict = {}, order_by : str = '') -> tuple[list, list]:
        '''
        Requests report records from the database.
        filter - a dictionary used to filter input. Used AND clause.
        order_by - a name of the field to sort by.
        '''
        result : list
        fields = ','.join(self._db._table_descriptions[TABLE_BM_MONITOR_REPORTS])
        sql = f'SELECT {fields} FROM {TABLE_BM_MONITOR_REPORTS}'
        sql_values = []
        if filter != None and len(filter.keys()) > 0:
            sql_fields = ' AND '.join([f'{key}=?' for key in filter])
            sql_values = [filter[key] for key in filter]
            sql += f' WHERE {sql_fields}'
        if len(order_by) > 0:
            sql += f' ORDER BY {order_by}'

        try:
            with sqlite3.connect(self._db_full_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, sql_values)
                result = (self._db._table_descriptions[TABLE_BM_MONITOR_REPORTS], cursor.fetchall())
                cursor.close()
        except sqlite3.Error as ex:
            logging.exception(f'SqLite error: {ex}')

        return result
    