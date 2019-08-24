.. _label-development:

===========
Development
===========

OctaDist is written entirely in Python 3 binding to Tkinter toolkit.
We have been developing OctaDist with the ease of use and flexibility.
In the current version, it supports both of a graphical user interface (GUI) and
a command line interface (CLI) version. The first one is mainly developed for
the general end-users who are not familiar with command line,
while the latter is primarily developed as a package which is appropriate for
those who works with CLI. Having designed as a third party package,
the command-line OctaDist version is an smart assistant helping with a wide range of
your problems.


Contribution
------------

To give a contribution on program development, please pull request on
`the OctaDist Github <https://github.com/OctaDist/OctaDist>`_.

.. code-block:: sh

    git clone https://github.com/OctaDist/OctaDist.git
    git checkout nightly-build
    git pull origin nightly-build


OctaDist Testing
----------------

When you have finished editing the source code of the program,
you can use ``setuptools`` for testing OctaDist such as build and install.
A ``setup.py`` file in top-level directory provides software testing as follows:

.. code-block:: sh

    pip setup.py build
    pip setup.py install
    pip setup.py test


Bug report
----------

If you found a bug in OctaDist, please submit it on
`issues page <https://github.com/OctaDist/OctaDist/issues>`_.
We appreciate all help and contribution in getting program development.


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


.. toctree::
    :max-depth: 1

    docs-development/program-structure.rst


.. tip::
    For OctaDist download stats, please go to https://octadist.github.io/stats.html.

