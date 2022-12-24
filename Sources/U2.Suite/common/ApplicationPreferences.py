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


class ApplicationPreferences(object):
    '''
    Represents base class for application preferences.
    The preferences data is stored in the <filename>.json file
    and is a simple key-value storage.
    '''

    _file : str
    _preferences : dict
    _reference_preference : dict

    def __init__(self, file : str, initial_data : dict) -> None:
        self._file = file
        self._preferences = initial_data
        self._reference_preference = self._preferences.copy()
        self.read_preferences()
        pass

    @property
    def Preferences(self) -> dict:
        return self._preferences

    def read_preferences(self):
        '''Reads preferences from the given file.'''
        try:
            preferences_file_name = f'./{self._file}'
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
        except IOError as exception:
            logging.critical("Error: %s", exception)

    def write_preferences(self):
        '''
        Writes the preferences to file. 
        Existing file is being overwritten, not existing is being created.
        '''
        with open(f'./{self._file}', "wt", encoding="utf-8") as file_descriptor:
            self._preferences = self._reference_preference.copy()
            file_descriptor.write(dumps(self._preferences, indent=4))
            logging.info("%s", self._preferences)


