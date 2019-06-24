========
Anaconda
========

OctaDist is also available on Anaconda cloud server.
The channel of OctaDist is at https://anaconda.org/rangsiman/octadist.

It can be installed on system using command::

    conda install -c rangsiman octadist 

To update OctaDist to the latest version::

    conda update -c rangsiman octadist

It is also a good idea to create a personal environment, for example called ``newenv``
for OctaDist project and install OctaDist using conda::

    conda create -n newenv python=3.7
    activate newenv
    conda update --all
    conda install -c rangsiman octadist

FYI: OctaDist package on Conda server has been imported from PyPI server.

