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


def calc_delta(cl):
    """Calculate Delta parameter
                                      2
                 1         / d_i - d \
    delta(d) =  --- * sum | -------- |
                 6        \    d    /

    where d_i is individual M-X distance and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

    :param cl: array - coordinate of atoms
    :return computed_delta: float - delta parameter (unitless)
    :return unique_distance: list - list of unique distances
    """
    print("Info: Calculate distance between metal center (M) and ligand atoms (Å)")

    unique_distance = []

    print("Info: Show 6 distances\n")
    print("      List of distances:")

    for i in range(1, 7):
        distance = linear.distance_between(cl[0], cl[i])
        print("       Distance between M and ligand atom {0} : {1:10.6f}"
              .format(i, distance))
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


def calc_sigma(cl):
    """Calculate Sigma parameter

          12
    Σ = sigma < 90 - angle_i >
         i=1

    Ref: J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    :param cl: array - coordinate of atoms
    :return computed_sigma: float - sigma parameter in degree
    :return new_angle_sigma: list - list of 12 unique angles
    """
    print("Info: Calculate angle (°) between ligand atoms")
    print("Info: Show 15 angles including cis and trans angles")

    angle_sigma = []
    ligand_atom = []

    for i in range(1, 7):
        for j in range(i + 1, 7):
            unique_angle_sigma = linear.angle_between(cl[0], cl[i], cl[j])
            angle_sigma.append(unique_angle_sigma)
            ligand_atom.append([i, j])

    print("\n      List of the angles before sorting angle out:")

    for i in range(len(angle_sigma)):
        print("       Angle between atoms {0} and {1} before sorted : {2:10.6f}"
              .format(ligand_atom[i][0], ligand_atom[i][1], angle_sigma[i]))

    # Sort the angle from the lowest to the highest
    i = 0
    while i < len(angle_sigma):
        k = i
        j = i + 1
        while j < len(angle_sigma):
            if angle_sigma[k] > angle_sigma[j]:
                k = j
            j += 1
        angle_sigma[i], angle_sigma[k] = angle_sigma[k], angle_sigma[i]
        ligand_atom[i], ligand_atom[k] = ligand_atom[k], ligand_atom[i]
        i += 1

    print("\nInfo: Delete 3 trans angles")
    print("Info: Show 12 cis angles after deleting trans angles")

    # Remove last three angles (last three rows)
    new_angle_sigma = angle_sigma[:len(angle_sigma) - 3]
    new_ligand_atom = ligand_atom[:len(ligand_atom) - 3]

    print("\n      List of sorted 12 angles after 3 trans angles deleted:")

    for i in range(len(new_angle_sigma)):
        print("       Angle between atoms {0} and {1} after sorted  : {2:10.6f}"
              .format(new_ligand_atom[i][0], new_ligand_atom[i][1], angle_sigma[i]))

    computed_sigma = 0

    for i in range(len(new_angle_sigma)):
        computed_sigma = abs(90.0 - new_angle_sigma[i]) + computed_sigma

    print("\n      ====================== SUMMARY of Σ ======================\n")
    for i in range(3):
        print("      Trans angle between atoms {0} and {1} : {2:10.6f}"
              .format(ligand_atom[i + 12][0], ligand_atom[i + 12][1], angle_sigma[i + 12]))

    print("\n      Computed Σ parameter : %10.6f \n" % computed_sigma)
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
    Thus, OctaDist uses new algorithm. It firstly chooses 4 faces out of 8 faces.
    The total number of combination is 8!/4!4! = 70 sets of faces.
    All of these combination of faces would give different 70 Theta values.
    Then, determine the optimal 4 faces that give the lowest Theta values.

    Moreover, OctaDist uses the algorithm, which is explained below, to determine
    6 unique angles for a pair of opposite faces.

    1. Suppose that we have an octahedron composed of one metal center atom (m)
        and six ligand atoms of which index 1-6. Given three atom of triangular plane

                    1
                4--/\--6            Face [1, 3, 5] is reference plane.
                 \/  \/
                 /\  /\
                3--\/--5            Face [2, 4, 6] is opposite plane.
                   2

        m is absent for clarity.

    2. Orthogonally project [2, 4, 6] onto the plane that defined by [1, 3, 5]

        [2, 4, 6] -----> [2', 4', 6']
                [1, 3, 5]

        The new location of projected atoms on the given plane is [2', 4', 6']

    3. Given the line segment that pass through two points (two projected atoms)
        In this case, the start and end points are 2' and 4'

        line segment no. 1 = 2' ------ 4'
        line segment no. 2 = 4' ------ 6'
        line segment no. 3 = 2' ------ 6'

    4. Project other two atoms onto the given line. For example, the new location
        of 1 and 6' on line is 1_l and 6'_l, respective. Then create vector between old
        and new points.

    5. Compute dot product between vectors 1--->1_l and 6'--->6'_l.
        If dot product is negative, they are anti-parallel, which means that
        the start (2') and end (4') points of the given line are adjacent atoms of 1.

        Example, projection onto line no. 1

                        2'                         2'
               1 ------>|                1 ------->|
                        |                          |
               6'------>|                          |<------- 6'
                        4'                         4'

                    Parallel                Anti-Parallel
               Positive dot-product     Negative dot-product

    6. Repeat step (2) - (5) by looping over the plane and reference atoms.

    7. Calculate the 6 unique angles.

    8. Repeat step (6) - (7) for other 7 faces.

    :param cl: array - coordinate of all atoms
    :return comp_theta: list - the lowest Theta value
    :return comp_theta_list: list - list of 70 Theta values
    :return pal: list - atomic number of all 8 faces
    :return pcl: list - atomic coordinates of all 8 faces
    :return sel_p_atom: list - atom number of selected 4 reference faces
    :return sel_p_coord: list - coordinates of selected 4 reference faces
    :return sel_p_oppo_atom: list - atom number of selected 4 opposite faces
    :return sel_p_oppo_coord: list - coordinates of selected 4 opposite faces
    :return all_comp: compile all results
    """
    print("\nInfo: Find the orthogonal projection of opposite atoms on the reference plane")
    print("      The general form of the equation is Ax + By + Cz = D\n")

    pal, pcl = plane.find_8_faces(cl)
    oppo_pal, oppo_pcl = plane.find_opposite_atoms(pal, cl)

    unique_24_angles = []

    # loop over 8 faces
    for i in range(8):
        # Define list for storing the unique angle for a plane
        unique_6_angles = []
        # Find the coefficients of the equation of plane
        a, b, c, d = plane.find_eq_of_plane(pcl[i][0], pcl[i][1], pcl[i][2])
        m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

        print("      Orthogonal projection onto the plane", i + 1)
        print("      The equation of plane: {0:10.6f}x + {1:10.6f}y + {2:10.6f}z = {3:10.6f}"
              .format(a, b, c, d))

        O1 = int(oppo_pal[i][0])
        O2 = int(oppo_pal[i][1])
        O3 = int(oppo_pal[i][2])

        print("\n      Old coordinate of atom on opposite plane (before projection)")
        print("       {0}  : {1:10.6f}, {2:10.6f}, {3:10.6f}"
              .format(O1, cl[O1][0], cl[O1][1], cl[O1][2]))
        print("       {0}  : {1:10.6f}, {2:10.6f}, {3:10.6f}"
              .format(O2, cl[O2][0], cl[O2][1], cl[O2][2]))
        print("       {0}  : {1:10.6f}, {2:10.6f}, {3:10.6f}\n"
              .format(O3, cl[O3][0], cl[O3][1], cl[O3][2]))

        # Project the three opposite atoms onto the given plane
        N1 = proj.project_atom_onto_plane(cl[O1], a, b, c, d)
        N2 = proj.project_atom_onto_plane(cl[O2], a, b, c, d)
        N3 = proj.project_atom_onto_plane(cl[O3], a, b, c, d)

        print("      New coordinate of atom on reference plane (after projection)")
        print("       {0}' : {1:10.6f}, {2:10.6f}, {3:10.6f}".format(O1, N1[0], N1[1], N1[2]))
        print("       {0}' : {1:10.6f}, {2:10.6f}, {3:10.6f}".format(O2, N2[0], N2[1], N2[2]))
        print("       {0}' : {1:10.6f}, {2:10.6f}, {3:10.6f}\n".format(O3, N3[0], N3[1], N3[2]))

        # Define line and find that if the two vectors are parallel or anti parallel.
        lal = [[O1, O2, O3],  # lal = atoms on line
               [O2, O3, O1],
               [O1, O3, O2]]

        lcl = [[N1, N2, N3],  # lcl = coord of atom on line
               [N2, N3, N1],
               [N1, N3, N2]]

        print("      List of 6 unique θ angles (°)")

        # loop over three reference atoms (vertices of triangular)
        for j in range(3):
            # Find projected point of "reference atom" and "candidate atom" on the given line
            for k in range(3):
                ref_on_line = proj.project_atom_onto_line(pcl[i][j], lcl[k][0], lcl[k][1])
                can_on_line = proj.project_atom_onto_line(lcl[k][2], lcl[k][0], lcl[k][1])

                # Find vectors from reference atom and candidate atom to a line segment
                vector_ref = ref_on_line - pcl[i][j]
                vector_can = can_on_line - lcl[k][2]

                # Compute dot product to check if two vectors are anti-parallel.
                if np.dot(vector_ref, vector_can) < 0:
                    # Compute two unique angles between reference atom and neighbors.
                    angle_1 = linear.angle_between(m, pcl[i][j], lcl[k][0])
                    unique_6_angles.append(angle_1)
                    angle_2 = linear.angle_between(m, pcl[i][j], lcl[k][1])
                    unique_6_angles.append(angle_2)

                    print("       Angle between atom {0} and {1} : {2:10.6f}".format(pal[i][j], lal[k][0], angle_1))
                    print("       Angle between atom {0} and {1} : {2:10.6f}".format(pal[i][j], lal[k][1], angle_2))

        unique_24_angles.append(unique_6_angles)

        print("      ----------------------------------------\n")

    print("Info: Show list of atoms of reference and opposite faces for 8 faces\n")
    print("                Reference     Opposite")
    print("       Face       atom          atom")
    print("       ----     ---------     --------")

    for i in range(len(pal)):
        print("         {0}      {1}     {2}".format(i + 1, pal[i], oppo_pal[i]))

    unique_angle_list = []

    for i in range(len(unique_24_angles)):
        diff_angle = 0.0
        for j in range(len(unique_24_angles[i])):
            diff_angle += abs(60.0 - unique_24_angles[i][j])
        unique_angle_list.append(diff_angle)

    print("\nInfo: Show computed Θ parameter (°) of 70 sets of pair of opposite faces\n")

    LIST = unique_angle_list
    plane_set = []
    comp_theta_list = []

    # loop - choose 4 planes out of 8 planes
    for i in range(0, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                for l in range(k + 1, 8):
                    plane_set.append([i + 1, j + 1, k + 1, l + 1])
                    sum_unique_angle = (LIST[i] + LIST[j] + LIST[k] + LIST[l])
                    comp_theta_list.append(sum_unique_angle)

    # Find the minimum Theta angle and print all values
    lowest_theta = min(comp_theta_list)

    print("       Set    Atom on face         Θ (°)")
    print("       ---    ------------     ----------")

    for i in range(len(comp_theta_list)):
        if comp_theta_list[i] == lowest_theta:
            print("       {0:2d}     {1}    {2:11.6f} ***".format(i+1, plane_set[i], comp_theta_list[i]))
            sel_plane_set = plane_set[i]
        else:
            print("       {0:2d}     {1}    {2:11.6f}".format(i+1, plane_set[i], comp_theta_list[i]))

    # sel = selected
    sel_p_atom = []
    sel_p_coord = []
    sel_p_oppo_atom = []
    sel_p_oppo_coord = []

    for i in range(len(sel_plane_set)):
        p = sel_plane_set[i] - 1
        sel_p_atom.append(pal[p])
        sel_p_coord.append(pcl[p])
        sel_p_oppo_atom.append(oppo_pal[p])
        sel_p_oppo_coord.append(oppo_pcl[p])

    all_comp = (pal, pcl, sel_p_atom, sel_p_coord, sel_p_oppo_atom, sel_p_oppo_coord)

    print("\n      ====================== SUMMARY of Θ ======================\n")
    print("      The face set %s gives the lowest Θ parameter\n" % sel_plane_set)

    for i in range(4):
        print("      Face no. %s" % sel_plane_set[i])
        print("      Reference atoms: {0}        Opposite atoms: {1}".format(sel_p_atom[i], sel_p_oppo_atom[i]))

        for j in range(3):
            print("      {0:9.6f},{1:9.6f},{2:9.6f}      {3:9.6f},{4:9.6f},{5:9.6f}"
                  .format(sel_p_coord[i][j][0], sel_p_coord[i][j][1], sel_p_coord[i][j][2],
                          sel_p_oppo_coord[i][j][0], sel_p_oppo_coord[i][j][1], sel_p_oppo_coord[i][j][2]))
        print("")
    print("      Selected Θ parameter : %11.6f\n" % lowest_theta)
    print("      ==========================================================\n")

    return lowest_theta, all_comp
