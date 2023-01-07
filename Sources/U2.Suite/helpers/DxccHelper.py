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

import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.FileSystemHelper import FileSystemHelper
from helpers.dxcc import dxcc

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
dxcc_inst : dxcc = None

class DxccHelper(object, metaclass=Singleton):

    _dxcc_inst : dxcc
    
    def __init__(self) -> None:
        import os

        path = str(FileSystemHelper.get_appdata_path(Path('U2.Suite') / 'dxcc')) + os.path.sep
        url = 'http://www.ok2cqr.com/linux/cqrlog/ctyfiles/cqrlog-cty.tar.gz'

        self._dxcc_inst = dxcc(path, url, AUTOFETCH_FILES=False, VERBOSE=0)
        
    def get_dxcc_inst(self) -> dxcc:
        return self._dxcc_inst

if __name__ == '__main__':
    dxcc_class = DxccHelper().get_dxcc_inst()
    
    data = dxcc_class.call2dxcc('AF4RU', None)
    assert data[1].get('name') != 'No DXCC'
    
    data = dxcc_class.call2dxcc('UT8UU', None)
    assert data[1].get('name') != 'No DXCC'
    
    data = dxcc_class.call2dxcc('LU7DXM', None)
    assert data[1].get('name') != 'No DXCC'
    
    data = dxcc_class.call2dxcc('M7AYL', None)
    assert data[1].get('name') != 'No DXCC'
    
