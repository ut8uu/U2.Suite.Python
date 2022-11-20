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

from contracts.RadioBand import *
from contracts.RadioMode import *
from typing import List


class Band70CM(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band70CM, self).__init__()
        self.Name = RadioBandName.B70cm
        self.BeginMhz = 430000000
        self.EndMhz = 440000000
        self.Group = RadioBandGroup.UHF
        self.Type = RadioBandType.B70cm
        self.SubBands = []

        self.SubBands.append(SubBand(430000000, 431975000, RadioMode.AllModes()))
        self.SubBands.append(SubBand(431975000, 432100000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(432100000, 432400000, RadioMode.CwSsbModes()))
        self.SubBands.append(SubBand(432500000, 432975000, RadioMode.AllModes()))
        self.SubBands.append(SubBand(433000000, 433575000, RadioMode.FmDigitalModes()))
        self.SubBands.append(SubBand(433600000, 434981000, RadioMode.AllModes()))
        self.SubBands.append(SubBand(435000000, 438000000, RadioMode.SatelliteModes()))
        self.SubBands.append(SubBand(438000000, 440000000, RadioMode.AllModes()))

class Band2M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band2M, self).__init__()
        self.Name = RadioBandName.B2m
        self.BeginMhz = 144000000
        self.EndMhz = 146000000
        self.Group = RadioBandGroup.VHF
        self.Type = RadioBandType.B2m
        self.SubBands = []

        self.SubBands.append(SubBand(144000000, 144025000, RadioMode.AllModes()))
        self.SubBands.append(SubBand(144025000, 144150000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(144150000, 144270000, RadioMode.CwSsbModes()))
        self.SubBands.append(SubBand(144500000, 144794000, RadioMode.AllModes()))
        self.SubBands.append(SubBand(144794000, 145806000, RadioMode.FmDigitalModes()))
        self.SubBands.append(SubBand(145806000, 146000000, RadioMode.AllModes()))

class Band4M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band4M, self).__init__()
        self.Name = RadioBandName.B4m
        self.BeginMhz = 70000000
        self.EndMhz = 70500000
        self.Group = RadioBandGroup.VHF
        self.Type = RadioBandType.B4m
        self.SubBands = []

        self.SubBands.append(SubBand(70000000, 70100000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(70100000, 70250000, RadioMode.CwSsbModes()))
        self.SubBands.append(SubBand(70250000, 70254000, RadioMode.AmFmModes()))
        self.SubBands.append(SubBand(70254000, 70500000, RadioMode.FmDigitalModes()))
        self.SubBands.append(SubBand(50500000, 54000000, RadioMode.AllModes()))

class Band6M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band6M, self).__init__()
        self.Name = RadioBandName.B6m
        self.BeginMhz = 50000000
        self.EndMhz = 54000000
        self.Group = RadioBandGroup.VHF
        self.Type = RadioBandType.B6m
        self.SubBands = []

        self.SubBands.append(SubBand(50000000, 50100000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(50100000, 50300000, RadioMode.CwSsbModes()))
        self.SubBands.append(SubBand(50300000, 50400000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(50400000, 50500000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(50500000, 54000000, RadioMode.AllModes()))

class Band10M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band10M, self).__init__()
        self.Name = RadioBandName.B10m
        self.BeginMhz = 28000000
        self.EndMhz = 29700000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B10m
        self.SubBands = []

        self.SubBands.append(SubBand(28000000, 28070000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(28070000, 28190000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(28225000, 29700000, RadioMode.AllModes()))

class Band12M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band12M, self).__init__()
        self.Name = RadioBandName.B12m
        self.BeginMhz = 24890000
        self.EndMhz = 24990000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B12m
        self.SubBands = []

        self.SubBands.append(SubBand(24890000, 24915000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(24915000, 24929000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(24931000, 24990000, RadioMode.AllModes()))

class Band15M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band15M, self).__init__()
        self.Name = RadioBandName.B15m
        self.BeginMhz = 21000000
        self.EndMhz = 21450000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B15m
        self.SubBands = []

        self.SubBands.append(SubBand(21000000, 21070000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(21070000, 21149000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(21151000, 21450000, RadioMode.AllModes()))

class Band17M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band17M, self).__init__()
        self.Name = RadioBandName.B17m
        self.BeginMhz = 18068000
        self.EndMhz = 18168000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B17m
        self.SubBands = []

        self.SubBands.append(SubBand(18068000, 18095000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(18095000, 18109000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(18111000, 18168000, RadioMode.AllModes()))

class Band20M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band20M, self).__init__()
        self.Name = RadioBandName.B20m
        self.BeginMhz = 14000000
        self.EndMhz = 14350000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B20m
        self.SubBands = []

        self.SubBands.append(SubBand(14000000, 14070000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(14070000, 14099000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(14101000, 14300000, RadioMode.AllModes()))

class Band30M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band30M, self).__init__()
        self.Name = RadioBandName.B30m
        self.BeginMhz = 10100000
        self.EndMhz = 10150000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B30m
        self.SubBands = []

        self.SubBands.append(SubBand(10100000, 10130000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(10130000, 10150000, RadioMode.NarrowBandDigitalModes()))

class Band40M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band40M, self).__init__()
        self.Name = RadioBandName.B40m
        self.BeginMhz = 7000000
        self.EndMhz = 7200000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B40m
        self.SubBands = []

        self.SubBands.append(SubBand(7000000, 7040000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(7040000, 7060000, RadioMode.NarrowBandDigitalModes()))
        self.SubBands.append(SubBand(7060000, 7200000, RadioMode.AllModes()))

class Band60M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band60M, self).__init__()
        self.Name = RadioBandName.B60m
        self.BeginMhz = 5351500
        self.EndMhz = 5366500
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B60m
        self.SubBands = []

        self.SubBands.append(SubBand(5351500, 5354000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(5354000, 5366000, RadioMode.NarrowBandDigitalModes()))

class Band80M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band80M, self).__init__()
        self.Name = RadioBandName.B80m
        self.BeginMhz = 3500000
        self.EndMhz = 3800000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B80m
        self.SubBands = []

        self.SubBands.append(SubBand(3500000, 3570000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(3570000, 3600000, RadioMode.NarrowBandModes()))
        self.SubBands.append(SubBand(3600000, 3800000, RadioMode.AllModes()))

class Band160M(RadioBand):
    Name : str
    BeginMhz: int
    EndMhz : int
    Group : RadioBandGroup
    Type : RadioBandType
    SubBands : List[SubBand]

    def __init__(self):
        super(Band160M, self).__init__()
        self.Name = RadioBandName.B160m
        self.BeginMhz = 1810000
        self.EndMhz = 2000000
        self.Group = RadioBandGroup.HF
        self.Type = RadioBandType.B160m
        self.SubBands = []

        self.SubBands.append(SubBand(1810000, 1838000, RadioMode.CwModes()))
        self.SubBands.append(SubBand(1838000, 1840000, RadioMode.NarrowBandModes()))
        self.SubBands.append(SubBand(1840000, 2000000, RadioMode.AllModes()))

class AllBands(object):
    Band160m : Band160M = Band160M()
    Band80m : Band80M = Band80M()
    Band60m : Band60M = Band60M()
    Band40m : Band40M = Band40M()
    Band30m : Band30M = Band30M()
    Band20m : Band20M = Band20M()
    Band17m : Band17M = Band17M()
    Band15m : Band15M = Band15M()
    Band12m : Band12M = Band12M()
    Band10m : Band10M = Band10M()
    Band6m : Band6M = Band6M()
    Band4m : Band4M = Band4M()
    Band2m : Band2M = Band2M()
    Band70cm : Band70CM = Band70CM()
    AllBands : List[RadioBand] = [Band160m, Band80m, Band60m, Band40m, Band30m, Band20m, 
        Band17m, Band15m, Band12m, Band10m, Band6m, Band4m, Band2m, Band70cm]
    