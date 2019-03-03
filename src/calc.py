"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import linear
import plane
import projection
import popup
import main


def calc_delta(self, a_octa, c_octa):
    """Calculate Delta parameter
                                      2
                 1         / d_i - d \
    delta(d) =  --- * sum | -------- |
                 6        \    d    /

    where d_i is individual M-X distance and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

    :param a_octa: list - atoms of octahedral structure
    :param c_octa: array - coordinate of octahedral structure
    :return computed_delta: float - delta parameter (unitless quantity)
    :return unique_distance: list - list of unique distances
    """
    main.print_stdout(self, "Info: Calculate distance between metal center (M) and ligand atoms")
    main.print_stdout(self, "Info: Show 6 unique bond distances (Angstrom)")
    main.print_stdout(self, "")
    main.print_stdout(self, "      No.     Bond       Distance")
    main.print_stdout(self, "      ---    -------     --------")

    unique_distance = []
    for i in range(1, 7):
        distance = linear.distance_between(c_octa[0], c_octa[i])
        main.print_stdout(self, "      {0:>2}     {1:>2} - {2:>2}   {3:10.6f}"
                          .format(i, a_octa[0], a_octa[i], distance))
        unique_distance.append(distance)
    main.print_stdout(self, "")

    computed_distance_avg = linear.distance_avg(c_octa)
    computed_delta = 0
    for i in range(6):
        diff_dist = (unique_distance[i] - computed_distance_avg) / computed_distance_avg
        computed_delta = ((diff_dist * diff_dist) / 6) + computed_delta

    main.print_stdout(self, "      ====================== SUMMARY of Δ ======================")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Average distance     : {0:10.6f} Angstrom".format(computed_distance_avg))
    main.print_stdout(self, "      Computed Δ parameter : {0:10.6f}".format(computed_delta))
    main.print_stdout(self, "")
    main.print_stdout(self, "      ==========================================================")
    main.print_stdout(self, "")

    return computed_delta


def calc_sigma(self, a_octa, c_octa):
    """Calculate Sigma parameter

          12
    Σ = sigma < 90 - angle_i >
         i=1

    where angle_i in an unique cis angle
    Ref: J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    :param a_octa: list - atoms of octahedral structure
    :param c_octa: array - coordinate of octahedral structure
    :return computed_sigma: float - sigma parameter in degree
    :return angle_sigma: list - list of 12 unique angles
    """
    main.print_stdout(self, "Info: Calculate angle between ligand atoms (including cis and trans angles)")
    main.print_stdout(self, "Info: Show 15 unique bond angles (°) before sorting")
    main.print_stdout(self, "")
    main.print_stdout(self, "      No.    Atom pair        Angle")
    main.print_stdout(self, "      ---    ---------     -----------")

    la = []
    angle_sigma = []
    k = 1
    for i in range(1, 7):
        for j in range(i + 1, 7):
            angle = linear.angle_between(self, c_octa[0], c_octa[i], c_octa[j])
            main.print_stdout(self, "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}"
                              .format(k, a_octa[i], a_octa[j], angle))
            la.append([a_octa[i], a_octa[j]])
            angle_sigma.append(angle)
            k += 1
    main.print_stdout(self, "")

    # Sort the angle from the lowest to the highest
    angle_sigma.sort()

    # Show trans angles (the last three angles)
    main.print_stdout(self, "Info: Show 3 trans angles")
    main.print_stdout(self, "")
    main.print_stdout(self, "      No.    Atom pair        Angle")
    main.print_stdout(self, "      ---    ---------     -----------")
    for i in range(-1, -4, -1):
        main.print_stdout(self, "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}"
                          .format(-i, la[i][0], la[i][1], angle_sigma[i]))
    main.print_stdout(self, "")

    # Remove 3 trans angles (last three angles)
    la = la[:-3]
    angle_sigma = angle_sigma[:-3]

    main.print_stdout(self, "Info: Show 12 cis angles after deleting trans angles")
    main.print_stdout(self, "")
    main.print_stdout(self, "      No.    Atom pair        Angle")
    main.print_stdout(self, "      ---    ---------     -----------")
    for i in range(len(angle_sigma)):
        main.print_stdout(self, "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}".format(i + 1, la[i][0], la[i][1], angle_sigma[i]))
    main.print_stdout(self, "")

    computed_sigma = 0
    for i in range(len(angle_sigma)):
        computed_sigma = abs(90.0 - angle_sigma[i]) + computed_sigma

    main.print_stdout(self, "      ====================== SUMMARY of Σ ======================")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Computed Σ parameter : {0:10.6f} degree".format(computed_sigma))
    main.print_stdout(self, "")
    main.print_stdout(self, "      ==========================================================")
    main.print_stdout(self, "")

    return computed_sigma


def find_6_unique_angles(self, face, eq_plane, c_octa, a_ref_f, c_ref_f, a_oppo_f):
    """Find 6 unique angles using algorithm 1

    1. Suppose that we have an octahedral structure composed of a metal center atom and 6 ligand atoms
    metal atom is absent for clarity.

                    1
                4--/\--6            Face [1, 3, 5] is reference plane
                 \/  \/
                 /\  /\
                3--\/--5            Face [2, 4, 6] is opposite plane
                   2

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

    6. Compute two unique angles between vectors from projected metal to reference and to adjacent atom

        4'    1         1     6'
         \   /           \   /
          \^/      and    \^/
           m'              m'

    7. Repeat step (2) - (6) by looping over the reference atom.

    8. Remove duplicate angles

    :param face: The face number i^th
    :param eq_plane: the equation of the projection plane
    :param c_octa: array - coordinate of octahedral structure
    :param a_ref_f: atom list of all plane
    :param c_ref_f: coordinate list of all plane
    :param a_oppo_f: opposite plane atom list
    :return unique_pair: pair of atoms of unique angle
    :return unique_angle: unique angles
    """
    a, b, c, d = eq_plane
    m = projection.project_atom_onto_plane(c_octa[0], a, b, c, d)

    # atoms on reference face
    r1 = a_ref_f[face][0]
    r2 = a_ref_f[face][1]
    r3 = a_ref_f[face][2]
    # coordinate of atoms on reference face
    cr1 = c_ref_f[face][0]
    cr2 = c_ref_f[face][1]
    cr3 = c_ref_f[face][2]
    # atoms on opposite face
    o1 = int(a_oppo_f[face][0])
    o2 = int(a_oppo_f[face][1])
    o3 = int(a_oppo_f[face][2])
    # coordinate of atoms on opposite face
    co1 = projection.project_atom_onto_plane(c_octa[o1], a, b, c, d)
    co2 = projection.project_atom_onto_plane(c_octa[o2], a, b, c, d)
    co3 = projection.project_atom_onto_plane(c_octa[o3], a, b, c, d)

    n = face + 1
    main.print_stdout(self, "               m --> m'      {0:9.6f}   {1:9.6f}   {2:9.6f}".format(m[0], m[1], m[2]))
    main.print_stdout(self, "        {0}      {1} --> {2}'      {3:9.6f}   {4:9.6f}   {5:9.6f}".format(n, o1, o1, co1[0], co1[1], co1[2]))
    main.print_stdout(self, "               {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o2, o2, co2[0], co2[1], co2[2]))
    main.print_stdout(self, "               {0} --> {1}'      {2:9.6f}   {3:9.6f}   {4:9.6f}".format(o3, o3, co3[0], co3[1], co3[2]))
    main.print_stdout(self, "      --------------------------------------------------------")

    # Create list of atoms and coordinates for the plane of interest
    six_atoms = [r1, r2, r3, o1, o2, o3]
    six_coords = [cr1, cr2, cr3, co1, co2, co3]

    # Find norm of vector from metal center atom to ligand atom
    norm_vect = []
    for i in range(6):
        norm = linear.norm_vector(self, six_coords[i] - m)
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
                    prof_ref = projection.project_atom_onto_line(norm_vect[ref], norm_vect[l1], norm_vect[l2])
                    # Project three candidate atoms onto the line
                    vector_proj_can = []
                    for can in range(6):
                        if can != ref and can != l1 and can != l2:
                            can_proj = projection.project_atom_onto_line(norm_vect[can], norm_vect[l1], norm_vect[l2])
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

    # Sort list in list
    for j in range(len(all_pair)):
        all_pair[j].sort()
    all_pair.sort()
    # Remove duplicate list
    all_pair = all_pair[1::2]

    # Find unique_pair and compute unique_angle
    for i in range(6):
        unique_pair.append([six_atoms[all_pair[i][0]], six_atoms[all_pair[i][1]]])
        angle = linear.angle_between(self, origin, norm_vect[all_pair[i][0]], norm_vect[all_pair[i][1]])
        unique_angle.append(angle)

    # Finally, check if sum of all angles in unique_angle is 360 or not
    sum_angles = sum([unique_angle[i] for i in range(len(unique_angle))])
    if len(unique_pair) != 6 or sum_angles <= 359.9 or sum_angles >= 360.1:
        popup.err_not_octa(self)
        return 1

    return unique_pair, unique_angle


def calc_theta(self, c_octa):
    """Calculate Theta parameter

          24
    Θ = sigma < 60 - angle_i >
         i=1

    where angle_i is an unique angle between two vectors of two twisting face.
    Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

    Algorithm 1:
        This algorithm firstly determines all possible combination of 4 faces.
    Then, it chooses 4 faces out of 8 faces. The total number of combination is 70.
    These combinations would give different 70 Theta values. The lowest Theta value is selected.

    :param c_octa: array - coordinate of octahedral structure
    :return min_theta: list - the lowest Theta value
    :return all_comp: compile all results
            a_ref_f: list - atomic number of all 8 faces
            c_ref_f: list - atomic coordinates of all 8 faces
            sel_f_atom: list - atom number of selected 4 reference faces
            sel_f_coord: list - coordinates of selected 4 reference faces
            sel_oppo_f_atom: list - atom number of selected 4 opposite faces
            sel_oppo_f_coord: list - coordinates of selected 4 opposite faces
    """
    main.print_stdout(self, "Info: Find 8 faces of octahedral structure and the equation of plane")
    main.print_stdout(self, "      The general form of the equation of plane is Ax + By + Cz = D")
    main.print_stdout(self, "")

    # Find 8 reference faces and 8 opposite faces
    a_ref_f, c_ref_f, a_oppo_f, c_oppo_f = plane.find_8_faces(self, c_octa)

    main.print_stdout(self, "Info: Show the equation of the projection plane")
    main.print_stdout(self, "")
    # Find the equation of plane
    eq_plane_set = []
    for i in range(8):
        a, b, c, d = plane.find_eq_of_plane(c_ref_f[i][0], c_ref_f[i][1], c_ref_f[i][2])
        main.print_stdout(self, "      Plane {0} : {1:9.6f}x {2:+9.6f}y {3:+9.6f}z = {4:9.6f}".format(i + 1, a, b, c, d))
        eq_plane_set.append([a, b, c, d])
    main.print_stdout(self, "")

    main.print_stdout(self, "Info: Find the orthogonal projection of opposite atoms onto the reference plane")
    main.print_stdout(self, "Info: Show new coordinate of projected atoms (m is a metal center)")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Face    Projection         X           Y           Z")
    main.print_stdout(self, "      ----    ----------     ---------   ---------   ---------")

    # Find orthogonal projection
    unique_6_pairs = []
    unique_6_angles = []
    # loop over 8 faces to find 6 unique angles for each face
    for i in range(8):
        eq_plane = eq_plane_set[i]
        unique_pair, unique_angle = find_6_unique_angles(self, i, eq_plane, c_octa, a_ref_f, c_ref_f, a_oppo_f)
        unique_6_pairs.append(unique_pair)
        unique_6_angles.append(unique_angle)
    main.print_stdout(self, "")

    # Sum 6 unique angles for each face
    sum_unique_angle = []
    for i in range(8):
        sum_angles = 0
        for j in range(6):
            sum_angles += unique_6_angles[i][j]
        sum_unique_angle.append(sum_angles)

    main.print_stdout(self, "Info: Calculate the 6 unique θ angles for each face")
    main.print_stdout(self, "Info: Show list of 6 unique θ angles for 8 face sets (°)")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Set    Atom pair      θ angle        |60 - θ|")
    main.print_stdout(self, "      ---    ---------     ---------      ----------")

    k = 0
    for i in range(len(unique_6_pairs)):
        for j in range(len(unique_6_pairs[i])):
            if j == 2:
                main.print_stdout(self, "       {0}       {1} & {2}      {3:10.6f}       {4:9.6f}"
                      .format(i + 1, unique_6_pairs[i][j][0], unique_6_pairs[i][j][1], unique_6_angles[i][j],
                              abs(60 - unique_6_angles[i][j])))
            else:
                main.print_stdout(self, "               {0} & {1}      {2:10.6f}       {3:9.6f}"
                      .format(unique_6_pairs[i][j][0], unique_6_pairs[i][j][1], unique_6_angles[i][j],
                              abs(60 - unique_6_angles[i][j])))
            k += 1
        main.print_stdout(self, "      ----------------------------------------------")
    main.print_stdout(self, "")

    main.print_stdout(self, "Info: The total number of unique θ angles is {0}".format(k))
    main.print_stdout(self, "")

    theta_angle_list = []
    for i in range(len(unique_6_angles)):
        diff_angle = 0.0
        for j in range(len(unique_6_angles[i])):
            diff_angle += abs(60.0 - unique_6_angles[i][j])
        theta_angle_list.append(diff_angle)

    main.print_stdout(self, "Info: Show unique Θ parameter for 8 projection planes")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Plane     Θ parameter")
    main.print_stdout(self, "      -----     -----------")
    for i in range(8):
        main.print_stdout(self, "        {0:d}       {1:11.6f}".format(i + 1, theta_angle_list[i]))
    main.print_stdout(self, "")

    plane_set = []
    comp_theta_list = []
    # loop over choosing 4 planes out of 8 planes
    for i in range(0, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                for l in range(k + 1, 8):
                    plane_set.append([i + 1, j + 1, k + 1, l + 1])
                    sum_unique_angle = (theta_angle_list[i] +
                                        theta_angle_list[j] +
                                        theta_angle_list[k] +
                                        theta_angle_list[l])
                    comp_theta_list.append(sum_unique_angle)

    # Find the lowest, highest, and mean Theta values and print all values
    min_theta = min(comp_theta_list)
    max_theta = max(comp_theta_list)
    mean_theta = (min_theta + max_theta) / 2

    main.print_stdout(self, "Info: Calculate Θ parameter for each face sets")
    main.print_stdout(self, "Info: Show computed Θ parameter (°) of 70 sets of pair of opposite faces")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Set    Atom on face         Θ (°)")
    main.print_stdout(self, "      ---    ------------     ----------")

    number_sel_set = 0
    sel_face_set = 0
    for i in range(len(comp_theta_list)):
        main.print_stdout(self, "      {0:2d}     {1}    {2:11.6f}".format(i + 1, plane_set[i], comp_theta_list[i]))
        if comp_theta_list[i] == min_theta:
            number_sel_set = i + 1
            sel_face_set = plane_set[i]
    main.print_stdout(self, "")

    sel_f_atom = []
    sel_f_coord = []
    sel_oppo_f_atom = []
    sel_oppo_f_coord = []
    # Get the data of optimal faces  selected face set
    for i in range(len(sel_face_set)):
        p = sel_face_set[i]
        sel_f_atom.append(a_ref_f[p - 1])
        sel_f_coord.append(c_ref_f[p - 1])
        sel_oppo_f_atom.append(a_oppo_f[p - 1])
        sel_oppo_f_coord.append(c_oppo_f[p - 1])

    all_comp = (a_ref_f, c_ref_f, sel_f_atom, sel_f_coord, sel_oppo_f_atom, sel_oppo_f_coord)

    main.print_stdout(self, "      ====================== SUMMARY of Θ ======================")
    main.print_stdout(self, "")
    main.print_stdout(self, "      The face set no. {0} of {1} gives the lowest Θ parameter"
                      .format(number_sel_set, sel_face_set))
    main.print_stdout(self, "")
    main.print_stdout(self, "      Pair   Reference    Opposite")
    main.print_stdout(self, "               face         face")
    main.print_stdout(self, "      ----   ---------    ---------")
    for i in range(4):
        main.print_stdout(self, "        {0}    {1}    {2}".format(sel_face_set[i], sel_f_atom[i], sel_oppo_f_atom[i]))
    main.print_stdout(self, "")
    main.print_stdout(self, "      Minimum Θ parameter : {0:11.6f} degree ***".format(min_theta))
    main.print_stdout(self, "      Maximum Θ parameter : {0:11.6f} degree".format(max_theta))
    main.print_stdout(self, "         Mean Θ parameter : {0:11.6f} degree".format(mean_theta))
    main.print_stdout(self, "")
    main.print_stdout(self, "      ==========================================================")
    main.print_stdout(self, "")

    return min_theta, max_theta, mean_theta, all_comp
