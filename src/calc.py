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
import tkinter as tk
import tools
import main


def calc_delta(self, a_octa, c_octa):
    """Calculate Delta parameter
                                      2
                 1         / d_i - d \
    delta(d) =  --- * sum | -------- |
                 6        \    d    /

    where d_i is individual M-X distance and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

    :param self: master frame
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

    :param self: master frame
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
            angle = linear.angle_btw_3vec(self, c_octa[0], c_octa[i], c_octa[j])
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

    max_indi_sigma = angle_sigma[-1]

    main.print_stdout(self, "Info: Show 12 cis angles after deleting trans angles")
    main.print_stdout(self, "")
    main.print_stdout(self, "      No.    Atom pair        Angle")
    main.print_stdout(self, "      ---    ---------     -----------")
    for i in range(len(angle_sigma)):
        main.print_stdout(self, "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}"
                          .format(i + 1, la[i][0], la[i][1], angle_sigma[i]))
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

    return computed_sigma, max_indi_sigma


def calc_theta(self, a_octa, c_octa, max_indi_sigma):
    """Calculate Theta parameter

          24
    Θ = sigma < 60 - angle_i >
         i=1

    where angle_i is an unique angle between two vectors of two twisting face.
    Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

    :param self: master frame
    :param a_octa: list - atom of octahedral structure
    :param c_octa: array - coordinate of octahedral structure
    :param max_indi_sigma: maximum individual cis angle
    :return min_theta: list - the lowest Theta value
    :return all_comp: compile all results
            a_ref_f: list - atomic number of all 8 faces
            c_ref_f: list - atomic coordinates of all 8 faces
            sel_f_atom: list - atom number of selected 4 reference faces
            sel_f_coord: list - coordinates of selected 4 reference faces
            sel_oppo_f_atom: list - atom number of selected 4 opposite faces
            sel_oppo_f_coord: list - coordinates of selected 4 opposite faces
    """
    main.print_stdout(self, "Info: Calculate the Theta parameter")
    main.print_stdout(self, "")
    main.print_stdout(self, "Info: The following items will be computed")
    main.print_stdout(self, "      1. 8 faces of octahedral structure")
    main.print_stdout(self, "      2. The equation of the plane for 8 faces")
    main.print_stdout(self, "         The general form of the equation of plane is Ax + By + Cz = D")
    main.print_stdout(self, "      3. Orthogonal projection of ligand atoms onto the projection plane (face)")
    main.print_stdout(self, "      4. Individual Theta parameter for each projection plane")
    main.print_stdout(self, "      5. Minimum, Maximum, and Mean Theta values")
    main.print_stdout(self, "")

    labels = list(a_octa[1:])
    ligands = list(c_octa[1:])

    _M = c_octa[0]
    N1 = c_octa[1]
    N2 = c_octa[2]
    N3 = c_octa[3]
    N4 = c_octa[4]
    N5 = c_octa[5]
    N6 = c_octa[6]

    # vector from metal to each ligand atom
    _MN1 = N1 - _M
    _MN2 = N2 - _M
    _MN3 = N3 - _M
    _MN4 = N4 - _M
    _MN5 = N5 - _M
    _MN6 = N6 - _M

    ligands_vec = [_MN1, _MN2, _MN3, _MN4, _MN5, _MN6]

    ###########################################
    # Determine the order of atoms in complex #
    ###########################################

    def_change = 6
    for n in range(6):  # This loop is used to identify which N is in line with N1
        test = linear.angle_btw_2vec(ligands_vec[0], ligands_vec[n])
        if test > (max_indi_sigma - 1):
            def_change = n

    testMax = 0
    for n in range(6):
        test = linear.angle_btw_2vec(ligands_vec[0], ligands_vec[n])
        if test > testMax:
            testMax = test
            new_change = n

    if def_change != new_change:
        def_change = new_change

    tp = ligands[4]
    ligands[4] = ligands[def_change]
    ligands[def_change] = tp

    tp = labels[4]
    labels[4] = labels[def_change]
    labels[def_change] = tp

    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

    # updated vector from metal to each ligand atom
    _MN1 = N1 - _M
    _MN2 = N2 - _M
    _MN3 = N3 - _M
    _MN4 = N4 - _M
    _MN5 = N5 - _M
    _MN6 = N6 - _M

    ligands_vec = [_MN1, _MN2, _MN3, _MN4, _MN5, _MN6]

    for n in range(6):  # This loop is used to identify which N is in line with N2
        test = linear.angle_btw_2vec(ligands_vec[1], ligands_vec[n])
        if test > (max_indi_sigma - 1):
            def_change = n

    testMax = 0
    for n in range(6):  # This loop is used to identify which N is in line with N2
        test = linear.angle_btw_2vec(ligands_vec[1], ligands_vec[n])
        if test > testMax:
            testMax = test
            new_change = n

    if def_change != new_change:
        def_change = new_change

    tp = ligands[5]
    ligands[5] = ligands[def_change]  # swapping of the atom (n+1) just identified above with N6
    ligands[def_change] = tp

    tp = labels[5]
    labels[5] = labels[def_change]
    labels[def_change] = tp

    # the new numbering of atoms is stored into the N1 - N6 lists
    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

    # updated vector from metal to each ligand atom
    _MN1 = N1 - _M
    _MN2 = N2 - _M
    _MN3 = N3 - _M
    _MN4 = N4 - _M
    _MN5 = N5 - _M
    _MN6 = N6 - _M

    ligands_vec = [_MN1, _MN2, _MN3, _MN4, _MN5, _MN6]  # update the ligands_vec list that contains M-N vector

    for n in range(6):  # This loop is used to identify which N is in line with N3
        test = linear.angle_btw_2vec(ligands_vec[2], ligands_vec[n])
        if test > (max_indi_sigma - 1):
            def_change = n

    testMax = 0
    for n in range(6):  # This loop is used to identify which N is in line with N3
        test = linear.angle_btw_2vec(ligands_vec[2], ligands_vec[n])
        if test > testMax:
            testMax = test
            new_change = n

    if def_change != new_change:
        def_change = new_change

    tp = ligands[3]
    ligands[3] = ligands[def_change]  # swapping of the atom (n+1) just identified above with N4
    ligands[def_change] = tp

    tp = labels[3]
    labels[3] = labels[def_change]
    labels[def_change] = tp

    # the new numbering of atoms is stored into the N1 - N6 lists.
    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

    #####################################################
    # Calculate the Theta parameter ans its derivatives #
    #####################################################

    ThetaValues = []  # list gathering the 6 theta angles
    # loop over 8 faces
    for proj in range(8):
        # Find the equation of the plane
        a, b, c, d = plane.find_eq_of_plane(N1, N2, N3)

        # Calculation of projection of M, N4, N5 and N6 onto the plane defined by N1, N2, N3
        _MP = projection.project_atom_onto_plane(_M, a, b, c, d)
        N4P = projection.project_atom_onto_plane(N4, a, b, c, d)
        N5P = projection.project_atom_onto_plane(N5, a, b, c, d)
        N6P = projection.project_atom_onto_plane(N6, a, b, c, d)

        # calculate vector from projected metal to projected ligand
        VTh1 = N1 - _MP
        VTh2 = N2 - _MP
        VTh3 = N3 - _MP
        VTh4 = N4P - _MP
        VTh5 = N5P - _MP
        VTh6 = N6P - _MP

        # calculation of 6 theta angles for 1 projection
        a12 = linear.angle_btw_2vec(VTh1, VTh2)
        a13 = linear.angle_btw_2vec(VTh1, VTh3)
        if a12 < a13:
            CrossDirect = np.cross(VTh1, VTh2)
        else:
            CrossDirect = np.cross(VTh3, VTh1)

        theta1 = linear.angles_sign(VTh1, VTh4, CrossDirect)
        theta2 = linear.angles_sign(VTh4, VTh2, CrossDirect)
        theta3 = linear.angles_sign(VTh2, VTh5, CrossDirect)
        theta4 = linear.angles_sign(VTh5, VTh3, CrossDirect)
        theta5 = linear.angles_sign(VTh3, VTh6, CrossDirect)
        theta6 = linear.angles_sign(VTh6, VTh1, CrossDirect)

        # sum individual Theta for 1 projection plane
        sumTheta = abs(theta1 - 60) + abs(theta2 - 60) + abs(theta3 - 60) + \
                   abs(theta4 - 60) + abs(theta5 - 60) + abs(theta6 - 60)

        # update Theta into ThetaValues list
        ThetaValues.append(sumTheta)

        tp = N2
        N2 = N4
        N4 = N6
        N6 = N3
        N3 = tp

        tp = labels[1]
        labels[1] = labels[3]
        labels[3] = labels[5]
        labels[5] = labels[2]
        labels[2] = tp

        # if the variable proj = 3, Octahedral face permutation face N1N2N3 switches to N1N4N2
        # then to N1N6N4 then N1N3N6 then back to N1N2N3
        if proj == 3:
            tp = N1
            N1 = N5
            N5 = tp
            tp = N2
            N2 = N6
            N6 = tp
            tp = N3
            N3 = N4
            N4 = tp
            tp = labels[0]
            labels[0] = labels[4]
            labels[4] = tp
            tp = labels[1]
            labels[1] = labels[5]
            labels[5] = tp
            tp = labels[2]
            labels[2] = labels[3]
            labels[3] = tp

        # End of the loop that calculate the 8 projections.

    ##################################
    # Summary of computed parameters #
    ##################################

    main.print_stdout(self, "Info: Show unique Θ parameter for 8 projection planes")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Plane     Θ parameter")
    main.print_stdout(self, "      -----     -----------")
    for i in range(8):
        main.print_stdout(self, "        {0:d}       {1:11.6f}".format(i + 1, ThetaValues[i]))
    main.print_stdout(self, "")

    mean_theta = 0
    for n in range(8):
        mean_theta = mean_theta + ThetaValues[n]

    mean_theta = mean_theta / 2

    # this list contains the sorted values of Theta from min to max
    sorted_Theta = sorted(ThetaValues)

    min_theta = 0
    for n in range(4):
        min_theta = min_theta + sorted_Theta[n]

    max_theta = 0
    for n in range(4, 8):
        max_theta = max_theta + sorted_Theta[n]

    NewMinTheta = []
    NewMaxTheta = []
    for n in range(4):
        if ThetaValues[n] < ThetaValues[n + 4]:
            NewMinTheta.append(ThetaValues[n])
            NewMaxTheta.append(ThetaValues[n + 4])
        else:
            NewMaxTheta.append(ThetaValues[n])
            NewMinTheta.append(ThetaValues[n + 4])

    min_theta_new = 0
    max_theta_new = 0
    for n in range(4):
        min_theta_new = min_theta_new + NewMinTheta[n]
        max_theta_new = max_theta_new + NewMaxTheta[n]

    main.print_stdout(self, "      ====================== SUMMARY of Θ ======================")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Minimum Θ parameter : {0:11.6f} degree ***".format(min_theta))
    main.print_stdout(self, "      Maximum Θ parameter : {0:11.6f} degree".format(max_theta))
    main.print_stdout(self, "         Mean Θ parameter : {0:11.6f} degree".format(mean_theta))
    main.print_stdout(self, "")
    main.print_stdout(self, "      ==========================================================")
    main.print_stdout(self, "")

    #############################################################
    # Find selected reference and opposite faces for displaying #
    #############################################################

    # # Find 8 reference faces and 8 opposite faces
    # a_ref_f, c_ref_f, a_oppo_f, c_oppo_f = plane.find_8_faces(self, c_octa)
    #
    # sel_face_set = 0
    # for i in range(8):
    #     if ThetaValues[i] == min_theta:
    #         sel_face_set = plane_set[i]
    #
    # sel_f_atom = []
    # sel_f_coord = []
    # sel_oppo_f_atom = []
    # sel_oppo_f_coord = []
    #
    # # Get the data of optimal faces from selected face set
    # for i in range(len(sel_face_set)):
    #     p = sel_face_set[i]
    #     sel_f_atom.append(a_ref_f[p - 1])
    #     sel_f_coord.append(c_ref_f[p - 1])
    #     sel_oppo_f_atom.append(a_oppo_f[p - 1])
    #     sel_oppo_f_coord.append(c_oppo_f[p - 1])
    #
    # all_comp = (a_ref_f, c_ref_f, sel_f_atom, sel_f_coord, sel_oppo_f_atom, sel_oppo_f_coord)

    all_comp = ()

    return mean_theta, min_theta, max_theta, min_theta_new, max_theta_new, all_comp


def calc_all(self, file_list, atom_coord_octa):
    """Calculate Delta, Sigma, and Theta.

    :param self: master frame
    :param file_list:
    :param atom_coord_octa:
    :return:
    """
    main.print_stdout(self, "Info: Calculate the Δ, Σ, and Θ parameters")
    main.print_stdout(self, "")

    all_sigma = []
    all_theta = []
    comp_result = []

    for i in range(len(atom_coord_octa)):
        main.print_stdout(self, "      *********************** Complex {0} ***********************".format(i + 1))
        main.print_stdout(self, "")

        # Calculate distortion parameters
        atom_octa, coord_octa = atom_coord_octa[i]
        delta = calc_delta(self, atom_octa, coord_octa)
        sigma, max_indi_sigma = calc_sigma(self, atom_octa, coord_octa)
        mean_theta, min_theta, max_theta, min_theta_new, max_theta_new, all_comp \
            = calc_theta(self, atom_octa, coord_octa, max_indi_sigma)

        # Collect results
        all_sigma.append(sigma)
        all_theta.append(min_theta)
        comp_result.append([delta, sigma, min_theta, max_theta, mean_theta])

    if len(file_list) == 1:
        # pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl = all_comp
        self.box_delta.insert(tk.INSERT, "{0:3.6f}".format(delta))
        self.box_sigma.insert(tk.INSERT, "{0:3.6f}".format(sigma))
        self.box_theta_min.insert(tk.INSERT, "{0:3.6f}".format(min_theta))
        self.box_theta_max.insert(tk.INSERT, "{0:3.6f}".format(max_theta))
        self.box_theta_mean.insert(tk.INSERT, "{0:3.6f}".format(mean_theta))

    elif len(file_list) > 1:
        tools.multi_results(self, comp_result)

    main.print_stdout(self, "Info: Show computed octahedral distortion parameters of all files")
    main.print_stdout(self, "")
    main.print_stdout(self, "      ==================== Overall Summary ====================")
    main.print_stdout(self, "")
    for i in range(len(comp_result)):
        main.print_stdout(self, "      Complex {0:2d} : {1}".format(i + 1, file_list[i].split('/')[-1]))
    main.print_stdout(self, "")
    main.print_stdout(self, "      Complex          Δ           Σ (°)         Θ (°)")
    main.print_stdout(self, "      -------      --------    ----------    ----------")
    for i in range(len(comp_result)):
        main.print_stdout(self, "      {0:2d}      {1:10.6f}    {2:10.6f}    {3:10.6f}"
                          .format(i + 1, comp_result[i][0], comp_result[i][1], comp_result[i][2]))
    main.print_stdout(self, "")
    main.print_stdout(self, "      =========================================================")
    main.print_stdout(self, "")

    return all_sigma, all_theta, comp_result, all_comp
