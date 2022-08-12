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

from contracts.RigParameter import RigParameter as rp
from contracts.ValueFormat import ValueFormat
from exceptions.FormatParseException import FormatParseException
from exceptions.ParameterParseException import ParameterParseException
from helpers.ConversionHelper import ConversionHelper as ch
from pyrsistent import b
import unittest

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
        
    def test_str_to_bytes(self):
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
        assert expected_result == actual_result
        
    def test_str_to_bitmask_empty(self):
        source = ''
        expected_mask = bytearray()        
        expected_flags = bytearray()
        expected_param = rp.none
        
        result = ch.StrToBitMask(source)
        assert result.Flags == expected_flags
        assert result.Mask == expected_mask
        assert result.Param == expected_param
        
    def test_str_to_bitmask_hex(self):
        #Mask:  FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        #Flags: FEFEA4E01A05013201FDFEFEE0A4FBFD
        #Param: None
        source = 'FEFEA4E01A05013201FD.FEFEE0A4FBFD'
        expected_mask = bytearray(b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF') 
        expected_flags = bytearray(b'\xFE\xFE\xA4\xE0\x1A\x05\x01\x32\x01\xFD\xFE\xFE\xE0\xA4\xFB\xFD')
        expected_param = rp.none
        
        result = ch.StrToBitMask(source)
        assert result.Flags == expected_flags
        assert result.Mask == expected_mask
        assert result.Param == expected_param
        
    def test_str_to_bitmask_two_params(self):
        # src: 00000000000000.00000000.0000.01.00|pmTx
        #Mask:  00000000000000000000000000FF00
        #Flags: 000000000000000000000000000100
        #Param: Tx
        source = '00000000000000.00000000.0000.01.00|pmTx'
        expected_mask = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\x00') 
        expected_flags = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00')
        expected_param = rp.tx
        
        result = ch.StrToBitMask(source)
        assert result.Flags == expected_flags
        assert result.Mask == expected_mask
        assert result.Param == expected_param
        
    def test_str_to_bitmask_three_params(self):
        # src: 00000000000000.00000000.0000.0F.00|00000000000000.00000000.0000.00.00|pmRx
        #Mask:  000000000000000000000000000F00
        #Flags: 000000000000000000000000000000
        #Param: Tx
        source = '00000000000000.00000000.0000.0F.00|00000000000000.00000000.0000.00.00|pmRx'
        expected_mask = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0F\x00') 
        expected_flags = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        expected_param = rp.rx
        
        result = ch.StrToBitMask(source)
        assert result.Flags == expected_flags
        assert result.Mask == expected_mask
        assert result.Param == expected_param
    
    def test_str_to_value_format_positive(self):
        #Src: vfText
        source = 'vfText'
        actual = ch.StrToValueFormat(source)
        assert actual == ValueFormat.text

        source = 'vfBcdLU'
        actual = ch.StrToValueFormat(source)
        assert actual == ValueFormat.bcdlu
        
    def test_str_to_value_format_negative(self):
        #Src: aaa
        with self.assertRaises(FormatParseException) as cm:
            ch.StrToValueFormat('aaa')
            
        with self.assertRaises(FormatParseException) as cm:
            ch.StrToValueFormat('vfAaaa')
            
    def test_from_bcd_bs(self):
        data = bytearray(b'\x10\x23\x32\x07')
        result = ch.FromBcdBS(data)
        self.assertEqual(-233207, result)
        
        data = bytearray(b'\x00\x23\x32\x07')
        result = ch.FromBcdBS(data)
        self.assertEqual(233207, result)
                
            