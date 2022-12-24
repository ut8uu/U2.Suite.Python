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

class  LoggerApplicationPreferences(unittest.TestCase):
    '''Represents a set of application preferences tests'''

    def test_CanWorkWithPreferences(self):
        '''Tests possibility to reaed and write application preferences'''

        file = 'test.preferences'
        path = Path(f'./{file}')
        if path.exists():
            path.unlink()
        initial_data = {'k1' : 'v1', 'k2' : 'v2'}
        pref1 = ApplicationPreferences(file, initial_data)

        self.assertTrue(path.exists())

        pref2 = ApplicationPreferences(file, initial_data)
        self.assertTrue('k1' in pref2.Preferences.keys())
        self.assertTrue('k2' in pref2.Preferences.keys())
        self.assertEqual(pref1.Preferences['k1'], pref2.Preferences['k1'])
        self.assertEqual(pref1.Preferences['k2'], pref2.Preferences['k2'])
        