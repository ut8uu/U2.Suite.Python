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

from common.contracts.RigCommands import RigCommands
from manyrig.rig.CustomRig import CustomRig
from manyrig.rig.enums.RigControlType import RigControlType

class Rig(CustomRig):
    
    def __init__(self, 
        control_type: RigControlType, 
        rig_number: int,
        application_id: str):
        super().__init__(control_type, rig_number, application_id)
