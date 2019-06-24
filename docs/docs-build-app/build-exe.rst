=======================
Compile OctaDist to EXE
=======================

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

