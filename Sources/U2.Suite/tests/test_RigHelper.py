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

from audioop import mul
import configparser
import unittest

from pyparsing import dict_of
from contracts.RigCommand import RigCommand
from contracts.RigParameter import RigParameter
from contracts.ValueFormat import ValueFormat
from exceptions.UnexpectedEntryException import UnexpectedEntryException
from helpers.FileSystemHelper import FileSystemHelper as fsh
from helpers.RigHelper import RigHelper
from os.path import join

class RigHelperTests(unittest.TestCase):
    def test_LoadIC705(self):
        folder = fsh.getIniFilesFolder()
        ini_file_path = join(folder, 'IC-705.ini')
        rig_commands = RigHelper.loadRigCommands(ini_file_path)
        self.assertEqual(3, len(rig_commands.InitCmd))
        self.assertEqual(9, len(rig_commands.StatusCmd))
        
        parameters = [
            RigParameter.freqa, RigParameter.freqb, RigParameter.rit0, RigParameter.pitch,
            RigParameter.spliton, RigParameter.splitoff, RigParameter.vfoa, RigParameter.vfob,
            RigParameter.vfoequal, RigParameter.vfoswap, RigParameter.vfoaa, RigParameter.vfoab,
            RigParameter.vfoba, RigParameter.vfobb, RigParameter.riton, RigParameter.ritoff,
            RigParameter.xiton, RigParameter.xitoff, RigParameter.rx, RigParameter.tx,
            RigParameter.cw_u, RigParameter.cw_l, RigParameter.ssb_u, RigParameter.ssb_l,
            RigParameter.dig_u, RigParameter.dig_l, RigParameter.am, RigParameter.fm,
        ]
        self.assertEqual(len(parameters), len(rig_commands.WriteCmd))
        
        cmd = rig_commands.WriteCmd[RigParameter.freqa.value]
        self.assertTrue(isinstance(cmd, RigCommand))
        code = bytearray(b'\xFE\xFE\xA4\xE0\x25\x00\x00\x00\x00\x00\x00\xFD')
        validation = bytearray(b'\xFE\xFE\xA4\xE0\x25\x00\x00\x00\x00\x00\x00\xFD\xFE\xFE\xE0\xA4\xFB\xFD')
        RigHelperTests.check_write_cmd(self, cmd, 18, 6, 5, 1, 0, ValueFormat.bcdlu, code, validation)

        cmd = rig_commands.WriteCmd[RigParameter.freqb.value]
        code = bytearray(b'\xFE\xFE\xA4\xE0\x25\x01\x00\x00\x00\x00\x00\xFD')
        validation = bytearray(b'\xFE\xFE\xA4\xE0\x25\x01\x00\x00\x00\x00\x00\xFD\xFE\xFE\xE0\xA4\xFB\xFD')
        RigHelperTests.check_write_cmd(self, cmd, 18, 6, 5, 1, 0, ValueFormat.bcdlu, code, validation)

        cmd = rig_commands.WriteCmd[RigParameter.rit0.value]
        code = bytearray(b'\xFE\xFE\xA4\xE0\x21\x00\x00\x00\x00\xFD')
        validation = bytearray(b'\xFE\xFE\xA4\xE0\x21\x00\x00\x00\x00\xFD\xFE\xFE\xE0\xA4\xFB\xFD')
        RigHelperTests.check_write_cmd(self, cmd, 16, 0, 0, 1, 0, ValueFormat.none, code, validation)

        cmd = rig_commands.WriteCmd[RigParameter.pitch.value]
        code = bytearray(b'\xFE\xFE\xA4\xE0\x14\x09\x00\x00\xFD')
        validation = bytearray(b'\xFE\xFE\xA4\xE0\x14\x09\x00\x00\xFD\xFE\xFE\xE0\xA4\xFB\xFD')
        RigHelperTests.check_write_cmd(self, cmd, 15, 6, 2, 0.425, -127.5, ValueFormat.bcdbu, code, validation)

    def check_write_cmd(self, cmd:RigCommand, reply_len:int, start:int, len:int, mult:int, 
                        add:int, format:ValueFormat, code:bytearray, validation:bytearray):
        self.assertEqual(reply_len, cmd.ReplyLength)
        self.assertEqual(code, cmd.Code)
        self.assertEqual(validation, cmd.Validation.Flags)
        self.assertEqual(start, cmd.Value.Start)
        self.assertEqual(len, cmd.Value.Len)
        self.assertEqual(mult, cmd.Value.Mult)
        self.assertEqual(add, cmd.Value.Add)
        self.assertEqual(format, cmd.Value.Format)
       
        
    def test_are_equal(self):
        assert RigHelper.AreEqual('a', 'a')
        assert not RigHelper.AreEqual('a', 'b')
        
    def test_validate_entries(self):
        allowed_entries = ['command', 'replylength', 'replyend', 'validate',]
        entries = [('command', 'xxx')]
        RigHelper.ValidateEntries(entries, allowed_entries)
        
        entries = [('yyy', 'xxx')]
        with self.assertRaises(UnexpectedEntryException) as cm:
            RigHelper.ValidateEntries(entries, allowed_entries)

    def test_read_string_from_ini(self):
        section = 'section1'

        parser = configparser.ConfigParser()
        parser.add_section(section)
        parser[section]['xxx'] = 'xxx'        
        parser[section]['yyy'] = '123'
        
        self.assertEqual('xxx', RigHelper.ReadStringFromIni(parser, section, 'xxx', 'default'))
        self.assertEqual('default', RigHelper.ReadStringFromIni(parser, section, 'zzz', 'default'))

        self.assertEqual(123, RigHelper.ReadIntFromIni(parser, section, 'yyy', 0))
        self.assertEqual(0, RigHelper.ReadIntFromIni(parser, section, 'zzz', 0))
