# OctaDist  Copyright (C) 2019-2024  Rangsiman Ketkaew et al.
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
        Angle between two vectors in degree unit with sign.

    See Also
    --------
    calc.calc_theta :
        Calculate theta parameter.

    Examples
    --------
    >>> vector1 = [1.21859514, -0.92569245, -0.51717955]
    >>> vector2 = [1.02186387,  0.57480095, -0.95220433]
    >>> direction = [1.29280503, 0.69301873, 1.80572438]
    >>> angle_sign(vector1, vector2, direction)
    60.38697927455357

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
        Angle between two vectors in degree unit.

    Examples
    --------
    >>> vector1 = [-0.412697, -0.357008, -1.788172]
    >>> vector2 = [-0.550839,  1.799178, -0.039114]
    >>> angle_btw_vectors(vector1, vector2)
    95.62773246517462

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

    ::

        General equation of plane:

        a*X + b*Y + c*Z + d = 0

    Parameters
    ----------
    a1, b1, c1 : float
        Coefficient of the equation of plane 1.
    a2, b2, c2 : float
        Coefficient of the equation of plane 2.

    Returns
    -------
    angle : float64
        Angle between 2 planes in degree unit.

    Examples
    --------
    >>> # Plane 1
    >>> a1 = -3.231203733528
    >>> b1 = -0.9688526458499996
    >>> c1 = 0.9391692927779998
    >>> # Plane 2
    >>> a2 = 1.3904813057000005
    >>> b2 = 3.928502357473003
    >>> c2 = -4.924114034864001
    >>> angle_btw_planes(a1, b1, c1, a2, b2, c2)
    124.89920902358416

    """
    d = a1 * a2 + b1 * b2 + c1 * c2
    e1 = sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    d = d / (e1 * e2)

    angle = np.float64(degrees(acos(d)))

    return angle


def triangle_area(a, b, c):
    """
    Calculate the area of the triangle using the cross product:

    ::

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

    Examples
    --------
    >>> # Three vertices
    >>> a = [2.298354000, 5.161785000, 7.971898000]
    >>> b = [1.885657000, 4.804777000, 6.183726000]
    >>> c = [1.747515000, 6.960963000, 7.932784000]
    >>> triangle_area(a, b, c)
    1.7508135235821773

    """
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    c = np.asarray(c, dtype=np.float64)

    ab = b - a
    ac = c - a
    value = (
        pow(np.dot(ab[1], ac[2]) - np.dot(ab[2], ac[1]), 2)
        + pow(np.dot(ab[2], ac[0]) - np.dot(ab[0], ac[2]), 2)
        + pow(np.dot(ab[0], ac[1]) - np.dot(ab[1], ac[0]), 2)
    )

    area = np.float64(sqrt(value) / 2)

    return area
