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

5. Standalone executable (binary) file will be automatically added to environment variables,
   you can start OctaDist by calling its names anywhere:

   - To start graphical-interface::

        octadist

   - To start command-line::

        octadist_cli


.. note::

    More details on Python package can be found its official website:
    https://packaging.python.org/tutorials/installing-packages.

