'''
This file is based on the work by DL8BH.
You can find the original file in the corresponding Github repository
vy the following URL: https://github.com/dl8bh/py-dxcc

Adapted and modified by Sergey Usmanov, UT8UU
'''

"""simple dxcc-resolution program to be used with cqrlogs dxcc-tables"""
import csv, dicttoxml, json, os, re, sys, tarfile
import logging
from pathlib import Path
from collections import OrderedDict
from datetime import datetime
import urllib.request
import fileinput

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
    
