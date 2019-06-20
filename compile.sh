#!/bin/bash

echo "Install PyInstaller"
echo "==================="

python -m pip install --upgrade --user pyinstaller

echo "Compile OctaDist using PyInstaller"
echo "=================================="

pyinstaller -F -w -n OctaDist -i octadist/logo/molecule.ico octadist/main.py

# Optional
# --onedir      or -D   (create one-folder containing packages)
# --onefile		or -F	(create one-file as a standalone executable)
# --windowed 	or -w	(turn off window console)
# --icon		or -i	(set program icon)
# --name 		or -n 	(set program name)
