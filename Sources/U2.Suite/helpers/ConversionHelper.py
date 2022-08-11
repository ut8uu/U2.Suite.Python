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
from contracts.BitMask import BitMask
from contracts.RigParameter import RigParameter
from contracts.ValueFormat import ValueFormat
from exceptions.FormatParseException import FormatParseException
from exceptions.MaskParseException import MaskParseException
from exceptions.ParameterParseException import ParameterParseException
from typing import List

class ConversionHelper():
    
    @staticmethod
    def BytesAnd(array1 : bytearray, array2 : bytearray) -> bytearray:
        result = bytearray()

        max_index = min(len(array1), len(array2))
        array1_1 = array1[:max_index]
        array2_1 = array2[:max_index]
        
        index = 0
        for x in array1_1:
            value = x & array2_1[index]
            result.append(value)
            index = index + 1

        return result
        
    
    @staticmethod
    def HexStrToBytes(s : str) -> bytearray:
        prepared = re.sub('[^0-9a-f]', '', s.lower())
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
    
    @staticmethod
    def SplitString(s : str) -> List[str]:
        return s.split('|')
    
    @staticmethod
    def FlagsFromBitMask(mask: bytearray, is_string: bool) -> bytearray:
        flags = bytearray(mask)
        dot = ord('.')
        
        index = 0
        if (is_string):
            for m in mask:
                if (m == dot):
                    mask[index] = 0x00
                    flags[index] = 0x00
                else:
                    mask[index] = 0xFF
                index = index + 1
        else:
            for m in mask:
                if (m != 0x00):
                    mask[index] = 0xFF
                index = index + 1
        return flags          
    
    @staticmethod
    def StrToRigParameter(s : str) -> RigParameter:
        if not s.startswith('pm'):
            raise ParameterParseException('Cannot recognize the parameter {}'.format(s))
        
        statuses = [status for status in dir(
            RigParameter) if not status.startswith('_')]
        
        cut_value = s.strip().removeprefix('pm').lower()
        if cut_value in statuses:
            return eval('RigParameter.' + cut_value)
        
        raise ParameterParseException('Cannot parse parameter {}'.format(s))
        
    @staticmethod
    def StrToBitMask(s : str) -> BitMask:
        input_string = s.strip()
        result = BitMask()
        
        if len(input_string) == 0:
            return result
        
        list = ConversionHelper.SplitString(input_string)
        result.Mask = ConversionHelper.StrToBytes(list[0])
        
        is_string = list[0][0] == '('
        size = len(list)
        if size == 1:
            is_string = list[0][0] == '('
            result.Flags = ConversionHelper.FlagsFromBitMask(result.Mask, is_string)
        
        elif size == 2:
            result.Param = ConversionHelper.StrToRigParameter(list[1])

            if result.Param != RigParameter.none:
                result.Flags = ConversionHelper.FlagsFromBitMask(result.Mask, is_string)
            else:
                result.Flags = result.Mask
        elif size == 3:
            result.Flags = ConversionHelper.StrToBytes(list[1])
            result.Param = ConversionHelper.StrToRigParameter(list[2])
        else:
            raise MaskParseException('Cannot parse mask {}'.format(input_string))

        return result

    def StrToValueFormat(s : str) -> ValueFormat:
        if not s.lower().startswith('vf'):
            raise FormatParseException('String "{}" not recognized as a valid FormatValue'.format(s));
        
        statuses = [status for status in dir(
            ValueFormat) if not status.startswith('_')]
        
        cut_value = s.strip().removeprefix('pm').lower()
        if cut_value in statuses:
            return eval('ValueFormat.' + cut_value)
        
        raise FormatParseException('Cannot parse ValueFormat {}'.format(s))
