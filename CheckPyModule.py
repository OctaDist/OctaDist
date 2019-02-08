'''
OctaDist: Octahedral distortion analysis
Rangsiman Ketkaew
February 2019, Thammasat University, Thailand
'''

import sys

print("Checking the Python packages required for OctaDist")
print("--------------------------------------------------")
print("Python version in system: %s\n" % sys.version)

if sys.version_info < (3,0):
   print("OctaDist supports only for Python 3.\n")

module = ["numpy", "math", "datetime", "tkinter", "webbrowser", "matplotlib"]

S = 1

for i, mod in enumerate(module):
   try:
      import mod
      print("%s. %s was installed on system." % (int(i+1), mod))
   except ImportError:
      print("%s. %s was not found on system." % (int(i+1), mod))
      S = 0

if S == 0:
   print("\nTo install Python package, you can use command \"python -m pip install -U PACKAGENAME\"\n")


