import sys
import os
import cx_Freeze
import matplotlib

os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python37\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python37\tcl\tK8.6'

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "tkinter", "matplotlib"],
                     "include_files": ["main.py", "calc.py",
                                       "coord.py", "draw.py", "elements.py",
                                       "linear.py", "plane.py", "popup.py",
                                       "proj.py", "tools.py", "molecule.ico"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py", base=base, icon="molecule.ico")]

cx_Freeze.setup(
    name = "OctaDist",
    version = "2.1",
    author = "Rangsiman Ketkaew",
    author_email = "rangsiman1993@gmail.com",
    description = "Octahedral Distortion Analysis",
    options = {"build_exe": build_exe_options},
    executables = executables
    )

