"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import linear
import plane
import proj


def calc_delta(al, cl):
    """Calculate Delta parameter
                                      2
                 1         / d_i - d \
    delta(d) =  --- * sum | -------- |
                 6        \    d    /

    where d_i is individual M-X distance and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

    :param al: list - list of atoms
    :param cl: array - coordinate of atoms
    :return computed_delta: float - delta parameter (unitless)
    :return unique_distance: list - list of unique distances
    """
    print("Info: Calculate distance between metal center (M) and ligand atoms")
    print("Info: Show 6 unique bond distances (Angstrom)\n")
    print("       Bond       Distance")
    print("      -------     --------")

    unique_distance = []

    for i in range(1, 7):
        distance = linear.distance_between(cl[0], cl[i])
        print("      {0:>2} - {1:>2}   {2:10.6f}".format(al[0], al[i], distance))
        unique_distance.append(distance)

    computed_distance_avg = linear.distance_avg(cl)
    computed_delta = 0

    for i in range(6):
        diff_dist = (unique_distance[i] - computed_distance_avg) / computed_distance_avg
        computed_delta = ((diff_dist * diff_dist) / 6) + computed_delta

    print("\n      ====================== SUMMARY of Δ ======================\n")
    print("      Average distance     : %10.6f Angstrom" % computed_distance_avg)
    print("      Computed Δ parameter : %10.6f\n" % computed_delta)
    print("      ==========================================================\n")

    return computed_delta


def calc_sigma(al, cl):
    """Calculate Sigma parameter

          12
    Σ = sigma < 90 - angle_i >
         i=1

    Ref: J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    :param al: list - list of atoms
    :param cl: array - coordinate of atoms
    :return computed_sigma: float - sigma parameter in degree
    :return angle_sigma: list - list of 12 unique angles
    """
    print("Info: Calculate angle between ligand atoms (including cis and trans angles)")
    print("Info: Show 15 unique bond angles (°) before sorting out\n")
    print("      Ligand atom       Angle")
    print("      -----------     ---------")

    la = []
    angle_sigma = []

    for i in range(1, 7):
        for j in range(i + 1, 7):
            angle = linear.angle_between(cl[0], cl[i], cl[j])
            print("       {0:>2} and {1:>2}     {2:10.6f}".format(al[i], al[j], angle))
            la.append([al[i], al[j]])
            angle_sigma.append(angle)

    # Sort the angle from the lowest to the highest
    i = 0
    while i < len(angle_sigma):
        k = i
        j = i + 1
        while j < len(angle_sigma):
            if angle_sigma[k] > angle_sigma[j]:
                k = j
            j += 1
        la[i], la[k] = la[k], la[i]
        angle_sigma[i], angle_sigma[k] = angle_sigma[k], angle_sigma[i]
        i += 1

    # Show trans angles
    print("\nInfo: Delete 3 trans angles\n")
    print("      Ligand atom       Angle")
    print("      -----------     ---------")

    for i in range(3):
        j = -(i+1)
        print("       {0:>2} and {1:>2}     {2:10.6f}".format(la[j][0], la[j][1], angle_sigma[j]))

    # Remove 3 trans angles (last three angles)
    la = la[:-3]
    angle_sigma = angle_sigma[:-3]

    print("\nInfo: Show 12 cis angles after deleting trans angles\n")
    print("      Ligand atom       Angle")
    print("      -----------     ---------")

    for i in range(len(angle_sigma)):
        print("       {0:>2} and {1:>2}     {2:10.6f}".format(la[i][0], la[i][1], angle_sigma[i]))

    computed_sigma = 0

    for i in range(len(angle_sigma)):
        computed_sigma = abs(90.0 - angle_sigma[i]) + computed_sigma

    print("\n      ====================== SUMMARY of Σ ======================\n")
    print("      Computed Σ parameter : %10.6f\n" % computed_sigma)
    print("      ==========================================================\n")

    return computed_sigma


def calc_theta(cl):
    """Calculate Theta parameter. Octahedron has 4 faces, 6 angles each,
    thus the total number of theta angle is 24 angles.

      24
    Θ = sigma < 60 - angle_i >
     i=1

    where angle_i is an angle between two vectors, one is vector from metal center to
    reference atom, and another one is vector from metal center to projected atom.

    Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

    However, we cannot find the 'real' medium plane that containing metal.
    Thus, we uses a new algorithm for determining 24 unique angles.
    It firstly chooses 4 faces out of 8 faces. The total number of combination is 70.
    These combinations would give different 70 Theta values.
    Then, we determine the one that give the lowest Theta values.

    1. Suppose that we have an octahedron composed of one metal center atom (m).
        and 6 ligand atoms of which index 1-6.

                    1
                4--/\--6            Face [1, 3, 5] is reference plane
                 \/  \/
                 /\  /\
                3--\/--5            Face [2, 4, 6] is opposite plane
                   2

        m is absent for clarity.

    2. Orthogonally project [2, 4, 6] onto the plane that defined by [1, 3, 5].

        [2, 4, 6] -----> [2', 4', 6']
                [1, 3, 5]

        The new location of projected atoms on the plane is [2', 4', 6']

    3. Define the line segment that pass through two projected atoms.
        In this case, the start and end points are 2' and 4'.

        line segment no. 1 = 2' ------ 4'
        line segment no. 2 = 4' ------ 6'
        line segment no. 3 = 2' ------ 6'

    4. Find the orthogonal vector of the other two atoms to the line (using projection).
        Then, compute dot product between vectors 1--->1_l and 6'--->6'_l.
        If dot product is negative, they are anti-parallel, which means that
        atoms 2' and 4' are adjacent atoms of atom 1.

        Example, projection onto line no. 1

                        2'                         2'
               1 ------>|                1 ------->|
                        |                          |
               6'------>|                          |<------- 6'
                        4'                         4'

                    Parallel                Anti-Parallel
               Positive dot-product     Negative dot-product

    5. Repeat step (2) - (4) by looping over the plane and reference atoms.

    6. Calculate the 6 unique angles.

    7. Repeat step (5) - (6) for other 7 faces.

    :param cl: array - coordinate of all atoms
    :return comp_theta: list - the lowest Theta value
    :return comp_theta_list: list - list of 70 Theta values
    :return pal: list - atomic number of all 8 faces
    :return pcl: list - atomic coordinates of all 8 faces
    :return sel_f_atom: list - atom number of selected 4 reference faces
    :return sel_f_coord: list - coordinates of selected 4 reference faces
    :return sel_oppo_f_atom: list - atom number of selected 4 opposite faces
    :return sel_oppo_f_coord: list - coordinates of selected 4 opposite faces
    :return all_comp: compile all results
    """
    # Find 8 reference faces and opposite faces
    pal, pcl = plane.find_8_faces(cl)
    oppo_pal, oppo_pcl = plane.find_opposite_atoms(pal, cl)

    print("\nInfo: Find the orthogonal projection of opposite atoms onto the reference plane")
    print("      The general form of the equation is Ax + By + Cz = D\n")
    print("Info: Show new coordinate of projected atoms\n")

    unique_6_pairs = []
    unique_6_angles = []

    # loop over 8 faces
    for i in range(8):
        a, b, c, d = plane.find_eq_of_plane(pcl[i][0], pcl[i][1], pcl[i][2])
        m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

        print("      Plane {0} : {1:9.6f}x {2:+9.6f}y {3:+9.6f}z = {4:9.6f}\n".format(i+1, a, b, c, d))

        o1 = int(oppo_pal[i][0])
        o2 = int(oppo_pal[i][1])
        o3 = int(oppo_pal[i][2])
        n1 = proj.project_atom_onto_plane(cl[o1], a, b, c, d)
        n2 = proj.project_atom_onto_plane(cl[o2], a, b, c, d)
        n3 = proj.project_atom_onto_plane(cl[o3], a, b, c, d)

        print("      Projection         X           Y           Z")
        print("      ----------     ---------   ---------   ---------")
        print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o1, o1, n1[0], n1[1], n1[2]))
        print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o2, o2, n2[0], n2[1], n2[2]))
        print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}\n".format(o3, o3, n3[0], n3[1], n3[2]))

        # Define line segment
        lal = [[o1, o2, o3],
               [o2, o3, o1],
               [o1, o3, o2]]

        lcl = [[n1, n2, n3],
               [n2, n3, n1],
               [n1, n3, n2]]

        unique_angle = []
        unique_pair = []

        # loop over three atoms (vertices of triangular)
        for j in range(3):
            # Find projected point of "reference atom" and "candidate atom" on the line
            for k in range(3):
                ref_on_line = proj.project_atom_onto_line(pcl[i][j], lcl[k][0], lcl[k][1])
                can_on_line = proj.project_atom_onto_line(lcl[k][2], lcl[k][0], lcl[k][1])
                # Find vectors from reference atom and candidate atom to a line segment
                vector_ref = ref_on_line - pcl[i][j]
                vector_can = can_on_line - lcl[k][2]
                # Compute dot product to check if two vectors are anti-parallel.
                # If so, compute two unique angles between reference atom and neighbors.
                if np.dot(vector_ref, vector_can) < 0:
                    angle_1 = linear.angle_between(m, pcl[i][j], lcl[k][0])
                    angle_2 = linear.angle_between(m, pcl[i][j], lcl[k][1])
                    unique_pair.append([pal[i][j], lal[k][0]])
                    unique_pair.append([pal[i][j], lal[k][1]])
                    unique_angle.append(angle_1)
                    unique_angle.append(angle_2)

        unique_6_pairs.append(unique_pair)
        unique_6_angles.append(unique_angle)

    print("Info: Show list of 6 unique θ angles for 8 face set (°)\n")
    print("      Set   Atom pair     Unique angle")
    print("      ---   ---------     ------------")

    for i in range(8):
        for j in range(6):
            if j == 2:
                print("       {0}      {1} & {2}         {3:9.6f}"
                      .format(i + 1, unique_6_pairs[i][j][0], unique_6_pairs[i][j][1], unique_6_angles[i][j]))
            else:
                print("              {0} & {1}         {2:9.6f}"
                      .format(unique_6_pairs[i][j][0], unique_6_pairs[i][j][1], unique_6_angles[i][j]))
        print("      --------------------------------")

    angle_list = []

    for i in range(len(unique_6_angles)):
        diff_angle = 0.0
        for j in range(len(unique_6_angles[i])):
            diff_angle += abs(60.0 - unique_6_angles[i][j])
        angle_list.append(diff_angle)

    plane_set = []
    comp_theta_list = []

    # loop over choosing 4 planes out of 8 planes
    for i in range(0, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                for l in range(k + 1, 8):
                    plane_set.append([i + 1, j + 1, k + 1, l + 1])
                    sum_unique_angle = (angle_list[i] + angle_list[j] + angle_list[k] + angle_list[l])
                    comp_theta_list.append(sum_unique_angle)

    # Find the minimum Theta angle and print all values
    lowest_theta = min(comp_theta_list)

    print("\nInfo: Show computed Θ parameter (°) of 70 sets of pair of opposite faces\n")
    print("      Set    Atom on face         Θ (°)")
    print("      ---    ------------     ----------")

    for i in range(len(comp_theta_list)):
        print("      {0:2d}     {1}    {2:11.6f}".format(i + 1, plane_set[i], comp_theta_list[i]))
        if comp_theta_list[i] == lowest_theta:
            sel_face_set = plane_set[i]

    sel_f_atom = []
    sel_f_coord = []
    sel_oppo_f_atom = []
    sel_oppo_f_coord = []

    for i in range(len(sel_face_set)):
        p = sel_face_set[i] - 1
        sel_f_atom.append(pal[p])
        sel_f_coord.append(pcl[p])
        sel_oppo_f_atom.append(oppo_pal[p])
        sel_oppo_f_coord.append(oppo_pcl[p])

    all_comp = (pal, pcl, sel_f_atom, sel_f_coord, sel_oppo_f_atom, sel_oppo_f_coord)

    print("\n      ====================== SUMMARY of Θ ======================\n")
    print("      The face set %s gives the lowest Θ parameter\n" % sel_face_set)
    print("      Selected Θ parameter : %11.6f\n" % lowest_theta)
    print("      ==========================================================\n")

    return lowest_theta, all_comp
