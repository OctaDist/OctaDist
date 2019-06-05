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

import octadist_gui.src.plane
from octadist_gui.src import linear, popup, projection
from octadist_gui import main


def find_bonds(self, fal, fcl, cutoff_global=2.0, cutoff_hydrogen=1.2):
    """
    Find all bond distance and filter the possible bonds.

    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance

    Parameters
    ----------
    fal : list
        List of atomic labels of full complex.
    fcl : list
        List of atomic coordinates of full complex.

    Returns
    -------
    check_2_bond_list : list
        Selected bonds.

    """
    # cutoff_global = main.OctaDist.get_cutoff_global(self)
    # cutoff_hydrogen = main.OctaDist.get_cutoff_hydrogen(self)

    pair_list = []
    bond_list = []
    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            if i == 0:
                distance = linear.euclidean_dist(fcl[i], fcl[j])
            else:
                distance = linear.euclidean_dist(fcl[i], fcl[j])

            pair_list.append([fal[i], fal[j]])
            bond_list.append([fcl[i], fcl[j], distance])

    check_1_bond_list = []
    screen_1_pair_list = []
    for i in range(len(bond_list)):
        if bond_list[i][2] <= cutoff_global:
            check_1_bond_list.append([bond_list[i][0],
                                      bond_list[i][1],
                                      bond_list[i][2]])

            screen_1_pair_list.append([pair_list[i][0],
                                       pair_list[i][1]])

    check_2_bond_list = []
    for i in range(len(check_1_bond_list)):
        if screen_1_pair_list[i][0] == "H" or screen_1_pair_list[i][1] == "H":
            if check_1_bond_list[i][2] <= cutoff_hydrogen:
                check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])

        else:
            check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])

    return check_2_bond_list


def find_faces_octa(c_octa):
    """
    Find the eight faces of octahedral structure.

    1) Choose 3 atoms out of 6 ligand atoms.
        The total number of combination is 20.
    2) Orthogonally project metal center atom onto the face:
        m ----> m'
    3) Calculate the shortest distance between original metal center to its projected point.
    4) Sort the 20 faces in ascending order of the shortest distance.
    5) Delete 12 faces that closest to metal center atom (first 12 faces).
    6) The remaining 8 faces are the (reference) face of octahedral structure.
    7) Find 8 opposite faces.

    Parameters
    ----------
    c_octa : array
        Atomic coordinates of octahedral structure.

    Returns
    -------
    a_ref_f : list
        Atomic labels of reference face.
    c_ref_f : array
        Atomic coordinates of reference face.
    a_oppo_f : list
        Atomic labels of opposite face.
    c_oppo_f : array
        Atomic coordinates of opposite face.

    Examples
    --------
    Reference plane             Opposite plane
        [[1 2 3]                   [[4 5 6]
        [1 2 4]        --->        [3 5 6]
          ...                        ...
        [2 3 5]]                   [1 4 6]]

    """
    ########################
    # Find reference faces #
    ########################

    # Find the shortest distance from metal center to each triangle
    distance = []
    a_ref_f = []
    c_ref_f = []
    for i in range(1, 5):
        for j in range(i + 1, 6):
            for k in range(j + 1, 7):
                a, b, c, d = octadist_gui.src.plane.find_eq_of_plane(c_octa[i],
                                                                     c_octa[j],
                                                                     c_octa[k])
                m = projection.project_atom_onto_plane(c_octa[0], a, b, c, d)
                d_btw = linear.euclidean_dist(m, c_octa[0])
                distance.append(d_btw)

                a_ref_f.append([i, j, k])
                c_ref_f.append([c_octa[i],
                                c_octa[j],
                                c_octa[k]])

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

    for i in range(len(a_ref_f)):
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
            coord_oppo.append([v[int(a_oppo_f[i][j])][0],
                               v[int(a_oppo_f[i][j])][1],
                               v[int(a_oppo_f[i][j])]][2])
        c_oppo_f.append(coord_oppo)

    return a_ref_f, c_ref_f, a_oppo_f, c_oppo_f


def find_surface_area(self, aco):
    """
    Calculate the area of eight triangular faces of octahedral structure.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    Returns
    -------
    None : None

    """
    if len(aco) == 0:
        popup.err_no_file()
        return 1

    wd = tk.Toplevel(self.master)
    wd.wm_iconbitmap(r"..\images\molecule.ico")
    wd.title("The area of triangular face")
    wd.geometry("380x500")
    wd.option_add("*Font", "Arial 10")
    frame = tk.Frame(wd)
    frame.grid()
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")

    for n in range(len(aco)):
        if n > 0:
            box.insert(tk.END, "\n==============================\n\n")

        num, metal, _, coord = aco[n]
        a_ref, c_ref, a_oppo, c_oppo = find_faces_octa(coord)

        box.insert(tk.INSERT, f"Entry: {n + 1}\n")
        box.insert(tk.INSERT, f"Complex no. {num} - Metal: {metal}\n")
        box.insert(tk.END, "                 Atoms*        Area (Å³)\n")

        totalArea = 0
        for i in range(8):
            area = linear.triangle_area(c_ref[i][0], c_ref[i][1], c_ref[i][2])
            box.insert(tk.END, f"Face no. {i + 1}:  {a_ref[i]}      {area:10.6f}\n")
            totalArea += area

        box.insert(tk.END, f"\nThe total surface area:   {totalArea:10.6f}\n")

    box.insert(tk.END, "\n*Three ligand atoms are vertices of triangular face.\n")


def data_complex(self, files, acf):
    """
    Show info of input complex.

    Parameters
    ----------
    files : list
        List containing the names of all input files.
    acf : list
        Atomic labels and coordinates of full complex.

    Returns
    -------
    None : None

    """
    if len(files) == 0:
        popup.err_no_file()
        return 1

    wd = tk.Toplevel(self.master)
    wd.wm_iconbitmap(r"..\images\molecule.ico")
    wd.title("Complex info")
    wd.geometry("550x500")
    wd.option_add("*Font", "Arial 10")
    frame = tk.Frame(wd)
    frame.grid()

    box = tkscrolled.ScrolledText(frame, wrap="word", width="75", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")
    box.delete(1.0, tk.END)

    for i in range(len(files)):
        box.insert(tk.END, f"File {i + 1:>2} : {files[i].split('/')[-1]}\n")
        box.insert(tk.END, f">> Number of atoms: {len(acf[i][0])}\n")
        atoms = list(set(acf[i][0]))
        box.insert(tk.END, f">> List of atoms: {atoms}\n")
        box.insert(tk.END, "\n")


def data_face(self, aco):
    """
    Show info of selected 4 octahedral faces.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    Returns
    -------
    None : None

    """
    if len(aco) == 0:
        popup.err_no_calc()
        return 1

    wd = tk.Toplevel(self.master)
    wd.wm_iconbitmap(r"..\images\molecule.ico")
    wd.title("Selected octahedral faces")
    wd.geometry("550x500")
    wd.option_add("*Font", "Arial 10")
    frame = tk.Frame(wd)
    frame.grid()
    box = tkscrolled.ScrolledText(frame, wrap="word", width="75", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")
    box.delete(1.0, tk.END)

    for n in range(len(aco)):
        if n > 0:
            box.insert(tk.END, "==============================\n\n")

        num, metal, _, coord = aco[n]
        a_ref, c_ref, a_oppo, c_oppo = find_faces_octa(coord)

        box.insert(tk.INSERT, f"Entry: {n + 1}\n")
        box.insert(tk.INSERT, f"Complex no. {num} - Metal: {metal}\n")
        for i in range(4):
            box.insert(tk.END, f"Reference atoms: {a_ref[i]}          Opposite atoms: {a_oppo[i]}\n")
            for j in range(3):
                box.insert(tk.END, f"{c_ref[i][j][0]:9.6f},{c_ref[i][j][1]:9.6f},{c_ref[i][j][2]:9.6f} \t "
                                   f"{c_oppo[i][j][0]:9.6f},{c_oppo[i][j][1]:9.6f},{c_oppo[i][j][2]:9.6f}\n")

            box.insert(tk.END, "\n")


def param_complex(self, acf):
    """
    Show structural parameters of the complex.

    Parameters
    ----------
    acf : list
        Atomic labels and coordinates of full complex.

    Returns
    -------
    None : None

    """
    if len(acf) == 0:
        popup.err_no_file()
        return 1
    elif len(acf) > 1:
        popup.err_many_files()
        return 1

    wd = tk.Toplevel(self.master)
    wd.wm_iconbitmap(r"..\images\molecule.ico")
    wd.title("Results")
    wd.geometry("380x530")
    wd.option_add("*Font", "Arial 10")
    frame = tk.Frame(wd)
    frame.grid()
    lbl = tk.Label(frame, text="Structural parameters of octahedral structure")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=1, pady="5", padx="5")
    box.insert(tk.INSERT, "Bond distance (Å)")

    fal, fcl = acf[0]
    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            distance = linear.euclidean_dist(fcl[i], fcl[j])

            if i == 0:
                texts = f"{fal[i]}-{fal[j]}{j} {distance:10.6f}"

            else:
                texts = f"{fal[i]}{i}-{fal[j]}{j} {distance:10.6f}"

            box.insert(tk.END, "\n" + texts)

    box.insert(tk.END, "\n\nBond angle (°)")

    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            for k in range(j + 1, len(fcl)):
                vec1 = fcl[i] - fcl[j]
                vec2 = fcl[k] - fcl[j]
                angle = linear.angle_btw_vectors(vec1, vec2)

                if i == 0:
                    texts = f"{fal[k]}{k}-{fal[i]}-{fal[j]}{j} {angle:10.6f}"

                else:
                    texts = f"{fal[k]}{k}-{fal[i]}{i}-{fal[j]}{j} {angle:10.6f}"

                box.insert(tk.END, "\n" + texts)

    box.insert(tk.END, "\n")


def param_octa(self, aco):
    """
    Show structural parameters of selected octahedral structure.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    Returns
    -------
    None : None

    """
    if len(aco) == 0:
        popup.err_no_file()
        return 1

    wd = tk.Toplevel(self.master)
    wd.wm_iconbitmap(r"..\images\molecule.ico")
    wd.title("Results")
    wd.geometry("380x530")
    wd.option_add("*Font", "Arial 10")
    frame = tk.Frame(wd)
    frame.grid()
    lbl = tk.Label(frame, text="Structural parameters of octahedral structure")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=1, pady="5", padx="5")

    for n in range(len(aco)):
        if n > 0:  # separator between files
            box.insert(tk.END, "\n\n=================================\n\n")

        box.insert(tk.INSERT, f"File : {aco[n][0]}\n")
        box.insert(tk.END, f"Metal: {aco[n][1]}\n")
        box.insert(tk.END, "Bond distance (Å)")

        for i in range(7):
            for j in range(i + 1, 7):
                distance = linear.euclidean_dist(aco[n][3][i], aco[n][3][j])

                if i == 0:
                    texts = f"{aco[n][2][i]}-{aco[n][2][j]}{j} {distance:10.6f}"

                else:
                    texts = f"{aco[n][2][i]}{i}-{aco[n][2][j]}{j} {distance:10.6f}"

                box.insert(tk.END, "\n" + texts)

        box.insert(tk.END, "\n\nBond angle (°)")

        for i in range(7):
            for j in range(i + 1, 7):
                for k in range(j + 1, 7):
                    vec1 = aco[n][3][i] - aco[n][3][j]
                    vec2 = aco[n][3][k] - aco[n][3][j]
                    angle = linear.angle_btw_vectors(vec1, vec2)

                    if i == 0:
                        texts = f"{aco[n][2][k]}{k}-{aco[n][2][i]}-{aco[n][2][j]}{j} {angle:10.6f}"

                    else:
                        texts = f"{aco[n][2][k]}{k}-{aco[n][2][i]}{i}-{aco[n][2][j]}{j} {angle:10.6f}"

                    box.insert(tk.END, "\n" + texts)

        box.insert(tk.END, "\n")
