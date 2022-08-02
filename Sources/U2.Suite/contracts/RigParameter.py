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
    freq_a = 2          # 0x00000002
    freq_b = 4          # 0x00000004
    pitch = 8           # 0x00000008
    rit_offset = 16     # 0x00000010
    rit0 = 32           # 0x00000020
    vfo_aa = 64         # 0x00000040
    vfo_ab = 128        # 0x00000080
    vfo_ba = 256        # 0x00000100
    vfo_bb = 512        # 0x00000200
    vfo_a = 1024        # 0x00000400
    vfo_b = 2048        # 0x00000800
    vfo_equal = 4096    # 0x00001000
    vfo_swap = 8192     # 0x00002000
    split_on = 16384    # 0x00004000
    split_off = 32768   # 0x00008000
    rit_on = 65536      # 0x00010000
    rit_off = 131072    # 0x00020000
    xit_on = 262144     # 0x00040000
    xit_off = 524288    # 0x00080000
    rx = 1048576        # 0x00100000
    tx = 2097152        # 0x00200000
    cw_u = 4194304      # 0x00400000
    cw_l = 8388608      # 0x00800000
    ssb_u = 16777216    # 0x01000000
    ssb_l = 33554432    # 0x02000000
    dig_u = 67108864    # 0x04000000
    dig_l = 134217728   # 0x08000000
    am = 268435456      # 0x10000000
    fm = 536870912      # 0x20000000
