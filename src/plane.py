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

    print("Command: Show three ligand atoms of the given face and their coordinates")
    print("")
    print("         List before sorted:")
    print("         The sequence of atom and coordinate (x,y,z):")

    for i in range(len(pcl)):
        print("         ", pal[i])
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

    print("Command: Sort the shortest distance from plane to metal center in ascending order")
    print("")
    print("         List after sorted:")
    print("         The sequence of atom and coordinate (x,y,z):")

    for i in range(len(pcl)):
        print("         ", pal[i])
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
        print("         ", sal[i])
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
    :return oppo_pal, oppo_pcl: array - 2 lists of atoms and coordinates on the opposite plane
    """
    all_atom = [1, 2, 3, 4, 5, 6]
    oppo_pal = []
    oppo_pcl = []

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
        new_pcl = []
        for j in range(3):
            new_pcl.append([v[int(oppo_pal[i][j])][0], v[int(oppo_pal[i][j])][1], v[int(oppo_pal[i][j])]][2])
            oppo_pcl.append(new_pcl)
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})"
                  .format(oppo_pal[i][j], oppo_pcl[i][j][0], oppo_pcl[i][j][1], oppo_pcl[i][j][2]))
    print("")

    return oppo_pal, oppo_pcl

