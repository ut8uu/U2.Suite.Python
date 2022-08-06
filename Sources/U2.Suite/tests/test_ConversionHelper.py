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

from pyrsistent import b
from exceptions.ParameterParseException import ParameterParseException
import unittest
from helpers.ConversionHelper import ConversionHelper as ch
from contracts.RigParameter import RigParameter as rp

class RigParameterTests(unittest.TestCase):
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

    def test_parse_rig_parameter(self):
        assert rp.none == ch.StrToRigParameter('pmNone')
        
        # non existent value
        with self.assertRaises(ParameterParseException) as cm:
            ch.StrToRigParameter('pm-non-existent-parameter')
            
        # no pm prefix
        with self.assertRaises(ParameterParseException) as cm:
            ch.StrToRigParameter('None')
        # non-existent parameter without prefix
        with self.assertRaises(ParameterParseException) as cm:
            ch.StrToRigParameter('non-existent-parameter')

    def test_bytes_and(self):
        arr1 = bytearray(b'\x10\x22\x80\x55')
        arr2 = bytearray(b'\x30\xff\x00\xa9')
        actual_result = ch.BytesAnd(arr1, arr2)
        expected_result = bytearray(b'\x10\x22\x00\x01')