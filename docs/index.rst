.. OctaDist documentation master file, created by
   sphinx-quickstart on Mon May 13 12:47:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |ver| replace:: 2.6.1

=============
OctaDist Docs
=============


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
Currently, OctaDist project has two branches: Master (stable)
and nightly-build (dev).

.. tabularcolumns:: |c|c|c|

+---------------+----------+---------+
| Branch        | Version  | Status  |
+===============+==========+=========+
| Master        ||ver|     | Active  |
+---------------+----------+---------+
| Nightly-build |     -    | Active  |
+---------------+----------+---------+

.. note::
   OctaDist is open-source computer software and freely distributed under
   The GNU General Public License v3.0.

.. tip::
   This documentation is generated be both user and reference code manuals. 
   For more details, please go to the development page.


Citation
--------

Please cite this project when you use OctaDist for scientific publication.

.. code-block:: sh

    OctaDist: A tool for calculating distortion parameters in coordination complexes.
    https://octadist.github.io

BibTeX

.. code-block:: sh

    @misc{KetkaewOctaDist2019, 
      author = {Rangsiman Ketkaew and Yuthana Tantirungrotechai and David J. Harding and Phimphaka Harding and and Mathieu Marchivie}, 
      title = {OctaDist: A tool for calculating distortion parameters in coordination complexes}, 
      url = {https://octadist.github.io}, 
      year = {2019}, 
      month = {Aug}}


Bug report
----------

For reporting a bug in OctaDist, please submit issues on
`OctaDist Github issues page <https://github.com/OctaDist/OctaDist/issues>`_.
We appreciate all help and contribution in getting program development.


----

User Documentation
------------------

:ref:`genindex`, :ref:`modindex`, :ref:`search`

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   getting-started.rst
   download.rst
   install.rst
   build.rst
   run.rst
   test.rst
   benchmarks.rst
   error-and-fixing.rst
   modules.rst
   dev.rst
   authors.rst
   license.rst

:Authors:
   Rangsiman Ketkaew,
   Yuthana Tantirungrotechai,
   David J. Harding,
   Phimphaka Harding,
   Mathieu Marchivie

:Version: |ver| of August 2019

