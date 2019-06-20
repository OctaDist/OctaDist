=================
Program structure
=================

Program structure of OctaDist
-----------------------------

==========  ================================================
Function    Description
==========  ================================================
main        Main program
calc        Calculating distortion parameters
draw        Displaying molecule
elements    Atomic properties
linear      Built-in mathematical functions
molecule    Manipulating atomic coordinates
plane       Manipulate projection plane
plot        Plotting graph and chart
popup       Error, warning, and info messages
projection  2D & 3D vector projections
scripting   Interactive code Console
structure   All data about structure
tools       Analysis tools by 3rd-party libraries
util        Frequently-used functions e.g. find atomic bonds
==========  ================================================

Application Program Interface (API)
-----------------------------------

============  =========================================
API version   Description
============  =========================================
octadist_gui  Graphical user interface (__main__.py)
octadist_cli  Command line interface (octadist_cli.py)
============  =========================================


Requirements
------------

OctaDist is written entirely in Python 3 binding to Tkinter GUI toolkit.
The following 3rd party library and package are used in OctaDist for specific functions.

.. code-block:: bash

    numpy
    scipy
    matplotlib
    rmsd


