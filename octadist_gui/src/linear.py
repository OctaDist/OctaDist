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

from octadist_gui.src import echo_logs


def norm_vector(self, v):
    """Returns the unit vector of the vector v

    :param self: master frame
    :param v: vector in 3D space
    :type v: list, array
    :return: unit (normalized) vector
    :rtype: list, array
    """
    if np.linalg.norm(v) == 0:
        echo_logs(self, "Error: Norm of vector {0} is 0".format(v))
        echo_logs(self, "")

    norm = v / np.linalg.norm(v)

    return norm


def distance_bwn_points(a, b):
    """Find distance between two point, a = (x1, y1, z1) and b = (x2, y2, z2)

                 -----------------------------------
    distance = \/ (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2

    :param a: cartesian coordinate of point a
    :param b: cartesian coordinate of point b
    :type a: list
    :type b: list
    :return: distance between two points
    :rtype: int, float
    """
    return sqrt(sum([pow(a[i] - b[i], 2) for i in range(len(a))]))


def midpoint_of_line(a, b):
    """Find the midpoint of line segment, a = (x1,y1,z1) and b = (x2,y2,z2)

    :param a: cartesian coordinate of point a (head atom)
    :param b: cartesian coordinate of point b (tail atom)
    :type a: list
    :type b: list
    :return: midpoint of line segment
    :rtype: array
    """
    return np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2])


def angles_sign(v1, v2, direct):
    """Compute angle between two vectors with sign and return value in degree

    :param v1: vector 1 in 3D space
    :param v2: vector 2 in 3D space
    :param direct: orientation vector of the plane
    :type v1: list, array
    :type v2: list, array
    :type direct: list, array
    :return angle: angle between two vectors with sign
    :rtype angle: int, float
    """
    Mod1 = np.sqrt((pow(v1[0], 2) + pow(v1[1], 2) + pow(v1[2], 2)))
    Mod2 = np.sqrt((pow(v2[0], 2) + pow(v2[1], 2) + pow(v2[2], 2)))

    Sca1 = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    leCos = Sca1 / (Mod1 * Mod2)

    if -1 <= leCos <= 1:
        angle = ((np.arccos(leCos)) / np.pi) * 180
    else:
        angle = 0

    matD = np.array([v1, v2, direct])
    detD = np.linalg.det(matD)

    if detD < 0:
        angle = angle * -1

    return angle


def angle_btw_2vec(v1, v2):
    """Compute angle between two vectors and return value in degree

    :param v1: vector 1 in 3D space
    :param v2: vector 2 in 3D space
    :type v1: list, array
    :type v2: list, array
    :return angle: angle between two vectors
    :rtype angle: int, float
    """
    ab_v1 = sqrt((pow(v1[0], 2) + pow(v1[1], 2) + pow(v1[2], 2)))
    ab_v2 = sqrt((pow(v2[0], 2) + pow(v2[1], 2) + pow(v2[2], 2)))

    scalar = (v1[0] * v2[0]) + (v1[1] * v2[1]) + (v1[2] * v2[2])

    dotVec = scalar / (ab_v1 * ab_v2)

    if -1 <= dotVec <= 1:
        angle = ((np.arccos(dotVec)) / np.pi) * 180
    else:
        angle = 0

    return angle


def angle_btw_3points(self, p1, p2, p3):
    """Compute the angle between vector p2 - p1 and p3 - p1

                    / p2_x * p3_x + p2_y * p3_y + p2_z * p3_z  \
    angle = arccos | ----------------------------------------- |
                   \               |p2| * |p3|                /

     and return value in degree

    :param self: master frame
    :param p1: coordinate of atom 1 (origin vector)
    :param p2: coordinate of atom 2
    :param p3: coordinate of atom 3
    :type p1: list, array
    :type p2: list, array
    :type p3: list, array
    :return: angle between vectors
    :rtype angle: int, float
    """
    # v1 = np.array(p2) - np.array(p1)
    # v2 = np.array(p3) - np.array(p1)

    v1 = p2 - p1
    v2 = p3 - p1

    nv1 = norm_vector(self, v1)
    nv2 = norm_vector(self, v2)

    nv1 = np.asarray(nv1)
    nv2 = np.asarray(nv2)

    angle = np.degrees(np.arccos(np.clip(np.dot(nv1, nv2), -1.0, 1.0)))

    return angle


def angle_btw_planes(a1, b1, c1, a2, b2, c2):
    """Find the angle between 2 planes in 3D

    a1*X + b1*Y + c1*Z + d1 = 0
    a2*X + b2*Y + c2*Z + d1 = 0

    :param a1: coefficient a of plane 1
    :param b1: coefficient b of plane 1
    :param c1: coefficient c of plane 1
    :param a2: coefficient a of plane 2
    :param b2: coefficient b of plane 2
    :param c2: coefficient c of plane 2
    :type a1: float
    :type b1: float
    :type c1: float
    :type a1: float
    :type b2: float
    :type c2: float
    :return angle: angle between 2 planes
    :rtype angle: int, float
    """
    d = (a1 * a2 + b1 * b2 + c1 * c2)
    e1 = sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    d = d / (e1 * e2)

    angle = degrees(acos(d))

    return angle


def triangle_area(a, b, c):
    """Calculate the area of the triangle using the cross product

           |  ab X ac |
    Area = | -------- |
           |    2     |

    where ab = b - a and ac = c - a

    :param a: coordinate of point a
    :param b: coordinate of point b
    :param c: coordinate of point c
    :type a: list, array
    :type b: list, array
    :type c: list, array
    :return area: the triangle area
    :rtype area: int, float
    """
    ab = b - a
    ac = c - a
    value = (pow(np.dot(ab[1], ac[2]) - np.dot(ab[2], ac[1]), 2) +
             pow(np.dot(ab[2], ac[0]) - np.dot(ab[0], ac[2]), 2) +
             pow(np.dot(ab[0], ac[1]) - np.dot(ab[1], ac[0]), 2))

    area = sqrt(value) / 2

    return area


def find_eq_of_plane(x, y, z):
    """Find the equation of plane of given three points using cross product

    The general form of plane equation is
    Ax + By + Cz = D, where A, B, C, and D are coefficient.

    -->    -->
    XZ  X  XY = (a, b, c)

    d = (a, b, c).Z

    :param x: coordinate of point a
    :param y: coordinate of point b
    :param z: coordinate of point c
    :type x: list, array
    :type y: list, array
    :type z: list, array
    :return a: coefficient of the equation of the plane
    :return b: coefficient of the equation of the plane
    :return c: coefficient of the equation of the plane
    :return d: coefficient of the equation of the plane
    :rtype a: int, float
    :rtype b: int, float
    :rtype c: int, float
    :rtype d: int, float
    """
    xz = z - x
    xy = y - x

    cross_vector = np.cross(xz, xy)
    a, b, c = cross_vector

    d = np.dot(cross_vector, z)

    return a, b, c, d
