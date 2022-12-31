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

import telebot 
from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient, sync, events 

# Send push notification via Telegram. Disabled if not configured in config.py
def push_telegram(msg):
    client = TelegramClient('bm_bot', cfg.telegram_api_id, cfg.telegram_api_hash) 
    client.connect() 
    if not client.is_user_authorized(): 
        client.send_code_request(cfg.phone) 
        client.sign_in(cfg.phone, input('Please enter the code which has been sent to your phone: ')) 
    try: 
        receiver = InputPeerUser('user_id', 'user_hash') 
        client.send_message(cfg.telegram_username, msg) 
    except Exception as e: 
        print(e); 
    client.disconnect() 

