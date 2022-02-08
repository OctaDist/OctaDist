# OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import functools
import scipy.optimize

import numpy as np


def find_eq_of_plane(x, y, z):
    """
    Find the equation of plane of given three points using cross product:

    ::

        The general form of plane equation:

        Ax + By + Cz = D

        where A, B, C, and D are coefficient.

        XZ  X  XY = (a, b, c)

        d = (a, b, c).Z

    Parameters
    ----------
    x : array_like
        3D Coordinate of point.
    y : array_like
        3D Coordinate of point.
    z : array_like
        3D Coordinate of point.

    Returns
    -------
    a : float64
        Coefficient of the equation of the plane.
    b : float64
        Coefficient of the equation of the plane.
    c : float64
        Coefficient of the equation of the plane.
    d : float64
        Coefficient of the equation of the plane.

    Examples
    --------
    >>> N1 = [2.298354000, 5.161785000, 7.971898000]
    >>> N2 = [1.885657000, 4.804777000, 6.183726000]
    >>> N3 = [1.747515000, 6.960963000, 7.932784000]
    >>> a, b, c, d = find_eq_of_plane(N1, N2, N3)
    >>> a
    -3.231203733528
    >>> b
    -0.9688526458499996
    >>> c
    0.9391692927779998
    >>> d
    -4.940497273569501

    """
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    z = np.asarray(z, dtype=np.float64)

    xz = z - x
    xy = y - x

    cross_vector = np.cross(xz, xy)
    a, b, c = cross_vector

    d = np.dot(cross_vector, z)

    return a, b, c, d


def find_fit_plane(coord):
    """
    Find best fit plane to the given data points (atoms).

    Parameters
    ----------
    coord : array_like
        Coordinates of selected atom chunk.

    Returns
    -------
    xx : float
        Coefficient of the surface.
    yy : float
        Coefficient of the surface.
    z : float
        Coefficient of the surface.
    abcd : tuple
        Coefficient of the equation of the plane.

    See Also
    --------
    scipy.optimize.minimize :
        Used to find the least-square plane.

    Examples
    --------
    >>> points = [(1.1, 2.1, 8.1),
                  (3.2, 4.2, 8.0),
                  (5.3, 1.3, 8.2),
                  (3.4, 2.4, 8.3),
                  (1.5, 4.5, 8.0),
                  (5.5, 6.7, 4.5)
                  ]
    >>> # To plot the plane, run following commands:
    >>> import matplotlib.pyplot as plt
    >>> # map coordinates for scattering plot
    >>> xs, ys, zs = zip(*points)
    >>> plt.scatter(xs, ys, zs)
    >>> plt.show()

    """

    def plane(x, y, params):
        a = params[0]
        b = params[1]
        c = params[2]
        z = a * x + b * y + c
        return z

    def error(params, points):
        result = 0
        for (x, y, z) in points:
            plane_z = plane(x, y, params)
            diff = abs(plane_z - z)
            result += diff ** 2
        return result

    def cross(a, b):
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0],
        ]

    points = coord

    fun = functools.partial(error, points=points)
    params0 = [0, 0, 0]
    res = scipy.optimize.minimize(fun, params0)

    a = res.x[0]
    b = res.x[1]
    c = res.x[2]

    point = np.array([0.0, 0.0, c])
    normal = np.array(cross([1, 0, a], [0, 1, b]))
    d = -point.dot(normal)
    xx, yy = np.meshgrid([-5, 10], [-5, 10])
    z = (-normal[0] * xx - normal[1] * yy - d) * 1.0 / normal[2]

    abcd = (a, b, c, d)

    return xx, yy, z, abcd
