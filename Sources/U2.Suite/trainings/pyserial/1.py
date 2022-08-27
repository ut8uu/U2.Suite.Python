import os, pty
from sys import prefix
from typing import Literal, Tuple
from serial import Serial
import threading

px = b'\xfe\xfe'

def parse_command(command : bytearray) -> Tuple[bool, str]:
    cmd = command.removeprefix(px)
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

def listener(port):
    #continuously listen to commands on the master device
    while 1:
        res = b''
        while True:
            res += os.read(port, 1)
            if res == px:
                continue
            if res.endswith(px):
                if len(res) > 2:
                    os.write(port, b'command reset')
                res = px
                continue
            (parsed, command) = parse_command(res)
            if parsed:
                break
        print("command: %s" % res)

        match command:
            case b'cmd1':
                os.write(port, b'resp1\r\n')
            case b'cmd2':
                os.write(port, b'resp2\r\n')
            case b'exit':
                os.write(port, b'exiting\r\n')
                break
            case _:
                os.write(port, b"I dont understand\r\n")

def test_serial():
    """Start the testing"""
    master,slave = pty.openpty() #open the pseudoterminal
    s_name = os.ttyname(slave) #translate the slave fd to a filename

    #create a separate thread that listens on the master device for commands
    thread = threading.Thread(target=listener, args=[master])
    thread.start()

    #open a pySerial connection to the slave
    ser = Serial(s_name, 2400, timeout=1)
    ser.write(px + b'cmd1') #write the first command
    res = b''
    while not res.endswith(b'\r\n'):
        #read the response
        res +=ser.read()
    print("result: %s" % res.strip())
    ser.write(px + b'cmd2') #write a second command
    res = b""
    while not res.endswith(b'\r\n'):
        #read the response
        res +=ser.read()
    print("result: %s" % res.strip())

    ser.write(px + b'exit')
    thread.join(1)

if __name__=='__main__':
    test_serial()
