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
from logger.logger_constants import KEY_CALLSIGNS, KEY_MIN_DURATION, KEY_TALK_GROUPS, KEY_VERBOSE, PREFERENCES_FILE_BM_MONITOR


class LoggerApplicationPreferences(ApplicationPreferences):
    '''
    Represents logger application preferences.
    Be aware, although preferences are autometically loaded upon object creation,
    it is required to save them explicitly. This is required to prevent breaking
    the file during two or more simultaneous implicit commits.
    '''
    
    def __init__(self) -> None:
        self._default_values = {
            }
        super().__init__(PREFERENCES_FILE_BM_MONITOR, self._default_values)

    @property
    def TalkGroups(self) -> list[str]:
        return self.get_bool_value(KEY_TALK_GROUPS, False)
    @TalkGroups.setter
    def TalkGroups(self, value : list[str]) -> None:
        self.Preferences[KEY_TALK_GROUPS] = value
        
    @property
    def Callsigns(self) -> list[str]:
        return self.get_bool_value(KEY_CALLSIGNS, False)
    @Callsigns.setter
    def Callsigns(self, value : list[str]) -> None:
        self.Preferences[KEY_CALLSIGNS] = value
        
    @property
    def MinDurationSec(self) -> int:
        return self.get_bool_value(KEY_MIN_DURATION, False)
    @MinDurationSec.setter
    def MinDurationSec(self, value : int) -> None:
        self.Preferences[KEY_MIN_DURATION] = value
        
    @property
    def Verbose(self) -> bool:
        return self.get_bool_value(KEY_VERBOSE, False)
    @Verbose.setter
    def Verbose(self, value : bool) -> None:
        self.Preferences[KEY_VERBOSE] = value
        
