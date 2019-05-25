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

import numpy as np

import octadist_gui.src.plane
from octadist_gui.src import linear, popup, projection


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

    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> calc_d_bond(coord)
    [1.869580869461656,
     1.8820188587261812,
     1.9465848640994314,
     1.9479642654866642,
     1.9702004656851546,
     1.9805587036803534]

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

    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> calc_d_mean(coord)
    1.93281800452324

    """
    bond_dist = calc_d_bond(c_octa)
    bond_dist = np.asarray(bond_dist)

    d_mean = np.mean(bond_dist)

    return d_mean


def calc_zeta(c_octa):
    """
    Calculate Zeta parameter and return value in Angstrom.

         6
    ζ = sum(|dist_i - d_mean|)
        i=1

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
    
    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> calc_zeta(coord)
    0.22807256171728651

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

          1
    Δ =  ---*sum((d_i - d)/d)^2
          6

    where d_i is individual M-X distance and d is mean M-X distance.

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

    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> calc_delta(coord)
    0.0004762517834704151

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
    c_octa : array or list
        Atomic coordinates of octahedral structure.

    Returns
    -------
    cis_angle : list
        List of 12 cis angles.
    trans_angle : list
        List of 3 trans angles.

    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> cis, trans = calc_bond_angle(coord)
    >>> cis
    [82.75749025175044, 83.11074412601039, 87.07433386260743,
     87.217426970301, 87.59010057569893, 88.49485029114034,
     89.71529920540053, 94.09217259687905, 94.2481644447923,
     94.51379613736219, 95.40490801797102, 95.62773246517462]
    >>> trans
    [173.8820603662232, 176.07966588060893, 176.58468599461276]

    """
    if type(c_octa) == np.ndarray:
        pass
    else:
        c_octa = np.asarray(c_octa)

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

          12
    Σ = sigma < 90 - angle_i >
         i=1

    where angle_i in an unique cis angle.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    sigma : float
        Sigma parameter.

    References
    ----------
    J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> calc_sigma(coord)
    47.926528379270124

    """
    cis_angle, _ = calc_bond_angle(c_octa)
    sigma = sum(abs(90.0 - cis_angle[i]) for i in range(12))

    return sigma


def calc_theta(c_octa):
    """
    Calculate Theta parameter and value in degree.

          24
    Θ = sigma < 60 - angle_i >
         i=1

    where angle_i is an unique angle between two vectors of two twisting face.

    Parameters
    ----------
    c_octa : array or list
        Atomic coordinates of octahedral structure.

    Returns
    -------
    theta_mean : float
        Mean Theta value.

    References
    ----------
    M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

    Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]
    >>> calc_theta(coord)
    122.68897277454599

    """
    if type(c_octa) == np.ndarray:
        pass
    else:
        c_octa = np.asarray(c_octa)

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

    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

    TMN1 = N1 - TM
    TMN2 = N2 - TM
    TMN3 = N3 - TM
    TMN4 = N4 - TM
    TMN5 = N5 - TM
    TMN6 = N6 - TM

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

    # New atom order is stored into the N1 - N6 lists
    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

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

    # New atom order is stored into the N1 - N6 lists
    N1 = ligands[0]
    N2 = ligands[1]
    N3 = ligands[2]
    N4 = ligands[3]
    N5 = ligands[4]
    N6 = ligands[5]

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

        # Project M, N4, N5, and N6 onto the plane defined by N1, N2, and N3
        TMP = projection.project_atom_onto_plane(TM, a, b, c, d)
        N4P = projection.project_atom_onto_plane(N4, a, b, c, d)
        N5P = projection.project_atom_onto_plane(N5, a, b, c, d)
        N6P = projection.project_atom_onto_plane(N6, a, b, c, d)

        VTh1 = N1 - TMP
        VTh2 = N2 - TMP
        VTh3 = N3 - TMP
        VTh4 = N4P - TMP
        VTh5 = N5P - TMP
        VTh6 = N6P - TMP

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

        sum_theta = sum(abs(indiTheta[proj][i] - 60) for i in range(6))

        allTheta.append(sum_theta)

        tp = N2
        N2 = N4
        N4 = N6
        N6 = N3
        N3 = tp

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

        # End of the loop that calculate the 8 projections.

    theta_mean = sum(allTheta[i] for i in range(8)) / 2

    # If geometry is True, the structure is non-octahedron
    if geometry:
        popup.warn_not_octa()

    return theta_mean


def calc_theta_min(allTheta):
    """
    Calculate minimum Theta parameter and return value in degree.

    Parameters
    ----------
    allTheta : list
        List of individual Theta angles.

    Returns
    -------
    theta_min : float
        Minimum Theta parameter.

    Examples
    --------
    >>> allTheta
    [36.62587317261202, 28.85054807796844,
     21.798434925314737, 28.57216604448481,
     41.292681064753346, 42.444094866386344,
     22.378910890588678, 23.41523650698359]
    >>> calc_theta_min(allTheta)
    96.16474836737183

    """
    sorted_theta = sorted(allTheta)
    theta_min = sum(sorted_theta[i] for i in range(4))

    return theta_min


def calc_theta_max(allTheta):
    """
    Calculate maximum Theta parameter and return value in degree.

    Parameters
    ----------
    allTheta : list
        List of individual Theta angles.

    Returns
    -------
    theta_max : float
        Maximum Theta parameter.

    Examples
    --------
    >>> allTheta
    [36.62587317261202, 28.85054807796844,
     21.798434925314737, 28.57216604448481,
     41.292681064753346, 42.444094866386344,
     22.378910890588678, 23.41523650698359]
    >>> calc_theta_max(allTheta)
    149.21319718172015

    """
    sorted_theta = sorted(allTheta)
    theta_max = sum(sorted_theta[i] for i in range(4, 8))

    return theta_max
