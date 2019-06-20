=====================
Distortion parameters
=====================

Mathematical expression of the octahedral distortion parameters are given by following equations


- Zeta parameter

.. math::

    \zeta = \sum_{i=1}^{6}\left | d_{i} - d_{mean}  \right |

    where :math:`d_{i}` is individual M-X bond distance and
    :math:`d_{mean}` is mean metal-ligand bond distance.

- Delta parameter

.. math::

    \Delta = \frac{1}{6} \sum_{i=1}^{6}(\frac{d_{i} - d_{mean}}{d_{mean}})^2

    where :math:`d_{i}` is individual M-X bond distance and
    :math:`d_{mean}` is mean metal-ligand bond distance.

- Sigma parameter

.. math::

    \Sigma = \sum_{i=1}^{12}\left | 90 - \phi_{i}  \right |

    where :math:`\phi_{i}` in individual cis angle.

- Theta parameter

.. math::

    \Theta = \sum_{i=1}^{24}\left | 60 - \theta_{i}  \right |

    where :math:`\theta_{i}` is individual angle between two vectors of two twisting face.

