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

from unittest import result
from contracts.Constants import Constants
from contracts.ParameterValue import ParameterValue
from contracts.RigParameter import RigParameter
from contracts.ValueFormat import ValueFormat
from exceptions.ArgumentOutOfRangeException import ArgumentOutOfRangeException
from exceptions.ConversionException import ConversionException
from exceptions.FormatParseException import FormatParseException
from exceptions.ParameterParseException import ParameterParseException
from exceptions.ParityConversionException import ParityConversionException
from exceptions.ValueConversionException import ValueConversionException
from helpers.ConversionHelper import ConversionHelper as ch
from pyrsistent import b
from rig.enums.Parity import Parity
import serial
import unittest

class RigParameterTests(unittest.TestCase):
    def test_hex_str_to_bytes(self):
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
        assert RigParameter.none == ch.StrToRigParameter('pmNone')
        
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
        arr1 = bytes(b'\x10\x22\x80\x55')
        arr2 = bytes(b'\x30\xff\x00\xa9')
        actual_result = ch.BytesAnd(arr1, arr2)
        expected_result = bytes(b'\x10\x22\x00\x01')
        assert expected_result == actual_result
        
    def test_str_to_bitmask_empty(self):
        source = ''
        expected_mask = bytearray()        
        expected_flags = bytearray()
        expected_param = RigParameter.none
        
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
        expected_param = RigParameter.none
        
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
        expected_param = RigParameter.tx
        
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
        expected_param = RigParameter.rx
        
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
                
    def test_from_bcd_ls(self):
        data = bytearray(b'\x07\x32\x23\x01')
        result = ch.FromBcdLS(data)
        self.assertEqual(-233207, result)
        
        data = bytearray(b'\x07\x32\x23\x00')
        result = ch.FromBcdLS(data)
        self.assertEqual(233207, result)
                
    def test_from_bin_b(self):
        data = bytearray(b'\x01')
        result = ch.FromBinB(data)
        self.assertEqual(1, result)
        
        data = bytearray(b'\x00\x00\x00\x00')
        result = ch.FromBinB(data)
        self.assertEqual(0, result)
        
        data = bytearray(b'\xFF\xFF\xFF\xFF')
        result = ch.FromBinB(data)
        self.assertEqual(-1, result)

    def test_from_text(self):
        data = bytearray(b'12345')
        result = ch.FromText(data)
        self.assertEqual(12345, result)
        
    def test_from_dpicom(self):
        data = bytearray(b';$PICOA,90,01,RXF,14.103600')
        result = ch.FromDPIcom(data)
        self.assertEqual(14103600, result)
        
        with self.assertRaises(ValueConversionException) as ex:
            ch.FromDPIcom(bytearray(b'asd'))
            
    def test_from_yaesu(self):
        # positive value
        self.assertEqual(4660, ch.FromYaesu(bytearray(b'\x12\x34'))) # 1*4096 + 2*256 + 3*16 + 4

        # negative value from previous case
        self.assertEqual(-4660, ch.FromYaesu(bytearray(b'\x92\x34'))) # 0x12 & 0x80 = 0x92
                
    def test_from_float(self):
        self.assertEqual(1, ch.FromFloat(bytearray(b'1.23')))
        
    def test_unformat_value(self):
        # 13|5|vfBcdLU|1|0|pmFreqA
        data = bytearray(b'\xFE\xFE\xA4\xE0\x25\x00\xFD\xFE\xFE\xE0\xA4\x25\x00\x23\x01\x00\x00\x00\xFD')
        pv = ParameterValue()
        pv.Format = ValueFormat.bcdlu
        pv.Start = 13
        pv.Len = 5
        result = ch.UnformatValue(data, pv)
        self.assertEqual(123, result)
        
    def test_to_text(self):
        result = ch.ToText(123, 4)
        self.assertEqual(bytearray(b'0123'), result)
        
    def test_to_bcdbu(self):
        result = ch.ToBcdBU(123, 2)
        self.assertEqual(bytearray(b'\x01\x23'), result)
    
    def test_to_bcdbs(self):
        result = ch.ToBcdBS(-123, 4)
        self.assertEqual(bytearray(b'\xff\x00\x01\x23'), result)
        
    def test_to_bcdls(self):
        result = ch.ToBcdLS(-123, 4)
        self.assertEqual(bytearray(b'\x23\x01\x00\xff'), result)
        result = ch.ToBcdLS(123, 4)
        self.assertEqual(bytearray(b'\x23\x01\x00\x00'), result)
        
    def test_to_bcdlu(self):
        result = ch.ToBcdLU(123, 4)
        self.assertEqual(bytearray(b'\x23\x01\x00\x00'), result)
        result = ch.ToBcdLU(-123, 4)
        self.assertEqual(bytearray(b'\x23\x01\x00\x00'), result)

    def test_to_bin(self):
        self.assertEqual(bytearray(b'\x01\x00\x00\x00'), ch.ToBinL(1, 4))
        self.assertEqual(bytearray(b'\x00\x00\x00\x01'), ch.ToBinB(1, 4))
    
    def test_to_dpicom(self):
        self.assertEqual(bytearray(b'1.234567'), ch.ToDPIcom(1234567, 8))

    def test_to_yaesu(self):
        # positive
        self.assertEqual(bytearray(b'\x00\x00\x00\x01'), ch.ToYaesu(1, 4))
        # negative
        self.assertEqual(bytearray(b'\x80\x00\x00\x01'), ch.ToYaesu(-1, 4))

    def test_to_float(self):
        self.assertEqual(bytearray(b' 123'), ch.ToFloat(123, 4))
        
    def test_to_text_ud(self):
        self.assertEqual(bytearray(b'U123'), ch.ToTextUD(123, 4))
        self.assertEqual(bytearray(b'D123'), ch.ToTextUD(-123, 4))
        
    def do_format_value(self, expected: bytearray, value: int, format: ValueFormat):
        pv = ParameterValue()
        pv.Format = format
        pv.Mult = 1
        pv.Add = 0
        pv.Start = 0
        pv.Len = 4
        
        self.assertEqual(expected, ch.FormatValue(value, pv))
        
    def test_format_value(self):
        self.do_format_value(bytearray(b'\xff\x00\x01\x23'), -123, ValueFormat.bcdbs)
        self.do_format_value(bytearray(b'\x00\x00\x01\x23'), 123, ValueFormat.bcdbu)
        self.do_format_value(bytearray(b'\x23\x01\x00\xff'), -123, ValueFormat.bcdls)
        self.do_format_value(bytearray(b'\x23\x01\x00\x00'), 123, ValueFormat.bcdlu)
        self.do_format_value(bytearray(b'\x01\x00\x00\x00'), 1, ValueFormat.binl)
        self.do_format_value(bytearray(b'\x00\x00\x00\x01'), 1, ValueFormat.binb)
        self.do_format_value(bytearray(b'1.234567'), 1234567, ValueFormat.dpicom)
        self.do_format_value(bytearray(b' 123'), 123, ValueFormat.float)
        self.do_format_value(bytearray(b'0123'), 123, ValueFormat.text)
        self.do_format_value(bytearray(b'D123'), -123, ValueFormat.textud)
        self.do_format_value(bytearray(b'U123'), 123, ValueFormat.textud)
        self.do_format_value(bytearray(b'\x00\x00\x00\x01'), 1, ValueFormat.yaesu)
        self.do_format_value(bytearray(b'\x80\x00\x00\x01'), -1, ValueFormat.yaesu)
        
        # unknown format
        pv = ParameterValue()
        pv.Format = 'aaa'
        pv.Mult = 1
        pv.Add = 0
        pv.Start = 0
        pv.Len = 4
        with self.assertRaises(ArgumentOutOfRangeException) as ex:
            ch.FormatValue(123, pv)
    
    def test_string_to_parity(self):
        self.assertEqual(serial.PARITY_NONE, ch.string_to_parity(Constants.ParityNone))
        self.assertEqual(serial.PARITY_EVEN, ch.string_to_parity(Constants.ParityEven))
        self.assertEqual(serial.PARITY_ODD, ch.string_to_parity(Constants.ParityOdd))
        self.assertEqual(serial.PARITY_MARK, ch.string_to_parity(Constants.ParityMark))
        self.assertEqual(serial.PARITY_SPACE, ch.string_to_parity(Constants.ParitySpace))
        
        with self.assertRaises(ParityConversionException) as ex:
            ch.string_to_parity('unknown')

    def test_parity_to_string(self):
        self.assertEqual(Constants.ParityNone, ch.parity_to_string(serial.PARITY_NONE))
        self.assertEqual(Constants.ParityEven, ch.parity_to_string(serial.PARITY_EVEN))
        self.assertEqual(Constants.ParityOdd, ch.parity_to_string(serial.PARITY_ODD))
        self.assertEqual(Constants.ParityMark, ch.parity_to_string(serial.PARITY_MARK))
        self.assertEqual(Constants.ParitySpace, ch.parity_to_string(serial.PARITY_SPACE))
        
    def test_int_to_databits(self):
        self.assertEqual(serial.FIVEBITS, ch.int_to_databits(5))
        self.assertEqual(serial.SIXBITS, ch.int_to_databits(6))
        self.assertEqual(serial.SEVENBITS, ch.int_to_databits(7))
        self.assertEqual(serial.EIGHTBITS, ch.int_to_databits(8))
        
        with self.assertRaises(ConversionException) as ex:
            ch.int_to_databits('unknown')

    def test_float_to_stopbits(self):
        self.assertEqual(serial.STOPBITS_ONE, ch.float_to_stopbits(1.0))
        self.assertEqual(serial.STOPBITS_ONE_POINT_FIVE, ch.float_to_stopbits(1.5))
        self.assertEqual(serial.STOPBITS_TWO, ch.float_to_stopbits(2.0))

        with self.assertRaises(ConversionException) as ex:
            ch.float_to_stopbits(3.0)
        