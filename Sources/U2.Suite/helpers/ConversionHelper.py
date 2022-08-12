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

    @staticmethod
    def StrToValueFormat(s : str) -> ValueFormat:
        if not s.lower().startswith('vf'):
            raise FormatParseException('String "{}" not recognized as a valid FormatValue'.format(s));
        
        statuses = [status for status in dir(
            ValueFormat) if not status.startswith('_')]
        
        cut_value = s.strip().removeprefix('vf').lower()
        if cut_value in statuses:
            return eval('ValueFormat.' + cut_value)
        
        raise FormatParseException('Cannot parse ValueFormat {}'.format(s))

    @staticmethod
    def FromBcdBS(data : bytearray) -> int:
        sign = -1
        if (data[0] == 0):
            sign = 1
        data[0] = 0
        return (sign * ConversionHelper.FromBcdBU(data))
    
    @staticmethod
    def FromBcdBU(data : bytearray) -> int:
        sb = ''
        i = 0
        while (i <= (len(data) - 1)):
            sb += chr(0x30 + round(data[i] / 16))
            sb += chr(0x30 + (data[i] % 16))
            i += 1
        try:
            x = int(sb)
            return x
        except Exception as ex:
            print("invalid BCD value: {0}. {1}", ConversionHelper.BytesToHex(data), ex.Message)
            raise
        
    @staticmethod
    def FromBcdLS(data : bytearray) -> int:
        data = data[::-1] # Array.Reverse(data)        
        return ConversionHelper.FromBcdBS(data)
    
    @staticmethod
    def FromBcdLU(data : bytearray) -> int:
        data = data[::-1] # Array.Reverse(data)        
        return ConversionHelper.FromBcdBU(data)
    
    @staticmethod
    def FromBinB(data : bytearray) -> int:
        data = data[::-1] # Array.Reverse(data)        
        return ConversionHelper.FromBinL(data)
    
    @staticmethod
    def FromBinL(data : bytearray) -> int:
        return int.from_bytes(data, byteorder='little', signed=True)
    
"""
    @staticmethod
    def FromText(data : bytearray):
        s = Encoding.UTF8.GetString(data)
        try:
            return Convert.ToInt32(s)
        except Exception as ex:
            ClassLog.ErrorFormat("Invalid reply: {0}", ConversionHelper.BytesToHex(data))
            raise ValueConversionException(message = "Cannot convert string {} to int.".format(s))
        
    @staticmethod
    def FromDPIcom(data : bytearray):
        try:
            s = Encoding.UTF8.GetString(data)
            s = RegularExpressionHelper.MatchAndGetFirst("([\\d+\\.*\\d*])", s)
            return Convert.ToInt32(Math.Round(Convert.ToDouble((1000000.0 * Convert.ToDouble(s.Trim()))), MidpointRounding.AwayFromZero))
        except Exception as ex:
            ClassLog.ErrorFormat("Invalid DPIcom reply: {0}", ConversionHelper.BytesToHex(data))
            raise
        
    @staticmethod
    def FromYaesu(data : bytearray):
        sign = -1
        if (data[0] & 128) == 0:
            sign = 1
        data[0] = data[0] & 127
        return (sign * ConversionHelper.FromBinB(data))
    
    @staticmethod
    def FromFloat(data : bytearray):
        try:
            s = Encoding.UTF8.GetString(data)
            value = Convert.ToDouble(s.Trim(), CultureInfo.InvariantCulture)
            return Convert.ToInt32(Math.Round(value, MidpointRounding.AwayFromZero))
        except Exception:
            ClassLog.ErrorFormat("Invalid reply: {0}", ConversionHelper.BytesToHex(data))
            raise
    @staticmethod
    def UnformatValue(sourceData, info):
        if (sourceData.Length < (info.Start + info.Len)):
            raise ValueValidationException("Reply too short")
        data = sourceData.Skip(info.Start).Take(info.Len).ToArray()
        if ((info.Format == ValueFormat.Text)):
            return FromText(data)
        elif ((info.Format == ValueFormat.BinL)):
            return FromBinL(data)
        elif ((info.Format == ValueFormat.BinB)):
            return FromBinB(data)
        elif ((info.Format == ValueFormat.BcdLU)):
            return FromBcdLU(data)
        elif ((info.Format == ValueFormat.BcdLS)):
            return FromBcdLS(data)
        elif ((info.Format == ValueFormat.BcdBU)):
            return FromBcdBU(data)
        elif ((info.Format == ValueFormat.BcdBS)):
            return FromBcdBS(data)
        elif ((info.Format == ValueFormat.DPIcom)):
            return FromDPIcom(data)
        elif ((info.Format == ValueFormat.Float)):
            return FromFloat(data)
        elif ((info.Format == ValueFormat.Yaesu)):
            return FromYaesu(data)
        elif (((info.Format == ValueFormat.None)) or ((info.Format == ValueFormat.TextUD))):
            return 0
        else:
            raise ArgumentOutOfRangeException("Parameter {} not recognized.".format(info.Format))

    @staticmethod
    def FormatValue(inputValue, info):
        value = Convert.ToInt32(Math.Round(Convert.ToDouble(((inputValue * info.Mult) + info.Add)), MidpointRounding.AwayFromZero))
        if ((((info.Format == ValueFormat.BcdLU) or (info.Format == ValueFormat.BcdBU))) and (value < 0)):
            ClassLog.ErrorFormat("Passed invalid value: {}. Expected to be a BCD kind.".format(inputValue))
            return Array.Empty()
        if ((info.Format == ValueFormat.Text)):
            return ToText(value, info.Len)
        elif ((info.Format == ValueFormat.BinL)):
            return ToBinL(value, info.Len)
        elif ((info.Format == ValueFormat.BinB)):
            return ToBinB(value, info.Len)
        elif ((info.Format == ValueFormat.BcdLU)):
            return ToBcdLU(value, info.Len)
        elif ((info.Format == ValueFormat.BcdLS)):
            return ToBcdLS(value, info.Len)
        elif ((info.Format == ValueFormat.BcdBU)):
            return ToBcdBU(value, info.Len)
        elif ((info.Format == ValueFormat.BcdBS)):
            return ToBcdBS(value, info.Len)
        elif ((info.Format == ValueFormat.Yaesu)):
            return ToYaesu(value, info.Len)
        elif ((info.Format == ValueFormat.DPIcom)):
            return ToDPIcom(value, info.Len)
        elif ((info.Format == ValueFormat.TextUD)):
            return ToTextUD(value, info.Len)
        elif ((info.Format == ValueFormat.Float)):
            return ToFloat(value, info.Len)
        elif ((info.Format == ValueFormat.None)):
            return Array.Empty()
        else:
            raise ArgumentOutOfRangeException("{} not recognized.".format(info.Format))

    @staticmethod
    def ToText(value, len):
        s = "value.ToString().PadLeft(len, \'0\')"
        return Encoding.UTF8.GetBytes(s)
    @staticmethod
    def ToBcdBS(value, len):
        result = ToBcdBU(Math.Abs(value), len)
        if (value < 0):
            result[0] = 255
        return result
    @staticmethod
    def ToBcdBU(value, len):
        chars = ToText(value, (len * 2))
        result = []
        i = 0
        while (i < len):
            char1 = ((((chars[(i * 2)] - 48)) << 4))
            char2 = ((chars[((i * 2) + 1)] - 48))
            result[i] = ((char1 | char2))
            i += 1
        return result
    @staticmethod
    def ToBcdLS(value, len):
        arr = ToBcdLU(Math.Abs(value), len)
        if (value < 0):
            arr[( ^ 1)] = 255
        return arr
    @staticmethod
    def ToBcdLU(value, len):
        arr = ToBcdBU(value, len)
        Array.Reverse(arr)
        return arr
    @staticmethod
    def ToBinB(value, len):
        arr = ToBinL(value, len)
        Array.Reverse(arr)
        return arr
    @staticmethod
    def ToBinL(value, len):
        bytes = BitConverter.GetBytes(value)
        if BitConverter.IsLittleEndian:
            Array.Reverse(bytes)
        return bytes
    @staticmethod
    def ToDPIcom(value, len):
        f = (value / 1000000)
        s = "Convert.ToString(f).PadLeft(len, \'0\')"
        return Encoding.UTF8.GetBytes(s)
    @staticmethod
    def ToYaesu(value, len):
        arr = ToBinB(Math.Abs(value), len)
        if (value < 0):
            arr[0] = ((arr[0] | 128))
        return arr
    @staticmethod
    def ToFloat(value, len):
        s = "value.ToString(\"F\", CultureInfo.InvariantCulture).PadLeft(len, \' \')"
        return Encoding.UTF8.GetBytes(s)
    @staticmethod
    def ToTextUD(value, len):
        prefix = ("U" if ((value >= 0)) else "D")
        s = "prefix + Convert.ToString(Math.Abs(value))            .PadLeft(len - 1, \'0\')"
        return Encoding.UTF8.GetBytes(s)
"""
