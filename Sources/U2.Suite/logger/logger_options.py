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

from database.database_core import DatabaseCore
from database.database_options import DatabaseOptions
from logger.logger_constants import OPTION_OPERATOR_NAME, OPTION_STATION_CALLSIGN


if __name__ == '__main__':
    print('This module cannot be executed directly')
    exit(0)

class LoggerOptions(object):
    '''Represents a logger options keeper class.'''

    _db : DatabaseCore
    _options : DatabaseOptions
    _station_callsign : str
    _operator_name : str

    def __init__(self, db : DatabaseCore) -> None:
        self._db = db
        self._options = DatabaseOptions(self._db)
        self._station_callsign = self._options.get_or_insert_option(OPTION_STATION_CALLSIGN)
        self._operator_name = self._options.get_or_insert_option(OPTION_OPERATOR_NAME)
        pass

    @property
    def StationCallsign(self) -> str:
        return self._station_callsign
    @StationCallsign.setter
    def StationCallsign(self, value):
        self._station_callsign = value
        self._options.update_or_insert_option(OPTION_STATION_CALLSIGN, value)

    @property
    def OperatorName(self) -> str:
        return self._operator_name
    @OperatorName.setter
    def OperatorName(self, value):
        self._operator_name = value
        self._options.update_or_insert_option(OPTION_OPERATOR_NAME, value)


