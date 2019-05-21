====================
Installing and Usage
====================

OctaDist is a cross-platform software which is available for Windows OS, Linux OS, and macOS; 
for both 32-bit and 64-bit systems.

Windows
-------

Most of the Windows end-user do not have Python installed on their OS, 
so we strongly suggest you download a ready-to-use OctaDist (GUI version) on your system.

For first time using OctaDist, you should run it as an administrator with full rights.
Changing property of program can be completed in a few steps as follows:

1. Download program executable (\*.exe) to your machine.
2. Right click on program icon and select **Run as administrator**.
3. Click **Yes**.
4. Wait program for process until open.

Linux
-----

1. Download the source code (*.tar.gz) to your machine, for example, at **Download** directory.
2. Uncompress the tarball, using **tar**::
   
    tar -xzvf OctaDist-*-Linux-x86-64.tar.gz

3. Move to OctaDist root directory, using **cd**::

    cd OctaDist-*-Linux-x86-64

4. Check if your system has all dependencies for OctaDist::
   
    python CheckPyModule.py
    
5. Execute program as a package (you have to stay outside **octadist_gui** directory)::
   
    python -m octadist_gui.main
   

macOS
-----

Installing and running the program on Mac are the same as Linux.

1. Download the source code (*.tar.gz) to your machine, for example, at **`Download`** directory.
2. Press Command - spacebar to launch Spotlight and type "*Terminal*", then double-click the search result.
3. Uncompress the tarball, using **tar**::
   
    tar -xzvf OctaDist-*-macOS-x86-64.tar.gz
   
4. Move to OctaDist root directory, using **cd**::
  
    cd OctaDist-*-macOS-x86-64
  
5. Check if your system has all dependencies for OctaDist::
  
    python CheckPyModule.py
  
6. Set `TkAgg` backend environment variable to prevent the dependencies error::
  
    export MPLBACKEND=TkAgg
   
7. Execute program (you have to stay outside **octadist_gui** directory)::
   
    python -m octadist_gui.main
   

PyPI
----

OctaDist CLI version is also available on Python package index library, 
which can be found at https://pypi.org/project/octadist.

The end-user can use `pip`, a Python package-management system, 
to find and install OctaDist and other dependencies on OS at the same time.

The following commands might be useful:
- Install program::

   pip install octadist

- Upgrade to the latest version::

   pip install --upgrade octadist

- Downgrade to a certain version, for example, version 2.5.1::

   pip install --upgrade octadist==2.5.1

More details on installing Python package can be found its official website: 
https://packaging.python.org/tutorials/installing-packages.

Anaconda 
--------

OctaDist is also available on Anaconda cloud server.
The channel of OctaDist is at https://anaconda.org/rangsiman/octadist.

It can be installed on system using command::

    conda install -c rangsiman octadist 


The platforms that OctaDist-Conda supported: [![Anaconda-Server Badge][Conda-platform-badge]][Conda-platform-link]




