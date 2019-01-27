"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np


def project_atom_onto_line(p, a, b):
    """Find the projected point of atom on the line that defined by two head and tail atoms

    a <------> b

    P(x) = x1 + (p - x1).(x2 - x1)/(x2-x1).(x2-x1) * (x2-x1)

    :param p: point to project
    :param a, b: head and tail atoms as two distinct end points
    :return: the projected point on the orthogonal line
    """

    ap = p - a
    ab = b - a

    return a + (np.dot(ap, ab) / np.dot(ab, ab) * ab)


def project_atom_onto_plane(p, a, b, c, d):
    """Find the orthogonal vector of point onto the given plane.
    If the equation of plane is Ax + By + Cz = D and the location of point is (L, M, N),
    then the location in the plane that is closest to the point (P, Q, R) is

    (P, Q, R) = (L, M, N) + λ * (A, B, C)
        where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2)

    :param p: array - coordinate of atom that will be projected
    :param a, b, c, d: float - coefficient of the equation of plane
    :return: the projected point on the orthogonal plane
    """

    plane = np.array([a, b, c])
    lambda_plane = (d - (a * p[0] + b * p[1] + c * p[2])) / np.dot(plane, plane)

    return p + (lambda_plane * plane)
