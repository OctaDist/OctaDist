"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import scipy.optimize
import functools
from math import sqrt, pow
import linear
import plane
import proj
import matplotlib.pyplot as plt


def calc_delta(x):
    """Calculate Delta parameter
                                      2
                 1         / d_i - d \
    delta(d) =  --- * sum | -------- |
                 6        \    d    /

    where d_i is individual M-X distance and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

    :param x: array - coordinate of atoms
    :return computed_delta: float - delta parameter (unitless)
    """
    print("Command: Calculate distance between metal center (M) and ligand atoms (in Ångström)")

    # Calculate and print individual distance
    distance_list = []

    for i in range(1, 7):
        distance_indi = sqrt(sum([pow(x[i][j] - x[0][j], 2) for j in range(3)]))
        print("          Distance between M and ligand atom {0} : {1:5.6f}"
              .format(i, distance_indi))
        distance_list.append(distance_indi)

    print("")
    print("         ====================== SUMMARY of Δ ======================\n")
    print("")
    print("         Total number of computed distance:", len(distance_list))
    print("")

    computed_distance_avg = linear.distance_avg(x)
    computed_delta = 0

    # Calculate Delta parameter
    for i in range(6):
        diff_dist = (distance_list[i] - computed_distance_avg) / computed_distance_avg
        computed_delta = (pow(diff_dist, 2) / 6) + computed_delta

    return computed_delta, distance_list


def calc_sigma(v):
    """Calculate Sigma parameter

                  12
    Σ = sigma < 90 - angle_i >
         i=1

    Ref: J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    :param v: array - coordinate of atoms
    :return computed_sigma: float - sigma parameter in degree
    """
    print("Command: Calculate angle between ligand atoms (in degree)")
    print("         Three trans angle (three biggest angles) are excluded.")
    print("         Metal center atom is taken as vertex.")
    print("")

    # Calculate individual angle and add to list
    angle_sigma_list = []
    ligand_atom_list = []

    for i in range(1, 7):
        for j in range(i + 1, 7):
            angle_sigma_indi = linear.angle_between(v[0], v[i], v[j])
            angle_sigma_list.append(angle_sigma_indi)
            ligand_atom_list.append([i, j])

    # Print list of angle
    print("         List of the angles before sorted:")
    # Print list of angles before sorted
    for i in range(len(angle_sigma_list)):
        print("          Angle between atom", ligand_atom_list[i][0], "and atom", ligand_atom_list[i][1],
              "before sorted: {0:5.6f}".format(angle_sigma_list[i]))
    print("")

    # Sort the angle from lowest to highest
    i = 0
    while i < len(angle_sigma_list):
        k = i
        j = i + 1
        while j < len(angle_sigma_list):
            if angle_sigma_list[k] > angle_sigma_list[j]:
                k = j
            j += 1
        angle_sigma_list[i], angle_sigma_list[k] = angle_sigma_list[k], angle_sigma_list[i]
        ligand_atom_list[i], ligand_atom_list[k] = ligand_atom_list[k], ligand_atom_list[i]
        i += 1

    print("         List of the angles after sorted:")

    for i in range(len(angle_sigma_list)):
        print("          Angle between atom", ligand_atom_list[i][0], "and atom", ligand_atom_list[i][1],
              "after sorted : {0: 5.6f}".format(angle_sigma_list[i]))
    print("")

    # Remove last three angles (last three rows)
    new_angle_sigma_list = angle_sigma_list[:len(angle_sigma_list) - 3]

    print("         ====================== SUMMARY of Σ ======================\n")
    # Print new list of angle after three trans angle deleted
    print("         List after three trans angles deleted:")

    for i in range(len(new_angle_sigma_list)):
        print("          {0: 5.6f} degree".format(new_angle_sigma_list[i]))

    print("")
    print("         Total number of angles before three trans angles deleted:", len(angle_sigma_list))
    print("         Total number of angles after three trans angles deleted :", len(new_angle_sigma_list))
    print("")

    computed_sigma = 0

    # Calculate Sigma parameter
    for i in range(len(new_angle_sigma_list)):
        computed_sigma = abs(90.0 - new_angle_sigma_list[i]) + computed_sigma

    return computed_sigma, new_angle_sigma_list


def theta_algorithm_1(z):
    """This method firstly finds the 8 faces of octahedron and choose 4 faces out of 8 faces
    The total number of combination is 8!/4!4! = 70. Then we determine the lowest Theta values.

    1. Suppose that we have an octahedron composed of one metal center atom (m)
        and six ligand atoms of which index 1-6. Given three atom of triangular plane

                    1
                4  /\  6            [1, 3, 5]
                 \/  \/
                 /\  /\             So the rest are on another parallel plane,
                3  \/  5
                   2                [2, 4, 6]

        m is absent for clarity.

    2. Orthogonally project [2, 4, 6] onto the plane that defined by [1, 3, 5]

        [2, 4, 6] -----> [2', 4', 6']
                [1, 3, 5]

        The new location of projected atoms on the given plane is [2', 4', 6']

    3. Given the line that pass through two points of the projected atoms

        line1 = 2' <------> 4'
        line2 = 4' <------> 6'
        line3 = 2' <------> 6'

    4. Project another atoms onto the given line
        and Check if two vectors are parallel or anti-parallel

        Example, line1

                        2'                          2'
               1 ------>|                1 ------->|
                        |                          |
                6' ---->|                          |<------ 6'
                        4'                         4'

                    Parallel                Anti-Parallel
               Negative dot-product     Positive dot-product

        If anti-parallel, the start and end points of line are adjacent atoms

    5. Repeat step (2) - (4) by looping the plane and reference atoms.

    6. Calculate the 6 unique angles. Then repeat step step (5) for other 7 faces.

    :param z: array - coordinate of all atoms
    :return:
    """
    computed_theta_list = []

    v = np.array(z)

    # Find suitable plane and atom on opposite plane
    pal, pcl = plane.search_8_planes(v)
    oppo_pal = plane.find_opposite_atoms(pal, v)

    print("Command: Find the orthogonal projection of atom on the given plane")
    computed_unique_angle_list = []

    # loop plane
    for i in range(8):
        # Define list for storing the unique angle for a plane
        computed_unique_angle = []
        # Find the coeff of the equation of plane
        a, b, c, d = plane.eq_of_plane(pcl[i][0], pcl[i][1], pcl[i][2])
        m = proj.project_atom_onto_plane(v[0], a, b, c, d)

        print("         Orthogonal projection onto the plane", i + 1)
        print("         The equation of plane: {0: 5.6f}x + {1: 5.6f}y + {2: 5.6f}z = {3: 5.6f}"
              .format(a, b, c, d))
        print("")

        o1 = int(oppo_pal[i][0])
        o2 = int(oppo_pal[i][1])
        o3 = int(oppo_pal[i][2])

        print("         Old coordinate of projected atom on the original plane")
        print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
        print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
        print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
        print("")

        # Project the opposite atom onto the given plane
        n1 = proj.project_atom_onto_plane(v[o1], a, b, c, d)
        n2 = proj.project_atom_onto_plane(v[o2], a, b, c, d)
        n3 = proj.project_atom_onto_plane(v[o3], a, b, c, d)

        print("         New coordinate of projected atom on the given projection plane")
        print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, n1[0], n1[1], n1[2]))
        print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, n2[0], n2[1], n2[2]))
        print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, n3[0], n3[1], n3[2]))
        print("")

        # Define line and find that if the two vectors are parallel or anti parallel.
        lal = [[o1, o2, o3],  # lal = line atom list
               [o2, o3, o1],
               [o1, o3, o2]]

        lcl = [[n1, n2, n3],  # lcl = line coord list
               [n2, n3, n1],
               [n1, n3, n2]]

        # loop three ref atoms (vertices of triangular)
        for j in range(3):
            # Find projected point of "reference atom" and "candidate atom" on the given line
            for k in range(3):
                ref_on_line = proj.project_atom_onto_line(pcl[i][j], lcl[k][0], lcl[k][1])
                can_on_line = proj.project_atom_onto_line(lcl[k][2], lcl[k][0], lcl[k][1])
                # Find vector of ref. atom and candidate atom
                vector_ref = ref_on_line - pcl[i][j]
                vector_can = can_on_line - lcl[k][2]
                # Check if two vectors are anti-parallel, if so, compute two unique angles
                # between ref. atom and its neighbor
                if np.dot(vector_ref, vector_can) < 0:
                    # angle 1
                    angle_1 = linear.angle_between(m, pcl[i][j], lcl[k][0])
                    computed_unique_angle.append(angle_1)
                    # angle 2
                    angle_2 = linear.angle_between(m, pcl[i][j], lcl[k][1])
                    computed_unique_angle.append(angle_2)

                    print("          Angle between atom {0} and {1}: {2: 5.6f}"
                          .format(pal[i][j], lal[k][0], angle_1))
                    print("          Angle between atom {0} and {1}: {2: 5.6f}"
                          .format(pal[i][j], lal[k][1], angle_2))
                    print("")

        computed_unique_angle_list.append(computed_unique_angle)

    unique_angle_list = []

    for i in range(len(computed_unique_angle_list)):
        diff_angle = 0.0
        for j in range(len(computed_unique_angle_list[i])):
            diff_angle += abs(60.0 - computed_unique_angle_list[i][j])
        unique_angle_list.append(diff_angle)

    LIST = unique_angle_list

    for i in range(0, 5):
        for j in range(i+1, 6):
            for k in range(j+1, 7):
                for l in range(k+1, 8):
                    print("4planes chosen:", i, j, k, l)
                    sum_unique_angle = LIST[i] + LIST[j] + LIST[k] + LIST[l]
                    computed_theta_list.append(sum_unique_angle)

    # Print each Theta parameter angles
    print("Command: Show computed Θ parameter for each view plane")
    for i in range(len(computed_theta_list)):
        print("         Θ from plane set {0}: {1: 5.6f} degree".format(i + 1, computed_theta_list[i]))

    print("")

    # Find the minimum Theta angle
    computed_theta = min(computed_theta_list)

    return computed_theta, computed_theta_list


def theta_algorithm_2(z):
    """This method employs the algorithm as used in algorithm 1, but find only the 4 closed-faces
    Therefore, this algorithm would give 6 different values of Theta parameters.

    :param z: array - coordinate of all atoms
    :return:
    """
    computed_theta_list = []
    # loop for swapping ligand atom 1, 2, 3, 4, & 5 with no.6 to find all possible plane
    for i in range(1, 7):
        # Copy coord_list to v_temp without touching to original array
        # use np.array(v) or v[:]
        v_temp = np.array(z)

        print("Command: Swap each ligand atom with 6th atom for finding the plane")
        print("         Swap no. {0} with original atom no.6".format(i))

        swapped_list = plane.rearrange_atom_order(v_temp, i)
        print("         Coordinate list after atom order swapped")

        for j in range(len(swapped_list)):
            s = swapped_list[j]
            if j == i:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- swapped atom".format(s[0], s[1], s[2]))
            if j == 6:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- Atom no.6".format(s[0], s[1], s[2]))
            else:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})".format(s[0], s[1], s[2]))
        print("")

        v = np.array(swapped_list)

        # Find suitable plane and atom on opposite plane
        pal, pcl = plane.search_4_planes(v)
        oppo_pal = plane.find_opposite_atoms(pal, z)

        print("Command: Find the orthogonal projection of atom on the given plane")
        computed_24_angle = []

        # loop plane
        for j in range(4):
            a, b, c, d = plane.eq_of_plane(pcl[j][0], pcl[j][1], pcl[j][2])
            m = proj.project_atom_onto_plane(v[0], a, b, c, d)

            print("         Orthogonal projection onto the plane", i + 1)
            print("         The equation of plane: {0: 5.6f}x + {1: 5.6f}y + {2: 5.6f}z = {3: 5.6f}"
                  .format(a, b, c, d))
            print("")

            o1 = int(oppo_pal[j][0])
            o2 = int(oppo_pal[j][1])
            o3 = int(oppo_pal[j][2])

            print("         Old coordinate of projected atom on the original plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
            print("")

            # Project the opposite atom onto the given plane
            n1 = proj.project_atom_onto_plane(v[o1], a, b, c, d)
            n2 = proj.project_atom_onto_plane(v[o2], a, b, c, d)
            n3 = proj.project_atom_onto_plane(v[o3], a, b, c, d)

            print("         New coordinate of projected atom on the given projection plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, n1[0], n1[1], n1[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, n2[0], n2[1], n2[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, n3[0], n3[1], n3[2]))
            print("")

            # Define line and find that if the two vectors are parallel or anti parallel.
            lal = [[o1, o2, o3],  # lal = line atom list
                   [o2, o3, o1],
                   [o1, o3, o2]]

            lcl = [[n1, n2, n3],  # lcl = line coord list
                   [n2, n3, n1],
                   [n1, n3, n2]]

            # loop three ref atoms (vertices of triangular)
            for p in range(3):
                # Find projected point of "reference atom" and "candidate atom" on the given line
                for q in range(3):
                    ref_on_line = proj.project_atom_onto_line(pcl[j][p], lcl[q][0], lcl[q][1])
                    can_on_line = proj.project_atom_onto_line(lcl[q][2], lcl[q][0], lcl[q][1])
                    # Find vector of ref. atom and candidate atom
                    vector_ref = ref_on_line - pcl[j][p]
                    vector_can = can_on_line - lcl[q][2]
                    # Check if two vectors are anti-parallel, if so, compute two unique angles
                    # between ref. atom and its neighbor
                    if np.dot(vector_ref, vector_can) < 0:
                        # angle 1
                        angle_1 = linear.angle_between(m, pcl[j][p], lcl[q][0])
                        computed_24_angle.append(angle_1)
                        # angle 2
                        angle_2 = linear.angle_between(m, pcl[j][p], lcl[q][1])
                        computed_24_angle.append(angle_2)

                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][0], angle_1))
                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][1], angle_2))
                        print("")

        # Print all 24 angles
        print("Command: Show all 24 angles")
        for a in range(len(computed_24_angle)):
            print("          Unique angle {0:}: {1: 5.6f} degree".format(a+1, computed_24_angle[a]))
        print("")

        # Sum all angles
        diff_angle = 0

        for a in range(len(computed_24_angle)):
            diff_angle += abs(60.0 - computed_24_angle[a])

        computed_theta_list.append(diff_angle)

    # Print each Theta parameter angles
    print("Command: Show computed Θ parameter for each view plane")
    for i in range(len(computed_theta_list)):
        print("         Θ from view plane {0}: {1: 5.6f} degree".format(i + 1, computed_theta_list[i]))

    print("")

    # Find the minimum Theta angle
    computed_theta = min(computed_theta_list)

    return computed_theta, computed_theta_list


def theta_algorithm_3(z):
    """This method uses the mid point on the two edges of the face to define the medium plane-like.

    :param z: array - coordinate of atom
    :return computed_theta: float - the minimum Theta parameter
    """
    computed_theta_list = []
    # loop for swapping ligand atom 1, 2, 3, 4, & 5 with no.6 to find all possible plane
    for i in range(1, 7):
        # Copy coord_list to v_temp without touching to original array
        # use np.array(v) or v[:]
        v_temp = np.array(z)

        print("Command: Swap each ligand atom with 6th atom for finding the plane")
        print("         Swap atom no. {0} with original atom no.6".format(i))

        swapped_list = plane.rearrange_atom_order(v_temp, i)
        print("         Coordinate list after atom order swapped")

        # loop to print coordinate list after atoms swapped
        for j in range(len(swapped_list)):
            s = swapped_list[j]
            if j == i:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- swapped atom".format(s[0], s[1], s[2]))
            elif j == 6:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- Atom no.6".format(s[0], s[1], s[2]))
            else:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})".format(s[0], s[1], s[2]))
        print("")

        # Find suitable plane and atom on opposite plane
        print("Command: Find the suitable plane for orthogonal projection")
        v = np.array(swapped_list)
        pal, pcl = plane.search_4_planes(v)
        oppo_pal = plane.find_opposite_atoms(pal, z)
        computed_24_angle = []

        # loop plane
        for j in range(4):
            a, b, c, d = plane.eq_of_plane(pcl[j][0], pcl[j][1], pcl[j][2])

            print("         Orthogonal projection onto the plane", i + 1)
            print("         The equation of plane: {0: 5.6f}x + {1: 5.6f}y + {2: 5.6f}z = {3: 5.6f}"
                  .format(a, b, c, d))
            print("")

            o1 = int(oppo_pal[j][0])
            o2 = int(oppo_pal[j][1])
            o3 = int(oppo_pal[j][2])

            print("         Old coordinate of projected atom on the original plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
            print("")

            # Project the opposite atom (lower plane) onto the given plane (upper plane) where ref. atom is
            n1 = proj.project_atom_onto_plane(v[o1], a, b, c, d)
            n2 = proj.project_atom_onto_plane(v[o2], a, b, c, d)
            n3 = proj.project_atom_onto_plane(v[o3], a, b, c, d)

            print("         New coordinate of projected atom on the given projection plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, n1[0], n1[1], n1[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, n2[0], n2[1], n2[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, n3[0], n3[1], n3[2]))
            print("")

            # Define three lines
            lal = [[o1, o2, o3],  # lal = line atom list
                   [o2, o3, o1],
                   [o1, o3, o2]]

            lcl = [[n1, n2, n3],  # lcl = line coord list
                   [n2, n3, n1],
                   [n1, n3, n2]]

            # loop three ref. atoms (vertices of triangular plane)
            for p in range(3):
                # Find projected point of "reference atom" and "candidate atom" on the given line
                # loop three lines
                for q in range(3):
                    ref_on_line = proj.project_atom_onto_line(pcl[j][p], lcl[q][0], lcl[q][1])
                    can_on_line = proj.project_atom_onto_line(lcl[q][2], lcl[q][0], lcl[q][1])
                    # Find vector of ref. atom and
                    vector_ref = ref_on_line - pcl[j][p]
                    vector_can = can_on_line - lcl[q][2]
                    # Check if two vectors are parallel (>0) or anti-parallel (<0),
                    if np.dot(vector_ref, vector_can) < 0:
                        # Find medium plane that containing metal center atom
                        # Define the mid point between ref. atom on upper plane and
                        # opposite one atoms on below plane
                        mp_1 = linear.midpoint_of_line(pcl[j][p], v[lal[q][0]])
                        mp_2 = linear.midpoint_of_line(pcl[j][p], v[lal[q][1]])

                        # Find the medium plane
                        e, f, g, h = plane.eq_of_plane(v[0], mp_1, mp_2)

                        # Orthogonally project all ligand atoms onto the given medium plane
                        mpcl = []

                        for ligand in range(1, 7):
                            mpcl.append(proj.project_atom_onto_plane(v[ligand], e, f, g, h))

                        print("         New coordinate of projected atom on the given medium plane")
                        for ligand in range(len(mpcl)):
                            print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                                  .format(mpcl[ligand][0], mpcl[ligand][1], mpcl[ligand][2]))

                        # Calculate unique angle
                        # angle 1
                        angle_1 = linear.angle_between(v[0], mpcl[pal[j][p] - 1], mpcl[lal[q][0] - 1])
                        computed_24_angle.append(angle_1)
                        # angle 2
                        angle_2 = linear.angle_between(v[0], mpcl[pal[j][p] - 1], mpcl[lal[q][1] - 1])
                        computed_24_angle.append(angle_2)

                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][0], angle_1))
                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][1], angle_2))
                        print("")

        # Print all 24 angles
        print("Command: Show all 24 unique angles")
        for a in range(len(computed_24_angle)):
            print("          Unique angle", a + 1, ": {0: 5.6f} degree".format(computed_24_angle[a]))
        print("")

        # Sum all angles
        diff_angle = 0

        for a in range(len(computed_24_angle)):
            diff_angle += abs(60.0 - computed_24_angle[a])

        computed_theta_list.append(diff_angle)

    # Print each Theta parameter angles
    print("Command: Show computed Θ parameter for each view plane")
    for i in range(len(computed_theta_list)):
        print("         Θ from view plane {0}: {1: 5.6f} degree"
              .format(i + 1, computed_theta_list[i]))

    print("")

    # Find the minimum Theta angle
    computed_theta = min(computed_theta_list)

    return computed_theta, computed_theta_list


def theta_algorithm_4(z):
    """This method uses the lease-squared technique in scipy.optimize module

    The initial guess of the plane is computed using the mid points on the face of octahedron
    taken from algorithm 3

    :param z:
    :return:
    """

    computed_theta_list = []
    # loop for swapping ligand atom 1, 2, 3, 4, & 5 with no.6 to find all possible plane
    for i in range(1, 7):
        # Copy coord_list to v_temp without touching to original array
        # use np.array(v) or v[:]
        v_temp = np.array(z)

        print("Command: Swap each ligand atom with 6th atom for finding the plane")
        print("         Swap atom no. {0} with original atom no.6".format(i))

        swapped_list = plane.rearrange_atom_order(v_temp, i)
        print("         Coordinate list after atom order swapped")

        # loop to print coordinate list after atoms swapped
        for j in range(len(swapped_list)):
            s = swapped_list[j]
            if j == i:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- swapped atom".format(s[0], s[1], s[2]))
            elif j == 6:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- Atom no.6".format(s[0], s[1], s[2]))
            else:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})".format(s[0], s[1], s[2]))
        print("")

        # Find suitable plane and atom on opposite plane
        print("Command: Find the suitable plane for orthogonal projection")
        v = np.array(swapped_list)
        pal, pcl = plane.search_4_planes(v)
        oppo_pal = plane.find_opposite_atoms(pal, z)
        computed_24_angle = []

        # loop plane
        for j in range(4):
            a, b, c, d = plane.eq_of_plane(pcl[j][0], pcl[j][1], pcl[j][2])

            print("         Orthogonal projection onto the plane", i + 1)
            print("         The equation of plane: {0: 5.6f}x + {1: 5.6f}y + {2: 5.6f}z = {3: 5.6f}"
                  .format(a, b, c, d))
            print("")

            o1 = int(oppo_pal[j][0])
            o2 = int(oppo_pal[j][1])
            o3 = int(oppo_pal[j][2])

            print("         Old coordinate of projected atom on the original plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
            print("")

            # Project the opposite atom (lower plane) onto the given plane (upper plane) where ref. atom is
            n1 = proj.project_atom_onto_plane(v[o1], a, b, c, d)
            n2 = proj.project_atom_onto_plane(v[o2], a, b, c, d)
            n3 = proj.project_atom_onto_plane(v[o3], a, b, c, d)

            print("         New coordinate of projected atom on the given projection plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, n1[0], n1[1], n1[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, n2[0], n2[1], n2[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, n3[0], n3[1], n3[2]))
            print("")

            # Define three lines
            lal = [[o1, o2, o3],  # lal = line atom list
                   [o2, o3, o1],
                   [o1, o3, o2]]

            lcl = [[n1, n2, n3],  # lcl = line coord list
                   [n2, n3, n1],
                   [n1, n3, n2]]

            # loop three ref. atoms (vertices of triangular plane)
            for p in range(3):
                # Find projected point of "reference atom" and "candidate atom" on the given line
                # loop three lines
                for q in range(3):
                    ref_on_line = proj.project_atom_onto_line(pcl[j][p], lcl[q][0], lcl[q][1])
                    can_on_line = proj.project_atom_onto_line(lcl[q][2], lcl[q][0], lcl[q][1])
                    # Find vector of ref. atom and
                    vector_ref = ref_on_line - pcl[j][p]
                    vector_can = can_on_line - lcl[q][2]
                    # Check if two vectors are parallel (>0) or anti-parallel (<0),
                    if np.dot(vector_ref, vector_can) < 0:
                        # Find medium plane that containing metal center atom
                        # Define the mid point between ref. atom on upper plane and
                        # opposite one atoms on below plane
                        mp_1 = linear.midpoint_of_line(pcl[j][p], v[lal[q][0]])
                        mp_2 = linear.midpoint_of_line(pcl[j][p], v[lal[q][1]])

                        # Find the initial guess of the medium plane
                        a_g, b_g, c_g, d_g = plane.eq_of_plane(v[0], mp_1, mp_2)

                        # Find the medium plane-like using optimize method
                        # coordinates of ligand atoms
                        zipped_coords = list(zip(v[0], v[1], v[2], v[4], v[5], v[6]))
                        coords = np.array(zipped_coords)

                        # Initial guess of the plane
                        p0 = [a_g, b_g, c_g, d_g]

                        def f_min(X, p):
                            plane_xyz = p[0:3]
                            distance = (plane_xyz * X.T).sum(axis=1) + p[3]
                            return distance / np.linalg.norm(plane_xyz)

                        def residuals(params, signal, X):
                            return f_min(X, params)

                        from scipy.optimize import leastsq
                        sol = leastsq(residuals, p0, args=(None, coords))[0]

                        a_m, b_m, c_m, d_m = sol

                        print("         Optimized plane: {0: 5.6f}x + {1: 5.6f}y + {2: 5.6f}z = {3: 5.6f}"
                              .format(a_m, b_m, c_m, d_m))
                        print("         Old Error: ", (f_min(coords, p0) ** 2).sum())
                        print("         New Error: ", (f_min(coords, sol) ** 2).sum())
                        print("")

                        # Orthogonally project all ligand atoms onto the given medium plane
                        mpcl = []

                        for ligand in range(1, 7):
                            mpcl.append(proj.project_atom_onto_plane(v[ligand], a_m, b_m, c_m, d_m))

                        print("         New coordinate of projected atom on the given medium plane")
                        for ligand in range(len(mpcl)):
                            print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})"
                                  .format(mpcl[ligand][0], mpcl[ligand][1], mpcl[ligand][2]))

                        # Calculate unique angle
                        # angle 1
                        angle_1 = linear.angle_between(v[0], mpcl[pal[j][p] - 1], mpcl[lal[q][0] - 1])
                        computed_24_angle.append(angle_1)
                        # angle 2
                        angle_2 = linear.angle_between(v[0], mpcl[pal[j][p] - 1], mpcl[lal[q][1] - 1])
                        computed_24_angle.append(angle_2)

                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][0], angle_1))
                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][1], angle_2))
                        print("")

        # Print all 24 angles
        print("Command: Show all 24 unique angles")
        for a in range(len(computed_24_angle)):
            print("          Unique angle", a + 1, ": {0: 5.6f} degree".format(computed_24_angle[a]))
        print("")

        # Sum all angles
        diff_angle = 0

        for a in range(len(computed_24_angle)):
            diff_angle += abs(60.0 - computed_24_angle[a])

        computed_theta_list.append(diff_angle)

    # Print each Theta parameter angles
    print("Command: Show computed Θ parameter for each view plane")
    for i in range(len(computed_theta_list)):
        print("         Θ from view plane {0}: {1: 5.6f} degree"
              .format(i + 1, computed_theta_list[i]))

    print("")

    # Find the minimum Theta angle
    computed_theta = min(computed_theta_list)

    return computed_theta, computed_theta_list


def theta_algorithm_5(z):
    """This method uses the minimize technique in scipy.optimize module

    :param z:
    :return:
    """
    def plane(x, y, params):
        a = params[0]
        b = params[1]
        c = params[2]
        z = a * x + b * y + c
        return z

    def error(params, points):
        result = 0
        for (x, y, z) in points:
            plane_z = plane(x, y, params)
            diff = abs(plane_z - z)
            result += diff ** 2
        return result

    points = [
        (1.74751500, 6.96096300, 7.93278400),
        (1.88565700, 4.80477700, 6.18372600),
        (2.81242500, 3.26655300, 8.13163700),
        (0.53900500, 4.48280900, 8.46000400),
        (2.88640400, 5.39292500, 9.84896600),
        (4.09438000, 5.80725700, 7.58868900)]

    fun = functools.partial(error, points=points)
    params0 = [0, 0, 0]
    res = scipy.optimize.minimize(fun, params0)

    a = res.x[0]
    b = res.x[1]
    c = res.x[2]

    xs, ys, zs = zip(*points)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xs, ys, zs)

    point = np.array([0.0, 0.0, c])
    normal = np.cross([1, 0, a], [0, 1, b])
    d = -point.dot(normal)
    xx, yy = np.meshgrid([-5, 10], [-5, 10])
    z = (-normal[0] * xx - normal[1] * yy - d) * 1.0 / normal[2]
    ax.plot_surface(xx, yy, z, alpha=0.2, color=[0, 1, 0])

    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.set_zlim(0, 10)

    #plt.show()

    print(a, b, c, d)

    #####################################

    computed_theta_list = []
    # loop for swapping ligand atom 1, 2, 3, 4, & 5 with no.6 to find all possible plane
    for i in range(1, 7):
        # Copy coord_list to v_temp without touching to original array
        # use np.array(v) or v[:]
        v_temp = np.array(z)

        print("Command: Swap each ligand atom with 6th atom for finding the plane")
        print("         Swap no. {0} with original atom no.6".format(i))

        swapped_list = plane.rearrange_atom_order(v_temp, i)
        print("         Coordinate list after atom order swapped")

        for j in range(len(swapped_list)):
            s = swapped_list[j]
            if j == i:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- swapped atom".format(s[0], s[1], s[2]))
            if j == 6:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f}) <- Atom no.6".format(s[0], s[1], s[2]))
            else:
                print("          ({0: 5.6f}, {1: 5.6f}, {2: 5.6f})".format(s[0], s[1], s[2]))
        print("")

        v = np.array(swapped_list)

        # Find suitable plane and atom on opposite plane
        pal, pcl = plane.search_view_plane(v)

        print("Command: Find the optimal view plane using minimization method")

        computed_24_angle = []
        oppo_pal = plane.find_atom_on_oppo_plane(pal, z)

        # loop plane
        for j in range(4):
            a, b, c, d = plane.eq_of_plane(pcl[j][0], pcl[j][1], pcl[j][2])
            m = proj.project_atom_onto_plane(v[0], a, b, c, d)

            print("         Orthogonal projection onto the plane", i + 1)
            print("         The equation of plane: {0: 5.6f}x + {1: 5.6f}y + {2: 5.6f}z = {3: 5.6f}"
                  .format(a, b, c, d))
            print("")

            o1 = int(oppo_pal[j][0])
            o2 = int(oppo_pal[j][1])
            o3 = int(oppo_pal[j][2])

            print("         Old coordinate of projected atom on the original plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
            print("")

            # Project the opposite atom onto the given plane
            n1 = proj.project_atom_onto_plane(v[o1], a, b, c, d)
            n2 = proj.project_atom_onto_plane(v[o2], a, b, c, d)
            n3 = proj.project_atom_onto_plane(v[o3], a, b, c, d)

            print("         New coordinate of projected atom on the given projection plane")
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o1, n1[0], n1[1], n1[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o2, n2[0], n2[1], n2[2]))
            print("          {0} --> ({1: 5.6f}, {2: 5.6f}, {3: 5.6f})".format(o3, n3[0], n3[1], n3[2]))
            print("")

            # Define line and find that if the two vectors are parallel or anti parallel.
            lal = [[o1, o2, o3],  # lal = line atom list
                   [o2, o3, o1],
                   [o1, o3, o2]]

            lcl = [[n1, n2, n3],  # lcl = line coord list
                   [n2, n3, n1],
                   [n1, n3, n2]]

            # loop three ref atoms (vertices of triangular)
            for p in range(3):
                # Find projected point of "reference atom" and "candidate atom" on the given line
                for q in range(3):
                    ref_on_line = proj.project_atom_onto_line(pcl[j][p], lcl[q][0], lcl[q][1])
                    can_on_line = proj.project_atom_onto_line(lcl[q][2], lcl[q][0], lcl[q][1])
                    # Find vector of ref. atom and candidate atom
                    vector_ref = ref_on_line - pcl[j][p]
                    vector_can = can_on_line - lcl[q][2]
                    # Check if two vectors are anti-parallel, if so, compute two unique angles
                    # between ref. atom and its neighbor
                    if np.dot(vector_ref, vector_can) < 0:
                        # angle 1
                        angle_1 = linear.angle_between(m, pcl[j][p], lcl[q][0])
                        computed_24_angle.append(angle_1)
                        # angle 2
                        angle_2 = linear.angle_between(m, pcl[j][p], lcl[q][1])
                        computed_24_angle.append(angle_2)

                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][0], angle_1))
                        print("          Angle between atom {0} and {1}: {2: 5.6f}"
                              .format(pal[j][p], lal[q][1], angle_2))
                        print("")

        # Print all 24 angles
        print("Command: Show all 24 angles")
        for a in range(len(computed_24_angle)):
            print("          Unique angle {0:}: {1: 5.6f} degree".format(a + 1, computed_24_angle[a]))
        print("")

        # Sum all angles
        diff_angle = 0

        for a in range(len(computed_24_angle)):
            diff_angle += abs(60.0 - computed_24_angle[a])

        computed_theta_list.append(diff_angle)

    # Print each Theta parameter angles
    print("Command: Show computed Θ parameter for each view plane")
    for i in range(len(computed_theta_list)):
        print("         Θ from view plane {0}: {1: 5.6f} degree".format(i + 1, computed_theta_list[i]))

    print("")

    # Find the minimum Theta angle
    computed_theta = min(computed_theta_list)

    return computed_theta, computed_theta_list


def calc_theta(v):
    """Calculate octahedral distortion parameter, Θ
    Octahedron has 4 faces, 6 angles each, thus the total number of theta angle is 24 angles.

      24
    Θ = sigma < 60 - angle_i >
     i=1

    where angle_i is angle between two plane defined by vector of metal center and ligand atoms.

    Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.
    """
    print("Command: Calculate the following items")
    print("         - The equation of plane given by three selected ligand atoms, Ax + By + Cz = D")
    print("           Use orthogonal projection to find the projection of all atoms on the given plane.")
    print("         - Angle between metal and ligand atom [i, j, k, p, q, r] (in degree)")
    print("")

    computed_theta_1, computed_theta_list_1 = theta_algorithm_1(v)
    computed_theta_2, computed_theta_list_2 = theta_algorithm_2(v)
    computed_theta_3, computed_theta_list_3 = theta_algorithm_3(v)
    computed_theta_4, computed_theta_list_4 = theta_algorithm_4(v)

    computed_theta = [computed_theta_1,
                      computed_theta_2,
                      computed_theta_3,
                      computed_theta_4]

    computed_theta_list = [computed_theta_list_1,
                           computed_theta_list_2,
                           computed_theta_list_3,
                           computed_theta_list_4]

    print("         ================== SUMMARY of Θ (Theta) ==================\n")
    print("Command: Show the computed Θ parameter for different methods.")

    for i in range(len(computed_theta_list)):
        print("         Method %s -----------------" % (i + 1))
        for j in range(len(computed_theta_list[i])):
            if computed_theta_list[i][j] == min(computed_theta_list[i]):
                print("         | Unique Θ %s : %5.6f ***" % (j + 1, computed_theta_list[i][j]))
            else:
                print("         | Unique Θ %s : %5.6f" % (j + 1, computed_theta_list[i][j]))
        print("")

    return computed_theta, computed_theta_list

