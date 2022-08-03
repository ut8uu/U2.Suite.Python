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

import re

class ConversionHelper():
    
    @staticmethod
    def HexStrToBytes(s : str) -> bytearray:
        prepared = re.sub('[^0-9a-f]', '', s)
        if (len(prepared) % 2 != 0):
            return []
        return bytearray.fromhex(prepared)
    
    @staticmethod
    def StrToBytes(s : str) -> bytearray:
        if (len(s) == 0):
            return []
        
        trimmed = s.strip()
        if (trimmed.startswith('(')):
            trimmed = trimmed.strip('(').strip(')')
            trimmed = trimmed.replace('.', chr(0))
            return bytearray([ord(f) for f in trimmed])
        
        elif ('0123456789abcdef'.find(trimmed[0].lower()) > -1):
            return ConversionHelper.HexStrToBytes(trimmed)