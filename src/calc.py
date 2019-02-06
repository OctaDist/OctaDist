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


def find_6_angles_algorithm_1(face, metal, proj_list, pal, pcl):
    """The three-lines algorithm

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

    :param face: The face number i^th
    :param metal: projected metal center
    :param proj_list: zipped atom and coordinate of projected points
    :param pal: plane_atom_list
    :param pcl: plane_coord_list
    :return unique_pair:
    :return unique_angle:
    """
    o1, o2, o3, n1, n2, n3 = proj_list

    # Define three lines (hard-code may be faster than using loop)
    lal = [[o1, o2, o3],
           [o2, o3, o1],
           [o1, o3, o2]]

    lcl = [[n1, n2, n3],
           [n2, n3, n1],
           [n1, n3, n2]]

    unique_pair = []
    unique_angle = []

    # loop over three atoms (vertices of triangle)
    for i in range(3):
        # loop over three lines
        for j in range(3):
            ref_on_line = proj.project_atom_onto_line(pcl[face][i], lcl[j][0], lcl[j][1])
            can_on_line = proj.project_atom_onto_line(lcl[j][2], lcl[j][0], lcl[j][1])

            # Find two vectors from reference atom and candidate atom to a line segment
            vector_ref = ref_on_line - pcl[face][i]
            vector_can = can_on_line - lcl[j][2]

            # Compute dot product to check if two vectors are anti-parallel
            # If so, compute two adjacent angles of the reference
            if np.dot(vector_ref, vector_can) < 0:
                angle_1 = linear.angle_between(metal, pcl[face][i], lcl[j][0])
                angle_2 = linear.angle_between(metal, pcl[face][i], lcl[j][1])

                unique_pair.append([pal[face][i], lal[j][0]])
                unique_pair.append([pal[face][i], lal[j][1]])

                unique_angle.append(angle_1)
                unique_angle.append(angle_2)

    return unique_pair, unique_angle


def find_6_angles_algorithm_2(face, metal, proj_list, pal, pcl):
    """The Five-lines algorithm

    :param face: The face number i^th
    :param metal: projected metal center
    :param proj_list: zipped atom and coordinate of projected points
    :param pal: plane_atom_list
    :param pcl: plane_coord_list
    :return unique_pair:
    :return unique_angle:
    """
    o1, o2, o3, n1, n2, n3 = proj_list

    # Create list which includes three reference atoms and three opposite atoms
    six_atoms = [pal[face][0], pal[face][1], pal[face][2], o1, o2, o3]
    six_coords = [pcl[face][0], pcl[face][1], pcl[face][2], n1, n2, n3]

    # Find norm of vector from metal center atom to ligand atom
    norm_vect = []

    for j in range(6):
        norm = linear.norm_vector(six_coords[j] - metal)
        norm_vect.append(norm)

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
                    # proj_can_atom = []

                    for can in range(6):
                        if can != ref and can != l1 and can != l2:
                            can_proj = proj.project_atom_onto_line(norm_vect[can], norm_vect[l1], norm_vect[l2])
                            vector_proj_can.append(can_proj - norm_vect[can])
                            # proj_can_atom.append(six_atoms[can])

                    vector_ref = prof_ref - norm_vect[ref]
                    vector_can_1 = vector_proj_can[0]
                    vector_can_2 = vector_proj_can[1]
                    vector_can_3 = vector_proj_can[2]

                    # Calculate dot product
                    dot_prod_1 = np.dot(vector_ref, vector_can_1)
                    dot_prod_2 = np.dot(vector_ref, vector_can_2)
                    dot_prod_3 = np.dot(vector_ref, vector_can_3)

                    # Check if three candidate vectors are all parallel and they are anti-parallel to
                    # the vector of reference atom. If these two conditions are true, then compute angle
                    if dot_prod_1 < 0 and dot_prod_2 < 0 and dot_prod_3 < 0:
                        angle_1 = linear.angle_between(origin, norm_vect[ref], norm_vect[l1])
                        angle_2 = linear.angle_between(origin, norm_vect[ref], norm_vect[l2])

                        # unique_pair.append([pal[face][ref], lal[k][0]])
                        # unique_pair.append([pal[face][ref], lal[k][1]])

                        unique_pair.append([six_atoms[ref], six_atoms[l1]])
                        unique_pair.append([six_atoms[ref], six_atoms[l2]])

                        unique_angle.append(angle_1)
                        unique_angle.append(angle_2)

                        # ref_line_can.append([prof_ref, proj_can[0], proj_can[1], proj_can[2]])
                        #
                        # ref_line_can_atom.append([six_atoms[ref], six_atoms[l1], six_atoms[l2],
                        #                           proj_can_atom[0], proj_can_atom[1], proj_can_atom[2]])

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
    print("      The general form of the equation is Ax + By + Cz = D\n")
    print("Info: Show new coordinate of projected atoms\n")

    unique_6_pairs = []
    unique_6_angles = []
    algorithm_2_list = []
    summary_angles = []

    # loop over 8 faces to find 6 unique angles for each face
    for i in range(8):
        a, b, c, d = plane.find_eq_of_plane(pcl[i][0], pcl[i][1], pcl[i][2])
        m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

        print("      Plane {0} : {1:9.6f}x {2:+9.6f}y {3:+9.6f}z = {4:9.6f}\n".format(i + 1, a, b, c, d))

        o1 = int(oppo_pal[i][0])
        o2 = int(oppo_pal[i][1])
        o3 = int(oppo_pal[i][2])
        n1 = proj.project_atom_onto_plane(cl[o1], a, b, c, d)
        n2 = proj.project_atom_onto_plane(cl[o2], a, b, c, d)
        n3 = proj.project_atom_onto_plane(cl[o3], a, b, c, d)

        print("      Projection         X           Y           Z")
        print("      ----------     ---------   ---------   ---------")
        print("       m --> m'      {0:9.6f}   {1:9.6f}   {2:9.6f}".format(m[0], m[1], m[2]))
        print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o1, o1, n1[0], n1[1], n1[2]))
        print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o2, o2, n2[0], n2[1], n2[2]))
        print("       {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}\n".format(o3, o3, n3[0], n3[1], n3[2]))

        # First, use the three-line algorithm to find the 6 unique angles and store into unique_pair list
        # Check if the face has 6 unique angles and the sum of 6 unique angles is equal to 360
        # If one of them is false, the multiple-line algorithm is used on-the-fly

        # Create proj_list for collecting the atom on the same face (plane)
        proj_list = (o1, o2, o3, n1, n2, n3)

        # The 1st algorithm is used first
        unique_pair, unique_angle = find_6_angles_algorithm_1(i, m, proj_list, pal, pcl)

        # Sum all 6 unique angles (expected results is 360.00)
        sum_angles = sum([unique_angle[j] for j in range(len(unique_angle))])

        if len(unique_pair) != 6 or 359.9 <= sum_angles >= 360.1:
            # Collect data
            summary_angles.append([len(unique_pair), sum_angles, 'X'])
            algorithm_2_list.append(i)

            # The 2nd algorithm is used
            unique_pair, unique_angle = find_6_angles_algorithm_2(i, m, proj_list, pal, pcl)

            # Remove redundant pair
            copy_unique_pair = list(unique_pair)
            unique_pair = []
            # Sort out list in list
            for j in range(len(copy_unique_pair)):
                sorted_pair = sorted(copy_unique_pair[j])
                unique_pair.append(sorted_pair)
            # Sort list
            unique_pair = sorted(unique_pair)
            # Remove element of which odd index
            unique_pair = unique_pair[1::2]

            # Remove redundant angles
            unique_angle = list(set(unique_angle))

            # Sum all 6 unique angles (expected results is 360.00)
            sum_angles = sum([unique_angle[j] for j in range(len(unique_angle))])

            if len(unique_pair) != 6 or 359.9 <= sum_angles >= 360.1:
                popup.not_octahedron_error()
                return 1

        else:
            summary_angles.append([len(unique_pair), sum_angles, '/'])

        unique_6_pairs.append(unique_pair)
        unique_6_angles.append(unique_angle)

    print("Info: Calculate the 6 unique θ angles for each face")
    print("Info: By default, OctaDist uses the 1st algorithm to find the 6 unique angles")
    print("      If it fails, the 2nd algorithm will be used (on-the-fly) instead\n")
    print("Info: Show summary of θ angles for each face computed by the 1st algorithm\n")
    print("      Face    Unique angles    Sum of unique angles    Check")
    print("      ----    -------------    --------------------    -----")

    for i in range(len(summary_angles)):
        print("        {0}           {1}               {2:9.6f}           {3}"
              .format(i+1, summary_angles[i][0], summary_angles[i][1], summary_angles[i][2]))

    if algorithm_2_list:
        print("\nInfo: The 1st algorithm failed to compute the 6 unique angles for face %s" % algorithm_2_list)
        print("Info: OctaDist switched it off and used the 2nd algorithm instead")
    else:
        print("\nInfo: Congrats! The 1st algorithm computed the 6 uniques angles of all faces correctly")

    print("\nInfo: Show list of 6 unique θ angles for 8 face sets (°)\n")
    print("      Set   Atom pair     Unique angle")
    print("      ---   ---------     ------------")

    k = 0
    for i in range(len(unique_6_pairs)):
        sum_angles = 0
        for j in range(len(unique_6_pairs[i])):
            # Find the row for showing the Set number in the middle
            set_row = len(unique_6_pairs[i])/2 - 1
            if set_row < 0:
                set_row = 0

            if j == set_row:
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

