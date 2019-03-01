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
import main


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

        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="75", height="30", undo="True")
        self.Box.grid(row=0, pady="5", padx="5")
        self.Box.delete(1.0, tk.END)

        for i in range(len(lf)):
            self.Box.insert(tk.END, "File {0:>2} : {1}\n".format(i + 1, lf[i].split('/')[-1]))
            self.Box.insert(tk.END, ">> Number of atoms: {0}\n".format(len(facl[i][0])))
            atoms = list(set(facl[i][0]))
            self.Box.insert(tk.END, ">> List of atoms: {0}".format(atoms) + "\n\n")


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
        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="75", height="30", undo="True")
        self.Box.grid(row=0, pady="5", padx="5")
        self.Box.delete(1.0, tk.END)

        for i in range(4):
            self.Box.insert(tk.END, "Reference atoms: {0}          Opposite atoms: {1}\n".format(sfa[i], sofa[i]))
            for j in range(3):
                self.Box.insert(tk.END, "{0:9.6f},{1:9.6f},{2:9.6f} \t {3:9.6f},{4:9.6f},{5:9.6f}\n"
                                .format(sfc[i][j][0], sfc[i][j][1], sfc[i][j][2],
                                        sofc[i][j][0], sofc[i][j][1], sofc[i][j][2]))
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

        self.Box.insert(tk.INSERT, "                         Δ               Σ                Θ\n")
        self.Box.insert(tk.INSERT, "                     -----------    -------------     ------------\n")
        for i in range(len(comp_result)):
            self.Box.insert(tk.END, "Complex {0} : {1:10.6f}   {2:10.6f}   {3:10.6f}\n"
                            .format(i + 1, comp_result[i][0], comp_result[i][1], comp_result[i][2]))


class ShowParamFull:
    def __init__(self, master, acf):
        """Show structural parameters, bond distance and bond angle, of selected complex

        :param acf: list - atom_coord_full
        :return:
        """
        self.master = master
        self.master.title("Results")
        self.master.geometry("380x530")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        self.lbl = tk.Label(self.frame, text="Structural parameters of octahedral structure")
        self.lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
        self.Box.grid(row=1, pady="5", padx="5")

        fal, fcl = acf

        self.Box.insert(tk.INSERT, "Bond distance (Å)")
        for i in range(len(fcl)):
            for j in range(i + 1, len(fcl)):
                if i == 0:
                    distance = linear.distance_between(fcl[i], fcl[j])
                    texts = "{0}-{1}{2} {3:10.6f}".format(fal[i], fal[j], j, distance)
                else:
                    distance = linear.distance_between(fcl[i], fcl[j])
                    texts = "{0}{1}-{2}{3} {4:10.6f}".format(fal[i], i, fal[j], j, distance)
                self.Box.insert(tk.END, "\n" + texts)

        self.Box.insert(tk.END, "\n\nBond angle (°)")
        for i in range(len(fcl)):
            for j in range(i + 1, len(fcl)):
                for k in range(j + 1, len(fcl)):
                    if i == 0:
                        angle = linear.angle_between(self, fcl[j], fcl[i], fcl[k])
                        texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(fal[k], k, fal[i], fal[j], j, angle)
                    else:
                        angle = linear.angle_between(self, fcl[j], fcl[i], fcl[k])
                        texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(fal[k], k, fal[i], i, fal[j], j, angle)
                    self.Box.insert(tk.END, "\n" + texts)
        self.Box.insert(tk.END, "\n")


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
        self.lbl = tk.Label(self.frame, text="Structural parameters of octahedral structure")
        self.lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
        self.Box.grid(row=1, pady="5", padx="5")

        self.Box.insert(tk.INSERT, "Bond distance (Å)")
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                if i == 0:
                    distance = linear.distance_between(cl[i], cl[j])
                    texts = "{0}-{1}{2} {3:10.6f}".format(al[i], al[j], j, distance)
                else:
                    distance = linear.distance_between(cl[i], cl[j])
                    texts = "{0}{1}-{2}{3} {4:10.6f}".format(al[i], i, al[j], j, distance)

                self.Box.insert(tk.END, "\n" + texts)

        self.Box.insert(tk.END, "\n\nBond angle (°)")
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                for k in range(j + 1, len(cl)):
                    if i == 0:
                        angle = linear.angle_between(self, cl[j], cl[i], cl[k])
                        texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(al[k], k, al[i], al[j], j, angle)
                    else:
                        angle = linear.angle_between(self, cl[j], cl[i], cl[k])
                        texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(al[k], k, al[i], i, al[j], j, angle)

                    self.Box.insert(tk.END, "\n" + texts)
        self.Box.insert(tk.END, "\n")


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
        self.Box = tkscrolled.ScrolledText(self.frame, wrap="word", width="50", height="30", undo="True")
        self.Box.grid(row=0, pady="5", padx="5")
        self.Box.insert(tk.INSERT, "                 Atoms*        Area (Å³)\n")

        for i in range(8):
            area = linear.triangle_area(pcl[i][0], pcl[i][1], pcl[i][2])
            self.Box.insert(tk.END, "Face no. {0}:  {1}      {2:10.6f}\n".format(i + 1, pal[i], area))

        self.Box.insert(tk.END, "\n\n\n*Three ligand atoms are vertices of triangular face.\n")


def calc_bond_distance(self, fal, fcl):
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

    main.print_stdout(self, "Info: Determine the correct bond for atoms pair")
    main.print_stdout(self, "Info: Global distance cutoff       : {0} Angstrom".format(global_distance_cutoff))
    main.print_stdout(self, "Info: Distance cutoff for Hydrogen : {0} Angstrom".format(hydrogen_distance_cutoff))

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

    main.print_stdout(self, "")
    main.print_stdout(self, "      Total number of bonds before screening    : {0:5d}".format(len(bond_list)))
    main.print_stdout(self, "      Total number of bonds after 1st screening : {0:5d}".format(len(check_1_bond_list)))
    main.print_stdout(self, "      Total number of bonds after 2nd screening : {0:5d}".format(len(check_2_bond_list)))
    main.print_stdout(self, "")

    return check_2_bond_list

