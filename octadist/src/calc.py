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
    >>> sigma = test.get_sigma()

    >>> sigma
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

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

        """
        self.bond_dist = [distance.euclidean(self.coord[0], self.coord[i]) for i in range(1, 7)]
        self.bond_dist = np.asarray(self.bond_dist, dtype=np.float64)

    def calc_d_mean(self):
        """
        Calculate mean distance parameter and return value in Angstrom.

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

        See Also
        --------
        calc_d_bond : Calculate metal-ligand bonds length.

        """
        self.d_mean = np.mean(self.bond_dist)

    def calc_bond_angle(self):
        """
        Calculate 12 cis and 3 trans unique angles in octahedral structure.

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

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

        |      6
        | ζ = sum(|dist_i - d_mean|)
        |     i=1

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

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

        |       1
        | Δ =  ---*sum((d_i - d)/d)^2
        |       6

        where d_i is individual M-X distance and d is mean M-X distance.

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

        References
        ----------
        DOI: 10.1107/S0108768103026661
        Acta Cryst. (2004). B60, 10-20

        See Also
        --------
        calc_d_bond : Calculate metal-ligand bonds length.
        calc_d_mean : Calculate mean metal-ligand bond length.

        """
        delta = sum(pow((self.bond_dist[i] - self.d_mean) / self.d_mean, 2) for i in range(6))
        self.delta = delta / 6

    def calc_sigma(self):
        """
        Calculate Sigma parameter and return value in degree.

        |       12
        | Σ = sigma < 90 - angle_i >
        |      i=1

        where angle_i in an unique cis angle.

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

        References
        ----------
        J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.

        See Also
        --------
        calc_bond_angle : Calculate bond angles between ligand-metal-ligand.

        """
        self.sigma = sum(abs(90.0 - self.cis_angle[i]) for i in range(12))

    def calc_theta(self):
        """
        Calculate Theta parameter and value in degree.

        |       24
        | Θ = sigma < 60 - angle_i >
        |      i=1

        where angle_i is an unique angle between two vectors of two twisting face.

        Parameters
        ----------
        coord : array_like
            Atomic coordinates of octahedral structure.

        References
        ----------
        M. Marchivie et al.
        Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

        See Also
        --------
        calc_theta_min : Calculate minimum Theta parameter.
        calc_theta_max : Calculate maximum Theta parameter.

        """
        ligands = list(self.coord[1:])

        TM = self.coord[0]
        N1 = self.coord[1]
        N2 = self.coord[2]
        N3 = self.coord[3]
        N4 = self.coord[4]
        N5 = self.coord[5]
        N6 = self.coord[6]

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

        max_angle = self.trans_angle[0]

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

        # self.non_octa is used to identify the type of octahedral structure
        if def_change != new_change:
            self.non_octa = True
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
            self.non_octa = True
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
            self.non_octa = True
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

        # loop over 8 faces
        for proj in range(8):
            a, b, c, d = plane.find_eq_of_plane(N1, N2, N3)
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

            self.allTheta.append(sum_theta)

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

        self.theta = sum(self.allTheta[i] for i in range(8)) / 2

    def calc_theta_min(self):
        """
        Calculate minimum Theta parameter and return value in degree.

        Parameters
        ----------
        allTheta : list
            List of individual Theta angles.

        """
        sorted_theta = sorted(self.allTheta)
        self.theta_min = sum(sorted_theta[i] for i in range(4))

    def calc_theta_max(self):
        """
        Calculate maximum Theta parameter and return value in degree.

        Parameters
        ----------
        allTheta : list
            List of individual Theta angles.

        """
        sorted_theta = sorted(self.allTheta)
        self.theta_max = sum(sorted_theta[i] for i in range(4, 8))

