import cx_Freeze
import sys
import matplotlib
import numpy
import os

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base, icon="tomato-icon2.ico")]

os.environ['TCL_LIBRARY'] = r'C:\Users\joshu\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\joshu\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'


cx_Freeze.setup(
    name = "RT-Client",
    options = {"build_exe": {"packages":["tkinter","matplotlib", "numpy"]}},
    version = "0.01",
    description = "Rotten Tomatoes grapher application",
    executables = executables
    )