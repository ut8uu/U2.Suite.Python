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

import os, unittest, serial
from rig.emulators.IC705Emulator import IC705Emulator

if os.name != 'nt':
    class test_IC705Emulator(unittest.TestCase):
        
        def test_emulator(self):
            emulator = IC705Emulator()
            emulator.start()

            # test using internal stuff
            emulator.test_serial()

            prefix = b'\xfe\xfe'

            ser = serial.Serial(emulator.SerialPortName, 2400, timeout=1)
            ser.write(prefix + b'cmd1')
            result = ser.read(5)
            self.assertEqual(b'resp1', result)

            ser.write(prefix + b'exit')
            emulator.stop()