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

from helpers.ConversionHelper import ConversionHelper as ch

def test_hex_str_to_bytes():
    expected = bytearray(b'ABC')
    actual = ch.HexStrToBytes('414243')
    assert expected == actual
    actual = ch.HexStrToBytes('41.42.43')
    assert expected == actual
    actual = ch.HexStrToBytes('41 42 43')
    assert expected == actual
    
    expected = []
    actual = ch.HexStrToBytes('411') # odd number of characters
    assert expected == actual
    actual = ch.HexStrToBytes('41.1') # odd number with a dot
    assert expected == actual
    actual = ch.HexStrToBytes('41 1') # odd number with space
    assert expected == actual
    
def test_str_to_bytes():
    expected = bytearray(b'AB\x00CY')
    actual = ch.StrToBytes('(AB.CY)')
    assert expected == actual
    