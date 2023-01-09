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
import unittest

from common.ApplicationPreferences import ApplicationPreferences
from logger.logger_constants import KEY_REALTIME, PREFERENCES_FILE_LOGGER
from logger.logger_preferences import LoggerApplicationPreferences

class  LoggerApplicationPreferencesTests(unittest.TestCase):
    """Represents a set of application preferences tests"""

    def test_CanWorkWithPreferences(self):
        """Tests possibility to read and write application preferences"""

        file = 'test.preferences'
        path = Path(f'./{file}')
        if path.exists():
            path.unlink()
        defaults = {'k1':'default_v1', 'k2':'default_v2'}
        pref0 = ApplicationPreferences(file, defaults)
        pref0.write_preferences() # default values should be written to disk
        
        pref1 = ApplicationPreferences(file, {})
        # check if default values were written to preferences file
        self.assertEqual(pref1.Preferences['k1'], 'default_v1')
        
        pref1.Preferences['k1'] = 'v1'
        pref1.Preferences['k2'] = 'v2'
        pref1.write_preferences()

        self.assertTrue(path.exists())

        pref2 = ApplicationPreferences(file, defaults)
        self.assertTrue('k1' in pref2.Preferences.keys())
        self.assertTrue('k2' in pref2.Preferences.keys())
        self.assertEqual(pref1.Preferences['k1'], pref2.Preferences['k1'])
        self.assertEqual(pref1.Preferences['k2'], pref2.Preferences['k2'])
        
    def test_CanWorkWithLoggerPreferences(self) -> None:
        """Tests how logger preferences can be read from and written to file."""

        # preferences should be created from scratch
        path = Path(f'./{PREFERENCES_FILE_LOGGER}')
        if path.exists():
            path.unlink()
        
        pref1 = LoggerApplicationPreferences()
        pref1.Utc = False
        pref1.Realtime = False
        pref1.DefaultMode = 'THROB'
        pref1.DefaultBand = '17m'

        pref1.write_preferences()

        pref2 = LoggerApplicationPreferences()
        self.assertEqual(pref1.Utc, pref2.Utc)
        self.assertEqual(pref1.Realtime, pref2.Realtime)
        self.assertEqual(pref1.DefaultMode, pref2.DefaultMode)
        self.assertEqual(pref1.DefaultBand, pref2.DefaultBand)

        self.assertEqual('17m', pref2.DefaultBand)
        self.assertEqual('THROB', pref2.DefaultMode)

        # cleanup
        path.unlink()
