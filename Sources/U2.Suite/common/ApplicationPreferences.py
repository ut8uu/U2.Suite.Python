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

from json import dumps, loads
import logging
import os
from pathlib import Path

from PyQt5.QtCore import pyqtSignal, QObject

class PreferencesChangedEvent(QObject):
    changed = pyqtSignal()

class ApplicationPreferences(object):
    '''
    Represents base class for application preferences.
    The preferences data is stored in the <filename>.json file
    and is a simple key-value storage.
    '''

    _preferences_changed : PreferencesChangedEvent
    _preferences_loaded : bool
    _directory : str = './'
    _file : str
    _preferences : dict
    _default_values : dict

    def __init__(self, file : str, default_values : dict) -> None:
        self._preferences_changed = PreferencesChangedEvent()
        self._preferences_loaded = False
        self._file = file
        self._default_values = default_values
        self._preferences = self._default_values.copy()
        pass
    
    @property
    def PreferencesChanged(self) -> PreferencesChangedEvent:
        return self._preferences_changed
    
    @property
    def Directory(self) -> str:
        '''
        A directory for BmMonitor preferences.
        By default it's a current directory (./).
        No trailing slashes, please.
        '''
        return self._directory
    @Directory.setter
    def Directory(self, path : str) -> None:
        '''
        A directory for BmMonitor preferences.
        By default it's a current directory (./).
        No trailing slashes, please.
        '''
        self._directory = path

    @property
    def DefaultValues(self) -> dict:
        return self._default_values

    @property
    def Preferences(self) -> dict:
        if not self._preferences_loaded:
            self.read_preferences()
        return self._preferences

    '''====================================================================='''
    def read_preferences(self):
        '''Reads preferences from the given file.'''
        try:
            path = Path(self._directory) / self._file
            preferences_file_name = str(path)
            if os.path.exists(preferences_file_name):
                with open(preferences_file_name, "rt", encoding="utf-8") as file_descriptor:
                    content = file_descriptor.read()
                    if len(content) == 0:
                        self.write_preferences()
                    else:
                        self._preferences = loads(content)
                        logging.info("%s", self._preferences)
            else:
                logging.info("No preference file. Writing preference.")
                self.write_preferences()
            self._preferences_loaded = True
        except IOError as exception:
            logging.critical("Error: %s", exception)

    '''====================================================================='''
    def write_preferences(self):
        '''
        Writes the preferences to file. 
        Existing file is being overwritten, not existing is being created.
        '''
        path = Path(self._directory) / self._file
        preferences_file_name = str(path)
        with open(preferences_file_name, "wt", encoding="utf-8") as file_descriptor:
            file_descriptor.write(dumps(self._preferences, indent=4))
            logging.info("%s", self._preferences)
            
        self._preferences_changed.changed.emit()

    '''====================================================================='''
    def get_string_value(self, key : str, default_value : str = '') -> str:
        '''
        Performs an attempt to get the preference by the given name.
        If preference not found, a default value will be returned.
        '''
        try:
            result = self.Preferences.get(key)
            if result != None:
                return result
            return default_value
        except KeyError:
            return default_value

    '''====================================================================='''
    def get_int_value(self, key : str, default_value : int = 0) -> int:
        '''
        Performs an attempt to get the preference by the given name.
        If preference not found, a default value will be returned.
        '''
        try:
            return int(self.Preferences.get(key))
        except KeyError:
            return default_value

    '''====================================================================='''
    def get_list_value(self, key : str, default_value : list = []) -> list:
        '''
        Performs an attempt to get the preference by the given name.
        If preference not found, a default value will be returned.
        '''
        try:
            list_data = self.Preferences.get(key)
            if list_data == None:
                return default_value
            return list(list_data)
        except KeyError:
            return default_value

    '''====================================================================='''
    def get_bool_value(self, key : str, default_value : bool) -> bool:
        value = self.get_string_value(key, default_value)
        if type(value) is bool:
            return value
        if value is None:
            return default_value
        if value.lower() == str(True).lower():
            return True
        elif value.lower() == str(False).lower():
            return False
        else:
            return default_value

