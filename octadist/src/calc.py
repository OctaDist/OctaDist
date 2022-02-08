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
    Calculate octahedral histortion parameters:

    - Bond distance : :meth:`calc_d_bond`
    - Mean bond distance : :meth:`calc_d_mean`
    - Bond angle around metal center atom : :meth:`calc_bond_angle`
    - zeta parameter : :meth:`calc_zeta`
    - Delta parameter : :meth:`calc_delta`
    - Sigma parameter : :meth:`calc_sigma`
    - Minimum Tehta parameter : :meth:`calc_theta_min`
    - Maximum Theta parameter : :meth:`calc_theta_max`
    - Mean Theta parametes : :meth:`calc_theta`

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
        self.eight_theta = []
        self.theta = 0
        self.theta_min = 0
        self.theta_max = 0
        self.eq_of_plane = []
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
        calc_d_mean : 
            Calculate mean metal-ligand bond length.

        """
        self.bond_dist = [distance.euclidean(self.coord[0], self.coord[i]) for i in range(1, 7)]
        self.bond_dist = np.asarray(self.bond_dist, dtype=np.float64)

    def calc_d_mean(self):
        """
        Calculate mean distance parameter and return value in Angstrom.

        See Also
        --------
        calc_d_bond : 
            Calculate metal-ligand bonds length.

        """
        self.d_mean = np.mean(self.bond_dist)

    def calc_bond_angle(self):
        """
        Calculate 12 cis and 3 trans unique angles in octahedral structure.

        See Also
        --------
        calc_sigma : 
            Calculate Sigma parameter.

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
        Calculate zeta parameter [1]_ and return value in Angstrom.

        See Also
        --------
        calc_d_bond : 
            Calculate metal-ligand bonds length.
        calc_d_mean : 
            Calculate mean metal-ligand bond length.

        References
        ----------
        .. [1] M. Buron-Le Cointe, J. Hébert, C. Baldé, N. Moisan,
            L. Toupet, P. Guionneau, J. F. Létard, E. Freysz,
            H. Cailleau, and E. Collet. - Intermolecular control of
            thermoswitching and photoswitching phenomena in two
            spin-crossover polymorphs. Phys. Rev. B 85, 064114.

        """
        diff_dist = [abs(self.bond_dist[i] - self.d_mean) for i in range(6)]
        self.diff_dist = np.asarray(diff_dist, dtype=np.float64)

        self.zeta = np.sum(self.diff_dist)

    def calc_delta(self):
        """
        Calculate Delta parameter, also known as Tilting distortion parameter [2]_.

        See Also
        --------
        calc_d_bond : 
            Calculate metal-ligand bonds length.
        calc_d_mean : 
            Calculate mean metal-ligand bond length.

        References
        ----------
        .. [2] M. W. Lufaso and P. M. Woodward. - Jahn–Teller distortions,
            cation ordering and octahedral tilting in perovskites.
            Acta Cryst. (2004). B60, 10-20. DOI: 10.1107/S0108768103026661

        """
        delta = sum(pow((self.bond_dist[i] - self.d_mean) / self.d_mean, 2) for i in range(6))
        self.delta = delta / 6

    def calc_sigma(self):
        """
        Calculate Sigma parameter [3]_ and return value in degree.

        See Also
        --------
        calc_bond_angle : 
            Calculate bond angles between ligand-metal-ligand.

        References
        ----------
        .. [3] James K. McCusker, A. L. Rheingold, D. N. Hendrickson.
            Variable-Temperature Studies of Laser-Initiated 5T2 → 1A1
            Intersystem Crossing in Spin-Crossover Complexes: 
            Empirical Correlations between Activation Parameters
            and Ligand Structure in a Series of Polypyridyl.
            Ferrous Complexes. Inorg. Chem. 1996, 35, 2100.

        """
        self.sigma = sum(abs(90.0 - self.cis_angle[i]) for i in range(12))

    def determine_faces(self):
        """
        Refine the order of ligand atoms in order to find the plane for projection.

        Returns
        -------
        coord_metal : array_like
            Coordinate of metal atom.
        coord_lig : array_like
            Coordinate of ligand atoms.

        See Also
        --------
        calc_theta : 
            Calculate mean Theta parameter

        Examples
        --------
        >>> bef = np.array([
                    [4.0674, 7.2040, 13.6117]
                    [4.3033, 7.3750, 11.7292]
                    [3.8326, 6.9715, 15.4926]
                    [5.8822, 6.4461, 13.4312]
                    [3.3002, 5.3828, 13.6316]
                    [4.8055, 8.9318, 14.2716]
                    [2.3184, 8.0165, 13.1152]
                    ])
        >>> metal, coord = self.determine_faces(bef)
        >>> metal
        [ 4.0674  7.204  13.6117]
        >>> coord_lig
        [[ 4.3033  7.375  11.7292]      # Front face
         [ 4.8055  8.9318 14.2716]      # Front face
         [ 5.8822  6.4461 13.4312]      # Front face
         [ 2.3184  8.0165 13.1152]      # Back face
         [ 3.8326  6.9715 15.4926]      # Back face
         [ 3.3002  5.3828 13.6316]]     # Back face

        """
        # Metal and ligand atoms
        coord_metal = self.coord[0]
        ligands = self.coord[1:]
        coord_lig = np.array([self.coord[i] for i in range(1, 7)])

        # Find vector from metal to ligand atoms
        metal_to_lig = coord_lig - coord_metal

        # Find maximum angle
        max_angle = self.trans_angle[0]

        # Identify which N is in line with ligand 1
        def_change = 6
        for n in range(6):
            test = linear.angle_btw_vectors(metal_to_lig[0], metal_to_lig[n])
            if test > (max_angle - 1):
                def_change = n

        test_max = 0
        new_change = 0
        for n in range(6):
            test = linear.angle_btw_vectors(metal_to_lig[0], metal_to_lig[n])
            if test > test_max:
                test_max = test
                new_change = n

        # Check if the structure is octahedron or not
        if def_change != new_change:
            self.non_octa = True
            def_change = new_change

        # Swap ligand
        # As ligands in 2-dimensions array, we use the following technique
        # to swap two lists of elements with avoiding passing reference value
        ligands[[4, def_change]] = ligands[[def_change, 4]]

        # Update vector from metal to ligand atoms
        metal_to_lig = ligands - coord_metal

        # Identify which N is in line with ligand 2
        for n in range(6):
            test = linear.angle_btw_vectors(metal_to_lig[1], metal_to_lig[n])
            if test > (max_angle - 1):
                def_change = n

        test_max = 0
        for n in range(6):
            test = linear.angle_btw_vectors(metal_to_lig[1], metal_to_lig[n])
            if test > test_max:
                test_max = test
                new_change = n

        if def_change != new_change:
            self.non_octa = True
            def_change = new_change

        # Swap ligand
        ligands[[5, def_change]] = ligands[[def_change, 5]]

        # Update vector from metal to ligand atoms
        metal_to_lig = ligands - coord_metal

        # Identify which N is in line with ligand 3
        for n in range(6):
            test = linear.angle_btw_vectors(metal_to_lig[2], metal_to_lig[n])
            if test > (max_angle - 1):
                def_change = n

        test_max = 0
        for n in range(6):
            test = linear.angle_btw_vectors(metal_to_lig[2], metal_to_lig[n])
            if test > test_max:
                test_max = test
                new_change = n

        if def_change != new_change:
            self.non_octa = True
            def_change = new_change

        # Swap ligand
        ligands[[3, def_change]] = ligands[[def_change, 3]]

        # New atom order
        coord_lig = np.array([ligands[i] for i in range(6)])

        return coord_metal, coord_lig

    def calc_theta(self):
        """
        Calculate Theta parameter [4]_ and value in degree.

        See Also
        --------
        calc_theta_min :
            Calculate minimum Theta parameter.
        calc_theta_max :
            Calculate maximum Theta parameter.
        octadist.src.linear.angle_btw_vectors :
            Calculate cosine angle between two vectors.
        octadist.src.linear.angle_sign :
            Calculate cosine angle between two vectors sensitive to CW/CCW direction.
        octadist.src.plane.find_eq_of_plane :
            Find the equation of the plane.
        octadist.src.projection.project_atom_onto_plane :
            Orthogonal projection of point onto the plane.

        References
        ----------
        .. [4] M. Marchivie, P. Guionneau, J.-F. Létard, D. Chasseau.
            Photo‐induced spin‐transition: the role of the iron(II)
            environment distortion. Acta Crystal-logr. Sect. B Struct.
            Sci. 2005, 61, 25.

        """
        # Get refined atomic coordinates
        coord_metal, coord_lig = self.determine_faces()

        # loop over 8 faces
        for r in range(8):
            a, b, c, d = plane.find_eq_of_plane(coord_lig[0], coord_lig[1], coord_lig[2])
            self.eq_of_plane.append([a, b, c, d])

            # Project metal and other three ligand atom onto the plane
            projected_m = projection.project_atom_onto_plane(coord_metal, a, b, c, d)
            projected_lig4 = projection.project_atom_onto_plane(coord_lig[3], a, b, c, d)
            projected_lig5 = projection.project_atom_onto_plane(coord_lig[4], a, b, c, d)
            projected_lig6 = projection.project_atom_onto_plane(coord_lig[5], a, b, c, d)

            # Find the vectors between atoms that are on the same plane
            # These vectors will be used to calculate Theta afterward.
            vector_theta = np.array(
                [
                    coord_lig[0] - projected_m,
                    coord_lig[1] - projected_m,
                    coord_lig[2] - projected_m,
                    projected_lig4 - projected_m,
                    projected_lig5 - projected_m,
                    projected_lig6 - projected_m,
                ]
            )

            # Check if the direction is CW or CCW
            a12 = linear.angle_btw_vectors(vector_theta[0], vector_theta[1])
            a13 = linear.angle_btw_vectors(vector_theta[0], vector_theta[2])

            # If angle of interest is smaller than its neighbor,
            # define it as CW direction, if not, it will be CCW instead.
            if a12 < a13:
                direction = np.cross(vector_theta[0], vector_theta[1])
            else:
                direction = np.cross(vector_theta[2], vector_theta[0])

            # Calculate individual theta angle
            theta1 = linear.angle_sign(vector_theta[0], vector_theta[3], direction)
            theta2 = linear.angle_sign(vector_theta[3], vector_theta[1], direction)
            theta3 = linear.angle_sign(vector_theta[1], vector_theta[4], direction)
            theta4 = linear.angle_sign(vector_theta[4], vector_theta[2], direction)
            theta5 = linear.angle_sign(vector_theta[2], vector_theta[5], direction)
            theta6 = linear.angle_sign(vector_theta[5], vector_theta[0], direction)

            indi_theta = np.array([theta1, theta2, theta3, theta4, theta5, theta6])

            self.eight_theta.append(sum(abs(indi_theta - 60)))

            # Use deep copy so as to avoid pass by reference
            tmp = coord_lig[1].copy()
            coord_lig[1] = coord_lig[3].copy()
            coord_lig[3] = coord_lig[5].copy()
            coord_lig[5] = coord_lig[2].copy()
            coord_lig[2] = tmp.copy()

            # If 3rd round, permutation face will be switched
            # from N1N2N3
            # to N1N4N2,
            # to N1N6N4,
            # to N1N3N6, and then back to N1N2N3
            if r == 3:
                coord_lig[[0, 4]] = coord_lig[[4, 0]]
                coord_lig[[1, 5]] = coord_lig[[5, 1]]
                coord_lig[[2, 3]] = coord_lig[[3, 2]]

        self.theta = sum(self.eight_theta) / 2

    def calc_theta_min(self):
        """
        Calculate minimum Theta parameter and return value in degree.

        See Also
        --------
        calc_theta :
            Calculate mean Theta parameter

        """
        sorted_theta = sorted(self.eight_theta)
        self.theta_min = sum(sorted_theta[i] for i in range(4))

    def calc_theta_max(self):
        """
        Calculate maximum Theta parameter and return value in degree.

        See Also
        --------
        calc_theta :
            Calculate mean Theta parameter

        """
        sorted_theta = sorted(self.eight_theta)
        self.theta_max = sum(sorted_theta[i] for i in range(4, 8))
