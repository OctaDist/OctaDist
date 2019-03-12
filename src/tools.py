"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import popup
import linear
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import matplotlib.pyplot as plt
import main


def data_complex(self, fl, facl):
    """Show info of input complex

    :param self: master frame
    :param fl: file_list - list containing the names of all input files
    :param facl: full_atom_coord_list
    :return:
    """
    if len(fl) == 0:
        popup.err_no_file(self)
        return 1

    main.print_stdout(self, "Info: Show info of input complex")
    main.print_stdout(self, "")

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
    :return:
    """
    if len(sfa) == 0:
        popup.err_no_calc(self)
        return 1

    main.print_stdout(self, "Info: Show info of selected 4 octahedral faces")
    main.print_stdout(self, "")

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


def multi_results(self, comp_result):
    """Show the computed octahedral distortion parameters of all complexes

    :param self: master frame
    :param comp_result: list - computed Delta, Sigma, and Theta values
    :return:
    """
    master = tk.Toplevel(self.master)
    master.title("Results")
    master.geometry("380x330")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()
    lbl = tk.Label(frame, text="Computed octahedral distortion parameters for all complexes")
    lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=1, pady="5", padx="5")

    box.insert(tk.INSERT, "                         Δ               Σ                Θ\n")
    box.insert(tk.INSERT, "                     -----------    -------------     ------------\n")
    for i in range(len(comp_result)):
        box.insert(tk.END, "Complex {0} : {1:10.6f}   {2:10.6f}   {3:10.6f}\n"
                   .format(i+1, comp_result[i][0], comp_result[i][1], comp_result[i][2]))


def param_octa(self, al, cl):
    """Show structural parameters of selected octahedral structure

    :param self: master frame
    :param al: list - atom_list
    :param cl: array - coord_list
    :return:
    """
    if len(al) == 0:
        popup.err_no_calc(self)
        return 1
    elif len(al) > 1:
        popup.err_many_files(self)
        return 1

    main.print_stdout(self, "Info: Show structural parameters of selected octahedral structure")
    main.print_stdout(self, "")

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

    box.insert(tk.INSERT, "Bond distance (Å)")
    for i in range(len(cl)):
        for j in range(i+1, len(cl)):
            if i == 0:
                distance = linear.distance_between(cl[i], cl[j])
                texts = "{0}-{1}{2} {3:10.6f}".format(al[i], al[j], j, distance)
            else:
                distance = linear.distance_between(cl[i], cl[j])
                texts = "{0}{1}-{2}{3} {4:10.6f}".format(al[i], i, al[j], j, distance)
            box.insert(tk.END, "\n" + texts)

    box.insert(tk.END, "\n\nBond angle (°)")
    for i in range(len(cl)):
        for j in range(i+1, len(cl)):
            for k in range(j+1, len(cl)):
                if i == 0:
                    angle = linear.angle_between(self, cl[j], cl[i], cl[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(al[k], k, al[i], al[j], j, angle)
                else:
                    angle = linear.angle_between(self, cl[j], cl[i], cl[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(al[k], k, al[i], i, al[j], j, angle)
                box.insert(tk.END, "\n" + texts)
    box.insert(tk.END, "\n")


def param_complex(self, acf):
    """Show structural parameters of the complex

    :param self: master frame
    :param acf: list - atom_coord_full
    :return:
    """
    if len(acf) == 0:
        popup.err_no_file(self)
        return 1
    elif len(acf) > 1:
        popup.err_many_files(self)
        return 1

    main.print_stdout(self, "Info: Show structural parameters of the complex")
    main.print_stdout(self, "")

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
        for j in range(i+1, len(fcl)):
            if i == 0:
                distance = linear.distance_between(fcl[i], fcl[j])
                texts = "{0}-{1}{2} {3:10.6f}".format(fal[i], fal[j], j, distance)
            else:
                distance = linear.distance_between(fcl[i], fcl[j])
                texts = "{0}{1}-{2}{3} {4:10.6f}".format(fal[i], i, fal[j], j, distance)
            box.insert(tk.END, "\n" + texts)

    box.insert(tk.END, "\n\nBond angle (°)")
    for i in range(len(fcl)):
        for j in range(i+1, len(fcl)):
            for k in range(j+1, len(fcl)):
                if i == 0:
                    angle = linear.angle_between(self, fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(fal[k], k, fal[i], fal[j], j, angle)
                else:
                    angle = linear.angle_between(self, fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(fal[k], k, fal[i], i, fal[j], j, angle)
                box.insert(tk.END, "\n" + texts)
    box.insert(tk.END, "\n")


def show_surface_area(self, pal, pcl):
    """Calculate the area of triangular face

    :param self: master frame
    :param pal: list - plane_atom_list
    :param pcl: array - plane_coord_list
    :return:
    """
    if len(pal) == 0:
        popup.err_no_calc(self)
        return 1

    main.print_stdout(self, "Info: Show the area of triangular face of octahedron")
    main.print_stdout(self, "")

    master = tk.Toplevel(self.master)
    master.title("The area of triangular face")
    master.geometry("380x500")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")
    box.insert(tk.INSERT, "                 Atoms*        Area (Å³)\n")
    for i in range(8):
        area = linear.triangle_area(pcl[i][0], pcl[i][1], pcl[i][2])
        box.insert(tk.END, "Face no. {0}:  {1}      {2:10.6f}\n".format(i+1, pal[i], area))

    box.insert(tk.END, "\n\n\n*Three ligand atoms are vertices of triangular face.\n")


def show_plot_angles(self, s, t):
    """Plot graph between Sigma and Theta parameters for multiple files

    :param self: master frame
    :param s: array - computed Sigma parameter
    :param t: array - computed Theta parameter
    :return:
    """
    if len(s) == 0:
        popup.err_no_calc(self)
        return 1

    main.print_stdout(self, "Info: Show relationship plot between Σ and Θ")
    main.print_stdout(self, "")

    ax = plt.subplot()
    for i in range(len(s)):
        ax.scatter(s, t, label='Complex {0}'.format(i+1))
        ax.text(s[i] + 0.2, t[i] + 0.2, i+1, fontsize=9)

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)

    plt.title("Relationship plot between $\Sigma$ and $\Theta$")
    plt.xlabel(r'$\Sigma$')
    plt.ylabel(r'$\Theta$')
    plt.show()


def calc_bond_distance(self, fal, fcl):
    """Show bond distance of atoms pair
    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance

    :param self: master frame
    :param fal: list - full_atom_list
    :param fcl: array - full_coord_list
    :return check_2_bond_list: list - selected bonds
    """
    global_distance_cutoff = 2.0
    hydrogen_distance_cutoff = 1.2

    pair_list = []
    bond_list = []
    for i in range(len(fcl)):
        for j in range(i+1, len(fcl)):
            if i == 0:
                distance = linear.distance_between(fcl[i], fcl[j])
            else:
                distance = linear.distance_between(fcl[i], fcl[j])

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

    main.print_stdout(self, "Info: Determine the correct bond for atoms pair")
    main.print_stdout(self, "Info: Global distance cutoff       : {0} Angstrom".format(global_distance_cutoff))
    main.print_stdout(self, "Info: Distance cutoff for Hydrogen : {0} Angstrom".format(hydrogen_distance_cutoff))
    main.print_stdout(self, "")
    main.print_stdout(self, "      Total number of bonds before screening    : {0:5d}".format(len(bond_list)))
    main.print_stdout(self, "      Total number of bonds after 1st screening : {0:5d}".format(len(check_1_bond_list)))
    main.print_stdout(self, "      Total number of bonds after 2nd screening : {0:5d}".format(len(check_2_bond_list)))
    main.print_stdout(self, "")

    return check_2_bond_list
