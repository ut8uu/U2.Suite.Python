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

from rig.Rig import Rig
from contracts.RigCommands import RigCommands
from contracts.RigSettings import RigSettings
from rig.enums.RigControlType import RigControlType

class HostRig(Rig):
    __application_id: int
    __rig_commands: RigCommands
    __rig_number: int
    __rig_settings: RigSettings

    def __init__(self, rig_number:int, application_id:int, 
                 rig_settings:RigSettings, rig_commands:RigCommands):
        __rig_number = rig_number
        __application_id = application_id
        __rig_settings = rig_settings
        __rig_commands = rig_commands
        super().__init__(RigControlType.host)
        
        