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
from math import sqrt, pow, degrees, acos


def angle_sign(v1, v2, direct):
    """
    Compute angle between two vectors with sign and return value in degree.

    Parameters
    ----------
    v1 : array_like
        Vector in 3D space.
    v2 : array_like
        Vector in 3D space.
    direct : array
        Vector that refers to orientation of the plane.

    Returns
    -------
    angle : float64
        Angle between two vectors with sign.

    """
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)

    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)

    angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))

    matrix = np.array([v1, v2, direct], dtype=np.float64)
    det = np.float64(np.linalg.det(matrix))

    if det < 0:
        angle = angle * -1

    return angle


def angle_btw_vectors(v1, v2):
    """
    Compute angle between two vectors and return value in degree.

    Parameters
    ----------
    v1 : array_like
        Vector in 3D space.
    v2 : array_like
        Vector in 3D space.

    Returns
    -------
    angle : float64
        Angle between two vectors.

    """
    v1 = np.asarray(v1, dtype=np.float64)
    v2 = np.asarray(v2, dtype=np.float64)

    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)

    angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)), dtype=np.float64)

    return angle


def angle_btw_planes(a1, b1, c1, a2, b2, c2):
    """
    Find the angle between 2 planes in 3D and return value in degree.

    General equation of plane: a*X + b*Y + c*Z + d = 0

    Parameters
    ----------
    a1, b1, c1 : float
        Coefficient of the equation of plane 1.
    a2, b2, c2 : float
        Coefficient of the equation of plane 2.

    Returns
    -------
    angle : float64
        Angle between 2 planes.

    """
    d = (a1 * a2 + b1 * b2 + c1 * c2)
    e1 = sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    d = d / (e1 * e2)

    angle = np.float64(degrees(acos(d)))

    return angle


def triangle_area(a, b, c):
    """
    Calculate the area of the triangle using the cross product:

    Area = abs(ab X ac)/2

    where vector ab = b - a and vector ac = c - a.

    Parameters
    ----------
    a : array_like
        3D Coordinate of point.
    b : array_like
        3D Coordinate of point.
    c : array_like
        3D Coordinate of point.

    Returns
    -------
    area : float64
        The triangle area.

    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    c = np.asarray(c, dtype=np.float64)

    ab = b - a
    ac = c - a
    value = (pow(np.dot(ab[1], ac[2]) - np.dot(ab[2], ac[1]), 2) +
             pow(np.dot(ab[2], ac[0]) - np.dot(ab[0], ac[2]), 2) +
             pow(np.dot(ab[0], ac[1]) - np.dot(ab[1], ac[0]), 2)
             )

    area = np.float64(sqrt(value) / 2)

    return area
