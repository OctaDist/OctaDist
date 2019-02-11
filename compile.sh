#!/bin/bash

echo "Compile OctaDist using PyInstaller"
echo "=================================="

pyinstaller main.py --onefile --version-file version.txt -i molecule.ico --name OctaDist-2.2-Win-x86-64 --distpath "../OctaDist-Executable"

# Optional
# --windowed (turn of window console)
