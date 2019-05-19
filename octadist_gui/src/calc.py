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

import octadist_gui.src.plane
from octadist_gui.src import echo_outs, linear, popup, projection, tools


def calc_d_bond(c_octa):
    """
    Calculate metal-ligand bond distance and return value in Angstrom.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    bond_dist : list
        Individual metal-ligand bond distance.

    """
    bond_dist = [linear.euclidean_dist(c_octa[0], c_octa[i]) for i in range(1, 7)]

    return bond_dist


def calc_d_mean(c_octa):
    """
    Calculate mean distance parameter and return value in Angstrom.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    d_mean : float
        Mean metal-ligand distance.

    """
    bond_dist = calc_d_bond(c_octa)
    bond_dist = np.asarray(bond_dist)

    d_mean = np.mean(bond_dist)

    return d_mean


def calc_zeta(c_octa):
    """
    Calculate Zeta parameter and return value in Angstrom.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    zeta : float
        Zeta parameter.

    References
    ----------
    Phys. Rev. B 85, 064114
    
    Notes
    -----
         6
    ζ = sum(|dist_i - d_mean|)
        i=1

    """
    bond_dist = calc_d_bond(c_octa)

    d_mean = calc_d_mean(c_octa)

    diff_dist = [abs(bond_dist[i] - d_mean) for i in range(6)]
    diff_dist = np.asarray(diff_dist)

    zeta = np.sum(diff_dist)

    return zeta


def calc_delta(c_octa):
    """
    Calculate Delta parameter, also known as Tilting distortion parameter.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    delta : float
        Delta parameter.

    References
    ----------
    DOI: 10.1107/S0108768103026661
    Acta Cryst. (2004). B60, 10-20

    Notes
    -----
          1
    Δ =  ---*sum((d_i - d)/d)^2
          6

    where d_i is individual M-X distance and d is mean M-X distance.

    """
    bond_dist = calc_d_bond(c_octa)

    d_mean = calc_d_mean(c_octa)

    delta = sum(pow((bond_dist[i] - d_mean) / d_mean, 2) for i in range(6))
    delta = delta / 6

    return delta


def calc_bond_angle(c_octa):
    """
    Calculate 12 cis and 3 trans unique angles in octahedral structure.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    cis_angle : list
        List of 12 cis angles.
    trans_angle : list
        List of 3 trans angles.

    """
    all_angle = []
    for i in range(1, 7):
        for j in range(i + 1, 7):
            vec1 = c_octa[i] - c_octa[0]
            vec2 = c_octa[j] - c_octa[0]
            angle = linear.angle_btw_vectors(vec1, vec2)
            all_angle.append(angle)

    # Sort the angle from the lowest to the highest
    sorted_angle = sorted(all_angle)
    cis_angle = [sorted_angle[i] for i in range(12)]
    trans_angle = [sorted_angle[i] for i in range(12, 15)]

    return cis_angle, trans_angle


def calc_sigma(c_octa):
    """
    Calculate Sigma parameter and return value in degree.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    sigma : float
        Sigma parameter.
    angle_sigma : list of float
        List of 12 unique cis angles.

    Notes
    -----
          12
    Σ = sigma < 90 - angle_i >
         i=1

    where angle_i in an unique cis angle.

    References
    ----------
    J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    """
    cis_angle, _ = calc_bond_angle(c_octa)
    sigma = sum(abs(90.0 - cis_angle[i]) for i in range(12))

    return sigma


def calc_theta(a_octa, c_octa):
    """
    Calculate Theta parameter and value in degree.

    Parameters
    ----------
    a_octa : list
        Atomic labels of octahedral structure.
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    theta_mean : float
        Mean Theta value.

    Notes
    -----

          24
    Θ = sigma < 60 - angle_i >
         i=1

    where angle_i is an unique angle between two vectors of two twisting face.

    References
    ----------
    M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

    """
    labels = list(a_octa[1:])
    ligands = list(c_octa[1:])

    TM = c_octa[0]
    N1 = c_octa[1]
    N2 = c_octa[2]
    N3 = c_octa[3]
    N4 = c_octa[4]
    N5 = c_octa[5]
    N6 = c_octa[6]

    # Vector from metal to ligand atom
    TMN1 = N1 - TM
    TMN2 = N2 - TM
    TMN3 = N3 - TM
    TMN4 = N4 - TM
    TMN5 = N5 - TM
    TMN6 = N6 - TM

    ligands_vec = [TMN1, TMN2, TMN3, TMN4, TMN5, TMN6]

    ###########################################
    # Determine the order of atoms in complex #
    ###########################################

    _, trans_angle = calc_bond_angle(c_octa)

    max_angle = trans_angle[0]

    # This loop is used to identify which N is in line with N1
    def_change = 6
    for n in range(6):
        test = linear.angle_btw_vectors(ligands_vec[0], ligands_vec[n])
        if test > (max_angle - 1):
            def_change = n

    test_max = 0
    new_change = 0
    for n in range(6):
        test = linear.angle_btw_vectors(ligands_vec[0], ligands_vec[n])
        if test > test_max:
            test_max = test
            new_change = n

    # geometry is used to identify the type of octahedral structure
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

    # Update vector from metal to each ligand atom
    TMN1 = N1 - TM
    TMN2 = N2 - TM
    TMN3 = N3 - TM
    TMN4 = N4 - TM
    TMN5 = N5 - TM
    TMN6 = N6 - TM

    # Update the ligands_vec list that contains M-N vector
    ligands_vec = [TMN1, TMN2, TMN3, TMN4, TMN5, TMN6]

    # This loop is used to identify which N is in line with N2
    for n in range(6):
        test = linear.angle_btw_vectors(ligands_vec[1], ligands_vec[n])
        if test > (max_angle - 1):
            def_change = n

    # This loop is used to identify which N is in line with N2
    test_max = 0
    for n in range(6):
        test = linear.angle_btw_vectors(ligands_vec[1], ligands_vec[n])
        if test > test_max:
            test_max = test
            new_change = n

    if def_change != new_change:
        geometry = True
        def_change = new_change

    # Swapping the atom (n+1) just identified above with N6
    tp = ligands[5]
    ligands[5] = ligands[def_change]
    ligands[def_change] = tp

    tp = labels[5]
    labels[5] = labels[def_change]
    labels[def_change] = tp

    # New atom order is stored into the N1 - N6 lists
    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

    # Update vector from metal to each ligand atom
    TMN1 = N1 - TM
    TMN2 = N2 - TM
    TMN3 = N3 - TM
    TMN4 = N4 - TM
    TMN5 = N5 - TM
    TMN6 = N6 - TM

    ligands_vec = [TMN1, TMN2, TMN3, TMN4, TMN5, TMN6]

    # This loop is used to identify which N is in line with N3
    for n in range(6):
        test = linear.angle_btw_vectors(ligands_vec[2], ligands_vec[n])
        if test > (max_angle - 1):
            def_change = n

    # This loop is used to identify which N is in line with N3
    test_max = 0
    for n in range(6):
        test = linear.angle_btw_vectors(ligands_vec[2], ligands_vec[n])
        if test > test_max:
            test_max = test
            new_change = n

    if def_change != new_change:
        geometry = True
        def_change = new_change

    # Swapping of the atom (n+1) just identified above with N4
    tp = ligands[3]
    ligands[3] = ligands[def_change]
    ligands[def_change] = tp

    tp = labels[3]
    labels[3] = labels[def_change]
    labels[def_change] = tp

    # New atom order is stored into the N1 - N6 lists.
    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

    updated_lig = [N1, N2, N3, N4, N5, N6]

    #####################################################
    # Calculate the Theta parameter ans its derivatives #
    #####################################################

    eqOfPlane = []
    indiTheta = []
    allTheta = []

    # loop over 8 faces
    for proj in range(8):
        a, b, c, d = octadist_gui.src.plane.find_eq_of_plane(N1, N2, N3)
        eqOfPlane.append([a, b, c, d])

        # Projecting M, N4, N5, and N6 onto the plane defined by N1, N2, and N3
        TMP = projection.project_atom_onto_plane(TM, a, b, c, d)
        N4P = projection.project_atom_onto_plane(N4, a, b, c, d)
        N5P = projection.project_atom_onto_plane(N5, a, b, c, d)
        N6P = projection.project_atom_onto_plane(N6, a, b, c, d)

        # Calculate vector from projected metal to projected ligand
        VTh1 = N1 - TMP
        VTh2 = N2 - TMP
        VTh3 = N3 - TMP
        VTh4 = N4P - TMP
        VTh5 = N5P - TMP
        VTh6 = N6P - TMP

        # Calculate 6 theta angles for 1 projection
        a12 = linear.angle_btw_vectors(VTh1, VTh2)
        a13 = linear.angle_btw_vectors(VTh1, VTh3)
        if a12 < a13:
            direction = np.cross(VTh1, VTh2)
        else:
            direction = np.cross(VTh3, VTh1)

        theta1 = linear.angle_sign(VTh1, VTh4, direction)
        theta2 = linear.angle_sign(VTh4, VTh2, direction)
        theta3 = linear.angle_sign(VTh2, VTh5, direction)
        theta4 = linear.angle_sign(VTh5, VTh3, direction)
        theta5 = linear.angle_sign(VTh3, VTh6, direction)
        theta6 = linear.angle_sign(VTh6, VTh1, direction)

        indiTheta.append([theta1, theta2, theta3, theta4, theta5, theta6])

        # Sum individual Theta for 1 projection plane
        sum_theta = sum(abs(indiTheta[proj][i] - 60) for i in range(6))

        # Update Theta into allTheta list
        allTheta.append(sum_theta)

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

        # If the proj = 3, permutation face will be switched from N1N2N3
        # to N1N4N2, to N1N6N4, then to N1N3N6, and then back to N1N2N3
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

    theta_mean = sum(allTheta[i] for i in range(8)) / 2

    # If geometry is True, the structure is non-octahedron
    if geometry:
        popup.warn_not_octa()

    return theta_mean


def calc_theta_max_min(allTheta):
    """

    Parameters
    ----------
    allTheta

    Returns
    -------

    """
    sorted_theta = sorted(allTheta)
    theta_min = sum(sorted_theta[i] for i in range(4))
    theta_max = sum(sorted_theta[i] for i in range(4, 8))

    return theta_min, theta_max


# def calc_all(self, a_c_octa):
#     """Calculate all distortion parameters:
#
#     Zeta, Delta, Sigma, and Theta_mean parameters.
#
#     Parameters
#     ----------
#     a_c_octa : list
#         Atomic labels and coordinates of octahedral structure.
#
#     Returns
#     -------
#     all_zeta : list of float
#         List of Zeta parameters.
#     all_delta : list of float
#         List of Delta parameters.
#     all_sigma : list of float
#         List of Sigma parameters.
#     all_theta : list of float
#         List of Theta parameters.
#     all_face : list
#         List of 8 faces of octahedral structures.
#
#     """
#     d_mean = 0
#     zeta = 0
#     delta = 0
#     sigma = 0
#     theta_mean = 0
#
#     all_zeta = []
#     all_delta = []
#     all_sigma = []
#     all_theta = []
#     all_face = []
#     comp_result = []
#
#     # loop over number of metal complexes
#     for i in range(len(a_c_octa)):
#         num_file, num_metal, atom_octa, coord_octa = a_c_octa[i]
#
#         # Calculate distortion parameters
#         d_mean = calc_d_mean(coord_octa)
#         zeta = calc_zeta(coord_octa)
#         delta = calc_delta(coord_octa)
#         sigma = calc_sigma(coord_octa)
#         theta_mean = calc_theta(atom_octa, coord_octa)
#
#         # Find 8 reference faces and 8 opposite faces
#         a_ref_f, c_ref_f, a_oppo_f, c_oppo_f = tools.find_faces_octa(coord_octa)
#
#         face_data = [a_ref_f, c_ref_f, a_oppo_f, c_oppo_f]
#
#         # Collect results
#         all_zeta.append(zeta)
#         all_delta.append(delta)
#         all_sigma.append(sigma)
#         all_theta.append(theta_mean)
#         all_face.append(face_data)
#
#         comp_result.append([num_file,
#                             num_metal,
#                             d_mean,
#                             zeta,
#                             delta,
#                             sigma,
#                             theta_mean
#                             ])
#
#     # Print results to each unique box
#     if len(a_c_octa) == 1:
#         self.box_d_mean.insert(tk.INSERT, "{0:3.6f}".format(d_mean))
#         self.box_zeta.insert(tk.INSERT, "{0:3.6f}".format(zeta))
#         self.box_delta.insert(tk.INSERT, "{0:3.6f}".format(delta))
#         self.box_sigma.insert(tk.INSERT, "{0:3.6f}".format(sigma))
#         self.box_theta_mean.insert(tk.INSERT, "{0:3.6f}".format(theta_mean))
#     else:
#         self.box_d_mean.insert(tk.INSERT, "See below")
#         self.box_zeta.insert(tk.INSERT, "See below")
#         self.box_delta.insert(tk.INSERT, "See below")
#         self.box_sigma.insert(tk.INSERT, "See below")
#         self.box_theta_mean.insert(tk.INSERT, "See below")
#
#     # Print results to result box
#     echo_outs(self, "Computed octahedral distortion parameters for all complexes")
#     echo_outs(self, "")
#     echo_outs(self, "Complex   Metal      <D>      Zeta      Delta      Sigma      Theta")
#     echo_outs(self, "*******************************************************************")
#     echo_outs(self, "")
#     for i in range(len(comp_result)):
#         echo_outs(self, " {0:2d}  -  {1} :  {2:9.4f}  {3:9.6f}  {4:9.6f}  {5:9.4f}  {6:9.4f}"
#                   .format(comp_result[i][0],
#                           comp_result[i][1],
#                           comp_result[i][2],
#                           comp_result[i][3],
#                           comp_result[i][4],
#                           comp_result[i][5],
#                           comp_result[i][6]))
#     echo_outs(self, "")
#
#     return all_zeta, all_delta, all_sigma, all_theta, all_face
