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
coord       Manipulating atomic coordinates
draw        Displaying molecule
elements    Atomic properties
linear      Built-in mathematical functions
plane       Manipulate projection plane
plot        Plotting graph and chart
popup       Error, warning, and info messages
projection  2D & 3D vector projections
structure   All data about structure
tools       Analysis tools by 3rd-party libraries
util        Frequently-used functions e.g. find atomic bonds
==========  ================================================

Requirements
------------

OctaDist is written entirely in Python 3 binding to Tkinter GUI toolkit.
The following 3rd party library and package are used in OctaDist for specific functions.

.. code-block:: bash

    numpy
    scipy
    matplotlib
    rmsd


