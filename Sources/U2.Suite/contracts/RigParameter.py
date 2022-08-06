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

import enum

@enum.unique
class RigParameter(enum.Enum):
    none = 0            # 0x00000000
    freq = 1            # 0x00000001
    freqa = 2          # 0x00000002
    freqb = 4          # 0x00000004
    pitch = 8           # 0x00000008
    ritoffset = 16     # 0x00000010
    rit0 = 32           # 0x00000020
    vfoaa = 64         # 0x00000040
    vfoab = 128        # 0x00000080
    vfoba = 256        # 0x00000100
    vfobb = 512        # 0x00000200
    vfoa = 1024        # 0x00000400
    vfob = 2048        # 0x00000800
    vfoequal = 4096    # 0x00001000
    vfoswap = 8192     # 0x00002000
    spliton = 16384    # 0x00004000
    splitoff = 32768   # 0x00008000
    riton = 65536      # 0x00010000
    ritoff = 131072    # 0x00020000
    xiton = 262144     # 0x00040000
    xitoff = 524288    # 0x00080000
    rx = 1048576        # 0x00100000
    tx = 2097152        # 0x00200000
    cwu = 4194304      # 0x00400000
    cwl = 8388608      # 0x00800000
    ssbu = 16777216    # 0x01000000
    ssbl = 33554432    # 0x02000000
    digu = 67108864    # 0x04000000
    digl = 134217728   # 0x08000000
    am = 268435456      # 0x10000000
    fm = 536870912      # 0x20000000    
