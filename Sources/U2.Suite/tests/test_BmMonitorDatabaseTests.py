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
import shutil
import unittest
from brandmeister.bm_monitor_constants import KEY_CALLSIGN, KEY_DURATION, KEY_TALK_GROUP
from brandmeister.bm_monitor_core import MonitorReportData

from brandmeister.bm_monitor_database import FIELD_BM_MONITOR_CALLSIGN, FIELD_BM_MONITOR_DURATION, FIELD_BM_MONITOR_TG, BmMonitorDatabase

class DatabaseTests(unittest.TestCase):
    '''A database-related unit tests'''

    _db_name : str
    _path : Path
    _full_path : Path

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self):
        self._db_name = 'test.db'
        self._path = self.GetPathToDatabase()
        if self._path.exists():
            shutil.rmtree(str(self._path))

        self._full_path = self._path / self._db_name
        if self._path.exists():
            try:
                self._full_path.unlink()
            except:
                print(f'Cannot remove file {self._full_path}')

    def tearDown(self) -> None:
        if self._path.exists():
            try:
                path = str(self.GetPathToDatabase())
                shutil.rmtree(path)
            except:
                print(f'Cannot remove directory {path}')
        
        return super().tearDown()

    def GetPathToDatabase(self) -> Path:
        '''Calculates the full path to the database'''
        return Path(os.path.abspath("./test_data/bm_monitor_database_tests"))

    def test_DatabaseCreatedAutomatically(self) -> None:
        '''A callsigns-related test'''
        self.assertFalse(self._full_path.exists())
        db = BmMonitorDatabase(self.GetPathToDatabase())
        self.assertTrue(self._full_path.exists())

    def test_CanInsertReports(self) -> None:
        '''This is to test how reports can be inserted.'''
        db = BmMonitorDatabase(self.GetPathToDatabase())
        reports = db.get_reports()
        self.assertEqual(0, len(reports[1]))
        
        report_data = {
            KEY_CALLSIGN : 'UT8UU',
            KEY_TALK_GROUP : '91',
            KEY_DURATION : 20,
        }
        report = MonitorReportData(report_data)
        db.insert_report(report)
        
        reports = db.get_reports()
        self.assertEqual(1, len(reports[1]))
        
    def insert_data(self, db: BmMonitorDatabase, callsign, tg, duration) -> None:
        report_data = {
            KEY_CALLSIGN : callsign,
            KEY_TALK_GROUP : tg,
            KEY_DURATION : duration,
        }
        report = MonitorReportData(report_data)
        db.insert_report(report)
    
    def test_CanFilterAndSort(self) -> None:
        db = BmMonitorDatabase(self.GetPathToDatabase())
        self.insert_data(db, 'UT8UU', 91, 10)
        self.insert_data(db, 'UT8UU', 50, 5)
        self.insert_data(db, 'UT1UU', 100, 1)

        # 1. in order of insertion
        reports = db.get_reports()
        self.assertEqual(3, len(reports[1]))
        callsign_index = reports[0].index(FIELD_BM_MONITOR_CALLSIGN)
        duration_index = reports[0].index(FIELD_BM_MONITOR_DURATION)
        tg_index = reports[0].index(FIELD_BM_MONITOR_TG)
        row0 = reports[1][0]
        self.assertEqual('UT8UU', row0[callsign_index])
        self.assertEqual(91, row0[tg_index])
        self.assertEqual(10, row0[duration_index])
        
        # 2. filtered by callsign
        reports = db.get_reports({KEY_CALLSIGN : 'UT1UU'})
        self.assertEqual(1, len(reports[1]))
        row0 = reports[1][0]
        self.assertEqual('UT1UU', row0[callsign_index])

        # 3. ordered by callsign
        reports = db.get_reports({}, FIELD_BM_MONITOR_CALLSIGN)
        self.assertEqual(3, len(reports[1]))
        row0 = reports[1][0]
        self.assertEqual('UT1UU', row0[callsign_index])
                
        # 4. ordered by TG
        reports = db.get_reports({}, FIELD_BM_MONITOR_TG)
        self.assertEqual(3, len(reports[1]))
        row0 = reports[1][0]
        self.assertEqual('UT8UU', row0[callsign_index])
        self.assertEqual(50, row0[tg_index])
        self.assertEqual(5, row0[duration_index])

        
