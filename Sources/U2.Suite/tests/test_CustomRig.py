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

import unittest
from contracts.RigParameter import RigParameter
from rig.CustomRig import CustomRig
from rig.enums.RigControlType import RigControlType

class CustomRigTests(unittest.TestCase):
    def test_setters(self):
        rig = CustomRig(RigControlType.host)

        rig.SetFreq(101)
        self.assertEqual(101, rig._freq)
        rig.Freq = 102
        self.assertEqual(102, rig.Freq)
        self.assertEqual(rig._freq, rig.Freq)

        rig.SetFreqA(201)
        self.assertEqual(201, rig._freqA)
        rig.FreqA = 202
        self.assertEqual(202, rig.FreqA)
        self.assertEqual(rig._freqA, rig.FreqA)

        rig.SetFreqB(301)
        self.assertEqual(301, rig._freqB)
        rig.FreqB = 302
        self.assertEqual(302, rig.FreqB)
        self.assertEqual(rig._freqB, rig.FreqB)

        rig.SetMode(RigParameter.am)
        self.assertEqual(RigParameter.am, rig._mode)
        self.assertEqual(rig.Mode, rig._mode)
        rig.Mode = RigParameter.fm
        self.assertEqual(RigParameter.fm, rig._mode)

        rig.SetPitch(401)
        self.assertEqual(401, rig._pitch)
        rig.Pitch = 402
        self.assertEqual(402, rig.Pitch)
        self.assertEqual(rig._pitch, rig.Pitch)

        rig.SetRit(RigParameter.ritoff)
        self.assertEqual(RigParameter.ritoff, rig._rit)
        rig.Rit = RigParameter.riton
        self.assertEqual(RigParameter.riton, rig.Rit)
        self.assertEqual(rig._rit, rig.Rit)

        rig.SetRitOffset(501)
        self.assertEqual(501, rig._ritOffset)
        rig.RitOffset = 502
        self.assertEqual(502, rig.RitOffset)
        self.assertEqual(rig._ritOffset, rig.RitOffset)

        rig.SetXit(RigParameter.xitoff)
        self.assertEqual(RigParameter.xitoff, rig._xit)
        rig.Xit = RigParameter.xiton
        self.assertEqual(RigParameter.xiton, rig.Xit)
        self.assertEqual(rig._xit, rig.Xit)

        rig.SetTx(RigParameter.rx)
        self.assertEqual(RigParameter.rx, rig.Tx)
        rig.Tx = RigParameter.tx
        self.assertEqual(RigParameter.tx, rig.Tx)
        self.assertEqual(rig._tx, rig.Tx)

        rig.SetSplit(RigParameter.splitoff)
        self.assertEqual(RigParameter.splitoff, rig.Split)
        rig.Split = RigParameter.spliton
        self.assertEqual(RigParameter.spliton, rig.Split)
        self.assertEqual(rig._split, rig.Split)

        rig.SetVfo(RigParameter.vfoaa)
        self.assertEqual(RigParameter.vfoaa, rig.Vfo)
        rig.Vfo = RigParameter.vfoab
        self.assertEqual(RigParameter.vfoab, rig.Vfo)
        self.assertEqual(rig._vfo, rig.Vfo)


