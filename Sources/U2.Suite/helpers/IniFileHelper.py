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
from typing import List, Tuple
from helpers.ConversionHelper import ConversionHelper as ch

class IniFileHelper():
    
    @staticmethod
    def Create(path: str) -> configparser.ConfigParser:
        config_parser = configparser.ConfigParser()
        config_parser.read(path)
        return config_parser
    
    @staticmethod
    def LoadSectionSettings(config_parser:configparser.ConfigParser, section: str) \
        -> List[Tuple[str, str]]:
        
        result = []
        options = config_parser.options(section)
        
        for option in options:
            result.append((option, config_parser.get(section, option)))
        
        return result
    
    @staticmethod
    def ReadString(config_parser:configparser.ConfigParser, section: str, option: str) -> str:
        return config_parser.get(section, option)
    
    @staticmethod
    def ReadInt(config_parser:configparser.ConfigParser, section: str, option: str) -> int:
        return config_parser.getint(section, option)
    
    @staticmethod
    def GetCommandOption(config_parser:configparser.ConfigParser, section: str) -> str:
        return config_parser.get(section, 'Command')

    @staticmethod
    def GetReplyEndOption(config_parser:configparser.ConfigParser, section: str) -> bytearray:
        try:
            s = config_parser.get(section, 'ReplyEnd')
            return ch.HexStrToBytes(s)
        except Exception as e:
            return bytearray()

    @staticmethod
    def GetValidateOption(config_parser:configparser.ConfigParser, section: str) -> str:
        return config_parser.get(section, 'Validate')

