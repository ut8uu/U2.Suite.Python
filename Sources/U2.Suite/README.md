# Introduction 
This is a Python implementation of the U2.Suite 

# Products
- U2.Suite (a main launcher)

# Setup
- Install poetry (https://python-poetry.org/docs/)
- Go to the 'U2.Suite' folder 
- Execute the following commands:
    $> poetry config virtualenvs.in-project true
    $> poetry install
    $> poetry shell

- IDE open project:
	+ Visual Studio (vers 2019/2022): open project U2.Suite.pyproj
	+ Visual Code: open folder 'U2.Suite'

# Working with the solution

## VS Code

Th solution contains a U2.Suite.code-workspace file. 
Tpen the solution as a Workspace click the menu File -> Open Workspace from File...

To select the proper interpreter:
- Open any Python file
- In the bottom right corner click the Interpreter panel and select the one you just have shelled.

## MSVS 20xx

[TBD]

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
- Run command: 'poetry run pytest'
All tests are located in the folder "U2.Suite\tests".
Its requared to name test files with format 'test_*.py'

# How to Use (Dev)
'launchSettings.py' - used for launching BP with different setup of inputs (similar as launchSettings.json in .NET projects)
Example: "poetry run python launchSettings.py"
'builder.py' - used for bp product generation (creates {bp_name}.exe and particular models).
Example: "poetry run python builder.py build"
'bp.pbspec' - used for generation bppack file (for registeration BP in Terminal). It contains BP name, version and binaries location.

# Issues and Warnings
If you use VS 2019 for python development be awaire using python analyzer (studio version 16.11.3 and lower). Sometimes it has problem with huge CPU/Memory consumption.
Disable special settings to avoid it: https://github.com/microsoft/PTVS/pull/6197. 
We recommend to use Visual Code.

# Run execution (Release)
OS Linux: required libs: 
                    sudo apt-get install libpython3.8-dev
                    sudo apt-get install libatlas-base-dev


  