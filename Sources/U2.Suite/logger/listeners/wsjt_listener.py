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

import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common.WsjtPackets import LoggedADIFPacket, WSJTXPacketClassFactory
from logger.listeners.udp_listener_base import UdpListenerBase

WSJT_UDP_PORT = 2237

class WsjtListener(UdpListenerBase):
    '''Represents a listener aimed at WSJT-X UDP packets.'''
    def __init__(self) -> None:
        super().__init__()
        
    def setup(self, address):
        super().setup(address, WSJT_UDP_PORT)
    
    def packet_received(self, pkt, addr_port) -> None:
        if (pkt != None):
            the_packet = WSJTXPacketClassFactory.from_udp_packet(addr_port, pkt)
            if type(the_packet) == LoggedADIFPacket:
                print(the_packet)
        
if __name__ == '__main__':
    '''DIrect call for demo purposes.'''
    
    from wsjt_listener import WsjtListener
    
    listener = WsjtListener()
    listener.setup('127.0.0.1')
    listener.start()
    
    input('Press Enter to continue...')
    
    listener.stop()