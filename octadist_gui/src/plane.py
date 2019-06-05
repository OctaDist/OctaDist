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

    The general form of plane equation: Ax + By + Cz = D
    where A, B, C, and D are coefficient.

    XZ  X  XY = (a, b, c)

    d = (a, b, c).Z

    Parameters
    ----------
    x : list or array
        3D Coordinate of point.
    y : list or array
        3D Coordinate of point.
    z : list or array
        3D Coordinate of point.

    Returns
    -------
    a : int or float
        Coefficient of the equation of the plane.
    b : int or float
        Coefficient of the equation of the plane.
    c : int or float
        Coefficient of the equation of the plane.
    d : int or float
        Coefficient of the equation of the plane.

    """
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)

    xz = z - x
    xy = y - x

    cross_vector = np.cross(xz, xy)
    a, b, c = cross_vector

    d = np.dot(cross_vector, z)

    return a, b, c, d
