"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
from math import sqrt


def norm_vector(v):
    """Returns the unit vector of the vector v

    :param v: array - vector
    :return: array - normallized vector
    """
    if np.linalg.norm(v) == 0:
        print("Error: Norm of vector", v, "is 0.")

    return v / np.linalg.norm(v)


def distance_between(x, y):
    """Find distance between two point, given points (x1,y1,z1) and (x2,y2,z2)

    :param x: array - cartesian coordinate of atom x
    :param y: array - cartesian coordinate of atom x
    :return: float - distance
    """

    return sqrt(sum([pow(x[i] - y[i], 2) for i in range(len(x))]))


def distance_avg(x):
    """Calculate average M-X distance

    :param x: array - coordinate of atom x
    :return: float - average M-X distance
    """
    dist_sum = []

    for i in range(1, 7):
        results_sum = distance_between(x[i], x[0])
        dist_sum.append(results_sum)

    return sum([dist_sum[i] for i in range(6)]) / 6


def midpoint_of_line(x, y):
    """Find the midpoint of line segment (between two point), given points (x1,y1,z1) and (x2,y2,z2)

    :param x: array - cartesian coordinate of atom x
    :param y: array - cartesian coordinate of atom x
    :return: float - point
    """

    return np.array([(x[0] + y[0]) / 2, (x[1] + y[1]) / 2, (x[2] + y[2]) / 2])


def angle_between(v0, v1, v2):
    """Compute the angle between vector v1 - v0 and v2 - v0

                                / v1_x * v2_x + v1_y * v2_y + v1_z * v2_z  \
    angle (in radian) = arccos | ----------------------------------------- |
                               \               |v1| * |v2|                /

    :param v0, v1, v2: array - coordinate of atom 1, 2, 3
    :return: float - angle in degree unit
    """
    sub_v1 = v1 - v0
    sub_v2 = v2 - v0

    v1_u = norm_vector(sub_v1)
    v2_u = norm_vector(sub_v2)

    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

