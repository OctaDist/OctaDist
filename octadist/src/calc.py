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
from scipy.spatial import distance

from octadist.src import linear, plane, projection


class CalcDistortion:
    """
    Calculate metal-ligand bond distance and return value in Angstrom.

    Parameters
    ----------
    coord : array_like
        Atomic coordinates of octahedral structure.

    Examples
    --------
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> test = CalcDistortion(coord)
    >>> test.sigma
    47.926528379270124

    """

    def __init__(self, coord):
        self.coord = coord

        if type(self.coord) == np.ndarray:
            pass
        else:
            self.coord = np.asarray(self.coord, dtype=np.float64)

        self.bond_dist = []
        self.d_mean = 0
        self.diff_dist = []
        self.zeta = 0
        self.delta = 0
        self.cis_angle = 0
        self.trans_angle = 0
        self.sigma = 0
        self.allTheta = []
        self.theta = 0
        self.theta_min = 0
        self.theta_max = 0
        self.non_octa = False

        self.calc_d_bond()
        self.calc_d_mean()
        self.calc_bond_angle()
        self.calc_zeta()
        self.calc_delta()
        self.calc_sigma()
        self.calc_theta()
        self.calc_theta_min()
        self.calc_theta_max()

    def calc_d_bond(self):
        """
        Calculate metal-ligand bond distance and return value in Angstrom.

        See Also
        --------
        calc_d_mean : Calculate mean metal-ligand bond length.

        """
        self.bond_dist = [distance.euclidean(self.coord[0], self.coord[i]) for i in range(1, 7)]
        self.bond_dist = np.asarray(self.bond_dist, dtype=np.float64)

    def calc_d_mean(self):
        """
        Calculate mean distance parameter and return value in Angstrom.

        See Also
        --------
        calc_d_bond : Calculate metal-ligand bonds length.

        """
        self.d_mean = np.mean(self.bond_dist)

    def calc_bond_angle(self):
        """
        Calculate 12 cis and 3 trans unique angles in octahedral structure.

        See Also
        --------
        calc_sigma : Calculate Sigma parameter.

        """
        all_angle = []
        for i in range(1, 7):
            for j in range(i + 1, 7):
                vec1 = self.coord[i] - self.coord[0]
                vec2 = self.coord[j] - self.coord[0]
                angle = linear.angle_btw_vectors(vec1, vec2)
                all_angle.append(angle)

        # Sort the angle from the lowest to the highest
        sorted_angle = sorted(all_angle)
        self.cis_angle = [sorted_angle[i] for i in range(12)]
        self.trans_angle = [sorted_angle[i] for i in range(12, 15)]

    def calc_zeta(self):
        """
        Calculate Zeta parameter and return value in Angstrom.

        See Also
        --------
        calc_d_bond : Calculate metal-ligand bonds length.
        calc_d_mean : Calculate mean metal-ligand bond length.

        References
        ----------
        Phys. Rev. B 85, 064114

        """
        diff_dist = [abs(self.bond_dist[i] - self.d_mean) for i in range(6)]
        self.diff_dist = np.asarray(diff_dist, dtype=np.float64)

        self.zeta = np.sum(self.diff_dist)

    def calc_delta(self):
        """
        Calculate Delta parameter, also known as Tilting distortion parameter.

        See Also
        --------
        calc_d_bond : Calculate metal-ligand bonds length.
        calc_d_mean : Calculate mean metal-ligand bond length.

        References
        ----------
        DOI: 10.1107/S0108768103026661
        Acta Cryst. (2004). B60, 10-20

        """
        delta = sum(pow((self.bond_dist[i] - self.d_mean) / self.d_mean, 2) for i in range(6))
        self.delta = delta / 6

    def calc_sigma(self):
        """
        Calculate Sigma parameter and return value in degree.

        See Also
        --------
        calc_bond_angle : Calculate bond angles between ligand-metal-ligand.

        References
        ----------
        J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

        """
        self.sigma = sum(abs(90.0 - self.cis_angle[i]) for i in range(12))

    def calc_theta(self):
        """
        Calculate Theta parameter and value in degree.

        See Also
        --------
        calc_theta_min :
            Calculate minimum Theta parameter.
        calc_theta_max :
            Calculate maximum Theta parameter.
        octadist.src.linear.angle_btw_vectors :
            Calculate cosine angle between two vectors.
        octadist.src.linear.angle_sign
            Calculate cosine angle between two vectors sensitive to CW/CCW direction.
        octadist.src.plane.find_eq_of_plane :
            Find the equation of the plane.
        octadist.src.projection.project_atom_onto_plane :
            Orthogonal projection of point onto the plane.

        References
        ----------
        M. Marchivie et al.
        Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

        """
        ligands = list(self.coord[1:])

        coord_metal = self.coord[0]
        coord_lig1 = self.coord[1]
        coord_lig2 = self.coord[2]
        coord_lig3 = self.coord[3]
        coord_lig4 = self.coord[4]
        coord_lig5 = self.coord[5]
        coord_lig6 = self.coord[6]

        # Vector from metal to ligand atom
        metal_to_lig1 = coord_lig1 - coord_metal
        metal_to_lig2 = coord_lig2 - coord_metal
        metal_to_lig3 = coord_lig3 - coord_metal
        metal_to_lig4 = coord_lig4 - coord_metal
        metal_to_lig5 = coord_lig5 - coord_metal
        metal_to_lig6 = coord_lig6 - coord_metal

        ligands_vec = [metal_to_lig1, 
                       metal_to_lig2, 
                       metal_to_lig3, 
                       metal_to_lig4, 
                       metal_to_lig5, 
                       metal_to_lig6]

        ###########################################
        # Determine the order of atoms in complex #
        ###########################################

        max_angle = self.trans_angle[0]

        # This loop is used to identify which N is in line with coord_lig1
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

        # self.non_octa is used to identify the type of octahedral structure
        if def_change != new_change:
            self.non_octa = True
            def_change = new_change

        tp = ligands[4]
        ligands[4] = ligands[def_change]
        ligands[def_change] = tp

        coord_lig1 = ligands[0]
        coord_lig2 = ligands[1]
        coord_lig3 = ligands[2]
        coord_lig4 = ligands[3]
        coord_lig5 = ligands[4]
        coord_lig6 = ligands[5]

        metal_to_lig1 = coord_lig1 - coord_metal
        metal_to_lig2 = coord_lig2 - coord_metal
        metal_to_lig3 = coord_lig3 - coord_metal
        metal_to_lig4 = coord_lig4 - coord_metal
        metal_to_lig5 = coord_lig5 - coord_metal
        metal_to_lig6 = coord_lig6 - coord_metal

        ligands_vec = [metal_to_lig1,
                       metal_to_lig2,
                       metal_to_lig3,
                       metal_to_lig4,
                       metal_to_lig5,
                       metal_to_lig6]

        # This loop is used to identify which N is in line with coord_lig2
        for n in range(6):
            test = linear.angle_btw_vectors(ligands_vec[1], ligands_vec[n])
            if test > (max_angle - 1):
                def_change = n

        # This loop is used to identify which N is in line with coord_lig2
        test_max = 0
        for n in range(6):
            test = linear.angle_btw_vectors(ligands_vec[1], ligands_vec[n])
            if test > test_max:
                test_max = test
                new_change = n

        if def_change != new_change:
            self.non_octa = True
            def_change = new_change

        # Swapping the atom (n+1) just identified above with coord_lig6
        tp = ligands[5]
        ligands[5] = ligands[def_change]
        ligands[def_change] = tp

        # New atom order is stored into the coord_lig1 - coord_lig6 lists
        coord_lig1 = ligands[0]
        coord_lig2 = ligands[1]
        coord_lig3 = ligands[2]
        coord_lig4 = ligands[3]
        coord_lig5 = ligands[4]
        coord_lig6 = ligands[5]

        metal_to_lig1 = coord_lig1 - coord_metal
        metal_to_lig2 = coord_lig2 - coord_metal
        metal_to_lig3 = coord_lig3 - coord_metal
        metal_to_lig4 = coord_lig4 - coord_metal
        metal_to_lig5 = coord_lig5 - coord_metal
        metal_to_lig6 = coord_lig6 - coord_metal

        ligands_vec = [metal_to_lig1,
                       metal_to_lig2,
                       metal_to_lig3,
                       metal_to_lig4,
                       metal_to_lig5,
                       metal_to_lig6]

        # This loop is used to identify which N is in line with coord_lig3
        for n in range(6):
            test = linear.angle_btw_vectors(ligands_vec[2], ligands_vec[n])
            if test > (max_angle - 1):
                def_change = n

        # This loop is used to identify which N is in line with coord_lig3
        test_max = 0
        for n in range(6):
            test = linear.angle_btw_vectors(ligands_vec[2], ligands_vec[n])
            if test > test_max:
                test_max = test
                new_change = n

        if def_change != new_change:
            self.non_octa = True
            def_change = new_change

        # Swapping of the atom (n+1) just identified above with coord_lig4
        tp = ligands[3]
        ligands[3] = ligands[def_change]
        ligands[def_change] = tp

        # New atom order is stored into the coord_lig1 - coord_lig6 lists
        coord_lig1 = ligands[0]
        coord_lig2 = ligands[1]
        coord_lig3 = ligands[2]
        coord_lig4 = ligands[3]
        coord_lig5 = ligands[4]
        coord_lig6 = ligands[5]

        #####################################################
        # Calculate the Theta parameter ans its derivatives #
        #####################################################

        eq_of_plane = []
        indi_theta = []

        # loop over 8 faces
        for proj in range(8):
            a, b, c, d = plane.find_eq_of_plane(coord_lig1, coord_lig2, coord_lig3)
            eq_of_plane.append([a, b, c, d])

            # Project M, coord_lig4, coord_lig5, and coord_lig6 onto the plane
            # that defined by coord_lig1, coord_lig2, and coord_lig3
            proj_m = projection.project_atom_onto_plane(coord_metal, a, b, c, d)
            proj_lig4 = projection.project_atom_onto_plane(coord_lig4, a, b, c, d)
            proj_lig5 = projection.project_atom_onto_plane(coord_lig5, a, b, c, d)
            proj_lig6 = projection.project_atom_onto_plane(coord_lig6, a, b, c, d)

            proj_m_to_lig1 = coord_lig1 - proj_m
            proj_m_to_lig2 = coord_lig2 - proj_m
            proj_m_to_lig3 = coord_lig3 - proj_m
            proj_m_to_lig4 = proj_lig4 - proj_m
            proj_m_to_lig5 = proj_lig5 - proj_m
            proj_m_to_lig6 = proj_lig6 - proj_m

            a12 = linear.angle_btw_vectors(proj_m_to_lig1, proj_m_to_lig2)
            a13 = linear.angle_btw_vectors(proj_m_to_lig1, proj_m_to_lig3)
            if a12 < a13:
                direction = np.cross(proj_m_to_lig1, proj_m_to_lig2)
            else:
                direction = np.cross(proj_m_to_lig3, proj_m_to_lig1)

            theta1 = linear.angle_sign(proj_m_to_lig1, proj_m_to_lig4, direction)
            theta2 = linear.angle_sign(proj_m_to_lig4, proj_m_to_lig2, direction)
            theta3 = linear.angle_sign(proj_m_to_lig2, proj_m_to_lig5, direction)
            theta4 = linear.angle_sign(proj_m_to_lig5, proj_m_to_lig3, direction)
            theta5 = linear.angle_sign(proj_m_to_lig3, proj_m_to_lig6, direction)
            theta6 = linear.angle_sign(proj_m_to_lig6, proj_m_to_lig1, direction)

            indi_theta.append([theta1, theta2, theta3, theta4, theta5, theta6])

            sum_theta = sum(abs(indi_theta[proj][i] - 60) for i in range(6))

            self.allTheta.append(sum_theta)

            tp = coord_lig2
            coord_lig2 = coord_lig4
            coord_lig4 = coord_lig6
            coord_lig6 = coord_lig3
            coord_lig3 = tp

            # If the proj = 3, permutation face will be switched from N1N2N3
            # to N1N4N2, to N1N6N4, then to N1N3N6, and then back to N1N2N3
            if proj == 3:
                tp = coord_lig1
                coord_lig1 = coord_lig5
                coord_lig5 = tp
                tp = coord_lig2
                coord_lig2 = coord_lig6
                coord_lig6 = tp
                tp = coord_lig3
                coord_lig3 = coord_lig4
                coord_lig4 = tp

            # End of the loop that calculate the 8 projections.

        self.theta = sum(self.allTheta[i] for i in range(8)) / 2

    def calc_theta_min(self):
        """
        Calculate minimum Theta parameter and return value in degree.

        """
        sorted_theta = sorted(self.allTheta)
        self.theta_min = sum(sorted_theta[i] for i in range(4))

    def calc_theta_max(self):
        """
        Calculate maximum Theta parameter and return value in degree.

        """
        sorted_theta = sorted(self.allTheta)
        self.theta_max = sum(sorted_theta[i] for i in range(4, 8))
