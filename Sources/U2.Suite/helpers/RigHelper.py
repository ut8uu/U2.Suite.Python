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
from contracts.RigCommand import RigCommand
from contracts.RigCommands import RigCommands
from contracts.RigParameter import RigParameter
from exceptions.EntryLoadErrorException import EntryLoadErrorException
from exceptions.IniFileLoadException import IniFileLoadException
from exceptions.MaskValidationException import MaskValidationException
from exceptions.UnexpectedEntryException import UnexpectedEntryException
from helpers.ConversionHelper import ConversionHelper as ch
from helpers.IniFileHelper import IniFileHelper as ih
from helpers.FileSystemHelper import FileSystemHelper as fsh
from os.path import join
from typing import List, Tuple

class RigHelper():
    
    @staticmethod
    def ValidateEntries(entries:List[Tuple[str,str]], allowed_entries:List[str]):
        if (empty(entries)):
            return
        for entry in entries:
            if (allowed_entries.count(entry) == 0):
                raise UnexpectedEntryException('Unexpected entry found: {}'.format(entry))
    
    @staticmethod
    def ValidateMaskChecks(mask, length):
        if mask.Mask.Length == 0 or mask.Flags.Length == 0:
            raise MaskValidationException("Incorrect mask length")
        if mask.Mask.Length != mask.Flags.Length:
            raise MaskValidationException("Incorrect mask length")
        if length > 0 and mask.Mask.Length != length:
            raise MaskValidationException("Mask length <> ReplyLength")
        if not ch.BytesAnd(mask.Flags, mask.Flags).SequenceEqual(mask.Flags):
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
            startIndex = mask.Flags.Length - reply_end.Length
            ending = mask.Flags.partition[startIndex:]
            if not ending.SequenceEqual(reply_end):
                raise MaskValidationException("Mask does not end with ReplyEnd")
        else:
            if mask.Param == RigParameter.none:
                raise MaskValidationException("Parameter name is missing")
            if mask.Mask.Length == 0:
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
        except:
            raise EntryLoadErrorException('Failed loading the Common section from {}'.format(section))
        
        if (len(result.Code) == 0):
            raise EntryLoadErrorException('Failed loading the Common section from {}'.format(section))

        result.ReplyLength = ih.ReadInt(config_parser, section, option)
        result.ReplyEnd = ih.GetReplyEndOption(config_parser, section)
        
        try:
            mask_value = ih.GetValidateOption(config_parser, section)
            result.Validation = ch.StrToBitMask(mask_value)
        except:
            raise EntryLoadErrorException('Failed loading the Validate section from {}'.format(section))
        
        RigHelper.ValidateMask('Validate', result.Validation, result.ReplyLength, result.ReplyEnd)
    
    @staticmethod
    def LoadInitCommands(config_parser : configparser.ConfigParser) -> List[RigCommand]:
        result = []
        
        sections = [f for f in config_parser.sections() if f.lower().find('init') > -1]
        assert len(sections) > 0
        
        for section in sections:
            entries = ih.LoadSectionSettings(config_parser, section)
            if (len(entries) == 0):
                continue
            
            allowed_entries = ['Command', 'ReplyLength', 'ReplyEnd', 'Validate',]
            RigHelper.ValidateEntries(entries, allowed_entries)
            
            command = RigHelper.LoadCommon(config_parser, section)
            
            
        return result
    
    @staticmethod
    def loadRigCommands(path) -> RigCommands:
        config_parser = ih.Create(path)
        
        rig_commands = RigCommands()
        rig_commands.InitCmd = RigHelper.LoadInitCommands(config_parser)
        
        return rig_commands
    
    @staticmethod
    def loadAllRigCommands(path) -> List[RigCommands]:
        list = []
        iniDirectory = fsh.getIniFilesFolder()
        files = fsh.enumerateDirectory(iniDirectory, '.ini')
        for file in files:
            try:
                list.append(RigHelper.loadRigCommands(file))
            except IniFileLoadException as ex:
                print('Error loading ini file {}. {}'.format(file, ex.Message))
        return list        
    