#!/usr/bin/python3
"""simple dxcc-resolution program to be used with cqrlogs dxcc-tables"""
import os
import csv
from pathlib import Path
import re
from collections import OrderedDict
from datetime import datetime
import sys
import dicttoxml
import json
import urllib.request
import tarfile
import fileinput

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from helpers.FileSystemHelper import FileSystemHelper


class dxcc:
    
    GLOBAL_DXCC_LIST = {}
    NODXCC = { 'long': None, 'lat': None, 'valid_to': None, 'utc': None, 'waz': None, 'adif': None, 'itu': None, 'valid_from': None, 'name': 'No DXCC', 'continent': None }
    DEBUG = 3
    TRACE1 = 4
    TRACE2 = 5
    VERBOSE = DEBUG
    def __init__(self, CTYFILES_URL, AUTOFETCH_FILES, VERBOSE=3):
        self.CTYFILES_PATH = FileSystemHelper.relpath('data/dxcc')
        if not os.path.exists(self.CTYFILES_PATH):
            os.mkdir(self.CTYFILES_PATH)
        self.CTYFILES_URL = CTYFILES_URL
        self.AUTOFETCH_FILES = AUTOFETCH_FILES
        self.init_country_tab(None)
        self.VERBOSE = VERBOSE
        self.callsign_cache = {}
    
    def fetch_country_files(self):
        """Downloads the countryfiles from the cqrlog project"""
        if self.VERBOSE >= self.DEBUG:
            print('Fetching new countryfiles')
        httpstream = urllib.request.urlopen(self.CTYFILES_URL)
        ctyfile = tarfile.open(fileobj=httpstream, mode="r|gz")
        ctyfile.extractall(path=self.CTYFILES_PATH)

    def process_country_files(self):
        """concatenates the countryfiles in a cqrlog-compatible way"""
        ctyfiles = [
            str(Path(self.CTYFILES_PATH) / 'Country.tab'), 
            str(Path(self.CTYFILES_PATH) / 'CallResolution.tbl'), 
            str(Path(self.CTYFILES_PATH) / 'AreaOK1RR.tbl')
        ]
        with open(str(Path(self.CTYFILES_PATH) / 'country.tab'), 'w') as countrytab, fileinput.input(ctyfiles) as fin:
            for line in fin:
                countrytab.write(line)

    def pattern_to_regex(self, patternlist):
        """transform pattern from file to regex"""
        # = is the hint in country.tab, that an explicit call is given
        returnlist = []
        patternlist = patternlist.replace('  ', ' ')
        for pattern in patternlist.split(' '):
            if '%' in pattern or '#' in pattern or '=' in pattern:
                pattern = pattern.replace('%', '[A-Z]').replace('#', '[0-9]')
                pattern += '$'
            pattern = '^' + pattern
            returnlist.append(pattern)
        return returnlist

    def date_country_tab(self, date = None):
        """initializes a dict with data from the dxcc-tables from file, filtered by date"""
        if not date:
            date = datetime.utcnow()
        date_dxcc_regex = re.compile(r'((?P<from>\d\d\d\d/\d\d/\d\d)*-(?P<to>\d\d\d\d/\d\d/\d\d)*)*(=(?P<alt_dxcc>\d*))*')
        try:
            open(str(Path(self.CTYFILES_PATH) / 'country.tab'), "r")
        except FileNotFoundError:
            self.fetch_country_files()
            self.process_country_files()
        with open(str(Path(self.CTYFILES_PATH) / 'country.tab'), "r", encoding='utf-8') as countrytab:
            # split country.tab to list linewise
            countrytabcsv = csv.reader(countrytab, delimiter='|')
            dxcc_list = {}
            for row in countrytabcsv:
                row_list = list(row)
                if True:
                    indaterange = True
                    try:
                        date_dxcc_string = date_dxcc_regex.search(row_list[10])
                    except IndexError as error:
                        if self.VERBOSE >= self.DEBUG:
                            print('{} for line {}'.format(error, row_list))
                    else:
                        dateto_string = None
                        dateto = None
                        datefrom_string = None
                        datefrom = None
                        # check, if timerange is (partly) given
                        if date_dxcc_string.group('to'):
                            try:
                                dateto = datetime.strptime(date_dxcc_string.group('to'), '%Y/%m/%d')
                                dateto_string = dateto.strftime("%Y-%m-%d")
                            except ValueError as valerr:
                                if self.VERBOSE >= self.DEBUG:
                                    print('{} in date_to of line {}'.format(valerr,row_list))
                        if date_dxcc_string.group('from'):
                            try:
                                datefrom = datetime.strptime(date_dxcc_string.group('from'), '%Y/%m/%d')
                                datefrom_string = datefrom.strftime("%Y-%m-%d")
                            except ValueError as valerr:
                                if self.VERBOSE >= self.DEBUG:
                                    print('{} in date_from of line {}'.format(valerr,row_list))
                        if dateto is not None:
                            if date > dateto:
                                indaterange = False
                        if indaterange and not datefrom is None:
                            if date < datefrom:
                                indaterange = False
                        if indaterange:
                            pattern = row_list[0]
                            if row_list[9] == "R":
                                adif = date_dxcc_string.group('alt_dxcc')
                            else:
                                adif = row_list[8]
                            attributes = {
                                'details' : row_list[1],
                                'continent' : row_list[2],
                                'utc' : row_list[3],
                                'lat' : row_list[4],
                                'lng' : row_list[5],
                                'itu' : row_list[6],
                                'waz' : row_list[7],
                                'valid_from' : datefrom_string,
                                'valid_to' : dateto_string,
                                'adif' : adif
                            }
                            for singlepattern in self.pattern_to_regex(pattern.strip()):
                                # prefix non-REGEX patterns with ~
                                if row_list[9] != "R":
                                    singlepattern = '~' + singlepattern
                                dxcc_list[singlepattern] = attributes
    
        if self.VERBOSE >= self.DEBUG:
            print("{} calls parsed".format(len(dxcc_list)))
        return dxcc_list
    
    def dxcc2xml(self, dxcc):
        return dicttoxml.dicttoxml(dxcc[1], attr_type=False)
    
    def dxcc2json(self, dxcc):
        return json.dumps(dxcc[1])
    
    def init_country_tab(self, date = None, fetch_files = None):
        """builds an initial GLOBAL_DXCC_LIST, if date not defined with date from today"""
        if fetch_files is None:
            fetch_files = self.AUTOFETCH_FILES
        if not date:
            date = datetime.utcnow()
            if self.VERBOSE >= self.DEBUG:
                print("initializing GLOBAL_DXCC_LIST with date {}".format(date.strftime("%Y-%m-%d")))
        if not fetch_files:
            country_file_path = Path(self.CTYFILES_PATH) / 'Country.tab'
            source_file_path = Path(self.CTYFILES_PATH) / 'data.tar.gz'
            if not country_file_path.exists():
                if source_file_path.exists():
                    ctyfile = tarfile.open(str(source_file_path))
                    ctyfile.extractall(path=self.CTYFILES_PATH)
                else:
                    fetch_files = True                
        
        if fetch_files == True:
            if self.VERBOSE >= self.DEBUG:
                print("fetching fresh tables")
            self.fetch_country_files()
            self.process_country_files()
        self.GLOBAL_DXCC_LIST[date.strftime("%Y-%m-%d")] = self.date_country_tab(date)
    
    def get_date_country_tab(self, date = None, fetch_files = None):
        """returns date-specific country-tab, builds it, if needed"""
        if fetch_files is None:
            fetch_files = self.AUTOFETCH_FILES
        if not date:
            date = datetime.utcnow()
        if not self.GLOBAL_DXCC_LIST.get(date.strftime("%Y-%m-%d")):
            if self.VERBOSE >= self.DEBUG:
                print("{} not found in GLOBAL_DXCC_LIST, adding".format(date.strftime("%Y-%m-%d")))
            if date.strftime("%Y-%m-%d") == datetime.utcnow().strftime("%Y-%m-%d") and fetch_files == True:
                self.fetch_country_files()
                self.process_country_files()
            self.GLOBAL_DXCC_LIST[date.strftime("%Y-%m-%d")] = self.date_country_tab(date)
        else:
            if self.VERBOSE >= self.DEBUG:
                print("{} found in GLOBAL_DXCC_LIST, using that".format(date.strftime("%Y-%m-%d")))
        return self.GLOBAL_DXCC_LIST[date.strftime("%Y-%m-%d")]
    
    def call2dxcc(self, callsign, date = None):
        """does the job in resolving the callsign"""
        ORIGINALCALLSIGN = callsign
        # if date is not given, assume date is now
        if not date:
            date = datetime.utcnow()
        else:
            date = datetime.strptime(date, "%Y-%m-%d")
        datestring = date.strftime("%Y-%m-%d")
        if datestring in self.callsign_cache:
            datedict = self.callsign_cache[datestring]
            if callsign in datedict:
                if self.VERBOSE >= self.DEBUG:
                        print("cache hit: {} {}".format(datedict[callsign]["pattern"], datedict[callsign]["entry"]))
                return [datedict[callsign]["pattern"], datedict[callsign]["entry"]]
        else:
            self.callsign_cache[datestring] = {}
        direct_hit_list = {}
        prefix_hit_list = {}
        regex_hit_list = OrderedDict()
    #    DXCC_DATE_LIST =  DXCC_LIST[date.strftime("%Y-%m-%d")]
        DXCC_LIST = self.get_date_country_tab(date)
        for pattern in DXCC_LIST:
            #print(pattern)
            if "=" in pattern and len(callsign) == (len(pattern) -3):
                direct_hit_list[pattern.replace('=', '')] = DXCC_LIST[pattern]
            # ~ indicates, that a PREFIX and not a REGEX is given for CEPT based resolution
            elif "~" in pattern:
                prefix_hit_list[pattern.replace('~', '')] = DXCC_LIST[pattern]
            else:
                regex_hit_list[pattern] = DXCC_LIST[pattern]
        # chech for direct hits
        for pattern in direct_hit_list:
            if re.match(pattern, callsign):
                pattern = pattern.replace('^', '^=')
                if self.VERBOSE >= self.DEBUG:
                    print("found direct hit {} {}".format(pattern, DXCC_LIST[pattern]))
                DXCC_LIST[pattern]["callsign"] = ORIGINALCALLSIGN
                self.callsign_cache[datestring][ORIGINALCALLSIGN] = {"pattern": pattern, "entry": DXCC_LIST[pattern]}
                return [pattern, DXCC_LIST[pattern]]
        # check for portable calls, after testing for direct hits
        if '/' in callsign:
            callsign = self.handleExtendedCalls(callsign)
            if callsign == False:
                if self.VERBOSE >= self.DEBUG:
                    print("callsign not valid for DXCC")
                    self.NODXCC["callsign"] = ORIGINALCALLSIGN
                return [None, self.NODXCC]
        # check for regex hits
        for pattern in regex_hit_list:
            if pattern[1] in [callsign[0],'[']:                    
                if self.VERBOSE >= self.TRACE1:
                    print(pattern)
                if re.match(pattern, callsign):
                    if self.VERBOSE >= self.DEBUG:
                        print("found {} {}".format(pattern, DXCC_LIST[pattern]))
                    DXCC_LIST[pattern]["callsign"] = ORIGINALCALLSIGN
                    self.callsign_cache[datestring][ORIGINALCALLSIGN] = {"pattern": pattern, "entry": DXCC_LIST[pattern]}
                    return [pattern, DXCC_LIST[pattern]]
        # check for prefix hits
        hitdict = {}
        for pattern in prefix_hit_list:
            if self.VERBOSE >= self.TRACE1:
                print(pattern)
            if re.match(pattern, callsign):
                pattern = pattern.replace('^', '~^')
                if self.VERBOSE >= self.DEBUG:
                    print("found {} {}".format(pattern, DXCC_LIST[pattern]))
                DXCC_LIST[pattern]["callsign"] = ORIGINALCALLSIGN
                # There could be multiple prefixes (FW, F for example)
                hitdict[pattern] = DXCC_LIST[pattern]
        if hitdict:
            # get and return longtest hit (FW takes precedence over F)
            longestpattern = max(hitdict.keys())
            self.callsign_cache[datestring][ORIGINALCALLSIGN] = {"pattern": longestpattern, "entry": hitdict[longestpattern]}
            return[longestpattern, hitdict[longestpattern]]
        if self.VERBOSE >= self.DEBUG:
            print("no matching dxcc found")
        self.NODXCC["callsign"] = ORIGINALCALLSIGN
        self.callsign_cache[datestring][ORIGINALCALLSIGN] = {"pattern": None, "entry": self.NODXCC}
        return[None, self.NODXCC]
    
    def handleExtendedCalls(self, callsign):
        """handles complexer callsigns with occurences of /"""
        if self.VERBOSE >= self.DEBUG:
            print('{} is an extended callsign'.format(callsign))
        callsign_parts = callsign.split('/')
        # Callsign has to parts, example 5B/DL8BH
        if len(callsign_parts) == 2:
            if self.VERBOSE >= self.DEBUG:
                print('callsign has 2 parts')
            prefix = callsign_parts[0]
            suffix = callsign_parts[1]
            if suffix in ['MM', 'MM1', 'MM2', 'MM3', 'AM']:
                return False
            # only one character of suffix: DL8BH/P DL8BH/1
            if len(suffix) == 1:
                if suffix in ['M', 'P'] and not re.match(r'^LU', prefix):
                    return prefix
                # KL7AA/1 -> W1
                if re.match(r'[0-9]', suffix[0]):
                    if self.VERBOSE >= self.DEBUG:
                        print('{} matches pattern KL7AA/1'.format(callsign))
                    if re.match(r'^A[A-L]|^[KWN]',prefix):
                        print('resulting callsign is: {}'.format('W{}'.format(suffix[0])))
                        return 'W{}'.format(suffix[0])
                    # RA1AAA/2 -> RA2AAA
                    else:
                        prefix_to_list = list(prefix)
                        prefix_to_list[2] = suffix[0]
                        prefix = ''.join(prefix_to_list)
                        if self.VERBOSE >= self.DEBUG:
                            print('resulting callsign is: {}'.format(prefix))
                        return prefix
                # handle special suffixes from argentina
                elif re.match(r'^[A-DEHJL-VX-Z]', suffix):
                    if self.VERBOSE >= self.DEBUG:
                        print('{} suffix from argentina?'.format(callsign))
                    # list of argenitian prefixes AY, AZ, LO-LW
                    if re.match(r'^(AY|AZ|L[O-W])', prefix):
                        # LU1ABC/z -> LU1zAB
                        prefix_to_list = list(prefix)
                        prefix_to_list[3] = suffix
                        prefix = ''.join(prefix_to_list)
                        print('resulting callsign is: {}'.format(prefix))
                        return prefix
                    else:
                        return callsign
            if len(prefix) <= 3 < len(suffix):
                return prefix
            if 1 < len(suffix) < 5:
                if suffix in ['QRP', 'QRPP']:
                    return prefix
                else:
                    return prefix
            if len(prefix) > len(suffix):
                return prefix
            else:
                return suffix
        elif len(callsign_parts) == 3:
            if self.VERBOSE >= self.DEBUG:
                print('callsign has 3 parts')
            prefix = callsign_parts[0]
            middle = callsign_parts[1]
            suffix = callsign_parts[2]
            # maritime mobile and aeronautic mobile is not valid for DXCC
            if suffix in ['MM', 'AM']:
                return False
            if suffix in ['M', 'QRP', 'P']:
                return self.handleExtendedCalls('{}/{}'.format(prefix, middle))
            if len(middle) > 0:
                # KL7AA/1/M -> W1
                if re.match(r'[0-9]', middle[0]):
                    if self.VERBOSE >= self.DEBUG:
                        print('{} matches pattern KL7AA/1/M'.format(callsign))
                    if re.match(r'^A[A-L]|^[KWN]',prefix):
                        return 'W{}'.format(middle[0])
                    # RA1AAA/2/M -> RA2AAA
                    else:
                        prefix_to_list = list(prefix)
                        prefix_to_list[2] = middle[0]
                        prefix = ''.join(prefix_to_list)
                        if self.VERBOSE >= self.DEBUG:
                            print('resulting callsign is: {}'.format(prefix))
                        return prefix
            # Fuzzy match for implausible suffixes like MM0/DL8BH/FOO
            if len(middle) > len(prefix) and len(middle) > len(suffix) and self.handleExtendedCalls(prefix + '/' + middle) != None:
                return self.handleExtendedCalls(prefix + '/' + suffix)
            else:
                 return None

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DxccHelper(object, metaclass=Singleton):

    _initiated : bool
    _pydxcc_instance : dxcc
    
    def __init__(self) -> None:
        self._initiated = False
        pass

    def Configure(self) -> None:
        if self._initiated:
            return
        
        import os
        import configparser

        CFG = configparser.ConfigParser()
        cfg_path = Path(os.path.dirname(os.path.abspath(__file__))) / 'DxccHelper.cfg'
        CFG.read(str(cfg_path))
        self.CTYFILES_URL = CFG.get('CTYFILES', 'url')
        self.AUTOFETCH_FILES = CFG.getboolean('CTYFILES', 'autofetch')

        self._pydxcc_instance = dxcc(self.CTYFILES_URL, self.AUTOFETCH_FILES)
        self._initiated = True
        
    def resolve_call(self, call : str, date : datetime = None) -> list:
        '''
        Resolves given call and returns the DXCC record.
        Returns NoDxcc record if the call was not resolved.
        '''
        if not self._initiated:
            self.Configure()
            
        return self._pydxcc_instance.call2dxcc(call, date)
    
if __name__ == '__main__':
    data = DxccHelper().resolve_call('UT8UU', None)
    assert data != None
    assert data[1].get('details') == 'Ukraine'