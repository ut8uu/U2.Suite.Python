# Introduction 
This is a Python implementation of the U2.Suite 

# Products
- U2.Suite (a main launcher)
- BrandmeisterMonitor - allows you to monitor DMR activity in the Brandmeister network.
- Logger - a simple logging software
- FastSatEntry - a small application to create ADIF files for your LEO SAT contacts. Inspired by the FLE application.

# Setup
- Install poetry (https://python-poetry.org/docs/)
- Navigate to the 'U2.Suite' folder 
- Execute the following commands:
    $> poetry config virtualenvs.in-project true
    $> poetry shell
    $> poetry install

- IDE open project:
	+ Visual Studio (vers 2019/2022): open the solution file `U2.Suite.sln`
	+ Visual Code: open folder `U2.Suite`

# Working with the solution

## VS Code

The solution contains a U2.Suite.code-workspace file. 
Tpen the solution as a Workspace click the menu File -> Open Workspace from File...

To select the proper interpreter:
- Open any Python file
- In the bottom right corner click the Interpreter panel and select the one you just have shelled.

## MSVS 20xx

The repository contains a .sln file allowing you to open the whole solution
inside the Visual Studio 20xx. Although the MSVS 20XX is a great and comfortable
IDE, it is recommended to use VS Code.

Be aware, the MSVS solution can be outdated.

# Environments

The solution can work under any OS supporting the Puthon language.

## RIG Emulator
 
The RIG Emulator has a native support under the posix operating systems (Linux, OSx)
Unfortunately, there is no native support of file descriptors under the Windows, so you have to install the com0com software to prepare the infrastructure for the emulator.

Once installed, the com0com software creates two pairs of virtual ports.
You can use any existing pair or create a new one.
Please note, that in case of using port names in form of CNCxx you have 
to add \\.\ prefix to that name.

Open the rig\emulators\EmulatorBase.py and make the following changes:
- Set the port name on the right pane as a value for the WINDOWS_MASTER_COM_PORT constant.
- Set the port name on the left pane as a value for the WINDOWS_LISTENER_COM_PORT constant.

# Test

Be aware, some COM-port-related tests can fail because a misconfiguration.
Please refer to the [Rig Emulator] section for details.

## Shell

- Run command: 'poetry run pytest'
All tests are located in the folder "U2.Suite\tests".
Its requared to name test files with format 'test_*.py'

## VS Code

You can run tests inside the VS Code IDE. 
To achieve this configure the Test Explorer to lookup for tests in the ./tests folder.

## MSVS 20xx

Use the Test Explorer to run all the tests from the solution.

# Issues and Warnings
If you use VS 2019 for python development be awaire using python analyzer (studio version 16.11.3 and lower). Sometimes it has problem with huge CPU/Memory consumption.
Disable special settings to avoid it: https://github.com/microsoft/PTVS/pull/6197. 
I recommend to use VS Code.

# Run execution (Release)
OS Linux: required libs: 
                    sudo apt-get install libpython3.8-dev
                    sudo apt-get install libatlas-base-dev

# Used libraries

[PyQtKeyBind](https://github.com/codito/pyqtkeybind)
[py-dxcc](https://github.com/dl8bh/py-dxcc)

## Building your own binary.

Install pyinstaller.

`python3 -m pip3 install pyinstaller`

To build a binary run corresponding script.

For Linux, OSx, and Raspberry PI:

`pyinstaller BrandmeisterMonitor.spec`
`pyinstaller FastSatEntry.spec`
`pyinstaller Logger.spec`

For Windows:

`pyinstaller BrandmeisterMonitor-win.spec`
`pyinstaller FastSatEntry-win.spec`
`pyinstaller Logger-win.spec`

You will find the binary in the newly created directory `dist`.

