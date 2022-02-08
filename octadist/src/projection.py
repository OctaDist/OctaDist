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

    ::

        a <----> b

        P(x) = x1 + (p - x1).(x2 - x1)/(x2-x1).(x2-x1) * (x2-x1)

    Parameters
    ----------
    p : array_like
        Coordinate of point to project.
    a : array_like
        Coordinate of head atom of the line.
    b : array_like
        Coordinate of tail atom of the line.

    Returns
    -------
    projected_point : array_like
        The projected point on the orthogonal line.

    Examples
    --------
    >>> # point to project
    >>> p = [10.1873, 5.7463, 5.615]
    >>> # head and end points of line
    >>> a = [8.494, 5.9735, 4.8091]
    >>> b = [9.6526, 6.4229, 7.3079]
    >>> project_atom_onto_line(p, a, b)
    [9.07023235 6.19701012 6.05188388]

    """
    p = np.asarray(p, dtype=np.float64)
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    ap = p - a
    ab = b - a

    projected_point = a + (np.dot(ap, ab) / np.dot(ab, ab)) * ab

    return projected_point


def project_atom_onto_plane(p, a, b, c, d):
    """
    Find the orthogonal vector of point onto the given plane.
    The equation of plane is ``Ax + By + Cz = D`` and point is ``(L, M, N)``,
    then the location on the plane that is closest to the point ``(P, Q, R)`` is

    ::

        (P, Q, R) = (L, M, N) + λ * (A, B, C)

        where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2).

    Parameters
    ----------
    p : array_like
        Point to project.
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
    projected_point: array_like
        The projected point on the orthogonal plane.

    Examples
    --------
    >>> # point to project
    >>> p = [10.1873, 5.7463, 5.615]
    >>> # coefficient of the equation of the plane
    >>> a = -3.231203733528
    >>> b = -0.9688526458499996
    >>> c = 0.9391692927779998
    >>> d = -4.940497273569501
    >>> project_atom_onto_plane(p, a, b, c, d)
    [2.73723598 3.51245316 7.78040705]

    """
    p = np.asarray(p, dtype=np.float64)
    plane = np.array([a, b, c], dtype=np.float64)

    lambda_plane = (d - (a * p[0] + b * p[1] + c * p[2])) / np.dot(plane, plane)

    projected_point = p + lambda_plane * plane

    return projected_point
