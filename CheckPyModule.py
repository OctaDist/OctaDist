#!/usr/bin/env python

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

import sys

print("Checking the Python packages required for OctaDist")
print("--------------------------------------------------")
print("Python version in system: %s\n" % sys.version)

if sys.version_info < (3,):
    print("OctaDist supports only for Python 3.\n")
    print("Please upgrade your Python to version 3 (Python 3.7 is recommended).")

module = ["numpy", "scipy", "matplotlib", "rmsd"]

S = False

for i, mod in enumerate(module):
    try:
        __import__(mod)
        print("[/] %s. %s was installed on system." % (int(i + 1), mod))
    except ImportError:
        print("[x] %s. %s was not found on system." % (int(i + 1), mod))
        print(
        "\nTo install Python package, you can use command \"python -m pip install -U PACKAGE_NAME\"\n"
        )
