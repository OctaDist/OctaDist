"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
from math import sqrt, pow, degrees, acos
import main


def norm_vector(self, v):
    """Returns the unit vector of the vector v

    :param self: master frame
    :param v: array - vector
    :return: array - normalized vector
    """
    if np.linalg.norm(v) == 0:
        main.print_stdout(self, "Error: Norm of vector {0} is 0".format(v))
        main.print_stdout(self, "")

    return v / np.linalg.norm(v)


def distance_between(a, b):
    """Find distance between two point, a = (x1, y1, z1) and b = (x2, y2, z2)

                 -----------------------------------
    distance = \/ (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2

    :param a: array - cartesian coordinate of point a
    :param b: array - cartesian coordinate of point b
    :return: float - distance
    """
    return sqrt(sum([pow(a[i] - b[i], 2) for i in range(len(a))]))


def midpoint_of_line(a, b):
    """Find the midpoint of line segment, a = (x1,y1,z1) and b = (x2,y2,z2)

    :param a: array - cartesian coordinate of head atom
    :param b: array - cartesian coordinate of tail atom
    :return: array - midpoint of line segment
    """
    return np.array([(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2])


def angles_sign(v1, v2, direct):
    """Compute angle between two vectors with sign

    :param v1:
    :param v2:
    :param direct:
    :return:
    """
    Mod1 = np.sqrt((pow(v1[0], 2) + pow(v1[1], 2) + pow(v1[2], 2)))
    Mod2 = np.sqrt((pow(v2[0], 2) + pow(v2[1], 2) + pow(v2[2], 2)))

    Sca1 = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    leCos = Sca1 / (Mod1 * Mod2)
    if -1 <= leCos <= 1:
        result = ((np.arccos(leCos)) / np.pi) * 180
    else:
        result = 0
    matD = np.array([v1, v2, direct])  # "direct" is a vector defined in the program core that define the
    detD = np.linalg.det(matD)  # orientation of the plane to know the sign of the angles.

    if detD < 0:
        result = result * -1

    return float(result)


def angle_btw_2vec(v1, v2):
    """Compute angle between two vectors

    :param v1:
    :param v2:
    :return:
    """
    Mod1 = sqrt((pow(v1[0], 2) + pow(v1[1], 2) + pow(v1[2], 2)))
    Mod2 = sqrt((pow(v2[0], 2) + pow(v2[1], 2) + pow(v2[2], 2)))

    Sca1 = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    leCos = Sca1 / (Mod1 * Mod2)
    if -1 <= leCos <= 1:
        result = ((np.arccos(leCos)) / np.pi) * 180
    else:
        result = 0

    return float(result)


def angle_btw_3vec(self, p1, p2, p3):
    """Compute the angle between vector p2 - p1 and p3 - p1

                                / p2_x * p3_x + p2_y * p3_y + p2_z * p3_z  \
    angle (in radian) = arccos | ----------------------------------------- |
                               \               |p2| * |p3|                /

    :param self: master frame
    :param p1: array - coordinate of atom 1
    :param p2: array - coordinate of atom 2
    :param p3: array - coordinate of atom 3
    :return: float - angle in degree unit
    """
    v1 = p2 - p1
    v2 = p3 - p1
    nv1 = norm_vector(self, v1)
    nv2 = norm_vector(self, v2)

    return np.degrees(np.arccos(np.clip(np.dot(nv1, nv2), -1.0, 1.0)))


def angle_btw_planes(a1, b1, c1, a2, b2, c2):
    """Find the angle between 2 planes in 3D

    a1*X + b1*Y + c1*Z + d1 = 0
    a2*X + b2*Y + c2*Z + d1 = 0

    :param a1, b1, c1, a2, b2, c2:
    :return:
    """
    d = (a1 * a2 + b1 * b2 + c1 * c2)
    e1 = sqrt(a1 * a1 + b1 * b1 + c1 * c1)
    e2 = sqrt(a2 * a2 + b2 * b2 + c2 * c2)
    d = d / (e1 * e2)
    angle = degrees(acos(d))

    return angle


def triangle_area(a, b, c):
    """Calculate the area of the triangle using the following equation


           |  ab X ac |
    Area = | -------- |     where ab = b - a
           |    2     |           ac = c - a

    :param a: point A - (Ax, Ay, Az)
    :param b: point B - (Bx, By, Bz)
    :param c: point C - (Cx, Cy, Cz)
    :return: float - triangle area
    """
    ab = b - a
    ac = c - a
    value = (pow(np.dot(ab[1], ac[2]) - np.dot(ab[2], ac[1]), 2) +
             pow(np.dot(ab[2], ac[0]) - np.dot(ab[0], ac[2]), 2) +
             pow(np.dot(ab[0], ac[1]) - np.dot(ab[1], ac[0]), 2))

    return sqrt(value) / 2
