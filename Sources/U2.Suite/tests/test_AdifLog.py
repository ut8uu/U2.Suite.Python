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


import datetime
import os
import unittest

from helpers.AdifHelper import ADIF_log, AdifHelper

class AdifTests(unittest.TestCase):
    '''Represents tests of ADIF helper'''

    TEST_DIR = './test_files'

    def test_CanWriteAdifFile(self)-> None:
        '''This is to test how to work with adif files'''
        TEST_DIR = './test_files'
        if not os.path.exists(TEST_DIR):
            os.mkdir(TEST_DIR)

        example_adx_file = f'{TEST_DIR}/example.adx'
        example_adif_file = f'{TEST_DIR}/example.adi'

        # Create a new log...
        log = ADIF_log()
        entry = log.newEntry()

        # New entry from K6BSD to WD1CKS
        entry['OPerator'] = 'K6BSD'
        entry['Call'] = 'WD1CKS'
        entry['QSO_Date']=datetime.datetime.now().strftime('%Y%m%d')
        entry['baNd']='20M'
        entry['mODe']='PSK'
        entry['SubMode']='PSK31'
        entry['TIME_ON']=datetime.datetime.now().strftime('%H%M')
        entry['comment_intl']=u'Testing...'

        # Write to example.adif
        AdifHelper.ExportAdif(example_adif_file, log)

        # Write to example.adx
        AdifHelper.ExportAdx(example_adx_file, log)

        # Read example.adif back...
        adif_log = AdifHelper.Import(example_adif_file)
        print(adif_log[0]['CALL'])
        print(adif_log[0]['BAND'])

        # Read example.adx back...
        adx_log = AdifHelper.Import(example_adx_file)
        print(adx_log[0]['call'],' band: ',adx_log[0]['band'])

        self.assertEqual(str(adif_log[0]['CALL']), str(adx_log[0]['CALL']))
        self.assertEqual(str(adif_log[0]['BAND']), str(adx_log[0]['BAND']))

        # Clean up... nothing interesting here...
        os.remove(example_adif_file)
        os.remove(example_adx_file)
