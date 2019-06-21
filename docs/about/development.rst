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
you can use the following command to check the version of Python on your system::

  python -v


The following external libraries are required for OctaDist::

  numpy
  scipy
  matplotlib
  rmsd

You need to install these libraries before running the program,
otherwise it will fail to start. The latest version is suggested.

To install requirements::

   pip install -r requirements.txt


Build the tarball, wheel, and egg files
---------------------------------------

- tar.gz: the tarball (supported by PIP)
- whl: wheel file (supported by PIP)
- egg: cross-platform zip file (supported by easy_install)

1. Build source code::

    python setup.py sdist bdist_wheel bdist_egg

2. Install OctaDist::

    python setup.py install

   or::

    pip install dist/*.tar.gz

3. Run test zip files::

    python setup.py test

4. Installed library of OctaDist will be install at ``build/lib/octadist`` directory.

5. OctaDist executable files will be automatically added to environment variables,
you can call the program anywhere and anytime:

- To start GUI::

     octadist

  or::

     octadist_gui

- To start command-line::

    octadist_cli

More details on Python package can be found its official website:
https://packaging.python.org/tutorials/installing-packages.


Program compilation
-------------------

Program source code can be compiled as a standalone executable file (\*.exe).
Compilation can be completed easily using `PyInstaller <https://www.pyinstaller.org/>`_.

1. Upgrade pip::

    pip install pip --upgrade

2. Install the latest version of PyInstaller::

    pip install pyinstaller --upgrade

3. Check the version of PyInstaller::

    pyinstaller -v

4. Change directory to ``octadist`` subdirectory, where ``main.py`` is, for example::

    cd OctaDist-*-src-x86-64/octadist/

5. Compile a standalone, like this::

    pyinstaller --onefile --windowed -n OctaDist-*-src-x86-64 main.py

6. The standalone executable will be build in ``dist`` directory.

FYI: Other useful options for building executable can be found at
`PyInstaller manual <https://pyinstaller.readthedocs.io/en/stable/>`_.
