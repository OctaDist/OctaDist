===========
Development
===========

OctaDist is written entirely in Python 3 binding to Tkinter GUI platform.
It is available for on Windows, Linux, and macOS for 32/64-bit systems.
It can be used as a graphical user interface (GUI) and a command line interface (CLI) version.
The first one is mainly developed for the end-users, who are not familiar with Linux command,
while the latter is appropriate for the end-users and developer who are working with CLI,
for example, on Linux or macOS.

Code maintenance
----------------

The source code of OctaDist is maintained on Github version control system.
Both master revision and nightly development build have been being tested and deployed on
`Travis CI <https://travis-ci.org/>`_, a continuous integration service.

Source code on Github:

- `Master (stable) version : github.com/OctaDist/OctaDist
  <https://github.com/OctaDist/OctaDist>`_

- `Nightly build version : github.com/OctaDist/OctaDist/tree/nightly-build
  <https://github.com/OctaDist/OctaDist/tree/nightly-build>`_

Contribution
------------

To give a contribution on program development, please pull request on
`the OctaDist Github <https://github.com/OctaDist/OctaDist>`_.
If you found a bug in program, please submit it on
`issues page <https://github.com/OctaDist/OctaDist/issues>`_.
We appreciate all help and contribution in getting program development.

Prerequisites
-------------

OctaDist commonly supports Python 3.5+. For using the program as CLI,
you can use the following command to check the version of Python on your system:

::

  python -v


The following external libraries are required for OctaDist:

::

  numpy
  scipy
  matplotlib
  rmsd

You need to install these libraries before running the program,
otherwise it will fail to start. The latest version is suggested.

Program compilation
-------------------

For GUI, OctaDist source code can be compiled to executable file easily using
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

4. Change directory to ``./octadist`` subdirectory, where ``main.py`` is, for example:

::

   cd OctaDist-*-Win-x86-64/octadist/

5. Compile a standalone, like this:

::

   pyinstaller --onefile --windowed -n OctaDist-*-Win-x86-64 main.py

6. The standalone executable will be build in ``dist`` directory.

Additionally, other useful options for compilation can be found at PyInstaller manual.
