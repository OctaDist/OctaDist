=======
Modules
=======

Program structure
-----------------

OctaDist is composed of the following modules:

============  ==================================================
Function      Description
============  ==================================================
main          Main program
calc          Calculating distortion parameters
draw          Displaying molecule
elements      Atomic properties
linear        Built-in mathematical functions
molecule      Manipulating atomic coordinates
plane         Manipulate projection plane
plot          Plotting graph and chart
popup         Error, warning, and info messages
projection    2D & 3D vector projections
scripting     Interactive code Console
structure     All data about structure
tools         Analysis tools by 3rd-party libraries
util          Frequently-used functions e.g. find atomic bonds
============  ==================================================

Application Program Interface (API)
-----------------------------------

==============  ===========================================
API version     Description
==============  ===========================================
octadist_gui    Graphical user interface (__main__.py)
octadist_cli    Command line interface (octadist_cli.py)
==============  ===========================================

Source code
-----------

.. toctree::
   :maxdepth: 1
   
   docs-modules/main.rst
   docs-modules/gui.rst
   docs-modules/cli.rst
   docs-modules/calc.rst
   docs-modules/draw.rst
   docs-modules/elements.rst
   docs-modules/linear.rst
   docs-modules/molecule.rst
   docs-modules/plane.rst
   docs-modules/plot.rst
   docs-modules/popup.rst
   docs-modules/projection.rst
   docs-modules/scripting.rst
   docs-modules/structure.rst
   docs-modules/tools.rst
   docs-modules/util.rst
