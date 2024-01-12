
import cx_Freeze
import sys
import os

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

    os.environ['TCL_LIBRARY'] = r"C:\Users\user\AppData\Local\Programs\Python\Python311\tcl\tcl8.6"
    os.environ['TK_LIBRARY'] = r"C:\Users\user\AppData\Local\Programs\Python\Python311\tcl\tk8.6"

    executables = [cx_Freeze.Executable("login.py", base=base, icon="SKicon.ico")]

    cx_Freeze.setup(
        name="SKIMS",
        options={
            "build_exe": {
                "packages": ["tkinter", "os", "sys"],
                "include_files": ['tcl86t.dll', 'tk86t.dll', 'SKicon.ico', 'CHECKFOLDER']
            }
        },
        version="1.0",
        description="SKIMS is SKYKRAFT Inventory Management System | Developed by AMAL KARN",
        executables=executables
    )
