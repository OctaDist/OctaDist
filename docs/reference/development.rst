===========
Development
===========

OctaDist is written entirely in Python 3 binding to Tkinter GUI platform.
It is available for on Windows, Linux, and macOS for 32/64-bit systems.
It is divided into two versions as different types of uses:
a graphical user interface (GUI) version and a command line interface (CLI) version.
The former is mainly developed for the end-users, who are not familiar with Linux command,
while the latter is appropriate for the end-users and programmer who are working with CLI,
for example, on Linux or macOS.

Code maintenance
----------------

The source code of OctaDist is maintained on Github version control system.
Both master revision and nightly development build have being tested and deployed on
`Travis CI <https://travis-ci.org/>`_, a continuous integration service.

Program source code on Github:

- `OctaDist GUI : github.com/OctaDist/OctaDist
  <https://github.com/OctaDist/OctaDist>`_

- `OctaDist CLI : github.com/OctaDist/OctaDist-PyPI
  <https://github.com/OctaDist/OctaDist-PyPI>`_

Contribution
------------

To give a contribution on program development, please pull request on
`the OctaDist Github <https://github.com/OctaDist/OctaDist>`_.
If you found a bug in program, please submit it on
`issues page <https://github.com/OctaDist/OctaDist/issues>`_.
We appreciate all help and contribution in getting program development.

Prerequisites
-------------

OctaDist supports Python 3.5+. For using the program as CLI,
you can use following command to check the version of your current Python:

::

  python -v


The following external libraries are required for OctaDist for GUI and CLI (PyPI):

::

  numpy
  scipy
  matplotlib
  rmsd


Program compilation
-------------------

For GUI, OctaDist source code can be compiled to executable easily using
`PyInstaller <https://www.pyinstaller.org/>`_.

Compilation instruction

1. Upgrade pip:

::

   pip install --upgrade pip

2. Install PyInstaller:

::

   pip install pyinstaller

3. Check the version of PyInstaller:

::

   pyinstaller --version

4. Change directory to ``./octadist_gui`` directory, ``where main.py`` is, for example:

::

   cd OctaDist-2.5.2-Win-x86-64/octadist_gui/

5. Compile a standalone, like this:

::

   pyinstaller --onefile -n OctaDist-2.5.2-Win-x86-64 main.py

6. The standalone executable will be build in ``dist`` directory.

Additionally useful option for compilation can be found at PyInstaller manual.
