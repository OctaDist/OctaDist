#!/bin/bash

# OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
