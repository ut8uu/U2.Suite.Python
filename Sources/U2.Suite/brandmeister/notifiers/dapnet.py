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

import bm_monitor_config as cfg

import json
import requests
from requests.auth import HTTPBasicAuth

# send pager notification via DAPNET. Disabled if not configured in config.py
def push_dapnet(msg):
    dapnet_json = json.dumps({"text": msg, "callSignNames": cfg.dapnet_callsigns, "transmitterGroupNames": [cfg.dapnet_txgroup], "emergency": True})
    response = requests.post(cfg.dapnet_url, data=dapnet_json, auth=HTTPBasicAuth(cfg.dapnet_user,cfg.dapnet_pass)) 

