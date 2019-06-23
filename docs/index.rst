.. OctaDist documentation master file, created by
   sphinx-quickstart on Mon May 13 12:47:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |Stable_ver| replace:: 2.6.0
.. |Nightly_ver| replace:: 2.6.1

=============
OctaDist Docs
=============

What is OctaDist?
-----------------

**OctaDist: A tool for computing the distortion parameters in coordination complexes.**


OctaDist (**Octa**\hedral **Dist**\ortion calculator) is an inorganic chemistry and
crystallography program for computing the distortion parameters, such as distance and
angle distortions, in coordination complexes. For example, they are used for tracking
structural change of the spin-crossover complex when the electronics spin-state
changes from low-spin to high-spin, and vice versa. OctaDist can also be used to study
other kind of the metal complex such as perovskite and metal-organic framework (MOF).

- Official homepage: https://octadist.github.io
- Github repository: https://github.com/OctaDist/OctaDist

Program Status
--------------

OctaDist is maintained on Github version control system.
All versions has been continuously tested using Travis CI.
Currently, OctaDist project has two branchs: Master (stable)
and nightly-build (dev).

=============   ==============   ======
Branch          Version          Status
=============   ==============   ======
Master          |Stable_ver|     Active
Nightly-build   |Nightly_ver|    Active
=============   ==============   ======

.. note::
   OctaDist is open-source computer software and freely distributed under
   The GNU General Public License v3.0.

.. tip::
   This document is a reference code of nightly development build of OctaDist.
   For the end-user, we strongly suggest you visit the user-friendly document
   at https://octadist.github.io/manual.html.

.. toctree::
   :maxdepth: 1
   :caption: ABOUT:
   :glob:

   about/getting-started

   about/features

   about/distortion-parameters

   about/program-structure

   about/installing-usage

   about/running-the-tests

   about/development

.. toctree::
   :maxdepth: 1
   :caption: MODULES:
   :glob:

   modules/*


.. toctree::
   :maxdepth: 1
   :caption: API:
   :glob:

   api/*


.. toctree::
   :maxdepth: 1
   :caption: REFERENCES:
   :glob:

   reference/*

----

:Authors:
   Rangsiman Ketkaew,
   Yuthana Tantirungrotechai,
   David J. Harding,
   Phimphaka Harding,
   Mathieu Marchivie

:Version: 2.6.0 of June 2019


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
