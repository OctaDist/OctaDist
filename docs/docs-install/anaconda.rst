========
Anaconda
========

OctaDist is also available on Anaconda cloud server.
The channel of OctaDist is at https://anaconda.org/rangsiman/octadist.

- It can be installed on system using command::

    conda install -c rangsiman octadist 

- To update OctaDist to the latest version::

    conda update -c rangsiman octadist

- You can also create a personal environment only for OctaDist.
  For example, the following commands will create new env called ``newenv``, 
  then activate to this new env, and then install OctaDist from conda server::

    conda create -n newenv python=3.7
    activate newenv
    conda update --all
    conda install -c rangsiman octadist

- To clean conda cache::

    conda clean --all

.. note::

    OctaDist package on Anaconda server has been imported from PyPI server.

If you experience any problems while installing OctaDist using Conda, 
please do not hesitate to post your question at https://groups.google.com/g/octadist-forum.
