============
Run OctaDist
============

OctaDist supports both a graphical user interface (GUI) 
and a command line interface (CLI).

Run OctaDist GUI using EXE
--------------------------

If you have a standalone executable (.exe) of OctaDist GUI on your system, 
run OctaDist by double-clicking the ``.exe`` file as if you open other program.


.. note::

    OctaDist can take time to launch the application, usually 5 - 10 seconds.
    However, if the program does not start, please restart your system and run it again.


Run OctaDist GUI on the terminal
--------------------------------

Moreover, OctaDist can be called on the terminal such as ``CMD``, 
``PowerShell``, and ``Terminal`` as long as it is added to environment variable, like this: 


.. code-block:: sh

    octadist


Run OctaDist CLI
----------------

You can execute command-line OctaDist interface by typing ``octadist_cli`` on the terminal.
If it is executed without argument, the help docs will show by default.

::

    (py37) user@Linux:~$ octadist_cli

    # output
    usage: octadist_cli [-h] [-i INPUT] [-f] [-r REF_CENTER_ATOM] [-c CUTOFF_DIST] [-s OUTPUT] [-p PARAMETER [PARAMETER ...]] [--show MOL [MOL ...]] [-g] [-a] [-v]

    Octahedral Distortion Calculator:
    A tool for computing octahedral distortion parameters in coordination complex.
    For more details, please visit https://octadist.github.io.

    optional arguments:
    -h, --help            show this help message and exit
    -i INPUT, --inp INPUT
                            Input structure in .xyz format
    -f, --format          Show formatted output summary
    -r REF_CENTER_ATOM, --ref-index REF_CENTER_ATOM
                            Index of the reference center atom. Default to 0
    -c CUTOFF_DIST, --cutoff CUTOFF_DIST
                            Cutoff distance (in Angstroms) for determining octahedron. Default to 2.8
    -s OUTPUT, --save OUTPUT
                            Save formatted output to text file, please specify name of OUTPUT file without '.txt' extension
    -p PARAMETER [PARAMETER ...], --par PARAMETER [PARAMETER ...]
                            Select which the parameter (zeta, delta, sigma, theta) to show
    --show MOL [MOL ...]  Show atomic symbol (atom) and atomic coordinate (coord) of octahedral structure
    -g, --gui             launch OctaDist GUI (this option is the same as 'octadist' command
    -a, --about           Show program info
    -v, --version         show program's version number and exit

    Rangsiman Ketkaew       Updated on 2021 E-mail: rangsiman1993@gmail.com


Using OctaDist to calculate the distortion of structure can be done as follows:

.. code-block:: sh

    # Compute parameters
    octadist_cli -i INPUT.xyz

    # Compute parameters and show formatted output
    octadist_cli -i INPUT.xyz -o

    # Compute parameters and save output as file
    octadist_cli -i INPUT.xyz -s OUTPUT

.. tip::

    On Windows, you can check whether OctaDist is added to environment 
    variables by using ``where`` command::
    
        where octadist
    
    For Linux and macOS, use ``which`` command instead::

        which octadist

    or ::

        type -P "octadist" && echo "It's in path" || echo "It's not in path"

