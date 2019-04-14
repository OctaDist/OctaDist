"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np


def project_atom_onto_line(p, a, b):
    """Find the point projection on the line, which defined by two distinct end points

    a <------> b

    P(x) = x1 + (p - x1).(x2 - x1)/(x2-x1).(x2-x1) * (x2-x1)

    :param p: point to project
    :param a: head atom of the line
    :param b: tail atom of the line
    :return projected_point: the projected point on the orthogonal line
    """
    ap = p - a
    ab = b - a
    projected_point = a + (np.dot(ap, ab)/np.dot(ab, ab))*ab

    return projected_point


def project_atom_onto_plane(p, a, b, c, d):
    """Find the orthogonal vector of point onto the given plane.
    The equation of plane is Ax + By + Cz = D and point is (L, M, N),
    then the location on the plane that is closest to the point (P, Q, R) is

    (P, Q, R) = (L, M, N) + λ * (A, B, C)

    where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2)

    :param a: float - coefficient of the equation of plane
    :param b: float - coefficient of the equation of plane
    :param c: float - coefficient of the equation of plane
    :param d: float - coefficient of the equation of plane
    :param p: array - coordinate of atom that will be projected
    :return projected_point: the projected point on the orthogonal plane
    """
    plane = np.array([a, b, c])
    lambda_plane = (d - (a*p[0] + b*p[1] + c*p[2]))/np.dot(plane, plane)
    projected_point = p + lambda_plane*plane

    return projected_point
