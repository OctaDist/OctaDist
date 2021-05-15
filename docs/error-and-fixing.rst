================
Error and Fixing
================

1. OctaDist Startup Slow on Windows? 
------------------------------------

Windows Defender slow down OctaDist by scanning its file.
You can fix this annoying issue by excluding OctaDist out of process scan list.

Here are the steps for adding OctaDist to exclusion list:

1. Go to ``Start`` > ``Settings`` -> ``Update & Security`` -> ``Virus & threat protection``

2. Under Virus & threat protection settings select ``Manage settings``

3. Under Exclusions, select ``Add or remove exclusions`` and select ``Add exclusion``

4. Specify the name of OctaDist executable, for example::

    OctaDist-3.0.0-Win-x86-64.exe
    
5. Close OctaDist and run it again.


2. Missing some packages
------------------------

If error message says `ImportError:` or `ModuleNotFoundError:`, some important packages have not been installed. 
To install all required packages, stay at top directory of OctaDist and type this command:

.. code-block:: sh

    pip install -r requirements.txt


3. MPL error
------------

If program crashes with confusing errors messages, you may need to set `MPLBACKEND` environment variable 
before running the program, like this:

.. code-block:: sh

    export MPLBACKEND=TkAgg
   

4. Cannot connect to X11 server
-------------------------------

If you run GUI using `octadist` or `octadist_gui` and then it fails with the following error:

.. code-block:: sh

    (py37) nutt@Ubuntu:~$ octadist

    Program Starts >>>
    ... OctaDist 3.0.0 January 2021 ...
    Traceback (most recent call last):
        File "/home/nutt/.local/bin/octadist", line 10, in <module>
        sys.exit(run_gui())
        File "/home/nutt/.local/lib/python3.7/site-packages/octadist/__main__.py", line 35, in run_gui
        app = octadist.main.OctaDist()
        File "/home/nutt/.local/lib/python3.7/site-packages/octadist/main.py", line 68, in __init__
        self.master = tk.Tk()
        File "/usr/lib/python3.7/tkinter/__init__.py", line 2023, in __init__
        self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
    _tkinter.TclError: couldn't connect to display ":0"


The above message implies that your system cannot connect to X11 server used for displaying the GUI of program.
This error usually happens on Debian or Ubuntu (and Windows Subsystem for Linux on Windows). 
So, you need to install X11 server as follows: 

**X11 Client Installation**

To install the `xauth` package, use `apt-get`:

.. code-block:: sh

    sudo apt-get install xauth


**X11 Server Installation**

To install a minimal X11 on Ubuntu Server edition:

.. code-block:: sh

    sudo apt-get install xorg
    sudo apt-get install openbox


.. tip::

    If you find any issues, do not hesitate to let us know.
    Your suggestions would help OctaDist getting improved.

