import os, serial, threading, time
from common.contracts.RigCommand import RigCommand
from common.contracts.RigCommands import RigCommands
from helpers.FileSystemHelper import FileSystemHelper
from helpers.RigHelper import RigHelper
from typing import List, Tuple

if os.name.lower().find('posix') > -1:
    import pty

_serial_port : serial.Serial
_port : str
_started = False
_thread : threading.Thread
_ini_file_name = 'IC-705.ini'
_commands : RigCommands
_prefix : bytearray
_freqa = 14200000
_freqb = 145500250

def start():
    master,slave = pty.openpty() #open the pseudoterminal
    s_name = os.ttyname(slave) #translate the slave fd to a filename

    # load commands from the INI file
    path = os.path.join(FileSystemHelper.getIniFilesFolder(), _ini_file_name)
    _commands = RigHelper.loadRigCommands(path)

    #create a separate thread that listens on the master device for commands
    _thread = threading.Thread(target=listener, args=[master, _commands])
    _thread.start()

    #open a pySerial connection to the slave
    _serial_port = serial.Serial(s_name, 2400, timeout=1)
    _started = True

def stop():
    if _started:
        return

    _started = False
    _serial_port.write(_prefix + b'exit')
    _serial_port.close()

    _thread.join(5)

def parse_command(command : bytearray) -> Tuple[bool, RigCommand]:
    if len(command) < 3:
        return False, None
    
    for item in _commands.InitCmd:
        if item.Code == command:
            return (True, item)
    # end for

    if _prefix + b'exit' == command:
        return (True, b'exit')

    return (False, b'')

def listener(port: int, commands: RigCommands):
    #continuously listen to commands on the master device
    res = b''
    while 1:
        if not _started:
            return

        res += os.read(port, 1)
        #print("command: %s" % res)

        if res.endswith(_prefix):
            res = _prefix # reset the command
            continue # resume reading

        if res.find(b'exit') > -1:
            return

        (parsed, command) = parse_command(self, res)
        if not parsed:
            continue

        if command != None:
            os.write(port, command.Validation.Flags)

        if not _started:
            return



def test_serial():
    _started = False

    """Start the testing"""
    start()

    for init_command in _commands.InitCmd:
        print(f'Testing command {init_command.Code}')
        _serial_port.write(init_command.Code)
        response = b''
        while len(response) < init_command.ReplyLength:
            #read the response
            res += _serial_port.read()

        if response != init_command.Validation.Flags:
            stop()
            assert False
        else:
            print('Correct response from emulator received.')
    
    stop()

if __name__=='__main__':
    test_serial()
