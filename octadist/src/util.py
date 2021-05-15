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
from scipy.spatial import distance

from octadist.src import plane, projection


def find_bonds(atom, coord, cutoff_global=2.0, cutoff_hydrogen=1.2):
    """
    Find all bond distance and filter the possible bonds.

    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance

    Parameters
    ----------
    atom : list
        List of atomic labels of molecule.
    coord : list
        List of atomic coordinates of molecule.
    cutoff_global : int or float
        Global cutoff for screening bonds.
        Default is 2.0.
    cutoff_hydrogen : int or float
        Cutoff for screening hydrogen bonds.
        Default is 1.2.

    Returns
    -------
    filtered_pair_2 : list
        List of pair of atoms of selected bonds in molecule after screening
    filtered_bond_2 : array_like
        Array of bond distances of selected bonds in molecule after screening.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> pair_bond, bond_dist = find_bonds(atom, coord)
    >>> pair_bond
    [['Fe', 'N'], ['Fe', 'N'], ['Fe', 'N'], ['Fe', 'O'], ['Fe', 'O'], ['Fe', 'O']]
    >>> bond_dist
    [[[2.298354 5.161785 7.971898]
      [1.885657 4.804777 6.183726]]
     [[2.298354 5.161785 7.971898]
      [1.747515 6.960963 7.932784]]
     [[2.298354 5.161785 7.971898]
      [4.09438  5.807257 7.588689]]
     [[2.298354 5.161785 7.971898]
      [0.539005 4.482809 8.460004]]
     [[2.298354 5.161785 7.971898]
      [2.812425 3.266553 8.131637]]
     [[2.298354 5.161785 7.971898]
      [2.886404 5.392925 9.848966]]]

    """
    all_pair = []
    all_bond = []

    for i in range(len(coord)):
        for j in range(i + 1, len(coord)):
            if i == 0:
                dist = distance.euclidean(coord[i], coord[j])
            else:
                dist = distance.euclidean(coord[i], coord[j])

            all_pair.append([atom[i], atom[j]])
            all_bond.append([coord[i], coord[j], dist])

    filtered_pair_1 = []
    filtered_bond_1 = []

    for i in range(len(all_bond)):
        if all_bond[i][2] <= cutoff_global:
            filtered_pair_1.append([all_pair[i][0], all_pair[i][1]])

            filtered_bond_1.append([all_bond[i][0], all_bond[i][1], all_bond[i][2]])

    filtered_pair_2 = []
    filtered_bond_2 = []

    for i in range(len(filtered_bond_1)):
        if filtered_pair_1[i][0] == "H" or filtered_pair_1[i][1] == "H":
            if filtered_bond_1[i][2] <= cutoff_hydrogen:
                filtered_pair_2.append([filtered_pair_1[i][0], filtered_pair_1[i][1]])
                filtered_bond_2.append([filtered_bond_1[i][0], filtered_bond_1[i][1]])
        else:
            filtered_pair_2.append([filtered_pair_1[i][0], filtered_pair_1[i][1]])
            filtered_bond_2.append([filtered_bond_1[i][0], filtered_bond_1[i][1]])

    return filtered_pair_2, np.array(filtered_bond_2)


def find_faces_octa(c_octa):
    """
    Find the eight faces of octahedral structure.

    ::

        1. Choose 3 atoms out of 6 ligand atoms. The total number of combination is 20.
        2. Orthogonally project metal center atom onto the face: m ----> m'
        3. Calculate the shortest distance between original metal center to its projected point.
        4. Sort the 20 faces in ascending order of the shortest distance.
        5. Delete 12 faces that closest to metal center atom (first 12 faces).
        6. The remaining 8 faces are the (reference) face of octahedral structure.
        7. Find 8 opposite faces.

        Reference plane              Opposite plane
           [[1 2 3],                    [[4 5 6],
            [1 2 4],        --->         [3 5 6],
              ...                          ...
            [2 3 5]]                     [1 4 6]]

    Parameters
    ----------
    c_octa : array_like
        Atomic coordinates of octahedral structure.

    Returns
    -------
    a_ref_f : list
        Atomic labels of reference face.
    c_ref_f : array_like
        Atomic coordinates of reference face.
    a_oppo_f : list
        Atomic labels of opposite face.
    c_oppo_f : array_like
        Atomic coordinates of opposite face.

    See Also
    --------
    octadist.src.plane.find_eq_of_plane :
        Find the equation of the plane.
    octadist.src.projection.project_atom_onto_plane :
        Orthogonal projection of point onto the plane.

    Examples
    --------
    >>> coord = [[14.68572, 18.49228, 6.66716],
                 [14.86476, 16.48821, 7.43379],
                 [14.44181, 20.59400, 6.21555],
                 [13.37473, 17.23453, 5.45099],
                 [16.26114, 18.54903, 8.20527],
                 [13.04897, 19.25464, 7.93122],
                 [16.09157, 18.96170, 5.02956]]
    >>> a_ref, c_ref, a_oppo, c_oppo = find_faces_octa(coord)
    >>> a_ref
    [[1, 3, 6], [1, 4, 6], [2, 3, 6], [2, 3, 5],
     [2, 4, 5], [1, 4, 5], [1, 3, 5], [2, 4, 6]]
    >>> c_ref
    [[[14.86476 16.48821  7.43379]
      [13.37473 17.23453  5.45099]
      [16.09157 18.9617   5.02956]],
     ...,
     ...,
     [[14.44181 20.594    6.21555]
      [16.26114 18.54903  8.20527]
      [16.09157 18.9617   5.02956]]]
    >>> a_octa
    [[2, 4, 5], [2, 3, 5], [1, 4, 5], [1, 4, 6],
     [1, 3, 6], [2, 3, 6], [2, 4, 6], [1, 3, 5]]
    >>> c_octa
    [[[14.44181 20.594    6.21555]
      [16.26114 18.54903  8.20527]
      [13.04897 19.25464  7.93122]],
     ...,
     ...,
     [[14.86476 16.48821  7.43379]
      [13.37473 17.23453  5.45099]
      [13.04897 19.25464  7.93122]]]

    """
    ########################
    # Find reference faces #
    ########################

    c_octa = np.asarray(c_octa, dtype=np.float64)

    # Find the shortest distance from metal center to each triangle
    dist = []
    a_ref_f = []
    c_ref_f = []

    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = plane.find_eq_of_plane(c_octa[i], c_octa[j], c_octa[k])
                m = projection.project_atom_onto_plane(c_octa[0], a, b, c, d)
                d_btw = distance.euclidean(m, c_octa[0])
                dist.append(d_btw)

                a_ref_f.append([i, j, k])
                c_ref_f.append([c_octa[i], c_octa[j], c_octa[k]])

    # Sort faces by distance in ascending order
    dist_a_c = sorted(zip(dist, a_ref_f, c_ref_f))
    dist, a_ref_f, c_ref_f = list(zip(*dist_a_c))
    c_ref_f = np.asarray(c_ref_f, dtype=np.float64)

    # Remove first 12 triangles, the rest of triangles is 8 faces of octahedron
    a_ref_f = a_ref_f[12:]
    c_ref_f = c_ref_f[12:]

    #######################
    # Find opposite faces #
    #######################

    all_atom = [1, 2, 3, 4, 5, 6]
    a_oppo_f = []

    for i in range(len(a_ref_f)):
        new_a_ref_f = []
        for j in all_atom:
            if j not in (a_ref_f[i][0], a_ref_f[i][1], a_ref_f[i][2]):
                new_a_ref_f.append(j)
        a_oppo_f.append(new_a_ref_f)

    c_oppo_f = []

    for i in range(len(a_oppo_f)):
        coord_oppo = []
        for j in range(3):
            coord_oppo.append(
                [
                    c_octa[int(a_oppo_f[i][j])][0],
                    c_octa[int(a_oppo_f[i][j])][1],
                    c_octa[int(a_oppo_f[i][j])],
                ][2]
            )
        c_oppo_f.append(coord_oppo)

    a_ref_f = list(a_ref_f)
    c_ref_f = list(c_ref_f)

    c_ref_f = np.asarray(c_ref_f, dtype=np.float64)
    c_oppo_f = np.asarray(c_oppo_f, dtype=np.float64)

    return a_ref_f, c_ref_f, a_oppo_f, c_oppo_f
