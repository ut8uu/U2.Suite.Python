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

# adapt the following variables to your needs
talkgroups = [91,3101] # Talkgroups to monitor, seperated by commas
callsigns = [] # Callsigns to monitor, seperated by commas
noisy_calls = ["L1DHAM", "N0CALL", "N0C4LL"] # Noisy calls signs that will be ignored
min_duration = 5 # Min. duration of a QSO to qualify for a push notification
min_silence = 300 # Min. time in seconds after the last QSO before a new push notification will be send
verbose = False # Enable extra messages (console only)

# Pushover configuration
pushover = False # Enable or disable notifications via Pushover
pushover_token = "1234567890" # Your Pushover API token
pushover_user = "abcdefghijklm" # Your Pushover user key

# Telegram configuration
telegram = False # Enable or disable notifications via Telegram
telegram_api_id = "1234567"
telegram_api_hash = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
telegram_username = "foo_bot"
phone = "+491234567890"

# DAPNet configuration
dapnet = False # Enable or disable notifications via dapnet
dapnet_user = "mycall"
dapnet_pass = "xxxxxxxxxxxxxxxxxxxx"
dapnet_url = 'http://www.hampager.de:8080/calls'
dapnet_callsigns = ["MYCALL"]
dapnet_txgroup = "dl-all"

# Discord Configuration
discord = False
discord_wh_url = 'DISCORD_WEBHOOK_HERE'
