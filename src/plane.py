"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import linear
import projection
import main


def find_8_faces(self, c_octa):
    """Find 8 faces of octahedral structure for computing Theta parameter using algorithm 1

    1) Choose 3 atoms out of 6 ligand atoms. The total number of combination is 20
    2) Orthogonally project metal center atom onto the face: m ----> m'
    3) Calculate the shortest distance between original metal center to its projected point
    4) Sort the 20 faces in ascending order of the shortest distance
    5) Delete 12 faces that closest to metal center atom (first 12 faces)
    6) The remaining 8 faces are the (reference) face of octahedral structure
    7) Find 8 opposite faces
    
    For example,

         Reference plane            Opposite plane
            [[1 2 3]                   [[4 5 6]
             [1 2 4]        --->        [3 5 6]
               ...                        ...
             [2 3 5]]                   [1 4 6]]

    :param c_octa: array - XYZ coordinate of a metal center atom and six ligand atoms
    :return a_ref_f: list - atom of reference face of octahedral structure
    :return c_ref_f: array - coordinate of reference face of octahedral structure
    :return a_oppo_f: list - atom of opposite face of octahedral structure
    :return c_oppo_f: array - coordinate of opposite face of octahedral structure
    """
    # Find the shortest distance from metal center to each triangle
    main.print_stdout(self, "Info: Find the reference and opposite faces of octahedral structure")

    #######################
    # Find reference faces
    #######################

    distance = []
    a_ref_f = []
    c_ref_f = []
    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = find_eq_of_plane(c_octa[i], c_octa[j], c_octa[k])
                m = projection.project_atom_onto_plane(c_octa[0], a, b, c, d)
                d_btw = linear.distance_between(m, c_octa[0])
                distance.append(d_btw)
                a_ref_f.append([i, j, k])
                c_ref_f.append([c_octa[i], c_octa[j], c_octa[k]])

    # Sort faces by distance in ascending order
    dist_a_c = list(zip(distance, a_ref_f, c_ref_f))
    dist_a_c.sort()
    distance, a_ref_f, c_ref_f = list(zip(*dist_a_c))
    c_ref_f = np.asarray(c_ref_f)

    # Remove first 12 triangles, the rest of triangles is 8 faces of octahedron
    a_ref_f = a_ref_f[12:]
    c_ref_f = c_ref_f[12:]

    #######################
    # Find opposite faces
    #######################

    all_atom = [1, 2, 3, 4, 5, 6]
    a_oppo_f = []
    # loop over 4 reference planes
    for i in range(len(a_ref_f)):
        # Find atoms of opposite plane
        new_a_ref_f = []
        for j in all_atom:
            if j not in (a_ref_f[i][0], a_ref_f[i][1], a_ref_f[i][2]):
                new_a_ref_f.append(j)
        a_oppo_f.append(new_a_ref_f)

    v = np.array(c_octa)
    c_oppo_f = []
    for i in range(len(a_oppo_f)):
        coord_oppo = []
        for j in range(3):
            coord_oppo.append([v[int(a_oppo_f[i][j])][0], v[int(a_oppo_f[i][j])][1], v[int(a_oppo_f[i][j])]][2])
        c_oppo_f.append(coord_oppo)

    ################
    # Show results
    ################
    main.print_stdout(self, "Info: Show 8 pairs of the opposite faces")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Pair   Reference    Opposite")
    main.print_stdout(self, "               face         face")
    main.print_stdout(self, "      ----   ---------    ---------")
    for i in range(len(a_oppo_f)):
        main.print_stdout(self, "        {0}    {1}    {2}".format(i + 1, a_ref_f[i], a_oppo_f[i]))
    main.print_stdout(self, "")
    # Print new face list after unwanted 12 triangles plane excluded
    main.print_stdout(self, "Info: Show the reference face")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Face    Atom         X           Y           Z")
    main.print_stdout(self, "      ----    ----     ---------   ---------   ---------")
    for i in range(len(c_ref_f)):
        main.print_stdout(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                          .format(a_ref_f[i][0], c_ref_f[i][0][0], c_ref_f[i][0][1], c_ref_f[i][0][2]))
        main.print_stdout(self, "        {0}       {1}     {2:10.6f}  {3:10.6f}  {4:10.6f}"
                          .format(i + 1, a_ref_f[i][1], c_ref_f[i][1][0], c_ref_f[i][1][1], c_ref_f[i][1][2]))
        main.print_stdout(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                          .format(a_ref_f[i][2], c_ref_f[i][2][0], c_ref_f[i][2][1], c_ref_f[i][2][2]))
        main.print_stdout(self, "      --------------------------------------------------")
    main.print_stdout(self, "")
    main.print_stdout(self, "Info: Show the opposite faces")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Face    Atom         X           Y           Z")
    main.print_stdout(self, "      ----    ----     ---------   ---------   ---------")

    for i in range(len(a_oppo_f)):
        main.print_stdout(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                          .format(a_oppo_f[i][0], c_oppo_f[i][0][0], c_oppo_f[i][0][1], c_oppo_f[i][0][2]))
        main.print_stdout(self, "        {0}       {1}     {2:10.6f}  {3:10.6f}  {4:10.6f}"
                          .format(i + 1, a_oppo_f[i][1], c_oppo_f[i][1][0], c_oppo_f[i][1][1], c_oppo_f[i][1][2]))
        main.print_stdout(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                          .format(a_oppo_f[i][2], c_oppo_f[i][2][0], c_oppo_f[i][2][1], c_oppo_f[i][2][2]))
        main.print_stdout(self, "      --------------------------------------------------")
    main.print_stdout(self, "")

    return a_ref_f, c_ref_f, a_oppo_f, c_oppo_f


def find_eq_of_plane(x, y, z):
    """Find the equation of plane of given three points (ligand atoms)
    The general form of plane equation is Ax + By + Cz = D
    where A, B, C, and D are coefficient. They can be computed using cross product definition

    -->    -->
    XZ  X  XY = (a, b, c)

    d = (a, b, c).Z

    :param x: array - point 1
    :param y: array - point 2
    :param z: array - point 3
    :return a, b, c, d: float - coefficients of the equation of the given plane
    """
    xz = z - x
    xy = y - x
    cross_vector = np.cross(xz, xy)
    a, b, c = cross_vector
    d = np.dot(cross_vector, z)

    return a, b, c, d
