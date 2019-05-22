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


def project_atom_onto_line(p, a, b):
    """
    Find the point projection on the line, which defined by two distinct end points.

    a <----> b

    P(x) = x1 + (p - x1).(x2 - x1)/(x2-x1).(x2-x1) * (x2-x1)

    Parameters
    ----------
    p : list or array
        Coordinate of point to project.
    a : list or array
        Coordinate of head atom of the line.
    b : list or array
        Coordinate of tail atom of the line.

    Returns
    -------
    projected_point : list or array
        The projected point on the orthogonal line.

    """
    ap = p - a
    ab = b - a

    projected_point = a + (np.dot(ap, ab) / np.dot(ab, ab)) * ab

    return projected_point


def project_atom_onto_plane(p, a, b, c, d):
    """
    Find the orthogonal vector of point onto the given plane.
    The equation of plane is Ax + By + Cz = D and point is (L, M, N),
    then the location on the plane that is closest to the point (P, Q, R) is

    (P, Q, R) = (L, M, N) + λ * (A, B, C)

    where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2).

    Parameters
    ----------
    p : array
        Point to project
    a : int or float
        Coefficient of the equation of the plane.
    b : int or float
        Coefficient of the equation of the plane.
    c : int or float
        Coefficient of the equation of the plane.
    d : int or float
        Coefficient of the equation of the plane.

    Returns
    -------
    projected_point: array
        The projected point on the orthogonal plane.

    """
    plane = np.array([a, b, c])
    lambda_plane = (d - (a * p[0] + b * p[1] + c * p[2])) / np.dot(plane, plane)
    projected_point = p + lambda_plane * plane

    return projected_point
