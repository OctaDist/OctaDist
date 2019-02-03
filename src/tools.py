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


class ShowData:
    def __init__(self, master, lf, facl):
        """Show info of input complex

        :param lf: list_file - list containing the names of all input files
        :param facl: full_atom_coord_list
        :return:
        """
        self.master = master
        self.master.title("Complex info")
        self.master.geometry("550x500")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        print("Info: Show general information of all complexes")

        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="75", height="30", undo="True")
        self.Box.grid(row=0, pady="5", padx="5")
        self.Box.delete(1.0, tk.END)

        for i in range(len(lf)):
            texts = "File {0:>2} : {1}".format(i + 1, lf[i].split('/')[-1])
            self.Box.insert(tk.END, texts)
            atoms = list(set(facl[i][0]))
            texts = ">> Number of atoms: {0}".format(len(facl[i][0]))
            self.Box.insert(tk.END, "\n" + texts)
            texts = ">> List of atoms: {0}".format(atoms)
            self.Box.insert(tk.END, "\n" + texts + "\n\n")


class ShowFaceSet:
    def __init__(self, master, sfa, sfc, sofa, sofc):
        """Show info of selected 4 octahedral face

        :param sfa: list_file - selected face atom
        :param sfc: selected face coordinates
        :param sofa: selected opposite face atom
        :param sofc: selected opposite face coordinates
        :return:
        """
        self.master = master
        self.master.title("Selected octahedral faces")
        self.master.geometry("550x500")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        print("Info: Show selected octahedral faces of complex")

        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="75", height="30", undo="True")
        self.Box.grid(row=0, pady="5", padx="5")
        self.Box.delete(1.0, tk.END)

        for i in range(4):
            texts = "Reference atoms: {0}          Opposite atoms: {1}\n".format(sfa[i], sofa[i])
            self.Box.insert(tk.END, texts)
            for j in range(3):
                texts = "{0:9.6f},{1:9.6f},{2:9.6f} \t {3:9.6f},{4:9.6f},{5:9.6f}\n"\
                    .format(sfc[i][j][0], sfc[i][j][1], sfc[i][j][2],
                            sofc[i][j][0], sofc[i][j][1], sofc[i][j][2])
                self.Box.insert(tk.END, texts)
            self.Box.insert(tk.END, "\n\n")


class ShowResults:
    def __init__(self, master, comp_result):
        """Show the computed octahedral distortion parameters of all selected files

        :param comp_result: list - computed Delta, Sigma, and Theta values
        :return:
        """
        self.master = master
        self.master.title("Results")
        self.master.geometry("380x530")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        self.lbl = tk.Label(self.frame, text="Computed octahedral distortion parameters for all complexes")
        self.lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
        self.Box.grid(row=1, pady="5", padx="5")

        texts = "                         Δ               Σ                Θ\n" \
                "                     -----------    -------------     ------------"
        self.Box.insert(tk.INSERT, texts)

        for i in range(len(comp_result)):
            texts = "Complex {0} : {1:10.6f}   {2:10.6f}   {3:10.6f}"\
                .format(i + 1, comp_result[i][0], comp_result[i][1], comp_result[i][2])
            self.Box.insert(tk.END, "\n" + texts)


class ShowParamOcta:
    def __init__(self, master, al, cl):
        """Show structural parameters, bond distance and bond angle, of selected complex

        :param al: list - atom_list
        :param cl: array - coord_list
        :return:
        """
        self.master = master
        self.master.title("Results")
        self.master.geometry("380x530")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        print("Info: Show structural parameters of truncated octahedron")

        self.lbl = tk.Label(self.frame, text="Structural parameters of octahedral structure")
        self.lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
        self.Box.grid(row=1, pady="5", padx="5")

        texts = "Bond distance (Å)"
        self.Box.insert(tk.INSERT, texts)

        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                if i == 0:
                    distance = linear.distance_between(cl[i], cl[j])
                    texts = "{0}-{1}{2} {3:10.6f}".format(al[i], al[j], j, distance)
                else:
                    distance = linear.distance_between(cl[i], cl[j])
                    texts = "{0}{1}-{2}{3} {4:10.6f}".format(al[i], i, al[j], j, distance)

                self.Box.insert(tk.END, "\n" + texts)

        texts = "Bond angle (°)"
        self.Box.insert(tk.END, "\n\n" + texts)

        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                for k in range(j + 1, len(cl)):
                    if i == 0:
                        angle = linear.angle_between(cl[j], cl[i], cl[k])
                        texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(al[k], k, al[i], al[j], j, angle)
                    else:
                        angle = linear.angle_between(cl[j], cl[i], cl[k])
                        texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(al[k], k, al[i], i, al[j], j, angle)

                    self.Box.insert(tk.END, "\n" + texts)
        self.Box.insert(tk.END, "\n")


class ShowParamFull:
    def __init__(self, master, fal, fcl):
        """Show structural parameters, bond distance and bond angle, of selected complex

        :param fal: list - full_atom_list
        :param fcl: array - full_coord_list
        :return:
        """
        self.master = master
        self.master.title("Results")
        self.master.geometry("380x530")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        print("Info: Show structural parameters of full complex")

        lbl = tk.Label(self.frame, text="Structural parameters of octahedral structure")
        lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
        Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
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
                        texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(fal[k], k, fal[i], fal[j], j, angle)
                    else:
                        angle = linear.angle_between(fcl[j], fcl[i], fcl[k])
                        texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(fal[k], k, fal[i], i, fal[j], j, angle)

                    Box.insert(tk.END, "\n" + texts)
        Box.insert(tk.END, "\n")


class ShowSurfaceArea:
    def __init__(self, master, pal, pcl):
        """Calculate the area of triangular face

        :param pal: list - plane_atom_list
        :param pcl: array - plane_coord_list
        :return:
        """
        self.master = master
        self.master.title("The area of triangular face")
        self.master.geometry("380x500")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        print("Info: Show the area of the triangular faces of truncated octahedron")

        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
        self.Box.grid(row=0, pady="5", padx="5")

        texts = "                 Atoms*        Area (Å³)"
        self.Box.insert(tk.INSERT, texts)

        for i in range(8):
            area = linear.triangle_area(pcl[i][0], pcl[i][1], pcl[i][2])
            texts = "Face no. {0}:  {1}      {2:10.6f}".format(i + 1, pal[i], area)
            self.Box.insert(tk.END, "\n" + texts)

        self.Box.insert(tk.END, "\n\n\n*Three ligand atoms are vertices of triangular face.\n")


def calc_bond_distance(fal, fcl):
    """Show bond distance of atoms pair
    - Compute distance of all bonds
    - Screen bonds out based on global cutoff distance
    - Screen H bonds out based on local cutoff distance

    :param fal: list - full_atom_list
    :param fcl: array - full_coord_list
    :return check_2_bond_list: list - selected bonds
    """
    global_distance_cutoff = 2.0
    hydrogen_distance_cutoff = 1.2

    print("Info: Determine correct bonds for atoms pair")
    print("Info: Global distance cutoff       : %s Angstrom"
          % global_distance_cutoff)
    print("Info: Distance cutoff for Hydrogen : %s Angstrom"
          % hydrogen_distance_cutoff)

    pair_list = []
    bond_list = []

    for i in range(len(fcl)):
        for j in range(i + 1, len(fcl)):
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

    print("\n      Total number of bonds before screening    : %5s"
          % len(bond_list))
    print("      Total number of bonds after 1st screening : %5s"
          % len(check_1_bond_list))
    print("      Total number of bonds after 2nd screening : %5s\n"
          % len(check_2_bond_list))

    return check_2_bond_list
