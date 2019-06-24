=================================
Build the tarball, wheel, and egg
=================================

- ``.tar.gz`` : the tarball (supported by PIP)
- ``.whl`` : wheel file (supported by PIP)
- ``.egg`` : cross-platform zip file (supported by easy_install)

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

