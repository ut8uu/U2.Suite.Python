import os, pty
from sys import prefix
from typing import Literal, Tuple
from serial import Serial
import threading

class x13():
    px = b'\xfe\xfe'
    __started = False
    __thread : threading.Thread
    __serial_port_name : str

    def start(self):
        if self.__started:
            return

        self.start_listener()
        self.__started = True

    def stop(self):
        if not self.__started:
            return
        self.__started = False

    def start_listener(self):
        """Start the testing"""
        master,slave = pty.openpty() #open the pseudoterminal
        self.__serial_port_name = os.ttyname(slave) #translate the slave fd to a filename

        #create a separate thread that listens on the master device for commands
        self.__thread = threading.Thread(target=self.listener, args=[master])
        self.__thread.start()

    def parse_command(self, command : bytearray) -> Tuple[bool, str]:
        cmd = command.removeprefix(self.px)
        if len(cmd) == 0:
            return False
        match cmd:
            case b'cmd1':
                return (True, cmd)
            case b'cmd2':
                return (True, cmd)
            case b'exit':
                return (True, cmd)

        return (False, b'')

    def listener(self, port):
        #continuously listen to commands on the master device
        while 1:
            res = b''
            while True:
                res += os.read(port, 1)
                if res == self.px:
                    continue
                if res.endswith(self.px):
                    if len(res) > 2:
                        os.write(port, b'command reset')
                    res = self.px
                    continue
                (parsed, command) = self.parse_command(res)
                if parsed:
                    break
            print("command: %s" % res.removeprefix(self.px))

            match command:
                case b'cmd1':
                    os.write(port, b'resp1')
                case b'cmd2':
                    os.write(port, b'resp2')
                case b'exit':
                    os.write(port, b'exiting')
                    break
                case _:
                    os.write(port, b"I dont understand\r\n")

    def read_from_serial(self, ser : Serial, count: int) -> str:
        res = b''
        while len(res) < count:
            #read the response
            res += ser.read()
        print("result: %s" % res.strip())

    def send_receive(self, ser : Serial, data: bytes, count: int):
        ser.write(self.px + data) #write the first command
        self.read_from_serial(ser, count)

    def test_serial(self):
        self.start()

        #open a pySerial connection to the slave
        ser = Serial(self.__serial_port_name, 2400, timeout=1)
        self.send_receive(ser, b'cmd1', 5)
        self.send_receive(ser, b'cmd2', 5)
        self.send_receive(ser, b'exit', 7)

        self.__thread.join(1)
        self.stop()

if __name__=='__main__':
    x = x13()
    x.test_serial()
