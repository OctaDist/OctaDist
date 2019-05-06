# OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tkinter as tk

import numpy as np

from octadist_gui.src import echo_logs, echo_outs, linear, popup, projection, tools


def calc_d_bond(self, a_octa, c_octa):
    """Calculate metal-ligand bond distance and return value in Angstrom

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return bond_dist: individual metal-ligand bond distance
    :rtype bond_dist: list
    """
    echo_logs(self, "Info: Calculate distance between metal center (M) and ligand atoms")
    echo_logs(self, "Info: Show 6 unique bond distances (Angstrom)")
    echo_logs(self, "")
    echo_logs(self, "      No.     Bond       Distance")
    echo_logs(self, "      ---    -------     --------")

    bond_dist = []
    for i in range(1, 7):
        distance = linear.distance_bwn_points(c_octa[0], c_octa[i])
        echo_logs(self, "      {0:>2}     {1:>2} - {2:>2}   {3:10.6f}".format(i, a_octa[0], a_octa[i], distance))
        bond_dist.append(distance)
    echo_logs(self, "")

    return bond_dist


def calc_d_mean(self, a_octa, c_octa):
    """Calculate mean distance parameter and return value in Angstrom

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return d_mean: mean metal-ligand bond distance
    :rtype d_mean: float
    """
    echo_logs(self, "Info: Calculate D_mean parameter")
    echo_logs(self, "")

    # calculate bond distances
    bond_dist = calc_d_bond(self, a_octa, c_octa)

    i = 0
    sum_distance = 0
    while i < 6:
        sum_distance += bond_dist[i]
        i += 1

    d_mean = sum_distance / 6

    echo_logs(self, "      =================== SUMMARY of D<mean> ===================")
    echo_logs(self, "")
    echo_logs(self, "      D<mean> : {0:10.6f}".format(d_mean))
    echo_logs(self, "")
    echo_logs(self, "      ==========================================================")
    echo_logs(self, "")

    return d_mean


def calc_zeta(self, a_octa, c_octa):
    """Calculate Zeta parameter and return value in Angstrom

         6
    ζ = sum(|dist_i - d_mean|)
        i=1

    Ref: Phys. Rev. B 85, 064114

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return zeta: Zeta parameter
    :rtype zeta: float
    """
    echo_logs(self, "Info: Calculate ζ parameter")
    echo_logs(self, "      This parameter is deviation from the average bond length")
    echo_logs(self, "")

    # calculate bond distances and mean distance
    bond_dist = calc_d_bond(self, a_octa, c_octa)
    d_mean = calc_d_mean(self, a_octa, c_octa)

    echo_logs(self, "Info: Show diff distance (Angstrom)")
    echo_logs(self, "")

    diff_dist = []
    for i in range(6):
        diff_dist.append(abs(bond_dist[i] - d_mean))
        echo_logs(self, "      Bond {0} : {1:10.6f}".format(i, diff_dist[i]))

    zeta = sum(diff_dist[i] for i in range(6))

    echo_logs(self, "")
    echo_logs(self, "      ====================== SUMMARY of ζ ======================")
    echo_logs(self, "")
    echo_logs(self, "      Computed ζ parameter : {0:10.6f}".format(zeta))
    echo_logs(self, "")
    echo_logs(self, "      ==========================================================")
    echo_logs(self, "")

    return zeta


def calc_delta(self, a_octa, c_octa):
    """Calculate Delta parameter (Tilting distortion parameter)

          1
    Δ =  ---*sum((d_i - d)/d)^2
          6

    where d_i is individual M-X distance and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return delta: Delta parameter
    :rtype delta: float
    """
    echo_logs(self, "Info: Calculate Δ parameter")
    echo_logs(self, "")

    # calculate bond distances and mean distance
    bond_dist = calc_d_bond(self, a_octa, c_octa)
    d_mean = calc_d_mean(self, a_octa, c_octa)

    delta = 0
    for i in range(6):
        diff_dist = (bond_dist[i] - d_mean) / d_mean
        delta += (diff_dist * diff_dist) / 6

    echo_logs(self, "      ====================== SUMMARY of Δ ======================")
    echo_logs(self, "")
    echo_logs(self, "      Computed Δ parameter : {0:10.6f}".format(delta))
    echo_logs(self, "")
    echo_logs(self, "      ==========================================================")
    echo_logs(self, "")

    return delta


def calc_bond_angle(self, a_octa, c_octa):
    """Calculate 12 cis and 3 trans unique angles in octahedral structure

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return cis_angle: list of 12 cis angles
    :rtype cis_angle: list
    :return trans_angle: list of 3 trans angles
    :rtype trans_angle: list
    """
    echo_logs(self, "Info: Calculate angle between ligand atoms (including cis and trans angles)")
    echo_logs(self, "Info: Show 15 unique bond angles (°) before sorting")
    echo_logs(self, "")
    echo_logs(self, "      No.    Atom pair        Angle")
    echo_logs(self, "      ---    ---------     -----------")

    la = []
    all_angle = []
    k = 1
    for i in range(1, 7):
        for j in range(i + 1, 7):
            angle = linear.angle_btw_3points(self, c_octa[0], c_octa[i], c_octa[j])
            echo_logs(self, "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}".format(k, a_octa[i], a_octa[j], angle))
            la.append([a_octa[i], a_octa[j]])
            all_angle.append(angle)
            k += 1
    echo_logs(self, "")

    # Sort the angle from the lowest to the highest
    all_angle.sort()

    # Get cis angles
    cis_angle = [all_angle[i] for i in range(12)]

    # Get trans angles
    trans_angle = [all_angle[i] for i in range(12, 15)]

    # Show cis angles
    echo_logs(self, "Info: Show 12 cis angles")
    echo_logs(self, "")
    echo_logs(self, "      No.    Atom pair        Angle")
    echo_logs(self, "      ---    ---------     -----------")
    for i in range(12):
        echo_logs(self, "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}".format(i, la[i][0], la[i][1], cis_angle[i]))
    echo_logs(self, "")

    # Show trans angles
    echo_logs(self, "Info: Show 3 trans angles")
    echo_logs(self, "")
    echo_logs(self, "      No.    Atom pair        Angle")
    echo_logs(self, "      ---    ---------     -----------")
    for i in range(3):
        echo_logs(self,
                  "      {0:>2}     {1:>2} and {2:>2}      {3:10.6f}".format(-i, la[-i][0], la[-i][1], trans_angle[i]))
    echo_logs(self, "")

    return cis_angle, trans_angle


def calc_sigma(self, a_octa, c_octa):
    """Calculate Sigma parameter and return value in degree

          12
    Σ = sigma < 90 - angle_i >
         i=1

    where angle_i in an unique cis angle
    Ref: J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return sigma: Sigma parameter
    :return angle_sigma: list of 12 unique cis angles
    :rtype sigma: float
    :rtype angle_sigma: list
    """
    echo_logs(self, "Info: Calculate Σ parameter")
    echo_logs(self, "")

    cis_angle, _ = calc_bond_angle(self, a_octa, c_octa)

    sigma = 0
    for i in range(len(cis_angle)):
        sigma = abs(90.0 - cis_angle[i]) + sigma

    echo_logs(self, "      ====================== SUMMARY of Σ ======================")
    echo_logs(self, "")
    echo_logs(self, "      Computed Σ parameter : {0:10.6f} degree".format(sigma))
    echo_logs(self, "")
    echo_logs(self, "      ==========================================================")
    echo_logs(self, "")

    return sigma


def calc_theta(self, a_octa, c_octa):
    """Calculate Theta parameter and value in degree

          24
    Θ = sigma < 60 - angle_i >
         i=1

    where angle_i is an unique angle between two vectors of two twisting face.
    Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

    :param self: master frame
    :param a_octa: atomic labels of octahedral structure
    :param c_octa: atomic coordinates of octahedral structure
    :type a_octa: list
    :type c_octa: list, array, tuple
    :return theta_mean: mean Theta value
    :rtype theta_mean: float
    """
    echo_logs(self, "Info: Calculate Θ parameter")
    echo_logs(self, "")
    echo_logs(self, "Info: The following items will be computed")
    echo_logs(self, "      1. 8 faces of octahedral structure")
    echo_logs(self, "      2. The equation of the plane for 8 faces")
    echo_logs(self, "         The general form of the equation of plane is Ax + By + Cz = D")
    echo_logs(self, "      3. Orthogonal projection of ligand atoms onto the projection plane (face)")
    echo_logs(self, "      4. Individual Theta parameter for each projection plane")
    echo_logs(self, "      5. Minimum, Maximum, and Mean Theta values")
    echo_logs(self, "")

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

    echo_logs(self, "Info: Show vector from metal center to each ligand atom")
    echo_logs(self, "")
    for i in range(6):
        echo_logs(self, "      M --> N{0} : ({1:8.5f}, {2:8.5f}, {3:8.5f})"
                  .format(i + 1, ligands_vec[i][0], ligands_vec[i][1], ligands_vec[i][2]))
    echo_logs(self, "")

    ###########################################
    # Determine the order of atoms in complex #
    ###########################################

    _, trans_angle = calc_bond_angle(self, a_octa, c_octa)

    max_angle = trans_angle[0]

    def_change = 6
    for n in range(6):  # This loop is used to identify which N is in line with N1
        test = linear.angle_btw_2vec(ligands_vec[0], ligands_vec[n])
        if test > (max_angle - 1):
            def_change = n

    test_max = 0
    new_change = 0
    for n in range(6):
        test = linear.angle_btw_2vec(ligands_vec[0], ligands_vec[n])
        if test > test_max:
            test_max = test
            new_change = n

    # geometry var is used to identify the type of octahedral structure
    geometry = False
    if def_change != new_change:
        geometry = True
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

    # update the ligands_vec list that contains M-N vector
    ligands_vec = [_MN1, _MN2, _MN3, _MN4, _MN5, _MN6]

    for n in range(6):  # This loop is used to identify which N is in line with N2
        test = linear.angle_btw_2vec(ligands_vec[1], ligands_vec[n])
        if test > (max_angle - 1):
            def_change = n

    test_max = 0
    for n in range(6):  # This loop is used to identify which N is in line with N2
        test = linear.angle_btw_2vec(ligands_vec[1], ligands_vec[n])
        if test > test_max:
            test_max = test
            new_change = n

    if def_change != new_change:
        geometry = True
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

    ligands_vec = [_MN1, _MN2, _MN3, _MN4, _MN5, _MN6]

    for n in range(6):  # This loop is used to identify which N is in line with N3
        test = linear.angle_btw_2vec(ligands_vec[2], ligands_vec[n])
        if test > (max_angle - 1):
            def_change = n

    test_max = 0
    for n in range(6):  # This loop is used to identify which N is in line with N3
        test = linear.angle_btw_2vec(ligands_vec[2], ligands_vec[n])
        if test > test_max:
            test_max = test
            new_change = n

    if def_change != new_change:
        geometry = True
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

    updated_lig = [N1, N2, N3, N4, N5, N6]

    echo_logs(self, "Info: Show the updated numbering atoms")
    echo_logs(self, "")
    # Front face: N1, N2, N3
    for i in range(3):
        echo_logs(self, "      N{0} : ({1:8.5f}, {2:8.5f}, {3:8.5f})"
                  .format(i + 1, updated_lig[i][0], updated_lig[i][1], updated_lig[i][2]))
    echo_logs(self, "      ------------------------------------------")
    # Back face: N4, N5, N6
    for i in range(3, 6):
        echo_logs(self, "      N{0} : ({1:8.5f}, {2:8.5f}, {3:8.5f})"
                  .format(i + 1, updated_lig[i][0], updated_lig[i][1], updated_lig[i][2]))
    echo_logs(self, "")

    #####################################################
    # Calculate the Theta parameter ans its derivatives #
    #####################################################

    eqOfPlane = []
    indiTheta = []
    allTheta = []  # list gathering the 6 theta angles

    # loop over 8 faces
    for proj in range(8):
        # Find the equation of the plane
        a, b, c, d = linear.find_eq_of_plane(N1, N2, N3)
        eqOfPlane.append([a, b, c, d])

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
            crossDirect = np.cross(VTh1, VTh2)
        else:
            crossDirect = np.cross(VTh3, VTh1)

        theta1 = linear.angles_sign(VTh1, VTh4, crossDirect)
        theta2 = linear.angles_sign(VTh4, VTh2, crossDirect)
        theta3 = linear.angles_sign(VTh2, VTh5, crossDirect)
        theta4 = linear.angles_sign(VTh5, VTh3, crossDirect)
        theta5 = linear.angles_sign(VTh3, VTh6, crossDirect)
        theta6 = linear.angles_sign(VTh6, VTh1, crossDirect)

        indiTheta.append([theta1, theta2, theta3, theta4, theta5, theta6])

        collectTheta = [theta1, theta2, theta3, theta4, theta5, theta6]

        # sum individual Theta for 1 projection plane
        sumTheta = sum(abs(collectTheta[i] - 60) for i in range(6))

        # update Theta into allTheta list
        allTheta.append(sumTheta)

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

    echo_logs(self, "Info: Show the equation of the plane")
    echo_logs(self, "")
    for i in range(8):
        echo_logs(self, "      Plane {0}: {1:8.5f}x {2:+8.5f}y {3:+8.5f}z = {4:8.5f}"
                  .format(i + 1, eqOfPlane[i][0], eqOfPlane[i][1], eqOfPlane[i][2], eqOfPlane[i][3]))
    echo_logs(self, "")
    echo_logs(self, "Info: Show 6 individual Theta of 8 projection planes")
    echo_logs(self, "")
    for i in range(8):
        echo_logs(self, "      Plane {0}: {1:5.2f}, {2:5.2f}, {3:5.2f}, {4:5.2f}, {5:5.2f}, {6:5.2f}"
                  .format(i + 1, indiTheta[i][0], indiTheta[i][1], indiTheta[i][2],
                          indiTheta[i][3], indiTheta[i][4], indiTheta[i][5]))
    echo_logs(self, "")

    ##################################
    # Summary of computed parameters #
    ##################################

    echo_logs(self, "Info: Show unique Θ parameter for 8 projection planes")
    echo_logs(self, "")
    echo_logs(self, "      Plane     Θ parameter")
    echo_logs(self, "      -----     -----------")
    for i in range(8):
        echo_logs(self, "        {0:d}       {1:11.6f}".format(i + 1, allTheta[i]))
    echo_logs(self, "")

    theta_mean = 0
    for n in range(8):
        theta_mean += allTheta[n]

    theta_mean = theta_mean / 2

    # this list contains the sorted values of Theta from min to max
    sorted_Theta = sorted(allTheta)

    theta_min = 0
    for n in range(4):
        theta_min += sorted_Theta[n]

    theta_max = 0
    for n in range(4, 8):
        theta_max += sorted_Theta[n]

    NewMinTheta = []
    NewMaxTheta = []
    for n in range(4):
        if allTheta[n] < allTheta[n + 4]:
            NewMinTheta.append(allTheta[n])
            NewMaxTheta.append(allTheta[n + 4])
        else:
            NewMaxTheta.append(allTheta[n])
            NewMinTheta.append(allTheta[n + 4])

    min_theta_new = 0
    max_theta_new = 0
    for n in range(4):
        min_theta_new += NewMinTheta[n]
        max_theta_new += NewMaxTheta[n]

    echo_logs(self, "      ====================== SUMMARY of Θ ======================")
    echo_logs(self, "")
    echo_logs(self, "      Minimum Θ parameter : {0:11.6f} degree".format(theta_min))
    echo_logs(self, "      Maximum Θ parameter : {0:11.6f} degree".format(theta_max))
    echo_logs(self, "         Mean Θ parameter : {0:11.6f} degree ***".format(theta_mean))
    echo_logs(self, "")
    if geometry:
        echo_logs(self, "      !!! Non-octahedral structure detected !!!")
        echo_logs(self, "")
    echo_logs(self, "      ==========================================================")
    echo_logs(self, "")

    # If geometry is True, the structure is non-octahedron
    if geometry:
        popup.warn_not_octa(self)

    return theta_mean


def calc_all(self, a_c_octa):
    """Calculate all distortion parameters:

    d_mean, Zeta, Delta, Sigma, and Theta_mean parameters

    :param self: master frame
    :param a_c_octa: atomic labels and coordinates of octahedral structure
    :type: list
    :return all_zeta: list of Zeta parameters
    :return all_delta: list of Delta parameters
    :return all_sigma: list of Sigma parameters
    :return all_theta: list of Theta parameters
    :return all_face: list of 8 faces of octahedral structures
    :rtype all_zeta: list
    :rtype all_delta: list
    :rtype all_sigma: list
    :rtype all_theta: list
    :rtype all_face: list
    """
    echo_logs(self, "Info: Calculate the Δ, Σ, and Θ parameters")
    echo_logs(self, "")

    # just assigned local var
    d_mean = 0
    zeta = 0
    delta = 0
    sigma = 0
    theta_mean = 0

    all_zeta = []
    all_delta = []
    all_sigma = []
    all_theta = []
    all_face = []
    comp_result = []

    # loop over number of metal complexes
    for i in range(len(a_c_octa)):
        echo_logs(self, "      *********************** Complex {0} ***********************".format(i + 1))
        echo_logs(self, "")

        num_file, num_metal, atom_octa, coord_octa = a_c_octa[i]

        # Calculate distortion parameters
        d_mean = calc_d_mean(self, atom_octa, coord_octa)
        zeta = calc_zeta(self, atom_octa, coord_octa)
        delta = calc_delta(self, atom_octa, coord_octa)
        sigma = calc_sigma(self, atom_octa, coord_octa)
        theta_mean = calc_theta(self, atom_octa, coord_octa)

        # Find 8 reference faces and 8 opposite faces
        a_ref_f, c_ref_f, a_oppo_f, c_oppo_f = tools.find_faces_octa(self, coord_octa)
        face_data = [a_ref_f, c_ref_f, a_oppo_f, c_oppo_f]

        # Collect results
        all_zeta.append(zeta)
        all_delta.append(delta)
        all_sigma.append(sigma)
        all_theta.append(theta_mean)
        all_face.append(face_data)
        comp_result.append([num_file, num_metal, d_mean, zeta, delta, sigma, theta_mean])

    # Print results to each unique box
    if len(a_c_octa) == 1:
        self.box_d_mean.insert(tk.INSERT, "{0:3.6f}".format(d_mean))
        self.box_zeta.insert(tk.INSERT, "{0:3.6f}".format(zeta))
        self.box_delta.insert(tk.INSERT, "{0:3.6f}".format(delta))
        self.box_sigma.insert(tk.INSERT, "{0:3.6f}".format(sigma))
        self.box_theta_mean.insert(tk.INSERT, "{0:3.6f}".format(theta_mean))
    else:
        self.box_d_mean.insert(tk.INSERT, "See below")
        self.box_zeta.insert(tk.INSERT, "See below")
        self.box_delta.insert(tk.INSERT, "See below")
        self.box_sigma.insert(tk.INSERT, "See below")
        self.box_theta_mean.insert(tk.INSERT, "See below")

    # Print results to result box
    echo_outs(self, "Computed octahedral distortion parameters for all complexes")
    echo_outs(self, "")
    echo_outs(self, "Complex   Metal       <D>      Zeta      Delta      Sigma      Theta")
    echo_outs(self, "  ---------     -------       -----      ------      -------      -------     -------")
    echo_outs(self, "")
    for i in range(len(comp_result)):
        echo_outs(self, " {0:2d}  -  {1} :  {2:9.4f}  {3:9.6f}  {4:9.6f}  {5:9.4f}  {6:9.4f}"
                  .format(comp_result[i][0], comp_result[i][1], comp_result[i][2], comp_result[i][3],
                          comp_result[i][4], comp_result[i][5], comp_result[i][6]))
    echo_outs(self, "")

    # Print results to stdout log box
    echo_logs(self, "Info: Show computed octahedral distortion parameters of all files")
    echo_logs(self, "")
    echo_logs(self, "      ==================== Overall Summary ====================")
    echo_logs(self, "")
    echo_logs(self, "      Complex   Metal       <D>      Zeta      Delta      Sigma      Theta")
    echo_logs(self, "      ---------     -------       -----      ------      -------      -------     -------")
    echo_logs(self, "")
    for i in range(len(comp_result)):
        echo_logs(self, "       {0:2d}  -  {1} :  {2:9.4f}  {3:9.6f}  {4:9.6f}  {5:9.4f}  {6:9.4f}"
                  .format(comp_result[i][0], comp_result[i][1], comp_result[i][2], comp_result[i][3],
                          comp_result[i][4], comp_result[i][5], comp_result[i][6]))
    echo_logs(self, "")
    echo_logs(self, "")
    echo_logs(self, "      =========================================================")
    echo_logs(self, "")

    return all_zeta, all_delta, all_sigma, all_theta, all_face
