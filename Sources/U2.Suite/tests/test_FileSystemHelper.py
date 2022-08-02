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

from locale import locale_alias
import sys
from helpers.FileSystemHelper import FileSystemHelper as fh
from os.path import join

def test_get_local_folder():
    folder = fh.getLocalFolder()
    assert folder.find('U2.Suite') > -1
    
def test_enumerate_files():
    local_folder = fh.getLocalFolder()
    path = join(local_folder, 'U2.Suite', 'ini')
    files = fh.enumerateDirectory(path, '.ini')
    assert files.count('IC-705.ini') == 1
    