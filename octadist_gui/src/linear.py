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


def norm_vector(v):
    """
    Normalizing vector and return the unit vector.

    Parameters
    ----------
    v : array
        2D or 3D vector.

    Returns
    -------
    norm : array
        Normalized vector.

    """
    norm = v / np.linalg.norm(v)

    return norm


def distance_bwn_points(a, b):
    """
    Find Euclidean distance between two points:

    a = (x1, y1, z1) and b = (x2, y2, z2).

    Parameters
    ----------
    a : list
        Cartesian coordinate of point a.
    b : list
        Cartesian coordinate of point b.

    Returns
    -------
    float
        Distance between two points.

    """
    return sqrt(sum([pow(a[i] - b[i], 2) for i in range(len(a))]))


def midpoint_of_line(a, b):
    """
    Find the midpoint of line segment, a = (x1,y1,z1) and b = (x2,y2,z2).

    Parameters
    ----------
    a : list
        Cartesian coordinate of point a (head atom)
    b : list
        Cartesian coordinate of point b (tail atom)

    Returns
    -------
    array
        Midpoint of line segment

    """
    return np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2])


def angles_sign(v1, v2, direct):
    """
    Compute angle between two vectors with sign and return value in degree.

    Parameters
    ----------
    v1 : array
        Vector in 3D space.
    v2 : array
        Vector in 3D space.
    direct : array
        Vector that refers to orientation of the plane.

    Returns
    -------
    angle : int or float
        Angle between two vectors with sign.

    """
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)

    v1 = norm_vector(v1)
    v2 = norm_vector(v2)

    angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))

    matD = np.array([v1, v2, direct])
    detD = np.linalg.det(matD)

    if detD < 0:
        angle = angle * -1

    return angle


def angle_btw_2vec(v1, v2):
    """
    Compute angle between two vectors and return value in degree.

    Parameters
    ----------
    v1 : array
        Vector in 3D space.
    v2 : array
        Vector in 3D space.

    Returns
    -------
    angle : int or float
        Angle between two vectors.

    """
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)

    v1 = norm_vector(v1)
    v2 = norm_vector(v2)

    angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))

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
    angle : int or float
        Angle between 2 planes.

    """
    d = (a1 * a2 + b1 * b2 + c1 * c2)
    e1 = sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    d = d / (e1 * e2)

    angle = degrees(acos(d))

    return angle


def triangle_area(a, b, c):
    """
    Calculate the area of the triangle using the cross product:

           |  ab X ac |
    Area = | -------- |
           |    2     |

    where ab = b - a and ac = c - a.

    Parameters
    ----------
    a : list or array
        3D Coordinate of point.
    b : list or array
        3D Coordinate of point.
    c : list or array
        3D Coordinate of point.

    Returns
    -------
    area : int or float
        The triangle area.

    """
    ab = b - a
    ac = c - a
    value = (pow(np.dot(ab[1], ac[2]) - np.dot(ab[2], ac[1]), 2) +
             pow(np.dot(ab[2], ac[0]) - np.dot(ab[0], ac[2]), 2) +
             pow(np.dot(ab[0], ac[1]) - np.dot(ab[1], ac[0]), 2))

    area = sqrt(value) / 2

    return area


def find_eq_of_plane(x, y, z):
    """
    Find the equation of plane of given three points using cross product

    The general form of plane equation:
    Ax + By + Cz = D

    where A, B, C, and D are coefficient.

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

    Notes
    -----
    -->    -->
    XZ  X  XY = (a, b, c)

    d = (a, b, c).Z

    """
    xz = z - x
    xy = y - x

    cross_vector = np.cross(xz, xy)
    a, b, c = cross_vector

    d = np.dot(cross_vector, z)

    return a, b, c, d
