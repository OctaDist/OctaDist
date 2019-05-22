"""
OctaDist: Octahedral distortion analysis
Rangsiman Ketkaew
February 2019, Thammasat University, Thailand
"""

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
        S = True

if S:
    print("\nTo install Python package, you can use command \"python -m pip install -U PACKAGE_NAME\"\n")
