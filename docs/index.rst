.. OctaDist documentation master file, created by
   sphinx-quickstart on Mon May 13 12:47:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OctaDist's documentation!
************************************

OctaDist: A tool for computingt the distortion parameters in coordination complexes.

Overview
========
1. Introduction
2. Installing
3. Running the tests
4. Credits

Program Structure
=================

==========  ================================
Function    Description
==========  ================================
main        Main program
coord       Manipulating atomic coordinates
elements    Atomic properties
calc        Calculating distortion parameters
linear      Built-in mathematical functions
projection  2D & 3D vector projections
plot        Plotting graph and chart
plane       Manipulate projection plane
draw        Displaying molecule
tools       3rd-party library
util        Utilities
popup       Error, warning, and info messages
==========  ================================

Document for the code
*********************

.. toctree::
   :maxdepth: 2
   :caption: Contents:

OctaDist main
=============

.. automodule:: octadist_gui.main
   :members:

OctaDist calc
=============

.. automodule:: octadist_gui.src.calc
   :members:

OctaDist coord
==============

.. automodule:: octadist_gui.src.coord
   :members:

OctaDist elements
=================

.. automodule:: octadist_gui.src.elements
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
