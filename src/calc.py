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
import popup


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
    print("      Ligand atom        Angle")
    print("      -----------     -----------")

    la = []
    angle_sigma = []

    for i in range(1, 7):
        for j in range(i + 1, 7):
            angle = linear.angle_between(cl[0], cl[i], cl[j])
            print("       {0:>2} and {1:>2}       {2:10.6f}".format(al[i], al[j], angle))
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
    print("      Ligand atom        Angle")
    print("      -----------     -----------")

    for i in range(3):
        j = -(i+1)
        print("       {0:>2} and {1:>2}       {2:10.6f}".format(la[j][0], la[j][1], angle_sigma[j]))

    # Remove 3 trans angles (last three angles)
    la = la[:-3]
    angle_sigma = angle_sigma[:-3]

    print("\nInfo: Show 12 cis angles after deleting trans angles\n")
    print("      Ligand atom        Angle")
    print("      -----------     -----------")

    for i in range(len(angle_sigma)):
        print("       {0:>2} and {1:>2}       {2:10.6f}".format(la[i][0], la[i][1], angle_sigma[i]))

    computed_sigma = 0

    for i in range(len(angle_sigma)):
        computed_sigma = abs(90.0 - angle_sigma[i]) + computed_sigma

    print("\n      ====================== SUMMARY of Σ ======================\n")
    print("      Computed Σ parameter : %10.6f\n" % computed_sigma)
    print("      ==========================================================\n")

    return computed_sigma


def find_6_unique_angles(face, cl, pal, pcl, oppo_pal):
    """Find 6 unique angles

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

    3. Define one of them is a reference atom, so the other 5 atoms are candidate atoms
        Define the line by choosing 2 atoms out of 5 atoms.

        For example, suppose that atom 1 is a reference atom, atoms 4' and 6' are a candidate line
        and the other candidate atoms are 3, 2', and 5.

        Reference atom:         1

        Candidate line:    4'-------6'

        Candidate atom:    3        5
                                2

    4. Find the orthogonal vector of the reference and candidate atoms to the candidate line.

        For example,
                            1
                            |
                            |
                            v
                   4'---------------6'
                      ^     ^     ^
                      |     |     |
                      |     |     |
                      3     |     5
                            2'

            Anti-Parallel (Negative dot-product)

    5. Compute dot product between reference vector and candidate vector.
        If three candidate vectors are all anti-parallel to the reference vector,
        the atom on the candidate line is adjacent atom of reference atom.

    6. Compute two angles of reference atom and two atoms

           ^               ^
        1--m--4'   and  1--m--6'

    7. Repeat step (2) - (6) by looping over the reference atom.

    8. Remove duplicate angles

    :param face: The face number i^th
    :param cl: coordinate of all atoms
    :param pal: atom list of all plane
    :param pcl: coordinate list of all plane
    :param oppo_pal: opposite plane atom list
    :return unique_pair:
    :return unique_angle:
    """
    a, b, c, d = plane.find_eq_of_plane(pcl[face][0], pcl[face][1], pcl[face][2])
    m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

    print("      Plane {0} : {1:9.6f}x {2:+9.6f}y {3:+9.6f}z = {4:9.6f}\n".format(face + 1, a, b, c, d))

    # atoms on reference face
    r1 = pal[face][0]
    r2 = pal[face][1]
    r3 = pal[face][2]
    # coordinate of atoms on reference face
    cr1 = pcl[face][0]
    cr2 = pcl[face][1]
    cr3 = pcl[face][2]
    # atoms on opposite face
    o1 = int(oppo_pal[face][0])
    o2 = int(oppo_pal[face][1])
    o3 = int(oppo_pal[face][2])
    # coordinate of atoms on opposite face
    co1 = proj.project_atom_onto_plane(cl[o1], a, b, c, d)
    co2 = proj.project_atom_onto_plane(cl[o2], a, b, c, d)
    co3 = proj.project_atom_onto_plane(cl[o3], a, b, c, d)

    print("      Projection         X           Y           Z")
    print("      ----------     ---------   ---------   ---------")
    print("       m --> m'      {0:9.6f}   {1:9.6f}   {2:9.6f}".format(m[0], m[1], m[2]))
    print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o1, o1, co1[0], co1[1], co1[2]))
    print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o2, o2, co2[0], co2[1], co2[2]))
    print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}\n".format(o3, o3, co3[0], co3[1], co3[2]))

    # Create list of atoms and coordinates for the plane of interest
    six_atoms = [r1, r2, r3, o1, o2, o3]
    six_coords = [cr1, cr2, cr3, co1, co2, co3]

    # Find norm of vector from metal center atom to ligand atom
    norm_vect = []
    for i in range(6):
        norm = linear.norm_vector(six_coords[i] - m)
        norm_vect.append(norm)

    all_pair = []
    unique_pair = []
    unique_angle = []
    origin = [0.0, 0.0, 0.0]

    # loop over six ligand atoms; choose 1 atom out of 6 atoms
    for ref in range(6):
        # loop over five lines; choose 2 atoms out of 5 candidate atoms
        for l1 in range(6):
            for l2 in range(6):
                # Make sure that three atoms are different
                if ref != l1 and ref != l2 and l2 > l1:
                    # Project reference atom onto the line
                    prof_ref = proj.project_atom_onto_line(norm_vect[ref], norm_vect[l1], norm_vect[l2])
                    # Project three candidate atoms onto the line
                    vector_proj_can = []
                    for can in range(6):
                        if can != ref and can != l1 and can != l2:
                            can_proj = proj.project_atom_onto_line(norm_vect[can], norm_vect[l1], norm_vect[l2])
                            vector_proj_can.append(can_proj - norm_vect[can])

                    # Define vectors
                    vector_ref = prof_ref - norm_vect[ref]
                    vector_can_1 = vector_proj_can[0]
                    vector_can_2 = vector_proj_can[1]
                    vector_can_3 = vector_proj_can[2]

                    # Calculate dot product between reference vector and candidate vector
                    dot_prod_1 = np.dot(vector_ref, vector_can_1)
                    dot_prod_2 = np.dot(vector_ref, vector_can_2)
                    dot_prod_3 = np.dot(vector_ref, vector_can_3)

                    # If the candidate vectors are all anti-parallel to a reference vector,
                    # the two atoms on the line of interest are adjacent to reference atom
                    if dot_prod_1 < 0 and dot_prod_2 < 0 and dot_prod_3 < 0:
                        all_pair.append([ref, l1])
                        all_pair.append([ref, l2])

    # all_pair contains 12 pairs of adjoining atoms
    # So we have to remove 6 duplicate pairs
    copy_all_pair = list(all_pair)
    all_pair = []
    # Sort out list in list
    for j in range(len(copy_all_pair)):
        sorted_pair = sorted(copy_all_pair[j])
        all_pair.append(sorted_pair)
    # Sort out list
    all_pair = sorted(all_pair)
    # Remove element of which odd index
    all_pair = all_pair[1::2]

    # Find unique_pair and compute unique_angle
    for i in range(6):
        unique_pair.append([six_atoms[all_pair[i][0]], six_atoms[all_pair[i][1]]])
        angle = linear.angle_between(origin, norm_vect[all_pair[i][0]], norm_vect[all_pair[i][1]])
        unique_angle.append(angle)

    # Finally, check if sum of all angles in unique_angle is 360 or not
    sum_angles = sum([unique_angle[i] for i in range(len(unique_angle))])
    if len(unique_pair) != 6 or 359.9 <= sum_angles >= 360.1:
        popup.not_octahedron_error()
        return 1

    return unique_pair, unique_angle


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
    Thus, we use a new algorithm for determining 24 unique angles.
    It firstly chooses 4 faces out of 8 faces. The total number of combination is 70.
    These combinations would give different 70 Theta values.
    Then, we determine the one that give the lowest Theta values.

    :param cl: array - coordinate of all atoms
    :return lowest_theta: list - the lowest Theta value
    :return all_comp: compile all results
            pal: list - atomic number of all 8 faces
            pcl: list - atomic coordinates of all 8 faces
            sel_f_atom: list - atom number of selected 4 reference faces
            sel_f_coord: list - coordinates of selected 4 reference faces
            sel_oppo_f_atom: list - atom number of selected 4 opposite faces
            sel_oppo_f_coord: list - coordinates of selected 4 opposite faces
    """
    # Find 8 reference faces and opposite faces
    pal, pcl = plane.find_8_faces(cl)
    oppo_pal, oppo_pcl = plane.find_opposite_faces(pal, cl)

    print("\nInfo: Find the orthogonal projection of opposite atoms onto the reference plane")
    print("      The general form of the equation is Ax + By + Cz = D")
    print("Info: Show new coordinate of projected atoms\n")

    unique_6_pairs = []
    unique_6_angles = []

    # loop over 8 faces to find 6 unique angles for each face
    for i in range(8):
        unique_pair, unique_angle = find_6_unique_angles(i, cl, pal, pcl, oppo_pal)
        unique_6_pairs.append(unique_pair)
        unique_6_angles.append(unique_angle)

    print("Info: Calculate the 6 unique θ angles for each face")
    print("Info: Show list of 6 unique θ angles for 8 face sets (°)\n")
    print("      Set   Atom pair     Unique angle")
    print("      ---   ---------     ------------")

    k = 0
    for i in range(len(unique_6_pairs)):
        sum_angles = 0
        for j in range(len(unique_6_pairs[i])):
            if j == 2:
                print("       {0}      {1} & {2}        {3:10.6f}"
                      .format(i + 1, unique_6_pairs[i][j][0], unique_6_pairs[i][j][1], unique_6_angles[i][j]))
            else:
                print("              {0} & {1}        {2:10.6f}"
                      .format(unique_6_pairs[i][j][0], unique_6_pairs[i][j][1], unique_6_angles[i][j]))
            sum_angles += unique_6_angles[i][j]
            k += 1

        print("                           ----------")
        print("                     Sum = %9.6f" % sum_angles)
        print("      --------------------------------")

    print("\nInfo: The total number of unique twisting angles is %s" % k)

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
        p = sel_face_set[i]
        sel_f_atom.append(pal[p-1])
        sel_f_coord.append(pcl[p-1])
        sel_oppo_f_atom.append(oppo_pal[p-1])
        sel_oppo_f_coord.append(oppo_pcl[p-1])

    all_comp = (pal, pcl, sel_f_atom, sel_f_coord, sel_oppo_f_atom, sel_oppo_f_coord)

    print("\n      ====================== SUMMARY of Θ ======================\n")
    print("      The face set %s gives the lowest Θ parameter" % sel_face_set)
    print("      Selected Θ parameter : %11.6f\n" % lowest_theta)

    for i in range(4):
        print("      Pair of opposite faces no.", sel_face_set[i])
        print("      Reference atom: {0}            Opposite atom : {1}".format(sel_f_atom[i], sel_oppo_f_atom[i]))
        print("      ====================================================================")
        print("          X          Y          Z      |       X          Y          Z ")
        print("      ---------  ---------  ---------  |   ---------  ---------  ---------")
        for j in range(3):
            print("      {0:9.6f}  {1:9.6f}  {2:9.6f}  |   {3:9.6f}  {4:9.6f}  {5:9.6f}"
                  .format(sel_f_coord[i][j][0], sel_f_coord[i][j][1], sel_f_coord[i][j][2],
                          sel_oppo_f_coord[i][j][0], sel_oppo_f_coord[i][j][1], sel_oppo_f_coord[i][j][2]))
        print("")
    print("      ==========================================================\n")

    return lowest_theta, all_comp
