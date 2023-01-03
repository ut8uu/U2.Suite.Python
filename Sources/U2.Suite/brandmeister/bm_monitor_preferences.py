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
from logger.logger_constants import KEY_CALLSIGNS, KEY_MIN_DURATION, KEY_MIN_SILENCE, KEY_NOISY_CALLS, KEY_NOTIFY_DAPNET, KEY_NOTIFY_DISCORD, KEY_NOTIFY_DISCORD_WH_URL, KEY_NOTIFY_PUSHOVER, KEY_NOTIFY_TELEGRAM, KEY_TALK_GROUPS, KEY_USE_CALLSIGNS, KEY_USE_TALK_GROUPS, KEY_VERBOSE, PREFERENCES_FILE_BM_MONITOR


class BrandmeisterMonitorApplicationPreferences(ApplicationPreferences):
    '''
    Represents logger application preferences.
    Be aware, although preferences are autometically loaded upon object creation,
    it is required to save them explicitly. This is required to prevent breaking
    the file during two or more simultaneous implicit commits.
    '''
    
    def __init__(self, file : str = PREFERENCES_FILE_BM_MONITOR) -> None:
        self._default_values = {
            KEY_NOTIFY_DISCORD : False,
            KEY_NOTIFY_DISCORD_WH_URL : '',
            KEY_NOTIFY_DAPNET : False,
            KEY_NOTIFY_PUSHOVER : False,
            KEY_NOTIFY_TELEGRAM : False,
            KEY_VERBOSE : True,
            KEY_USE_CALLSIGNS : False,
            KEY_CALLSIGNS : [],
            KEY_NOISY_CALLS : [],
            KEY_USE_TALK_GROUPS : False,
            KEY_TALK_GROUPS : ['91'],
            KEY_MIN_SILENCE : 300,
            KEY_MIN_DURATION : 5
            }
        super().__init__(file, self._default_values)

    @property
    def UseTalkGroups(self) -> bool:
        return self.get_bool_value(KEY_USE_TALK_GROUPS, False)
    @UseTalkGroups.setter
    def UseTalkGroups(self, value : bool) -> None:
        self.Preferences[KEY_USE_TALK_GROUPS] = value

    @property
    def TalkGroups(self) -> list[str]:
        return self.get_list_value(KEY_TALK_GROUPS, False)
    @TalkGroups.setter
    def TalkGroups(self, value : list[str]) -> None:
        self.Preferences[KEY_TALK_GROUPS] = value
        
    @property
    def NoisyCalls(self) -> list[str]:
        return self.get_list_value(KEY_NOISY_CALLS, False)
    @NoisyCalls.setter
    def NoisyCalls(self, value : list[str]) -> None:
        self.Preferences[KEY_NOISY_CALLS] = value
        
    @property
    def UseCallsigns(self) -> bool:
        return self.get_bool_value(KEY_USE_CALLSIGNS, False)
    @UseCallsigns.setter
    def UseCallsigns(self, value : bool) -> None:
        self.Preferences[KEY_USE_CALLSIGNS] = value

    @property
    def Callsigns(self) -> list[str]:
        return self.get_list_value(KEY_CALLSIGNS, False)
    @Callsigns.setter
    def Callsigns(self, value : list[str]) -> None:
        self.Preferences[KEY_CALLSIGNS] = value
        
    @property
    def MinDurationSec(self) -> int:
        return self.get_int_value(KEY_MIN_DURATION, False)
    @MinDurationSec.setter
    def MinDurationSec(self, value : int) -> None:
        self.Preferences[KEY_MIN_DURATION] = value
        
    @property
    def Verbose(self) -> bool:
        return self.get_bool_value(KEY_VERBOSE, False)
    @Verbose.setter
    def Verbose(self, value : bool) -> None:
        self.Preferences[KEY_VERBOSE] = value
        
    @property
    def MinSilenceSec(self) -> int:
        return self.get_int_value(KEY_MIN_SILENCE, False)
    @MinSilenceSec.setter
    def MinSilenceSec(self, value : int) -> None:
        self.Preferences[KEY_MIN_SILENCE] = value
        
    @property
    def NotifyDapnet(self) -> bool:
        return self.get_bool_value(KEY_NOTIFY_DAPNET, False)
    @NotifyDapnet.setter
    def NotifyDapnet(self, value : bool) -> None:
        self.Preferences[KEY_NOTIFY_DAPNET] = value
        
    @property
    def NotifyDiscord(self) -> bool:
        return self.get_bool_value(KEY_NOTIFY_DISCORD, False)
    @NotifyDiscord.setter
    def NotifyDiscord(self, value : bool) -> None:
        self.Preferences[KEY_NOTIFY_DISCORD] = value
        
    @property
    def NotifyDiscordWhUrl(self) -> str:
        return self.get_string_value(KEY_NOTIFY_DISCORD_WH_URL, False)
    @NotifyDiscordWhUrl.setter
    def NotifyDiscordWhUrl(self, value : str) -> None:
        self.Preferences[KEY_NOTIFY_DISCORD_WH_URL] = value
        
    @property
    def NotifyPushover(self) -> bool:
        return self.get_bool_value(KEY_NOTIFY_PUSHOVER, False)
    @NotifyPushover.setter
    def NotifyPushover(self, value : bool) -> None:
        self.Preferences[KEY_NOTIFY_PUSHOVER] = value
        
    @property
    def NotifyTelegram(self) -> bool:
        return self.get_bool_value(KEY_NOTIFY_TELEGRAM, False)
    @NotifyTelegram.setter
    def NotifyTelegram(self, value : bool) -> None:
        self.Preferences[KEY_NOTIFY_TELEGRAM] = value
        
