====================
Installing and Usage
====================

OctaDist is a cross-platform software which is available for Windows, Linux, and macOS;
for both 32-bit and 64-bit systems.


Windows
-------

Most of the Windows end-users do not have Python installed on their OS,
so we strongly suggest you download and use a ready-to-use OctaDist executable.

Running OctaDist can be completed in a few steps as follows:

1. Download program executable (\*.exe) to your machine::

    OctaDist-*-Win-x86-64.exe

2. Right click on program icon and select::

    Run as administrator

3. Click::

    Yes

FYI: For first time using OctaDist, you should run it as an administrator with full rights.


Linux
-----

OctaDist is available on Python package index library,
which can be found at https://pypi.org/project/octadist.

The end-user can use ``pip``, a Python package-management system,
to find and install OctaDist and other dependencies simultaneously.

Installing OctaDist can be completed in a few steps as follows:

1. Use ``pip`` command to install OctaDist::

    pip install octadist

2. Start OctaDist GUI, just type::

    octadist

   or::

    octadist_gui

3. If you want to run OctaDist with command-line, just type::

    octadist_cli
   

macOS
-----

Like Linux, installing OctaDist on macOS can be completed in a few steps as follows:

1. Press **Command** - **spacebar** to launch Spotlight and type ``Terminal``,
   then double-click the search result.

2. Use ``pip`` command to install OctaDist::
   
    pip install octadist
   
3. Start OctaDist GUI, just type::
  
    octadist

   or::

    octadist_gui
  
4. If you want to run OctaDist with command-line, just type::

    octadist_cli


PyPI
----

The following commands are also useful for those who want to play with ``pip``:

- Show info of package::

   pip show octadist

- Install requirements packages::

   pip install -r requirements.txt

- Upgrade to the latest version::

   pip install --upgrade octadist

- Upgrade/downgrade to a certain version, for example, version 2.6.0::

   pip install --upgrade octadist==2.6.0

- Uninstall program::

   pip uninstall octadist


More details on installing Python package can be found its official website:
https://packaging.python.org/tutorials/installing-packages.


Anaconda 
--------

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


Source Code
-----------

To build OctaDist from source:

1. Check if your system has all dependencies for OctaDist::

    python CheckPyModule.py

2. Download the source code (\*.tar.gz) to your machine, for example, at **Download** directory::

    OctaDist-*-src-x86-64.tar.gz

3. Uncompress the tarball, using **tar**::

    tar -xzvf OctaDist-*-src-x86-64.tar.gz

4. Move to OctaDist root directory, using **cd**::

    cd OctaDist-*-src-x86-64

5. Execute program like a package (you have to stay outside **octadist** directory)::

    python -m octadist

   or command-line::

    python -m octadist_cli
