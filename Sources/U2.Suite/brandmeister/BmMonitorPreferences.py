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
from common.ApplicationPreferences import ApplicationPreferences
import brandmeister.BmMonitorConstants as bm_const

class BrandmeisterMonitorApplicationPreferences(ApplicationPreferences):
    """
    Represents logger application preferences.
    Be aware, although preferences are autometically loaded upon object creation,
    it is required to save them explicitly. This is required to prevent breaking
    the file during two or more simultaneous implicit commits.
    """
    
    def __init__(self, file : str = bm_const.PREFERENCES_FILE_BM_MONITOR) -> None:
        self._default_values = {
            bm_const.KEY_LOG_LEVEL : 'ERROR',
            bm_const.KEY_NOTIFY_DISCORD : False,
            bm_const.KEY_NOTIFY_DISCORD_WH_URL : '',
            bm_const.KEY_NOTIFY_DAPNET : False,
            bm_const.KEY_NOTIFY_PUSHOVER : False,
            bm_const.KEY_NOTIFY_TELEGRAM : False,
            bm_const.KEY_VERBOSE : True,
            bm_const.KEY_USE_CALLSIGNS : False,
            bm_const.KEY_CALLSIGNS : [],
            bm_const.KEY_NOISY_CALLS : [],
            bm_const.KEY_USE_TALK_GROUPS : True,
            bm_const.KEY_DISPLAY_ALL_TALK_GROUPS : True,
            bm_const.KEY_TALK_GROUPS : [91],
            bm_const.KEY_MIN_SILENCE : 300,
            bm_const.KEY_MIN_DURATION : 5,
            bm_const.KEY_PATH_TO_DATABASE : os.path.abspath("./"),
            bm_const.KEY_SAVE_TO_DATABASE : True,
            bm_const.KEY_SAVE_TO_DATABASE_LIMIT : bm_const.DB_LIMIT_NO_LIMIT,
            bm_const.KEY_USE_COUNTRIES : False,
            bm_const.KEY_COUNTRIES : []
            }
        super().__init__(file, self._default_values)

    @property
    def LogLevel(self) -> str:
        level = self.get_string_value(bm_const.KEY_LOG_LEVEL, 'ERROR')
        if level is None or len(level) == 0:
            level = 'ERROR'
            self._preferences[bm_const.KEY_LOG_LEVEL] = level
            self.write_preferences()
        return level
        
    @property
    def PathToDatabase(self) -> str:
        path = self.get_string_value(bm_const.KEY_PATH_TO_DATABASE, '')
        if path is None or len(path) == 0:
            path = os.path.abspath("./")
            self._preferences[bm_const.KEY_PATH_TO_DATABASE] = path
            self.write_preferences()
        return path
    @PathToDatabase.setter
    def PathToDatabase(self, value) -> None:
        self.get_string_value(bm_const.KEY_PATH_TO_DATABASE, value)
        
    @property
    def SaveToDatabase(self) -> bool:
        return self.get_bool_value(bm_const.KEY_SAVE_TO_DATABASE, True)
    @SaveToDatabase.setter
    def SaveToDatabase(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_SAVE_TO_DATABASE] = value

    @property
    def SaveToDatabaseLimit(self) -> str:
        limit = self.get_string_value(bm_const.KEY_SAVE_TO_DATABASE_LIMIT, bm_const.DB_LIMIT_NO_LIMIT)
        if len(limit) == None:
            limit = bm_const.DB_LIMIT_NO_LIMIT
        return limit
    @SaveToDatabaseLimit.setter
    def SaveToDatabaseLimit(self, value : str) -> None:
        self.Preferences[bm_const.KEY_SAVE_TO_DATABASE_LIMIT] = value

    @property
    def UseTalkGroups(self) -> bool:
        return self.get_bool_value(bm_const.KEY_USE_TALK_GROUPS, False)
    @UseTalkGroups.setter
    def UseTalkGroups(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_USE_TALK_GROUPS] = value

    @property
    def DisplayAllTalkGroups(self) -> bool:
        return self.get_bool_value(bm_const.KEY_DISPLAY_ALL_TALK_GROUPS, False)
    @DisplayAllTalkGroups.setter
    def DisplayAllTalkGroups(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_DISPLAY_ALL_TALK_GROUPS] = value

    @property
    def TalkGroups(self) -> list[str]:
        return self.get_list_value(bm_const.KEY_TALK_GROUPS, [])
    @TalkGroups.setter
    def TalkGroups(self, value : list[str]) -> None:
        self.Preferences[bm_const.KEY_TALK_GROUPS] = value
        
    @property
    def Countries(self) -> list[str]:
        return self.get_list_value(bm_const.KEY_COUNTRIES, [])
    @Countries.setter
    def Countries(self, value : list[str]) -> None:
        self.Preferences[bm_const.KEY_COUNTRIES] = value
        
    @property
    def NoisyCalls(self) -> list[str]:
        return self.get_list_value(bm_const.KEY_NOISY_CALLS, [])
    @NoisyCalls.setter
    def NoisyCalls(self, value : list[str]) -> None:
        self.Preferences[bm_const.KEY_NOISY_CALLS] = value
        
    @property
    def UseCallsigns(self) -> bool:
        return self.get_bool_value(bm_const.KEY_USE_CALLSIGNS, False)
    @UseCallsigns.setter
    def UseCallsigns(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_USE_CALLSIGNS] = value

    @property
    def UseCountries(self) -> bool:
        return self.get_bool_value(bm_const.KEY_USE_COUNTRIES, False)
    @UseCountries.setter
    def UseCountries(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_USE_COUNTRIES] = value

    @property
    def Callsigns(self) -> list[str]:
        return self.get_list_value(bm_const.KEY_CALLSIGNS, False)
    @Callsigns.setter
    def Callsigns(self, value : list[str]) -> None:
        self.Preferences[bm_const.KEY_CALLSIGNS] = value
        
    @property
    def MinDurationSec(self) -> int:
        return self.get_int_value(bm_const.KEY_MIN_DURATION, 5)
    @MinDurationSec.setter
    def MinDurationSec(self, value : int) -> None:
        self.Preferences[bm_const.KEY_MIN_DURATION] = value
        
    @property
    def Verbose(self) -> bool:
        return self.get_bool_value(bm_const.KEY_VERBOSE, False)
    @Verbose.setter
    def Verbose(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_VERBOSE] = value
        
    @property
    def MinSilenceSec(self) -> int:
        return self.get_int_value(bm_const.KEY_MIN_SILENCE, 300)
    @MinSilenceSec.setter
    def MinSilenceSec(self, value : int) -> None:
        self.Preferences[bm_const.KEY_MIN_SILENCE] = value
        
    @property
    def NotifyDapnet(self) -> bool:
        return self.get_bool_value(bm_const.KEY_NOTIFY_DAPNET, False)
    @NotifyDapnet.setter
    def NotifyDapnet(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_NOTIFY_DAPNET] = value
        
    @property
    def NotifyDiscord(self) -> bool:
        return self.get_bool_value(bm_const.KEY_NOTIFY_DISCORD, False)
    @NotifyDiscord.setter
    def NotifyDiscord(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_NOTIFY_DISCORD] = value
        
    @property
    def NotifyDiscordWhUrl(self) -> str:
        return self.get_string_value(bm_const.KEY_NOTIFY_DISCORD_WH_URL, False)
    @NotifyDiscordWhUrl.setter
    def NotifyDiscordWhUrl(self, value : str) -> None:
        self.Preferences[bm_const.KEY_NOTIFY_DISCORD_WH_URL] = value
        
    @property
    def NotifyPushover(self) -> bool:
        return self.get_bool_value(bm_const.KEY_NOTIFY_PUSHOVER, False)
    @NotifyPushover.setter
    def NotifyPushover(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_NOTIFY_PUSHOVER] = value
        
    @property
    def NotifyTelegram(self) -> bool:
        return self.get_bool_value(bm_const.KEY_NOTIFY_TELEGRAM, False)
    @NotifyTelegram.setter
    def NotifyTelegram(self, value : bool) -> None:
        self.Preferences[bm_const.KEY_NOTIFY_TELEGRAM] = value
        
