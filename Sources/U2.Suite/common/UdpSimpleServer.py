#
# In WSJTX parlance, the 'network server' is a program external to the wsjtx.exe program that handles packets emitted by wsjtx
#
# TODO: handle multicast groups.
#
# see dump_wsjtx_packets.py example for some simple usage
#
import socket
import struct
#import common.WsjtPackets
import logging
import ipaddress

from common.WsjtPackets import GenericWSJTXPacket

class UdpSimpleServer(object):
    logger = logging.getLogger()
    MAX_BUFFER_SIZE = GenericWSJTXPacket.MAXIMUM_NETWORK_MESSAGE_SIZE
    DEFAULT_UDP_PORT = 2237
    
    _address : str
    _port : int
    _timeout : float
    _verbose : bool
    
    #
    #
    def __init__(self):
        self.timeout = None

    def setup(self, address : str, port : int, timeout : float = 2.0, verbose : bool = False):
        self._address = address
        self._port = port
        self._timeout = timeout
        self._verbose = verbose
        
        the_address = ipaddress.ip_address(address)
        if not the_address.is_multicast:
            self._sock = socket.socket(socket.AF_INET,  # Internet
                                 socket.SOCK_DGRAM)  # UDP

            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._sock.bind((self._address, int(self._port)))
        else:
            self.multicast_setup(self._address, self._port)

        if self._timeout is not None:
            self._sock.settimeout(self._timeout)

    def multicast_setup(self, group, port=''):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(('', port))
        mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
        self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def rx_packet(self):
        try:
            pkt, addr_port = self._sock.recvfrom(self.MAX_BUFFER_SIZE)  # buffer size is 1024 bytes
            return(pkt, addr_port)
        except socket.timeout:
            if self._verbose:
                logging.debug("rx_packet: socket.timeout")
            return (None, None)

    def send_packet(self, addr_port, pkt):
        bytes_sent = self._sock.sendto(pkt,addr_port)
        self.logger.debug("send_packet: Bytes sent {} ".format(bytes_sent))

                