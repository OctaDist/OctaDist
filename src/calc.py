"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import coord
import linear
import plane
import proj


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
    print("Command: Calculate 6 distances between metal center (M) and ligand atoms (in Angstrom)")

    # Calculate and print individual distance
    distance_list = []

    print("         Show distance list")
    for i in range(1, 7):
        distance_indi = linear.distance_between(x[0], x[i])
        print("         Distance between M and ligand atom {0} : {1:10.6f}"
              .format(i, distance_indi))
        distance_list.append(distance_indi)
    print("")

    computed_distance_avg = linear.distance_avg(x)
    computed_delta = 0

    # Calculate Delta parameter
    for i in range(6):
        diff_dist = (distance_list[i] - computed_distance_avg) / computed_distance_avg
        computed_delta = ((diff_dist*diff_dist) / 6) + computed_delta

    print("         ====================== SUMMARY of Δ ======================")
    print("")
    print("         Average distance     : %10.6f Angstrom" % computed_distance_avg)
    print("         Computed Δ parameter : %10.6f" % computed_delta)
    print("")
    print("         ==========================================================")
    print("")

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
    print("         Metal center atom is taken as vertex.")
    print("         Three trans angles (the three biggest angles) are deleted.")
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
              "before sorted: {0:10.6f}".format(angle_sigma_list[i]))
    print("")

    # Sort the angle from the lowest to the highest
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

    # Remove last three angles (last three rows)
    new_angle_sigma_list = angle_sigma_list[:len(angle_sigma_list) - 3]
    new_ligand_atom_list = ligand_atom_list[:len(ligand_atom_list) - 3]

    print("         List of the sorted angles after three trans angles deleted:")

    for i in range(len(new_angle_sigma_list)):
        print("          Angle between atom", new_ligand_atom_list[i][0], "and atom", new_ligand_atom_list[i][1],
              "after sorted : {0:10.6f}".format(angle_sigma_list[i]))
    print("")

    computed_sigma = 0

    # Calculate Sigma parameter
    for i in range(len(new_angle_sigma_list)):
        computed_sigma = abs(90.0 - new_angle_sigma_list[i]) + computed_sigma

    print("         ====================== SUMMARY of Σ ======================")
    print("")
    for i in range(3):
        print("         Trans angle no.{0} is atom {1} <- Metal -> atom {2} : {3:10.6f}"
              .format(i+1, ligand_atom_list[i+12][0], ligand_atom_list[i+12][1], angle_sigma_list[i+12]))
    print("")
    print("         Total number of angles before three trans angles deleted:", len(angle_sigma_list))
    print("         Total number of angles after three trans angles deleted :", len(new_angle_sigma_list))
    print("")
    print("         Computed Σ parameter : %10.6f" % computed_sigma)
    print("")
    print("         ==========================================================")
    print("")

    return computed_sigma, new_angle_sigma_list


def calc_theta(z):
    """Calculate octahedral distortion parameter, Θ
    Octahedron has 4 faces, 6 angles each, thus the total number of theta angle is 24 angles.

      24
    Θ = sigma < 60 - angle_i >
     i=1

    where angle_i is angle between two plane defined by vector of metal center and ligand atoms.

    Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.


    This method firstly finds the 8 faces of octahedron and choose 4 faces out of 8 faces
    The total number of combination is 8!/4!4! = 70. Then we determine the lowest Theta values.

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

        line segment no. 1 = 2' <------> 4'
        line segment no. 2 = 4' <------> 6'
        line segment no. 3 = 2' <------> 6'

    4. Project another atoms onto the given line and check if two vectors are anti-parallel

        Example, line1

                        2'                         2'
               1 ------>|                1 ------->|
                        |                          |
               6'------>|                          |<------- 6'
                        4'                         4'

                    Parallel                Anti-Parallel
               Positive dot-product     Negative dot-product

        Compute dot product between vectors 1 and 6'. If they are anti-parallel,
        this means that the start (2') and end (4') points of line segment are adjacent atoms of 1.

    5. Repeat step (2) - (4) by looping the plane and reference atoms.

    6. Calculate the 6 unique angles. Then repeat step step (5) for other 7 faces.

    :param z: array - coordinate of all atoms
    :return:
    """
    print("Command: Calculate the following items")
    print("         - The equation of plane that given by selected three ligand atoms")
    print("           The general form of the equation is Ax + By + Cz = D")
    print("         - Orthogonal projection of all opposite atoms and metal center onto the reference plane")
    print("         - 6 unique angles (θ) between vectors of reference atom and projected atom")
    print("           for 8 planes (in degree)")
    print("")

    v = np.array(z)

    # Find suitable plane and atom on opposite plane
    pal, pcl = plane.search_8_planes(v)
    oppo_pal, oppo_pcl = plane.find_opposite_atoms(pal, v)

    print("Command: Find the orthogonal projection of opposite atoms on the given reference plane")
    computed_unique_angle_list = []

    # loop plane
    for i in range(8):
        # Define list for storing the unique angle for a plane
        computed_unique_angle = []
        # Find the coefficients of the equation of plane
        a, b, c, d = plane.eq_of_plane(pcl[i][0], pcl[i][1], pcl[i][2])
        m = proj.project_atom_onto_plane(v[0], a, b, c, d)

        print("         Orthogonal projection onto the plane", i + 1)
        print("         The equation of plane: {0:10.6f}x + {1:10.6f}y + {2:10.6f}z = {3:10.6f}"
              .format(a, b, c, d))
        print("")

        o1 = int(oppo_pal[i][0])
        o2 = int(oppo_pal[i][1])
        o3 = int(oppo_pal[i][2])

        print("         Old coordinate of atom on opposite plane (before projection)")
        print("          {0}  --> ({1:10.6f}, {2:10.6f}, {3:10.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
        print("          {0}  --> ({1:10.6f}, {2:10.6f}, {3:10.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
        print("          {0}  --> ({1:10.6f}, {2:10.6f}, {3:10.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
        print("")

        # Project the opposite atom onto the given plane
        n1 = proj.project_atom_onto_plane(v[o1], a, b, c, d)
        n2 = proj.project_atom_onto_plane(v[o2], a, b, c, d)
        n3 = proj.project_atom_onto_plane(v[o3], a, b, c, d)

        print("         New coordinate of atom on reference plane (after projection)")
        print("          {0}' --> ({1:10.6f}, {2:10.6f}, {3:10.6f})".format(o1, n1[0], n1[1], n1[2]))
        print("          {0}' --> ({1:10.6f}, {2:10.6f}, {3:10.6f})".format(o2, n2[0], n2[1], n2[2]))
        print("          {0}' --> ({1:10.6f}, {2:10.6f}, {3:10.6f})".format(o3, n3[0], n3[1], n3[2]))
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
                # Find vectors from reference atom and candidate atom to a line segment
                vector_ref = ref_on_line - pcl[i][j]
                vector_can = can_on_line - lcl[k][2]
                # Compute dot product to check if two vectors are anti-parallel, if so,
                # then compute two unique angles between reference atom and its neighbor.
                if np.dot(vector_ref, vector_can) < 0:
                    # angle 1
                    angle_1 = linear.angle_between(m, pcl[i][j], lcl[k][0])
                    computed_unique_angle.append(angle_1)
                    # angle 2
                    angle_2 = linear.angle_between(m, pcl[i][j], lcl[k][1])
                    computed_unique_angle.append(angle_2)

                    print("          Angle between atom {0} and {1}: {2:10.6f}"
                          .format(pal[i][j], lal[k][0], angle_1))
                    print("          Angle between atom {0} and {1}: {2:10.6f}"
                          .format(pal[i][j], lal[k][1], angle_2))

        computed_unique_angle_list.append(computed_unique_angle)

        print("         ----------------------------------------")
        print("")

    print("Command: Show list of atoms of reference and opposite faces for 8 faces")
    print("")
    print("                  Reference atom    Opposite atom")
    for i in range(len(pal)):
        print("         Face {0} : {1}         {2}".format(i+1, pal[i], oppo_pal[i]))
    print("")

    unique_angle_list = []

    for i in range(len(computed_unique_angle_list)):
        diff_angle = 0.0
        for j in range(len(computed_unique_angle_list[i])):
            diff_angle += abs(60.0 - computed_unique_angle_list[i][j])
        unique_angle_list.append(diff_angle)

    # Print 70 Theta values for different plane sets and add to computed_theta_list
    print("Command: Show computed Θ parameters (in degree) for 70 sets of pair of opposite faces")

    LIST = unique_angle_list
    plane_set = []
    computed_theta_list = []

    # loop - choose 4 planes out of 8 planes
    for i in range(0, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                for l in range(k + 1, 8):
                    plane_set.append([i + 1, j + 1, k + 1, l + 1])
                    sum_unique_angle = LIST[i] + LIST[j] + LIST[k] + LIST[l]
                    computed_theta_list.append(sum_unique_angle)

    # Find the minimum Theta angle
    computed_theta = min(computed_theta_list)

    # Print the Theta value for all 70 combinations
    for i in range(len(computed_theta_list)):
        if computed_theta_list[i] == computed_theta:
            print("         Θ of face set {0} : {1:11.6f} ***"
                  .format(plane_set[i], computed_theta_list[i]))
            selected_plane_set = plane_set[i]
        else:
            print("         Θ of face set {0} : {1:11.6f}"
                  .format(plane_set[i], computed_theta_list[i]))
    print("")

    sel_p_atom, sel_p_coord, sel_p_oppo_atom, sel_p_oppo_coord = [], [], [], []

    for i in range(len(selected_plane_set)):
        p = selected_plane_set[i]
        sel_p_atom.append(pal[p - 1])
        sel_p_coord.append(pcl[p - 1])
        sel_p_oppo_atom.append(oppo_pal[p - 1])
        sel_p_oppo_coord.append(oppo_pcl[p - 1])

    # Put all selected array into one list for returning
    # pal & pcl   : atom number and coordinates of all 8 faces
    # sel_p_atom, sel_p_coord   : atom number and coordinates of selected 4 reference faces
    # sel_p_oppo_atom, sel_p_oppo_coord   : atom number and coordinates of selected 4 opposite faces

    selected_plane_list = (pal, pcl, sel_p_atom, sel_p_coord, sel_p_oppo_atom, sel_p_oppo_coord)

    print("         ====================== SUMMARY of Θ ======================")
    print("")
    print("         The face set {0} gives the lowest Θ value : {1:11.6f} degree"
          .format(selected_plane_set, computed_theta))
    print("")
    for i in range(4):
        print("         Face no.", selected_plane_set[i])
        print("          Reference atom: {0}".format(sel_p_atom[i]))
        for j in range(3):
            print("                        : ({0:10.6f}, {1:10.6f}, {2:10.6f})"
                  .format(sel_p_coord[i][j][0], sel_p_coord[i][j][1], sel_p_coord[i][j][2]))
        print("          Opposite atom : {0}".format(sel_p_oppo_atom[i]))
        for j in range(3):
            print("                        : ({0:10.6f}, {1:10.6f}, {2:10.6f})"
                  .format(sel_p_oppo_coord[i][j][0], sel_p_oppo_coord[i][j][1], sel_p_oppo_coord[i][j][2]))
        print("")
    print("         ==========================================================")
    print("")

    return computed_theta, computed_theta_list, selected_plane_list


def calc_mult(f, l):
    """Calculate octahedral distortion parameters for all selected input files
    :param f, l: array - list of file name and list of atom and coordinates
    :return computed_results: array - results for all complexes
    """
    print("Command: Calculate octahedral distortion parameters")
    print("")

    list_file = f
    atom_coord_list = l
    computed_results = []

    for i in range(len(list_file)):
        print("         ====================== Complex %s ======================" % int(i+1))
        print("")
        print("Command: Get coordinate and compute Δ, Σ, and Θ parameters")

        # Check file type and get coordinate
        print("")
        print("Command: Determine file type")
        full_atom_list, full_coord_list = atom_coord_list[i]

        if len(full_coord_list) != 0:
            atom_list, coord_list = coord.cut_coord(full_atom_list, full_coord_list)
        else:
            return 1

        if np.any(coord_list) != 0:
            print("Command: Calculate octahedral distortion parameters")
            computed_delta, distance_list = calc_delta(coord_list)
            computed_sigma, new_angle_sigma_list = calc_sigma(coord_list)
            computed_theta, computed_theta_list, selected_plane_lists = calc_theta(coord_list)

            print("Command: Show computed octahedral distortion parameters")
            print("")
            print("         Δ = {0:10.6f}".format(computed_delta))
            print("         Σ = {0:10.6f} degree".format(computed_sigma))
            print("         Θ = {0:10.6f} degree".format(computed_theta))
            print("")

        computed_results.append([computed_delta, computed_sigma, computed_theta])

    print("         ==========================================================")
    print("")
    print("Command: Show file name for all complexes")

    for i in range(len(computed_results)):
        print("         Complex {0:2d} : {1}".format(i+1, list_file[i].split('/')[-1]))
    print("")

    print("Command: Show computed octahedral distortion parameters for all complexes")
    print("")
    print("                            Δ             Σ             Θ")
    print("                         --------     ---------     ---------")
    for i in range(len(computed_results)):

        print("         Complex {0:2d} : {1:10.6f}   {2:10.6f}   {3:10.6f}"
              .format(i+1, computed_results[i][0], computed_results[i][1], computed_results[i][2]))
    print("")

    show_results_mult(computed_results)

    return computed_results


def show_results_mult(computed_results):
    """

    :param computed_results:
    :return: show the results in new text box
    """
    mult = tk.Tk()
    mult.option_add("*Font", "Arial 10")
    mult.geometry("380x530")
    mult.title("Results")

    lbl = tk.Label(mult, text="Computed octahedral distortion parameters for all complexes")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    Box = tkscrolled.ScrolledText(mult, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=1, pady="5", padx="5")

    texts = "                             Δ               Σ               Θ\n" \
            "                        --------------------------------------------"
    Box.insert(tk.INSERT, texts)

    for i in range(len(computed_results)):
        texts = "Complex {0} : {1:10.6f}  {2:10.6f}  {3:10.6f}" \
        .format(i+1, computed_results[i][0], computed_results[i][1], computed_results[i][2])
        Box.insert(tk.END, "\n" + texts)

    mult.mainloop()

