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
from brandmeister.BmMonitorPreferences import BrandmeisterMonitorApplicationPreferences

from logger.logger_constants import KEY_REALTIME, PREFERENCES_FILE_LOGGER
from logger.logger_preferences import LoggerApplicationPreferences

class  BrandmeisterMonitorApplicationPreferencesTests(unittest.TestCase):
    """Represents a set of application preferences tests"""

    _path = Path(os.path.abspath("./test_data/bm_monitor"))

    def setUp(self):
        if self._path.exists():
            shutil.rmtree(str(self._path))
        self._path.mkdir()
        
    def tearDown(self) -> None:
        if self._path.exists():
            shutil.rmtree(str(self._path))
        return super().tearDown()

    def test_CanWorkWithMonitorPreferences(self):
        """Tests possibility to read and write application preferences"""

        file = 'preferences.json'
        pref0 = BrandmeisterMonitorApplicationPreferences(file)
        pref0.Directory = str(self._path)
        pref0.Callsigns = ['call1', 'call2']
        pref0.TalkGroups = [1,2]
        pref0.NoisyCalls = ['call3', 'call4']
        pref0.MinDurationSec = 3
        pref0.MinSilenceSec = 4
        pref0.Verbose = True
        
        pref0.write_preferences() # default values should be written to disk
        
        pref1 = BrandmeisterMonitorApplicationPreferences(file)
        pref1.Directory = str(self._path)
        self.assertEqual(2, len(pref1.Callsigns))
        self.assertTrue('call1' in pref1.Callsigns)
        self.assertTrue('call2' in pref1.Callsigns)
        
        self.assertTrue(1 in pref1.TalkGroups)
        self.assertTrue(2 in pref1.TalkGroups)

        self.assertTrue('call3' in pref1.NoisyCalls)
        self.assertTrue('call4' in pref1.NoisyCalls)
            