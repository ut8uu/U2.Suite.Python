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

from common.ApplicationPreferences import ApplicationPreferences
from logger.logger_constants import KEY_DEFAULT_BAND, KEY_DEFAULT_MODE, KEY_REALTIME, KEY_UTC, PREFERENCES_FILE_LOGGER


class LoggerApplicationPreferences(ApplicationPreferences):
    '''Represents logger application preferences.'''
    
    def __init__(self) -> None:
        self._default_values = {
                KEY_UTC : str(True),
                KEY_REALTIME : str(True),
                KEY_DEFAULT_BAND : '160m',
                KEY_DEFAULT_MODE : 'SSB'
            }
        super().__init__(PREFERENCES_FILE_LOGGER)

    @property
    def Realtime(self) -> bool:
        return self.get_bool_value(KEY_REALTIME, False)
    @Realtime.setter
    def Realtime(self, value : bool) -> None:
        self.Preferences[KEY_REALTIME] = value
        
    @property
    def Utc(self) -> bool:
        return self.get_bool_value(KEY_UTC, False)
    @Utc.setter
    def Utc(self, value : bool) -> None:
        self.Preferences[KEY_UTC] = value
        
    @property
    def DefaultMode(self) -> str:
        return self.get_bool_value(KEY_DEFAULT_MODE, 'AM')
    @DefaultMode.setter
    def DefaultMode(self, value : str) -> None:
        self.Preferences[KEY_DEFAULT_MODE] = value
        
    @property
    def DefaultBand(self) -> str:
        return self.get_bool_value(KEY_DEFAULT_BAND, '160m')
    @DefaultBand.setter
    def DefaultBand(self, value : str) -> None:
        self.Preferences[KEY_DEFAULT_BAND] = value
        
    