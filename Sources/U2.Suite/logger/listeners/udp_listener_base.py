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

if __name__ == "__main__":
    print('This file cannot be executed directly.')
    exit(0)

from threading import Thread
from common.UdpSimpleServer import UdpSimpleServer

class UdpListenerBase():
    '''
    Represents a generic UDP listener. 
    Can be used as a base class for other listeners.
    '''
    
    _address : str
    _port : int
    _timeout : float
    _thread : Thread
    _started : bool
    
    def __init__(self) -> None:
        pass
    
    def setup(self, address, port, timeout : float = 2.0):
        self._address = address
        self._port = port
        self._timeout = timeout
        self._started = False
        self._thread = Thread(target=self.listening_worker, args = ())
        
    def start(self):
        '''Starts listening to the multicast channel.'''
        if self._started:
            return
        
        self._started = True
        self._thread.start()
        
    def stop(self) -> None:
        '''Stops listening to the multicast channel.'''
        if not self._started:
            return
        self._started = False
        self._thread.join()
        
    def listening_worker(self) -> None:
        print(f'Started listening to {self._address}:{self._port}')
        s = UdpSimpleServer()
        s.setup(self._address, self._port, self._timeout)
        while (self._started):
            (pkt, addr_port) = s.rx_packet()
            if pkt != None:
                self.packet_received(pkt, addr_port)
            
    def packet_received(self, pkt, addr_port) -> None:
        '''
        A simple method dumping the packet.
        Can be overridden in derived classes.
        '''
        print(addr_port, pkt)
        