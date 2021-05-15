=============
Prerequisites
=============

This section will explain the dependency requirements for building OctaDist.
As OctaDist is written in Python 3, you have to make sure that the version of Python
on your system is equal or higher than 3.5. Check it by following command::

    python --version

or

::

    python3 --version


.. tip::

    If you do have Python on the system, I would suggest you to read 
    The Hitchhiker's Guide to Python. It is very useful!

    Install Python 3 on:
    
    - `Windows <https://docs.python-guide.org/starting/install3/win/?highlight=install>`_
    - `Linux <https://docs.python-guide.org/starting/install3/linux/?highlight=install>`_
    - `macOS <https://docs.python-guide.org/starting/install3/osx/?highlight=install>`_



The following third-party packages are used in OctaDist.

.. code-block:: sh

    numpy
    scipy
    matplotlib
    rmsd
    pymatgen


Actually, if you use ``pip`` to install OctaDist, the required dependencies
will be installed automatically. However, you can install these packages yourself.
This can be done with only one step::

    pip install -r requirements.txt

