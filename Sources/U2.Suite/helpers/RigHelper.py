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

import configparser

from pyparsing import empty

from contracts.BitMask import BitMask
from contracts.ParameterValue import ParameterValue
from contracts.RigCommand import RigCommand
from contracts.RigCommands import RigCommands
from contracts.RigParameter import RigParameter
from exceptions.EntryLoadErrorException import EntryLoadErrorException
from exceptions.IniFileLoadException import IniFileLoadException
from exceptions.LoadInitCommandsException import LoadInitCommandsException
from exceptions.LoadStatusCommandsException import LoadStatusCommandsException
from exceptions.LoadWriteCommandException import LoadWriteCommandException
from exceptions.MaskValidationException import MaskValidationException
from exceptions.UnexpectedEntryException import UnexpectedEntryException
from exceptions.ValueLoadException import ValueLoadException
from exceptions.ValueValidationException import ValueValidationException
from helpers.ConversionHelper import ConversionHelper as ch
from helpers.IniFileHelper import IniFileHelper as ih
from helpers.FileSystemHelper import FileSystemHelper as fsh
from os.path import join
from typing import List, Tuple

class RigHelper():
    
    NumericParameters = [ RigParameter.freq, RigParameter.freqa, 
                         RigParameter.freqb, RigParameter.pitch, ]
    
    @staticmethod
    def ValidateEntries(entries:List[Tuple[str,str]], allowed_entries:List[str]):
        if (len(entries) == 0):
            return
        for entry in entries:
            if (allowed_entries.count(entry[0].lower()) == 0):
                raise UnexpectedEntryException('Unexpected entry found: {}'.format(entry))
    
    @staticmethod
    def ValidateMaskChecks(mask, length):
        if len(mask.Mask) == 0 or len(mask.Flags) == 0:
            raise MaskValidationException("Incorrect mask length")
        if len(mask.Mask) != len(mask.Flags):
            raise MaskValidationException("Incorrect mask length")
        if length > 0 and len(mask.Mask) != length:
            raise MaskValidationException("Mask length <> ReplyLength")
        if not ch.BytesAnd(mask.Flags, mask.Flags) == mask.Flags:
            raise MaskValidationException("Mask hides valid bits")

    @staticmethod
    def AreEqual(string_one : str, string_two : str) -> bool:
        try:
            return string_one.lower() == string_two.lower()
        except AttributeError:
            return string_one == string_two

    @staticmethod
    def ValidateMask(entry_name: str, mask: BitMask, length: int, reply_end: bytearray):
        if len(mask.Mask) == 0 and len(mask.Flags) == 0 and mask.Param == RigParameter.none:
            return
        
        RigHelper.ValidateMaskChecks(mask, length)
        if RigHelper.AreEqual(entry_name, "validate"):
            if mask.Param != RigParameter.none:
                raise MaskValidationException("Parameter name is not allowed")
            startIndex = len(mask.Flags) - len(reply_end)
            ending = mask.Flags[startIndex:]
            if ending != reply_end:
                raise MaskValidationException("Mask does not end with ReplyEnd")
        else:
            if mask.Param == RigParameter.none:
                raise MaskValidationException("Parameter name is missing")
            if len(mask.Mask) == 0:
                raise MaskValidationException("Mask is blank")
        
    
    @staticmethod
    def LoadCommon(config_parser:configparser.ConfigParser, section: str) -> RigCommand:
        result = RigCommand()
        try:
            option = ih.GetCommandOption(config_parser, section)
            if (option.startswith('(')):
                result.Code = ch.StrToBytes(option)
            else:
                result.Code = ch.HexStrToBytes(option)
        except Exception:
            raise EntryLoadErrorException(f'Failed loading the Common section from {section}')
        
        if (len(result.Code) == 0):
            raise EntryLoadErrorException(f'Failed loading the Common section from {section}')

        result.ReplyLength = ih.ReadInt(config_parser, section, "replylength")
        result.ReplyEnd = ih.GetReplyEndOption(config_parser, section)
        
        try:
            mask_value = ih.GetValidateOption(config_parser, section)
            result.Validation = ch.StrToBitMask(mask_value)
        except Exception as ex:
            raise EntryLoadErrorException(f'Failed loading the Validate section from {section}')
        
        RigHelper.ValidateMask('Validate', result.Validation, result.ReplyLength, result.ReplyEnd)
        return result
    
    @staticmethod
    def LoadAllSections(config_parser : configparser.ConfigParser) \
        -> List[str]:
        return [f for f in config_parser.sections()]
    
    @staticmethod
    def LoadSections(config_parser : configparser.ConfigParser, section_name : str) \
        -> List[str]:
        return [f for f in config_parser.sections() if f.lower().find(section_name) > -1]
    
    @staticmethod
    def LoadInitCommands(config_parser : configparser.ConfigParser) -> List[RigCommand]:
        result = []
        
        sections = RigHelper.LoadSections(config_parser, 'init')
        assert len(sections) > 0
        
        for section in sections:
            try:
                entries = ih.LoadSectionSettings(config_parser, section)
                if (len(entries) == 0):
                    continue
                
                allowed_entries = ['command', 'replylength', 'replyend', 'validate',]
                RigHelper.ValidateEntries(entries, allowed_entries)
                
                command = RigHelper.LoadCommon(config_parser, section)
                if len(command.Code) > 0:
                    result.append(command)
            except Exception as ex:
                raise LoadInitCommandsException(f'Failed to load the INIT commands. {ex}')
            
        return result
    
    @staticmethod
    def ReadStringFromIni(config_parser: configparser.ConfigParser, section : str,
        setting_name : str, default_value : str) -> str:
        ini_setting = config_parser[section][setting_name]
        if ini_setting != None:
            return ini_setting

        return default_value

    @staticmethod
    def ReadIntFromIni(config_parser: configparser.ConfigParser, section : str,
        setting_name : str, default_value : str) -> int:
        return int(RigHelper.ReadStringFromIni(config_parser, section, setting_name, '0'))
    
    @staticmethod
    def ParseParameterValue(value : str) -> ParameterValue:
        if len(value) == 0:
            return ParameterValue()
        
        elements = value.split('|')
        if len(elements) == 0:
            return ParameterValue()
        
        elif len(elements) != 5 and len(elements) != 6:
            raise ValueLoadException("A value \'{}\' has invalid syntax.".format(value))
        
        result = ParameterValue()
        
        if len(elements) == 6:
            result.Param = ch.StrToRigParameter(elements[5])
        try:
            result.Start = int(elements[0])
        except Exception:
            raise ValueLoadException(f"invalid Start value in '{value}'")
        
        try:
            result.Len = int(elements[1])
        except Exception:
            raise ValueLoadException(f"Invalid Length value in '{value}'")
        
        result.Format = ch.StrToValueFormat(elements[2])
        try:
            result.Mult = float(elements[3])
        except Exception as ex:
            raise ValueLoadException(f"invalid Multiplier value in '{value}'. {ex}")
        
        try:
            result.Add = float(elements[4])
        except Exception as ex:
            raise ValueLoadException(f"invalid Add value in '{value}'. {ex}")
        return result

    @staticmethod
    def LoadValue(config_parser: configparser.ConfigParser,
                             section: str, setting_name: str) -> ParameterValue:
        try:
            value = RigHelper.ReadStringFromIni(config_parser, section, setting_name, '')
            return RigHelper.ParseParameterValue(value)
        
        except ValueLoadException as ex:
            raise ex
        except KeyError as ex:
            return ParameterValue()
        except Exception as ex:
            raise ValueLoadException(ex.Message)
        
    @staticmethod
    def ValidateValue(value : ParameterValue, size: int):
        try:
            if value.Param == RigParameter.none:
                return
            if size == 0:
                size = int.MaxValue
            if value.Start < 0 or value.Start >= size:
                raise ValueValidationException("Invalid Start value: {}".format(value.Start))
            if value.Len < 0 or value.Start + value.Len > size:
                raise ValueValidationException("invalid Length value. Start={}, Len={}".format(value.Start, value.Len))
            if value.Mult <= 0:
                raise ValueValidationException("invalid Multiplier value: {}".format(value.Mult))
        except Exception as e:
            raise ValueValidationException(e.Message)

    @staticmethod
    def ReadStatusEntryValue(cmd: RigCommand, config_parser: configparser.ConfigParser,
                             section: str, entry: Tuple[str, str]) -> Tuple[bool, ParameterValue]:
        result = None
        key = entry[0].lower()
        try:
            if not key.startswith('value'):
                return False, None

            value = RigHelper.LoadValue(config_parser, section, key)
            RigHelper.ValidateValue(value, max(cmd.ReplyLength, len(cmd.Validation.Mask)))

            if value.Param == RigParameter.none:
                # parameter name is missing
                return False, None
            elif RigHelper.NumericParameters.count(value.Param) == 0:
                # parameter must be of numeric type
                return False, None

            return True, value
        except ValueLoadException:
            return False, None
        
    @staticmethod
    def ReadStatusEntryFlag(cmd: RigCommand,
        ini_setting: Tuple[str, str]) -> Tuple[bool, BitMask]:
    
        if not ini_setting[0].startswith("flag"):
            return False, None

        try:
            flag = ch.StrToBitMask(ini_setting[1])
            RigHelper.ValidateMask(ini_setting[0], flag, cmd.ReplyLength, cmd.ReplyEnd)
            return True, flag
        except MaskValidationException:
            return False, None
    
    @staticmethod
    def LoadStatusCommandsEntries(config_parser : configparser.ConfigParser,
                                 section : str, entries : List[Tuple[str, str]],
                                 cmd : RigCommand):
        cmd.Values = []
        cmd.Flags = []

        for entry in entries:
            status_entry_value = RigHelper.ReadStatusEntryValue(cmd, config_parser, section, entry)
            if status_entry_value[0]:
                cmd.Values.append(status_entry_value[1])
                continue
            
            status_entry_flag = RigHelper.ReadStatusEntryFlag(cmd, entry)
            if status_entry_flag[0]:
                cmd.Flags.append(status_entry_flag[1])

    @staticmethod
    def LoadStatusCommands(config_parser : configparser.ConfigParser) -> List[RigCommand]:
        result = []

        sections = RigHelper.LoadSections(config_parser, 'status')
        for section in sections:
            try:
                entries = ih.LoadSectionSettings(config_parser, section)
                if (len(entries) == 0):
                    continue
                
                allowed_entries = [
                    'command', 'replylength', 'replyend', 'validate',
                    'value', 'value1', 'value2', 'value3', 'value4', 'value5',
                    'value6', 'value7', 'value8', 'value9', 'value10',
                    'flag1', 'flag2', 'flag3', 'flag4',
                    'flag5', 'flag6', 'flag7', 'flag8',
                    'flag9', 'flag10', 'flag11', 'flag12', 'flag13',
                    'flag14', 'flag15', 'flag16', 'flag17', 'flag18',
                    'flag19', 'flag20', 'flag21', 'flag22',
                ]
                RigHelper.ValidateEntries(entries, allowed_entries)

                cmd = RigHelper.LoadCommon(config_parser, section)

                if cmd.ReplyLength == 0 and len(cmd.ReplyEnd) == 0:
                    raise LoadStatusCommandsException("Reply length or reply end must be specified.")

                RigHelper.LoadStatusCommandsEntries(config_parser, section, entries, cmd)

                if len(cmd.Values) == 0 and len(cmd.Flags) == 0:
                    raise LoadStatusCommandsException("at least one ValueNN or FlagNN must be defined")

                result.append(cmd)
            except LoadStatusCommandsException as ex:
                raise ex
            except Exception as ex:
                raise LoadStatusCommandsException(f"Error loading of STATUS section. {ex}")

        return result
    
    @staticmethod
    def ValidateWriteCommandEntries(config_parser: configparser.ConfigParser, section: str):
        try:
            allowed_entries = ['command', 'replylength', 'replyend', 'validate', 'value']
            entries = config_parser.items(section)
            RigHelper.ValidateEntries(entries, allowed_entries)
        except UnexpectedEntryException as ex:
            raise LoadWriteCommandException(ex)

    
    @staticmethod
    def LoadWriteCommands(config_parser: configparser.ConfigParser):
        result = {}
        all_sections = RigHelper.LoadAllSections(config_parser)
        sections = [f for f in all_sections 
                    if f.lower().find('status') < 0 and f.lower().find('init') < 0]
        
        for section in sections:
            try:
                items = config_parser.items(section)
                if len(items) == 0:
                    continue
                RigHelper.ValidateWriteCommandEntries(config_parser, section)
                cmd = RigHelper.LoadCommon(config_parser, section)
                parameterValue = RigHelper.LoadValue(config_parser, section, 'value')
                RigHelper.ValidateValue(parameterValue, len(cmd.Code))
                if parameterValue.Param != RigParameter.none:
                    raise LoadWriteCommandException("parameter name is not allowed")
                param = ch.StrToRigParameter(section)
                parameterValue.Param = param
                if RigHelper.NumericParameters.count(param) > 0 and parameterValue.Len == 0:
                    raise LoadWriteCommandException("Value is missing")
                if RigHelper.NumericParameters.count(param) == 0 and parameterValue.Len > 0:
                    raise LoadWriteCommandException("parameter does not require a value")
                cmd.Value = parameterValue
                result[param.value] = cmd
            except Exception as ex:
                raise LoadWriteCommandException(ex.Message, ex)
        return result

    
    @staticmethod
    def loadRigCommands(path : str) -> RigCommands:
        config_parser = ih.Create(path)
        
        rig_commands = RigCommands()
        rig_commands.InitCmd = RigHelper.LoadInitCommands(config_parser)
        rig_commands.StatusCmd = RigHelper.LoadStatusCommands(config_parser)
        rig_commands.WriteCmd = RigHelper.LoadWriteCommands(config_parser)
        
        return rig_commands
    
    @staticmethod
    def loadAllRigCommands(path) -> List[RigCommands]:
        list = List[RigCommands]()
        iniDirectory = fsh.getIniFilesFolder()
        files = fsh.enumerateDirectory(iniDirectory, '.ini')
        for file in files:
            try:
                list.append(RigHelper.loadRigCommands(file))
            except IniFileLoadException as ex:
                print('Error loading ini file {}. {}'.format(file, ex.Message))
        return list        
    