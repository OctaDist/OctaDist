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
from tkinter import scrolledtext as tkscrolled

import numpy as np

from octadist_gui.src import echo_logs, linear, popup, projection


def data_complex(self, fl, facl):
    """Show info of input complex

    :param self: master frame
    :param fl: list containing the names of all input files
    :param facl: atomic labels and coordinates of full complex
    :type fl: list
    :type facl: list
    """
    if len(fl) == 0:
        popup.err_no_file(self)
        return 1

    echo_logs(self, "Info: Show info of input complex")
    echo_logs(self, "")

    master = tk.Toplevel(self.master)
    master.title("Complex info")
    master.geometry("550x500")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()

    box = tkscrolled.ScrolledText(frame, wrap="word", width="75", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")
    box.delete(1.0, tk.END)

    for i in range(len(fl)):
        box.insert(tk.END, "File {0:>2} : {1}\n".format(i + 1, fl[i].split('/')[-1]))
        box.insert(tk.END, ">> Number of atoms: {0}\n".format(len(facl[i][0])))
        atoms = list(set(facl[i][0]))
        box.insert(tk.END, ">> List of atoms: {0}".format(atoms) + "\n\n")


def data_face(self, sfa, sfc, sofa, sofc):
    """Show info of selected 4 octahedral faces

    :param self: master frame
    :param sfa: selected face atom
    :param sfc: selected face coordinates
    :param sofa: selected opposite face atom
    :param sofc: selected opposite face coordinates
    :type sfa: list
    :type sfc: list
    :type sofa: list
    :type sofc: list
    """
    if len(sfa) == 0:
        popup.err_no_calc(self)
        return 1

    echo_logs(self, "Info: Show info of selected 4 octahedral faces")
    echo_logs(self, "")

    master = tk.Toplevel(self.master)
    master.title("Selected octahedral faces")
    master.geometry("550x500")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()
    box = tkscrolled.ScrolledText(frame, wrap="word", width="75", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")
    box.delete(1.0, tk.END)

    for i in range(4):
        box.insert(tk.END, "Reference atoms: {0}          Opposite atoms: {1}\n".format(sfa[i], sofa[i]))
        for j in range(3):
            box.insert(tk.END, "{0:9.6f},{1:9.6f},{2:9.6f} \t {3:9.6f},{4:9.6f},{5:9.6f}\n"
                       .format(sfc[i][j][0], sfc[i][j][1], sfc[i][j][2], sofc[i][j][0], sofc[i][j][1], sofc[i][j][2]))
        box.insert(tk.END, "\n\n")


def param_complex(self, acf):
    """Show structural parameters of the complex

    :param self: master frame
    :param acf: atomic labels and coordinates of full complex
    :type acf: list
    """
    if len(acf) == 0:
        popup.err_no_file(self)
        return 1
    elif len(acf) > 1:
        popup.err_many_files(self)
        return 1

    echo_logs(self, "Info: Show structural parameters of the complex")
    echo_logs(self, "")

    master = tk.Toplevel(self.master)
    master.title("Results")
    master.geometry("380x530")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()
    lbl = tk.Label(frame, text="Structural parameters of octahedral structure")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=1, pady="5", padx="5")

    fal, fcl = acf[0]

    box.insert(tk.INSERT, "Bond distance (Å)")
    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            if i == 0:
                distance = linear.distance_bwn_points(fcl[i], fcl[j])
                texts = "{0}-{1}{2} {3:10.6f}".format(fal[i], fal[j], j, distance)
            else:
                distance = linear.distance_bwn_points(fcl[i], fcl[j])
                texts = "{0}{1}-{2}{3} {4:10.6f}".format(fal[i], i, fal[j], j, distance)
            box.insert(tk.END, "\n" + texts)

    box.insert(tk.END, "\n\nBond angle (°)")
    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            for k in range(j + 1, len(fcl)):
                if i == 0:
                    angle = linear.angle_btw_3vec(self, fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(fal[k], k, fal[i], fal[j], j, angle)
                else:
                    angle = linear.angle_btw_3vec(self, fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(fal[k], k, fal[i], i, fal[j], j, angle)
                box.insert(tk.END, "\n" + texts)
    box.insert(tk.END, "\n")


def param_octa(self, aco):
    """Show structural parameters of selected octahedral structure

    :param self: master frame
    :param aco: atomic labels and coordinates of octahedral structure
    :type aco: list
    """
    if len(aco) == 0:
        popup.err_no_file(self)
        return 1

    echo_logs(self, "Info: Show structural parameters of selected octahedral structure")
    echo_logs(self, "")

    master = tk.Toplevel(self.master)
    master.title("Results")
    master.geometry("380x530")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()
    lbl = tk.Label(frame, text="Structural parameters of octahedral structure")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=1, pady="5", padx="5")

    for n in range(len(aco)):
        if n > 0:  # separator between files
            box.insert(tk.END, "\n\n=================================\n\n")

        box.insert(tk.INSERT, "File : {0}".format(aco[n][0]))
        box.insert(tk.END, "\nMetal: {0}".format(aco[n][1]))
        box.insert(tk.END, "\nBond distance (Å)")
        for i in range(7):
            for j in range(i + 1, 7):
                if i == 0:
                    distance = linear.distance_bwn_points(aco[n][3][i], aco[n][3][j])
                    texts = "{0}-{1}{2} {3:10.6f}".format(aco[n][2][i], aco[n][2][j], j, distance)
                else:
                    distance = linear.distance_bwn_points(aco[n][3][i], aco[n][3][j])
                    texts = "{0}{1}-{2}{3} {4:10.6f}".format(aco[n][2][i], i, aco[n][2][j], j, distance)
                box.insert(tk.END, "\n" + texts)

        box.insert(tk.END, "\n\nBond angle (°)")
        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    if i == 0:
                        angle = linear.angle_btw_3vec(self, aco[n][3][j], aco[n][3][i], aco[n][3][k])
                        texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(aco[n][2][k], k, aco[n][2][i], aco[n][2][j], j,
                                                                     angle)
                    else:
                        angle = linear.angle_btw_3vec(self, aco[n][3][j], aco[n][3][i], aco[n][3][k])
                        texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(aco[n][2][k], k, aco[n][2][i], i, aco[n][2][j],
                                                                        j, angle)
                    box.insert(tk.END, "\n" + texts)
        box.insert(tk.END, "\n")


def find_bonds(self, fal, fcl):
    """Find all bond distance and filter the possible bonds

    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance

    :param self: master frame
    :param fal: list of atomic labels of full complex
    :param fcl: list of atomic coordinates of full complex
    :type fal: list
    :type fcl: list
    :return check_2_bond_list: selected bonds
    :rtype check_2_bond_list: list
    """
    global_distance_cutoff = 2.0
    hydrogen_distance_cutoff = 1.2

    pair_list = []
    bond_list = []
    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            if i == 0:
                distance = linear.distance_bwn_points(fcl[i], fcl[j])
            else:
                distance = linear.distance_bwn_points(fcl[i], fcl[j])

            pair_list.append([fal[i], fal[j]])
            bond_list.append([fcl[i], fcl[j], distance])

    check_1_bond_list = []
    screen_1_pair_list = []
    for i in range(len(bond_list)):
        if bond_list[i][2] <= global_distance_cutoff:
            check_1_bond_list.append([bond_list[i][0], bond_list[i][1], bond_list[i][2]])
            screen_1_pair_list.append([pair_list[i][0], pair_list[i][1]])

    check_2_bond_list = []
    for i in range(len(check_1_bond_list)):
        if screen_1_pair_list[i][0] == "H" or screen_1_pair_list[i][1] == "H":
            if check_1_bond_list[i][2] <= hydrogen_distance_cutoff:
                check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])
        else:
            check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])

    echo_logs(self, "Info: Determine the correct bond for atoms pair")
    echo_logs(self, "Info: Global distance cutoff       : {0} Angstrom".format(global_distance_cutoff))
    echo_logs(self, "Info: Distance cutoff for Hydrogen : {0} Angstrom".format(hydrogen_distance_cutoff))
    echo_logs(self, "")
    echo_logs(self, "      Total number of bonds before screening    : {0:5d}".format(len(bond_list)))
    echo_logs(self, "      Total number of bonds after 1st screening : {0:5d}".format(len(check_1_bond_list)))
    echo_logs(self, "      Total number of bonds after 2nd screening : {0:5d}".format(len(check_2_bond_list)))
    echo_logs(self, "")

    return check_2_bond_list


def find_faces_octa(self, c_octa):
    """Find the eight faces of octahedral structure

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

    :param self: master frame
    :param c_octa: atomic coordinates of octahedral structure
    :type c_octa: list, array, tuple    :return a_ref_f: list - atomic labels of reference face
    :return a_ref_f: atomic labels of reference face
    :return c_ref_f: atomic coordinates of reference face
    :return a_oppo_f: atomic labels of opposite face
    :return c_oppo_f: atomic coordinates of opposite face
    :rtype a_ref_f: list
    :rtype c_ref_f: array
    :rtype a_oppo_f: list
    :rtype c_oppo_f: array
    """
    ########################
    # Find reference faces #
    ########################

    echo_logs(self, "Info: Find the reference and opposite faces of octahedral structure")

    # Find the shortest distance from metal center to each triangle
    distance = []
    a_ref_f = []
    c_ref_f = []
    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = linear.find_eq_of_plane(c_octa[i], c_octa[j], c_octa[k])
                m = projection.project_atom_onto_plane(c_octa[0], a, b, c, d)
                d_btw = linear.distance_bwn_points(m, c_octa[0])
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
    # Find opposite faces #
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
    # Show results #
    ################

    echo_logs(self, "Info: Show 8 pairs of the opposite faces")
    echo_logs(self, "")
    echo_logs(self, "      Pair   Reference    Opposite")
    echo_logs(self, "               face         face")
    echo_logs(self, "      ----   ---------    ---------")
    for i in range(len(a_oppo_f)):
        echo_logs(self, "        {0}    {1}    {2}".format(i + 1, a_ref_f[i], a_oppo_f[i]))
    echo_logs(self, "")
    # Print new face list after unwanted 12 triangles plane excluded
    echo_logs(self, "Info: Show the reference face")
    echo_logs(self, "")
    echo_logs(self, "      Face    Atom         X           Y           Z")
    echo_logs(self, "      ----    ----     ---------   ---------   ---------")
    for i in range(len(c_ref_f)):
        echo_logs(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                  .format(a_ref_f[i][0], c_ref_f[i][0][0], c_ref_f[i][0][1], c_ref_f[i][0][2]))
        echo_logs(self, "        {0}       {1}     {2:10.6f}  {3:10.6f}  {4:10.6f}"
                  .format(i + 1, a_ref_f[i][1], c_ref_f[i][1][0], c_ref_f[i][1][1], c_ref_f[i][1][2]))
        echo_logs(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                  .format(a_ref_f[i][2], c_ref_f[i][2][0], c_ref_f[i][2][1], c_ref_f[i][2][2]))
        echo_logs(self, "      --------------------------------------------------")
    echo_logs(self, "")
    echo_logs(self, "Info: Show the opposite faces")
    echo_logs(self, "")
    echo_logs(self, "      Face    Atom         X           Y           Z")
    echo_logs(self, "      ----    ----     ---------   ---------   ---------")

    for i in range(len(a_oppo_f)):
        echo_logs(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                  .format(a_oppo_f[i][0], c_oppo_f[i][0][0], c_oppo_f[i][0][1], c_oppo_f[i][0][2]))
        echo_logs(self, "        {0}       {1}     {2:10.6f}  {3:10.6f}  {4:10.6f}"
                  .format(i + 1, a_oppo_f[i][1], c_oppo_f[i][1][0], c_oppo_f[i][1][1], c_oppo_f[i][1][2]))
        echo_logs(self, "                {0}     {1:10.6f}  {2:10.6f}  {3:10.6f}"
                  .format(a_oppo_f[i][2], c_oppo_f[i][2][0], c_oppo_f[i][2][1], c_oppo_f[i][2][2]))
        echo_logs(self, "      --------------------------------------------------")
    echo_logs(self, "")

    return a_ref_f, c_ref_f, a_oppo_f, c_oppo_f


def find_surface_area(self, all_face):
    """Calculate the area of eight triangular faces of octahedral structure

    :param self: master frame
    :param all_face: atomic labels and coordinates of 8 faces
    :type all_face: list
    """
    if len(all_face) == 0:
        popup.err_no_calc(self)
        return 1

    echo_logs(self, "Info: Show the area of triangular face of octahedron")
    echo_logs(self, "")

    master = tk.Toplevel(self.master)
    master.title("The area of triangular face")
    master.geometry("380x500")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")

    for n in range(len(all_face)):
        if n > 0:
            box.insert(tk.END, "\n==============================\n\n")

        face_data = all_face[n]
        a_ref, c_ref, a_oppo, c_oppo = face_data

        box.insert(tk.INSERT, "Octahedral structure no. {0}\n".format(n + 1))
        box.insert(tk.END, "                 Atoms*        Area (Å³)\n")

        totalArea = 0
        for i in range(8):
            area = linear.triangle_area(c_ref[i][0], c_ref[i][1], c_ref[i][2])
            box.insert(tk.END, "Face no. {0}:  {1}      {2:10.6f}\n".format(i + 1, a_ref[i], area))
            totalArea += area
        box.insert(tk.END, "\nThe total surface area:   {0:10.6f}\n".format(totalArea))

    box.insert(tk.END, "\n*Three ligand atoms are vertices of triangular face.\n")
