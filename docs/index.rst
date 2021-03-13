.. OctaDist documentation master file, created by
   sphinx-quickstart on Mon May 13 12:47:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |year-ver| replace:: 2021
.. |sta-ver| replace:: 3.0.0
.. |dev-ver| replace:: 3.1.0

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
| Master        ||sta-ver| | Active  |
+---------------+----------+---------+
| Nightly-build ||dev-ver| | Active  |
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

   Ketkaew, R.; Tantirungrotechai, Y.; Harding, P.; Chastanet, G.; Guionneau, P.; Marchivie, M.; Harding, D. J. 
   OctaDist: A Tool for Calculating Distortion Parameters in Spin Crossover and Coordination Complexes. 
   Dalton Trans., 2021,50, 1086-1096. https://doi.org/10.1039/D0DT03988H

BibTeX

.. code-block:: sh

   @article{Ketkaew2021,
      doi = {10.1039/d0dt03988h},
      url = {https://doi.org/10.1039/d0dt03988h},
      year = {2021},
      publisher = {Royal Society of Chemistry ({RSC})},
      volume = {50},
      number = {3},
      pages = {1086--1096},
      author = {Rangsiman Ketkaew and Yuthana Tantirungrotechai and Phimphaka Harding and Guillaume Chastanet and Philippe Guionneau and Mathieu Marchivie and David J. Harding},
      title = {OctaDist: a tool for calculating distortion parameters in spin crossover and coordination complexes},
      journal = {Dalton Transactions}
   }


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

:Version: |sta-ver| of |year-ver|

