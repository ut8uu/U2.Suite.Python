from operator import truediv
import os, pty
from sys import prefix
import time
from typing import Literal, Tuple
from serial import Serial
import threading

class x:

    _started = False

    def __init__(self) -> None:
        self._started = False
        pass

    def listener(self, port):

        while True:
            if not self._started:
                break
            res = b''
            try:
                while True:
                    if not self._started:
                        break
                    res += os.read(port, 1)

                    if len(res) > 3:
                        print(res)
                        break

            except Exception:
                """"""
        print('exiting the thread')

    def test1(self):
        """"""
        self._started = True

        self._master_port,slave = pty.openpty() #open the pseudoterminal
        self._serial_port_name = os.ttyname(slave) #translate the slave fd to a filename
        thread = threading.Thread(target=self.listener, args=[self._master_port])
        thread.start()

        serial = Serial(self._serial_port_name)
        print('12345')
        serial.write(b'12345')
        print('mama')
        serial.write(b'mama')
        print('exit')
        serial.write(b'exit')

        time.sleep(5)

        self._started = False
        print('234')
        serial.write(b'234')


if __name__=='__main__':
    xx = x()
    xx.test1()
    #time.sleep(100)  # import time
