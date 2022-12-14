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

import datetime as dt
import json
import logging
import os
import sys
import socketio
from threading import Thread, Timer
import time
from PyQt5.QtCore import QObject, pyqtSignal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from brandmeister.BmMonitorPreferences import BrandmeisterMonitorApplicationPreferences
import brandmeister.BmMonitorConstants as const
from helpers.DxccHelper import DxccHelper
from helpers.dxcc import dxcc

class MonitoringStats(object):
    def __init__(self, total : int = 0, caught : int = 0) -> None:
        self._total = total
        self._caught = caught
        pass
    
    @property
    def Total(self) -> int:
        return self._total
    @Total.setter
    def Total(self, value : int) -> None:
        self._total = value

    @property
    def Caught(self) -> int:
        return self._caught
    @Caught.setter
    def Caught(self, value : int) -> None:
        self._caught = value

class MonitorReportData(object):
    """Represents a data to report outside of the monitor."""
    def __init__(self, data: dict) -> None:
        self._id = 0
        self._timestamp = data.get(const.KEY_TIMESTAMP, dt.datetime.utcnow())
        self._tg = data[const.KEY_TALK_GROUP]
        self._callsign = data[const.KEY_CALLSIGN]
        dxcc_id = data.get(const.KEY_DXCC, 0)
        if dxcc_id == None:
            dxcc_id = 0
        self._dxcc = dxcc_id
        self._duration = data[const.KEY_DURATION]
        pass
    
    @property
    def Id(self) -> int:
        return self._id
    @Id.setter
    def Id(self, value : int) -> None:
        self._id = value
    
    @property
    def Timestamp(self) -> dt.datetime:
        return self._timestamp
    
    @property
    def TG(self) -> str:
        return self._tg
    
    @property
    def Callsign(self) -> str:
        return self._callsign
    
    @property
    def Dxcc(self) -> int:
        return self._dxcc
    
    @property
    def Duration(self) -> int:
        return self._duration

class MonitorReportEvent(QObject):
    report = pyqtSignal(MonitorReportData, MonitoringStats)
    heartbeat = pyqtSignal(MonitoringStats)
    
class BmMonitorClientNamespace(socketio.ClientNamespace):
    
    def __init__(self, namespace=None):
        #self._monitor = monitor
        super().__init__(namespace)
        
    def setup(self, monitor):
        self._monitor = monitor
        
    def on_connect(self):
        logging.info('connection established')
        pass

    def on_disconnect(self):
        logging.info('disconnected from server')
        pass

    def on_mqtt(self, data):
        self._monitor.RegisterMqtt(data)

class BrandmeisterMonitorCore(object):
    """Represents a monitor for BM network activities."""
    
    #############################
    ##### Define Variables

    _preferences : BrandmeisterMonitorApplicationPreferences

    _monitor_report_event : MonitorReportEvent
    _sio : socketio.Client
    _last_DXCC_activity : dict
    _last_TG_activity : dict
    _last_OM_activity : dict
    _started : bool
    _thread : Thread
    _heartbeat_timer : Timer
    _mqtt_process_timer : Timer
    
    _dapnet_imported : bool
    _discord_imported : bool
    _pushover_imported : bool
    _telegram_imported : bool
    
    _monitoringStats : MonitoringStats
    
    _dxcc_inst : dxcc
    _mqtt_data : list
    
    def __init__(self) -> None:
        self._started = False
        self._dapnet_imported = False
        self._discord_imported = False
        self._pushover_imported = False
        self._telegram_imported = False
        
        self._mqtt_data = []
        
        self._monitoringStats = MonitoringStats()
        
        self._preferences = BrandmeisterMonitorApplicationPreferences()
        
        self._dxcc_inst = DxccHelper().get_dxcc_inst()
        
        self._sio = socketio.Client()
        namespace = BmMonitorClientNamespace()
        namespace.setup(self)
        self._sio.register_namespace(namespace)

        self._last_TG_activity = {}
        self._last_OM_activity = {}
        self._last_DXCC_activity = {}
        
        self._preferences.PreferencesChanged.changed.connect(self.preferences_changed)
        
        self._monitor_report_event = MonitorReportEvent()
        self._heartbeat_timer = Timer(1, self.heartbeat)
        self._heartbeat_timer.start()
        
        self.StartMqttProcessorTimer()
        pass

    @property
    def Preferences(self) -> BrandmeisterMonitorApplicationPreferences:
        return self._preferences
    
    """==================================================================="""
    @property
    def MonitorReport(self) -> MonitorReportEvent:
        return self._monitor_report_event
    
    """==================================================================="""
    def heartbeat(self):
        self._monitor_report_event.heartbeat.emit(self._monitoringStats)
        if self._started:
            self._heartbeat_timer = Timer(1, self.heartbeat)
            self._heartbeat_timer.start()
    
    """==================================================================="""
    def preferences_changed(self) -> None:
        """Handles changing of the application preferences."""

    def Start(self) -> None:
        if self._started:
            return
        self._thread = Thread(target=self.monitor_worker, args = ())
        self._thread.start() 
        self._started = True
        
        # launch the heartbeat
        self.heartbeat()        
        self.StartMqttProcessorTimer()
    
    def StartMqttProcessorTimer(self):
        if not self._started:
            return
        
        self._mqtt_process_timer = Timer(1, self.HandleTimerTick)
        self._mqtt_process_timer.start()
    
    def Stop(self) -> None:
        if not self._started:
            return
        self._started = False
        self._sio.disconnect()

    def OnDisconnectedFromServer(self):
        self._started = False

    def Say(self, msg : str) -> None:
        if self._preferences.Verbose:
            logging.info(msg)

    def monitor_worker(self) -> None:
        logging.info(f'Starting monitoring of TG {self._preferences.TalkGroups}')        
        
        while self._started:
            try:
                self._sio.connect(url='https://api.brandmeister.network', socketio_path="/lh/socket.io", transports="websocket")
                self._sio.wait()
            except Exception as ex:
                logging.exception(ex)
                time.sleep(1)

        self.Say('Thread exit...')

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

    def RegisterMqtt(self, data):
        self._mqtt_data.append(data)
        
    def HandleTimerTick(self) -> None:
        """Handles a tick from the MqttProcessTimer."""
        if not self._started:
            return
        
        print(f'MQTT Timer tick. {len(self._mqtt_data)} items in queue.')
        try:
            while True:
                if len(self._mqtt_data) == 0:
                    break
                item = self._mqtt_data[len(self._mqtt_data)-1]
                item_to_process = item.copy()
                self._mqtt_data.remove(item)
                self.ProcessMqtt(item_to_process)
        except Exception as ex:
            logging.exception(ex)

        # start the timer again
        self.StartMqttProcessorTimer()
    
    def ProcessMqtt(self, data): 
        
        call = json.loads(data['payload'])
        tg = call["DestinationID"]
        callsign = call["SourceCall"]
        if callsign == None or len(callsign) == 0:
            return
        start_time = call["Start"]
        stop_time = call["Stop"]
        notify = False
        now = int(time.time())

        if self._preferences.Verbose and callsign in self._preferences.NoisyCalls:
            logging.info("Ignored noisy ham " + callsign)
        
        else:
            self._monitoringStats.Total += 1

            dxcc_data = self._dxcc_inst.call2dxcc(callsign.upper())
            adif = dxcc_data[1].get('adif', '0')
            dxcc_id = 0
            if adif != None:
                dxcc_id = int(adif)
            report : MonitorReportData = None
            
            # check if callsign is monitored, the transmis_sion has already been finished
            # and the person was inactive for n seconds
            if self._preferences.UseCallsigns and callsign in self._preferences.Callsigns:
                if callsign not in self._last_OM_activity:
                    self._last_OM_activity[callsign] = 9999999
                inactivity = now - self._last_OM_activity[callsign]
                if inactivity >= self._preferences.MinSilenceSec or callsign not in self._last_OM_activity:
                    # If the activity has happened in a monitored TG, remember the transmis_sion start time stamp
                    if stop_time > 0 and tg in self._preferences.TalkGroups:
                        self._last_TG_activity[tg] = now
                    # remember the transmis_sion time stamp of this particular DMR user
                    self._last_OM_activity[callsign] = now
                    notify = True
            # Continue if the talkgroup is monitored, the transmission has been
            # finished and there was no activity during the last n seconds in this talkgroup
            if stop_time > 0 and self._preferences.UseTalkGroups and tg in self._preferences.TalkGroups:# and callsign not in cfg.noisy_calls:
                if tg not in self._last_TG_activity:
                    self._last_TG_activity[tg] = 9999999
                inactivity = now - self._last_TG_activity[tg]
                # calculate duration of key down
                duration = stop_time - start_time
                if duration > self._preferences.MinDurationSec:
                    self.Say(f'[{tg}] {callsign} for {duration} seconds.')
                    report_data = {
                        const.KEY_TIMESTAMP : dt.datetime.utcnow(),
                        const.KEY_CALLSIGN : callsign,
                        const.KEY_DXCC : dxcc_id,
                        const.KEY_TALK_GROUP : tg,
                        const.KEY_DURATION : duration
                    }
                    report = MonitorReportData(report_data)
                # only proceed if the key down has been long enough
                if duration >= self._preferences.MinDurationSec:
                    if tg not in self._last_TG_activity or inactivity >= self._preferences.MinSilenceSec:
                        notify = True
                    else:
                        self.Say("ignored activity in TG " + str(tg) + " from " + callsign + ": last action " + str(inactivity) + " seconds ago.")
                    self._last_TG_activity[tg] = now

            # Continue if the DXCC is monitored, the transmission has been
            # finished and there was no activity during the last n seconds in this talkgroup
            if self._preferences.UseCountries:
                #self.Say(f'{callsign} DXCC [{dxcc_id}]')
                if dxcc_id != None and stop_time > 0 \
                    and dxcc_id in self._preferences.Countries:
                    if dxcc_id not in self._last_DXCC_activity:
                        self._last_DXCC_activity[dxcc_id] = 9999999
                    inactivity = now - self._last_DXCC_activity[dxcc_id]
                    # calculate duration of key down
                    duration = stop_time - start_time
                    if duration > self._preferences.MinDurationSec:
                        #self.Say(f'DXCC [{dxcc_id}] {callsign} for {duration} seconds.')
                        report_data = {
                            const.KEY_TIMESTAMP : dt.datetime.utcnow(),
                            const.KEY_CALLSIGN : callsign,
                            const.KEY_DXCC : dxcc_id,
                            const.KEY_TALK_GROUP : tg,
                            const.KEY_DURATION : duration
                        }
                        report = MonitorReportData(report_data)
                    # only proceed if the key down has been long enough
                    if duration >= self._preferences.MinDurationSec:
                        if tg not in self._last_DXCC_activity \
                            or inactivity >= self._preferences.MinSilenceSec:
                            notify = True
                        elif self._preferences.Verbose:
                            logging.info("ignored activity in DXCC " + str(dxcc_id) + " from " + callsign + ": last action " + str(inactivity) + " seconds ago.")
                        self._last_TG_activity[tg] = now

            if report != None:
                self._monitoringStats.Caught += 1
                self._monitor_report_event.report.emit(report, self._monitoringStats)

            if notify:
                if self._preferences.NotifyPushover:
                    if not self._pushover_imported:
                        from brandmeister.notifiers.pushover import push_pushover
                        self._pushover_imported = True
                    self.push_pushover(self.construct_message(call))
                if self._preferences.NotifyTelegram:
                    if not self._telegram_imported:
                        from brandmeister.notifiers.telegram import push_telegram
                        self._telegram_imported = True
                    push_telegram(self.construct_message(call))
                if self._preferences.NotifyDapnet:
                    if not self._dapnet_imported:
                        from brandmeister.notifiers.dapnet import push_dapnet
                        self._dapnet_imported = True
                    push_dapnet(self.construct_message(call))
                if self._preferences.NotifyDiscord:
                    if not self._discord_imported:
                        from brandmeister.notifiers.discord import push_discord
                        self._discord_imported = True
                    push_discord(self._preferences.NotifyDiscordWhUrl, self.construct_message(call))

if __name__ == '__main__':
    monitor = BrandmeisterMonitorCore()
    monitor.Start()
    input('Press Enter to finish...')
    monitor.Stop()