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

MODE_AM = 'AM'
MODE_CW = 'CW'
MODE_DIGITALVOICE = 'DIGITALVOICE'
MODE_FM = 'FM'
MODE_FT4 = 'FT4'
MODE_FT8 = 'FT8'
MODE_OLIVIA = 'OLIVIA'
MODE_RTTY = 'RTTY'
MODE_SSB = 'SSB'
MODE_THOR = 'THOR'
MODE_THROB = 'THROB'

ALL_MODES = (MODE_AM, MODE_CW, MODE_DIGITALVOICE, MODE_FM, MODE_FT4, MODE_FT8,
            MODE_OLIVIA, MODE_RTTY, MODE_SSB, MODE_THOR, MODE_THROB)

BAND_160 = '160m'
BAND_80 = '80m'
BAND_60 = '60m'
BAND_40 = '40m'
BAND_30 = '30m'
BAND_20 = '20m'
BAND_17 = '17m'
BAND_15 = '15m'
BAND_12 = '12m'
BAND_10 = '10m'
BAND_6 = '6m'
BAND_4 = '4m'
BAND_2 = '2m'
BAND_70 = '70cm'

ALL_BANDS = (BAND_160, BAND_80, BAND_60, BAND_40, 
            BAND_30, BAND_20, BAND_17, BAND_15, 
            BAND_12, BAND_10, BAND_6, BAND_4, 
            BAND_2, BAND_70)

DISPLAY_FORMAT_MMDDYY_HHMMSS_AP = 'MM/dd/yyyy hh:mm:ss AP'
DISPLAY_FORMAT_MMDDYY_HHMMSS = 'MM/dd/yyyy HH:mm:ss'
DISPLAY_FORMAT_DDMMYY_HHMMSS_AP = 'dd.MM.yyyy hh:mm:ss AP'
DISPLAY_FORMAT_DDMMYY_HHMMSS = 'dd.MM.yyyy HH:mm:ss'

DATABASE_DEFAULT = 'default.sqlite'

KEY_MYCALLSIGN = 'mycallsign'
KEY_MYGRID = 'mygrid'
KEY_DEFAULT_MODE = 'mode'
KEY_DEFAULT_SATELLITE = 'satellite'

PREFERENCES_FILE = 'FastSatEntry_preferences.json'

UNIQUE_ID_FAST_SAT_ENTRY = 'U2.Suite.FastSatEntry'

TABLE_CALLS = 'calls'
TABLE_CONTACTS = 'contacts'
TABLE_OPTIONS = 'options'
TABLE_VERSION = 'version'

FIELD_ADDRESS = 'address'
FIELD_BAND = 'band'
FIELD_CALLSIGN = 'callsign'
FIELD_CALLSIGN_ID = 'callsign_id'
FIELD_DIRTY = 'dirty'
FIELD_EMAIL = 'email'
FIELD_FREQUENCY = 'frequency'
FIELD_HAS_DATA = 'has_data'
FIELD_ID = 'id'
FIELD_IS_RUN_QSO = 'is_run_qso'
FIELD_MODE = 'mode'
FIELD_OPNAME = 'opname'
FIELD_RST_SENT = 'rst_sent'
FIELD_RST_RCVD = 'rst_rcvd'
FIELD_SOURCE = 'source'
FIELD_TIMESTAMP = 'timestamp'
FIELD_UNIQUE_ID = 'unique_id'
FIELD_KEY = 'key'
FIELD_VALUE = 'value'
FIELD_VERSION_MAJOR = 'major'
FIELD_VERSION_MINOR = 'minor'

OPTION_VERSION = 'version'
OPTION_STATION_CALLSIGN = 'station_callsign'
OPTION_OPERATOR_NAME = 'operator_name'

CALLSIGN_FIELDS = (FIELD_CALLSIGN, FIELD_OPNAME, FIELD_EMAIL, FIELD_ADDRESS, FIELD_HAS_DATA, FIELD_SOURCE)
CONTACT_FIELDS = (FIELD_BAND, FIELD_CALLSIGN, FIELD_DIRTY, FIELD_FREQUENCY, FIELD_IS_RUN_QSO,
                    FIELD_MODE, FIELD_OPNAME, FIELD_RST_RCVD, FIELD_RST_SENT, FIELD_TIMESTAMP)
CONTACT_CHANGE_FIELDS = (FIELD_BAND, FIELD_CALLSIGN, FIELD_FREQUENCY, 
                    FIELD_MODE, FIELD_OPNAME, FIELD_RST_RCVD, FIELD_RST_SENT, FIELD_TIMESTAMP)
