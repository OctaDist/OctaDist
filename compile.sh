#!/bin/bash

echo "Compile OctaDist using PyInstaller"
echo "=================================="

pyinstaller -F -w -i molecule.ico --version-file version.txt -n OctaDist-2.5-Win-x86-64

# Optional
# --onefile		or -F	(compile as a standalone executable)
# --windowed 	or -w	(turn off window console)
# -i 					(set program icon)
# --version-file		(set program version file)
# --name 		or -n 	(set program name)
