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
import datetime as dt
import json
import socketio
from threading import Thread
import time

if cfg.discord:
    from brandmeister.notifiers.discord import push_discord
    
if cfg.pushover:
    from brandmeister.notifiers.pushover import push_pushover
    
if cfg.telegram:
    from brandmeister.notifiers.telegram import push_telegram
    
class BmMonitorClientNamespace(socketio.ClientNamespace):
    
    def __init__(self, namespace=None):
        #self._monitor = monitor
        super().__init__(namespace)
        
    def setup(self, monitor):
        self._monitor = monitor
        
    def on_connect(self):
        print('connection established')
        pass

    def on_disconnect(self):
        print('disconnected from server')
        pass

    def on_mqtt(self, data):
        self._monitor.ProcessMqtt(data)


class BrandmeisterMonitor(object):
    '''Represents a monitor for BM network activities.'''
    
    #############################
    ##### Define Variables

    _sio : socketio.Client
    _last_TG_activity : dict
    _last_OM_activity : dict
    _started : bool
    _thread : Thread
    
    _dapnet_imported : bool
    _discord_imported : bool
    _pushover_imported : bool
    _telegram_imported : bool
    
    def __init__(self) -> None:
        self._started = False
        self._dapnet_imported = False
        self._discord_imported = False
        self._pushover_imported = False
        self._telegram_imported = False
        
        self._sio = socketio.Client()
        namespace = BmMonitorClientNamespace()
        namespace.setup(self)
        self._sio.register_namespace(namespace)

        self._last_TG_activity = {}
        self._last_OM_activity = {}
        
        self._thread = Thread(target=self.monitor_worker, args = ())

        pass

    def Start(self) -> None:
        if self._started:
            return
        self._thread.start() 
        self._started = True
        
    def Stop(self) -> None:
        if not self._started:
            return
        self._started = False
        self._sio.disconnect()

    def monitor_worker(self) -> None:
        self._sio.connect(url='https://api.brandmeister.network', socketio_path="/lh/socket.io", transports="websocket")
        self._sio.wait()
        print('Thread exit...')

    #############################
    ##### Define Functions

    def construct_message(self, c):
        tg = c["DestinationID"]
        out = ""
        duration = c["Stop"] - c["Start"]
        # convert unix time stamp to human readable format
        time = dt.datetime.utcfromtimestamp(c["Start"]).strftime("%Y/%m/%d %H:%M")
        # construct text message from various transmis_sion properties
        out += c["SourceCall"] + ' (' + c["SourceName"] + ') was active on '
        out += str(tg) + ' (' + c["DestinationName"] + ') at '
        out += time + ' (' + str(duration) + ' seconds)'
        # finally return the text message
        return out

    def ProcessMqtt(self, data):
        call = json.loads(data['payload'])
        tg = call["DestinationID"]
        callsign = call["SourceCall"]
        start_time = call["Start"]
        stop_time = call["Stop"]
        notify = False
        now = int(time.time())

        if cfg.verbose and callsign in cfg.noisy_calls:
            print("ignored noisy ham " + callsign)
        
        else:
            # check if callsign is monitored, the transmis_sion has already been finished
            # and the person was inactive for n seconds
            if callsign in cfg.callsigns:
                if callsign not in self._last_OM_activity:
                    self._last_OM_activity[callsign] = 9999999
                inactivity = now - self._last_OM_activity[callsign]
                if callsign not in self._last_OM_activity or inactivity >= cfg.min_silence:
                    # If the activity has happened in a monitored TG, remember the transmis_sion start time stamp
                    if tg in cfg.talkgroups and stop_time > 0:
                        self._last_TG_activity[tg] = now
                    # remember the transmis_sion time stamp of this particular DMR user
                    self._last_OM_activity[callsign] = now
                    notify = True
            # Continue if the talkgroup is monitored, the transmis_sion has been
            # finished and there was no activity during the last n seconds in this talkgroup
            elif tg in cfg.talkgroups and stop_time > 0:# and callsign not in cfg.noisy_calls:
                if tg not in self._last_TG_activity:
                    self._last_TG_activity[tg] = 9999999
                inactivity = now - self._last_TG_activity[tg]
                # calculate duration of key down
                duration = stop_time - start_time
                if duration > cfg.min_duration:
                    print(f'[{tg}] {callsign} for {duration} seconds.')
                # only proceed if the key down has been long enough
                if duration >= cfg.min_duration:
                    if tg not in self._last_TG_activity or inactivity >= cfg.min_silence:
                        notify = True
                    elif cfg.verbose:
                        print("ignored activity in TG " + str(tg) + " from " + callsign + ": last action " + str(inactivity) + " seconds ago.")
                    self._last_TG_activity[tg] = now


            if notify:
                if cfg.pushover:
                    if not self._pushover_imported:
                        from brandmeister.notifiers.pushover import push_pushover
                        self._pushover_imported = True
                    self.push_pushover(self.construct_message(call))
                if cfg.telegram:
                    if not self._telegram_imported:
                        from brandmeister.notifiers.telegram import push_telegram
                        self._telegram_imported = True
                    push_telegram(self.construct_message(call))
                if cfg.dapnet:
                    if not self._dapnet_imported:
                        from brandmeister.notifiers.dapnet import push_dapnet
                        self._dapnet_imported = True
                    push_dapnet(self.construct_message(call))
                if cfg.discord:
                    if not self._discord_imported:
                        from brandmeister.notifiers.discord import push_discord
                        self._discord_imported = True
                    push_discord(cfg.discord_wh_url, self.construct_message(call))

if __name__ == '__main__':
    monitor = BrandmeisterMonitor()
    monitor.Start()
    input('Press Enter to finish.')
    monitor.Stop()