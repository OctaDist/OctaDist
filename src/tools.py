"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import linear
import tkinter as tk
import tkinter.scrolledtext as tkscrolled


def show_data_summary(lf, facl):
    """Show info of input complex
    
    :param lf: list_file - list containing the names of all input files
    :param facl: full_atom_coord_list 
    :return: 
    """

    print("Command: Show general information of all complexes")

    window = tk.Tk()
    window.option_add("*Font", "Arial 10")
    window.geometry("380x500")
    window.title("Complex info")

    Box = tkscrolled.ScrolledText(window, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=0, pady="5", padx="5")

    Box.delete(1.0, tk.END)

    for i in range(len(lf)):
        texts = "File {0:>2} : {1}".format(i + 1, lf[i].split('/')[-1])
        Box.insert(tk.END, texts)
        atoms = list(set(facl[i][0]))
        texts = ">> Number of atoms: {0}".format(len(facl[i][0]))
        Box.insert(tk.END, "\n" + texts)
        texts = ">> List of atoms: {0}".format(atoms)
        Box.insert(tk.END, "\n" + texts + "\n\n")

    window.mainloop()


def show_results_mult(computed_results):
    """Show the computed octahedral distortion parameters of all selected files

    :param computed_results: list - computed Delta, Sigma, and Theta values
    :return: show the results in new text box
    """

    multi = tk.Tk()
    multi.option_add("*Font", "Arial 10")
    multi.geometry("380x530")
    multi.title("Results")

    lbl = tk.Label(multi, text="Computed octahedral distortion parameters for all complexes")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    Box = tkscrolled.ScrolledText(multi, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=1, pady="5", padx="5")

    texts = "                            Δ               Σ                Θ\n" \
            "                        -----------    -------------     ------------"
    Box.insert(tk.INSERT, texts)

    for i in range(len(computed_results)):
        texts = "Complex {0} : {1:10.6f}   {2:10.6f}   {3:10.6f}" \
            .format(i + 1, computed_results[i][0], computed_results[i][1], computed_results[i][2])
        Box.insert(tk.END, "\n" + texts)

    multi.mainloop()


def calc_strct_param_octa(al, cl):
    """Show structural parameters of selected complex

    :param al: atom_list
    :param cl: coord_list
    :return: bond distance and bond angle
    """

    print("Command: Show structural parameters of truncated octahedron")

    window = tk.Tk()
    window.option_add("*Font", "Arial 10")
    window.geometry("380x530")
    window.title("Results")

    lbl = tk.Label(window, text="Structural parameters of octahedral structure")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    Box = tkscrolled.ScrolledText(window, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=1, pady="5", padx="5")

    texts = "Bond distance (Å)"
    Box.insert(tk.INSERT, texts)

    for i in range(len(cl)):
        for j in range(i + 1, len(cl)):
            if i == 0:
                distance = linear.distance_between(cl[i], cl[j])
                texts = "{0}-{1}{2} {3:10.6f}".format(al[i], al[j], j, distance)
            else:
                distance = linear.distance_between(cl[i], cl[j])
                texts = "{0}{1}-{2}{3} {4:10.6f}".format(al[i], i, al[j], j, distance)

            Box.insert(tk.END, "\n" + texts)

    texts = "Bond angle (°)"
    Box.insert(tk.END, "\n\n" + texts)

    for i in range(len(cl)):
        for j in range(i + 1, len(cl)):
            for k in range(j + 1, len(cl)):
                if i == 0:
                    angle = linear.angle_between(cl[j], cl[i], cl[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}" \
                        .format(al[k], k, al[i], al[j], j, angle)
                else:
                    angle = linear.angle_between(cl[j], cl[i], cl[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}" \
                        .format(al[k], k, al[i], i, al[j], j, angle)

                Box.insert(tk.END, "\n" + texts)

    Box.insert(tk.END, "\n")

    window.mainloop()


def calc_strct_param_full(fal, fcl):
    """Show structural parameters of selected complex

    :param fal: full_atom_list
    :param fcl: full_coord_list
    :return: bond distance and bond angle
    """

    print("Command: Show structural parameters of full complex")

    window = tk.Tk()
    window.option_add("*Font", "Arial 10")
    window.geometry("380x530")
    window.title("Results")

    lbl = tk.Label(window, text="Structural parameters of octahedral structure")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    Box = tkscrolled.ScrolledText(window, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=1, pady="5", padx="5")

    texts = "Bond distance (Å)"
    Box.insert(tk.INSERT, texts)

    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            if i == 0:
                distance = linear.distance_between(fcl[i], fcl[j])
                texts = "{0}-{1}{2} {3:10.6f}".format(fal[i], fal[j], j, distance)
            else:
                distance = linear.distance_between(fcl[i], fcl[j])
                texts = "{0}{1}-{2}{3} {4:10.6f}".format(fal[i], i, fal[j], j, distance)

            Box.insert(tk.END, "\n" + texts)

    texts = "Bond angle (°)"
    Box.insert(tk.END, "\n\n" + texts)

    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            for k in range(j + 1, len(fcl)):
                if i == 0:
                    angle = linear.angle_between(fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}" \
                        .format(fal[k], k, fal[i], fal[j], j, angle)
                else:
                    angle = linear.angle_between(fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}" \
                        .format(fal[k], k, fal[i], i, fal[j], j, angle)

                Box.insert(tk.END, "\n" + texts)

    Box.insert(tk.END, "\n")

    window.mainloop()


def calc_bond_distance(fal, fcl):
    """Show bond distance of atoms pair
    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance
    - Return the remaining bonds

    :param fal: full_atom_list
    :param fcl: full_coord_list
    :return check_2_bond_list: selected bonds
    """

    cutoff_distance = 2.0
    hydrogen_cutoff_distance = 1.2

    print("Command: Determine correct bonds for atoms pair")
    print("         Distance cut-off is %s Angstroms" % cutoff_distance)

    bond_list = []
    pair_list = []

    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
            if i == 0:
                distance = linear.distance_between(fcl[i], fcl[j])
                # print("         {0}-{1}{2} {3:10.6f}".format(fal[i], fal[j], j, distance))
            else:
                distance = linear.distance_between(fcl[i], fcl[j])
                # print("         {0}{1}-{2}{3} {4:10.6f}".format(fal[i], i, fal[j], j, distance))

            bond_list.append([fcl[i], fcl[j], distance])
            pair_list.append([fal[i], fal[j]])

    check_1_bond_list = []
    screen_1_pair_list = []

    for i in range(len(bond_list)):
        if bond_list[i][2] <= cutoff_distance:
            check_1_bond_list.append([bond_list[i][0], bond_list[i][1], bond_list[i][2]])
            screen_1_pair_list.append([pair_list[i][0], pair_list[i][1]])

    check_2_bond_list = []

    for i in range(len(check_1_bond_list)):
        if screen_1_pair_list[i][0] == "H" or screen_1_pair_list[i][1] == "H":
            if check_1_bond_list[i][2] <= hydrogen_cutoff_distance:
                check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])
        else:
            check_2_bond_list.append([check_1_bond_list[i][0], check_1_bond_list[i][1]])

    print("\n         Total number of bonds before screening: %4s" % len(bond_list))
    print("         Total number of bonds after screening : %4s\n" % len(check_2_bond_list))

    return check_2_bond_list


def calc_surface_area(pal, pcl):
    """Calculate the area of triangular face

    :param pal: plane_atom_list
    :param pcl: plane_coord_list
    :return: surface area of face
    """

    print("Command: Show the area of the triangular faces of truncated octahedron")

    window = tk.Tk()
    window.option_add("*Font", "Arial 10")
    window.geometry("380x500")
    window.title("The area of triangular face")

    Box = tkscrolled.ScrolledText(window, wrap="word", width="50", height="30", undo="True")
    Box.grid(row=0, pady="5", padx="5")

    texts = "                    Atoms*        Area (Å³)"
    Box.insert(tk.INSERT, texts)

    for i in range(8):
        area = linear.triangle_area(pcl[i][0], pcl[i][1], pcl[i][2])
        texts = "Face no. {0}:  {1}      {2:10.6f}".format(i + 1, pal[i], area)
        Box.insert(tk.END, "\n" + texts)

    Box.insert(tk.END, "\n\n\n*Three ligand atoms are vertices of triangular face.\n")

    window.mainloop()
