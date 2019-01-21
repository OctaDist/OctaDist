"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import linear
import proj


def rearrange_atom_order(v, n):
    """Rearrange order of atoms

    :param v: array - original coordinate list of ligand atoms
    :param n: int - number of atom for that the last atom would be swapped with
    :return: row-swapped coordinate list
    """
    v[n], v[6] = v[6].copy(), v[n].copy()

    return v


def search_4_planes(v):
    """Find the plane of octahedral complex

    1. The total number of plane defined by given any three ligand atoms is
        (5!/2!3!) = 10 planes. Then project metal center atom onto the new plane one-by-one
        The projected metal center on new plane is called m'.

    2. Find the minimum distance between metal center atom and its projected point
        d_plane_i = norm(m' - m)
        So we will get d_plane_1, d_plane_2, ..., d_plane_6

    3. Given plane_coord_list array with dimension 10 x 1 x 4.
        This array contains sequence of vertices and the minimum distance from previous step.

                     [[ [coor] [coor] [coor] distance ]  --> plane 1
                      | [coor] [coor] [coor] distance ]  --> plane 2
        plane_coord = | ...          ...           ...|
                      | ...          ...           ...|
                      [ [coor] [coor] [coor] distance ]] ---> plane 10

        where [coor] is array of coordinate (xyz) of atom i

    4. Sort plane_coord_list in ascending order of the minimum distance (column 4)
        Unwanted plane is close to metal center atom. So, delete first 6 plane out of list.
        The remaining 4 planes are the correct plane for atom projection.

    :param v: array - XYZ coordinate of one metal center and six ligand atoms
                v[0] = metal center atom of complex
                v[i] = ligand atom of complex
    :return: array - pal and pcl = lists of atom and coordinate on the plane
    """
    pal, pcl = [], []

    # Use any three ligand atoms to find possible triangular faces
    for i in range(1, 4):
        for j in range(i + 1, 5):
            for k in range(j + 1, 6):
                if i != j and j != k and i != k:
                    a, b, c, d = eq_of_plane(v[i], v[j], v[k])
                    # Find metal center atom projection onto the new plane
                    m = proj.project_atom_onto_plane(v[0], a, b, c, d)
                    # Find distance between metal center atom to its projected point
                    d_btw = linear.distance_between(m, v[0])
                    # Insert the number of ligand atoms into list
                    pal.append([i, j, k])
                    # Insert the minimum distance into list
                    pcl.append([v[i], v[j], v[k], d_btw])

    # Do not convert list to array!
    # pal = np.asarray(pal)
    # pcl = np.asarray(pcl)

    print("Command: Show the given three atoms and shortest distance from metal center to the plane")
    print("         Format of list:")
    print("")
    print("         [<atom_i> <atom_j> <atom_k> <shortest_distance_from_metal_center_to_the_plane>]")
    print("")
    print("         List before sorted:")
    print("          The sequence of atom and coordinate (x,y,z):")

    for i in range(len(pcl)):
        print("          ", pal[i])
        for j in range(3):
            print("           ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                  .format(pcl[i][j][0], pcl[i][j][1], pcl[i][j][2]))
    print("")

    # Sort pcl in ascending order of the minimum distance (column 4)
    i = 0
    while i < len(pcl):
        k = i
        j = i + 1
        while j < len(pcl):
            # Compare the minimum distance
            if pcl[k][3] > pcl[j][3]:
                k = j
            j += 1
        # Reorder of atom sequence for both arrays
        pcl[i], pcl[k] = pcl[k], pcl[i]
        pal[i], pal[k] = pal[k], pal[i]
        i += 1

    print("         List after sorted:")
    print("          The sequence of atom and coordinate (x,y,z):")

    for i in range(len(pcl)):
        print("          ", pal[i])
        for j in range(3):
            print("           ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                  .format(pcl[i][j][0], pcl[i][j][1], pcl[i][j][2]))
    print("")

    # Remove first 6 out of 10 planes (first 6 rows), now pcl remains 4 planes
    scl = pcl[6:]
    sal = pal[6:]

    # Print new plane list after unwanted plane excluded
    print("Command: Delete 6 planes that mostly close to metal center atom")
    print("         List after unwanted plane deleted:")

    for i in range(len(scl)):
        print("          ", sal[i])
        for j in range(3):
            print("           ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                  .format(scl[i][j][0], scl[i][j][1], scl[i][j][2]))
    print("")

    plane_atom_list = sal
    # Remove the 4th column of distance
    plane_coord_list = np.delete(scl, 3, 1)

    return plane_atom_list, plane_coord_list


def search_8_planes(v):
    """Find 8 planes (faces) of octahedron

    :param v: array - XYZ coordinate of one metal center and six ligand atoms
                v[0] = metal center atom of complex
                v[i] = ligand atom of complex
    :return: array - pal and pcl = lists of atom and coordinate on the plane
    """
    pal, pcl = [], []

    # Use any three ligand atoms to find all possible triangular faces
    # The total number is 6!/3!3! = 20 planes, but we want only 8 faces.
    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = eq_of_plane(v[i], v[j], v[k])
                # Find metal center atom projection onto the new plane
                m = proj.project_atom_onto_plane(v[0], a, b, c, d)
                # Find distance between metal center atom to its projected point
                d_btw = linear.distance_between(m, v[0])
                # Insert the number of ligand atoms into list
                pal.append([i, j, k])
                # Insert the minimum distance into list
                pcl.append([v[i], v[j], v[k], d_btw])

    # Do not convert list to array!
    # pal = np.asarray(pal)
    # pcl = np.asarray(pcl)

    print("Command: Show the given three atoms and shortest distance from metal center to the plane")
    print("         Format of list:")
    print("")
    print("         [<atom_i> <atom_j> <atom_k> <shortest_distance_from_metal_center_to_the_plane>]")
    print("")
    print("         List before sorted:")
    print("          The sequence of atom and coordinate (x,y,z):")

    for i in range(len(pcl)):
        print("          ", pal[i])
        for j in range(3):
            print("           ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                  .format(pcl[i][j][0], pcl[i][j][1], pcl[i][j][2]))
    print("")

    # Sort pcl in ascending order of the minimum distance (column 4)
    i = 0
    while i < len(pcl):
        k = i
        j = i + 1
        while j < len(pcl):
            # Compare the minimum distance
            if pcl[k][3] > pcl[j][3]:
                k = j
            j += 1
        # Reorder of atom sequence for both arrays
        pcl[i], pcl[k] = pcl[k], pcl[i]
        pal[i], pal[k] = pal[k], pal[i]
        i += 1

    print("         List after sorted:")
    print("          The sequence of atom and coordinate (x,y,z):")

    for i in range(len(pcl)):
        print("          ", pal[i])
        for j in range(3):
            print("           ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                  .format(pcl[i][j][0], pcl[i][j][1], pcl[i][j][2]))
    print("")

    # Remove first 12 out of 20 planes (first 12 rows), now pcl remains 8 planes (faces)
    scl = pcl[12:]
    sal = pal[12:]

    # Print new plane list after unwanted plane excluded
    print("Command: Delete 6 planes that mostly close to metal center atom")
    print("         List after unwanted plane deleted:")

    for i in range(len(scl)):
        print("          ", sal[i])
        for j in range(3):
            print("           ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                  .format(scl[i][j][0], scl[i][j][1], scl[i][j][2]))
    print("")

    plane_atom_list = sal
    # Remove the 4th column of distance
    plane_coord_list = np.delete(scl, 3, 1)

    return plane_atom_list, plane_coord_list


def eq_of_plane(p1, p2, p3):
    """Find the equation of plane of given three ligand atoms
    The general form of plane equation is Ax + By + Cz = D

    :param p1, p2, p3: array - given three points
    :return: float - coefficient of the equation of given plane
    """
    v1 = p3 - p1
    v2 = p2 - p1

    # Find the vector orthogonal to the plane using cross product method
    ortho_vector = np.cross(v1, v2)
    a, b, c = ortho_vector
    d = np.dot(ortho_vector, p3)

    return a, b, c, d


def find_opposite_atoms(x, z):
    """Find the atom on the parallel opposite plane. For example,

    list of the atom on plane    list of the atom on opposite plane
            [[1 2 3]                       [[4 5 6]
             [1 2 4]         --->           [3 5 6]
             [2 3 5]]                       [1 4 6]]

    :param x: array - three ligand atoms
    :return oppo_pal: array - list of atoms on the opposite plane
    """
    all_atom = [1, 2, 3, 4, 5, 6]
    oppo_pal = []

    print("Command: Find the atoms on the opposite plane")

    # loop for 4 planes
    for i in range(len(x)):
        new_pal = []
        # Find the list of atoms on opposite plane
        for j in all_atom:
            if j not in (x[i][0], x[i][1], x[i][2]):
                new_pal.append(j)
        oppo_pal.append(new_pal)
    print("         List of the coordinate of atom on the opposite plane:")

    # z is coord_list
    v = np.array(z)

    for i in range(len(oppo_pal)):
        print("         Opposite to {0}".format(x[i]))
        for j in range(3):
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})"
                  .format(oppo_pal[i][j],
                          v[int(oppo_pal[i][j])][0], v[int(oppo_pal[i][j])][1], v[int(oppo_pal[i][j])][2]))
    print("")

    return oppo_pal

