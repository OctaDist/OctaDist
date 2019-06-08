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

import numpy as np


def find_eq_of_plane(x, y, z):
    """
    Find the equation of plane of given three points using cross product

    | The general form of plane equation:
    |
    | Ax + By + Cz = D
    |
    | where A, B, C, and D are coefficient.
    |
    | XZ  X  XY = (a, b, c)
    |
    | d = (a, b, c).Z

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
