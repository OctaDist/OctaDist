"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import popup
import linear
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import elements
import scipy.optimize
import functools
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
                    angle = linear.angle_btw_3vec(self, fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(fal[k], k, fal[i], fal[j], j, angle)
                else:
                    angle = linear.angle_btw_3vec(self, fcl[j], fcl[i], fcl[k])
                    texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(fal[k], k, fal[i], i, fal[j], j, angle)
                box.insert(tk.END, "\n" + texts)
    box.insert(tk.END, "\n")


def param_octa(self, atom_coord_octa):
    """Show structural parameters of selected octahedral structure

    :param self: master frame
    :param atom_coord_octa: list of label and coordinate of octahedral structure
    :return:
    """
    aco = atom_coord_octa

    if len(aco) == 0:
        popup.err_no_file(self)
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

    for n in range(len(aco)):
        if n > 0:   # separator between files
            box.insert(tk.END, "\n\n=================================\n\n")

        box.insert(tk.INSERT, "File : {0}".format(aco[n][0]))
        box.insert(tk.END, "\nMetal: {0}".format(aco[n][1]))
        box.insert(tk.END, "\nBond distance (Å)")
        for i in range(7):
            for j in range(i+1, 7):
                if i == 0:
                    distance = linear.distance_between(aco[n][3][i], aco[n][3][j])
                    texts = "{0}-{1}{2} {3:10.6f}".format(aco[n][2][i], aco[n][2][j], j, distance)
                else:
                    distance = linear.distance_between(aco[n][3][i], aco[n][3][j])
                    texts = "{0}{1}-{2}{3} {4:10.6f}".format(aco[n][2][i], i, aco[n][2][j], j, distance)
                box.insert(tk.END, "\n" + texts)

        box.insert(tk.END, "\n\nBond angle (°)")
        for i in range(7):
            for j in range(i+1, 7):
                for k in range(j+1, 7):
                    if i == 0:
                        angle = linear.angle_btw_3vec(self, aco[n][3][j], aco[n][3][i], aco[n][3][k])
                        texts = "{0}{1}-{2}-{3}{4} {5:10.6f}".format(aco[n][2][k], k, aco[n][2][i], aco[n][2][j], j, angle)
                    else:
                        angle = linear.angle_btw_3vec(self, aco[n][3][j], aco[n][3][i], aco[n][3][k])
                        texts = "{0}{1}-{2}{3}-{4}{5} {6:10.6f}".format(aco[n][2][k], k, aco[n][2][i], i, aco[n][2][j], j, angle)
                    box.insert(tk.END, "\n" + texts)
        box.insert(tk.END, "\n")


def calc_surface_area(self, all_face):
    """Calculate the area of triangular face

    :param self: master frame
    :param all_face: list - atomic labels and coordinates of 8 faces
    :return:
    """
    if len(all_face) == 0:
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

    for n in range(len(all_face)):
        if n > 0:
            box.insert(tk.END, "\n==============================\n\n")

        face_data = all_face[n]
        a_ref, c_ref, a_oppo, c_oppo = face_data

        box.insert(tk.INSERT, "Octahedral structure no. {0}\n".format(n + 1))
        box.insert(tk.END, "                 Atoms*        Area (Å³)\n")
        for i in range(8):
            area = linear.triangle_area(c_ref[i][0], c_ref[i][1], c_ref[i][2])
            box.insert(tk.END, "Face no. {0}:  {1}      {2:10.6f}\n".format(i+1, a_ref[i], area))

        box.insert(tk.END, "\n*Three ligand atoms are vertices of triangular face.\n")


def plot_sigma_theta(self, s, t):
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


def insert_text(self, text, coord, group):
    """Insert text in box A & B

    :param self: root
    :param text: string text
    :param coord: coordinates
    :param group: group A or B
    :return:
    """
    if group == "A":
        self.box_1.insert(tk.INSERT, text + "\n")
        self.box_1.see(tk.END)

        self.coord_A.append(coord)

    elif group == "B":
        self.box_2.insert(tk.INSERT, text + "\n")
        self.box_2.see(tk.END)

        self.coord_B.append(coord)


def clear_text(self):
    """Clear text in box A & B

    :param self: root
    :return:
    """
    self.box_1.delete(1.0, tk.END)
    self.box_2.delete(1.0, tk.END)

    self.box_angle1.delete(0, tk.END)
    self.box_angle2.delete(0, tk.END)

    self.box_eq1.delete(0, tk.END)
    self.box_eq2.delete(0, tk.END)

    self.coord_A = []
    self.coord_B = []


def calc_fit_plane(coord):
    """Find best fit plane to the given data points (atoms)

    scipy.optimize.minimize is used to find the least-square plane

    :param coord: coordinates of selected atom chunk
    :return: the equation of the plane
    """
    def plane(x, y, params):
        a = params[0]
        b = params[1]
        c = params[2]
        z = a * x + b * y + c
        return z

    def error(params, points):
        result = 0
        for (x, y, z) in points:
            plane_z = plane(x, y, params)
            diff = abs(plane_z - z)
            result += diff ** 2
        return result

    def cross(a, b):
        return [a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0]]

    # Example of set of coordinate of atoms
    # points = [(1.1, 2.1, 8.1),
    #           (3.2, 4.2, 8.0),
    #           (5.3, 1.3, 8.2),
    #           (3.4, 2.4, 8.3),
    #           (1.5, 4.5, 8.0),
    #           (5.5, 6.7, 4.5)]

    points = coord

    fun = functools.partial(error, points=points)
    params0 = [0, 0, 0]
    res = scipy.optimize.minimize(fun, params0)

    a = res.x[0]
    b = res.x[1]
    c = res.x[2]

    # map coordinates for scattering plot
    # xs, ys, zs = zip(*points)
    # ax.scatter(xs, ys, zs)

    point = np.array([0.0, 0.0, c])
    normal = np.array(cross([1, 0, a], [0, 1, b]))
    d = -point.dot(normal)
    xx, yy = np.meshgrid([-5, 10], [-5, 10])
    z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

    abcd = (a, b, c, d)

    return xx, yy, z, abcd


def plot_fit_plane(self, acf):
    """Plot complex and two fit planes of two sets of ligand in molecule

    :param self: root
    :param acf: atom_coord_full
    :return:
    """
    ########################
    # Find eq of the plane #
    ########################

    main.print_stdout(self, "Info: Find the best fit plane to the given set of ligands")
    main.print_stdout(self, "")

    xx, yy, z, abcd = calc_fit_plane(self.coord_A)
    plane_A = (xx, yy, z)
    a1, b1, c1, d1 = abcd

    self.box_eq1.insert(tk.INSERT, "{0:8.5f}x {1:+8.5f}y {2:+8.5f}z {3:+8.5f} = 0".format(a1, b1, c1, d1))

    main.print_stdout(self, "Info: Plane A")
    main.print_stdout(self, "         xx : {0} {1}".format(xx[0], xx[1]))
    main.print_stdout(self, "         yy : {0} {1}".format(yy[0], xx[1]))
    main.print_stdout(self, "          z : {0} {1}".format(z[0], z[1]))
    main.print_stdout(self, "")

    xx, yy, z, abcd = calc_fit_plane(self.coord_B)
    plane_B = (xx, yy, z)
    a2, b2, c2, d2 = abcd

    self.box_eq2.insert(tk.INSERT, "{0:8.5f}x {1:+8.5f}y {2:+8.5f}z {3:+8.5f} = 0".format(a2, b2, c2, d2))

    main.print_stdout(self, "Info: Plane B")
    main.print_stdout(self, "         xx : {0} {1}".format(xx[0], xx[1]))
    main.print_stdout(self, "         yy : {0} {1}".format(yy[0], xx[1]))
    main.print_stdout(self, "          z : {0} {1}".format(z[0], z[1]))
    main.print_stdout(self, "")

    ####################################
    # Calculate angle between 2 planes #
    ####################################

    main.print_stdout(self, "Info: Calculate the angle between two planes in 3D")
    main.print_stdout(self, "")

    angle = linear.angle_btw_planes(a1, b1, c1, a2, b2, c2)
    self.box_angle1.insert(tk.INSERT, "{0:10.6f}".format(angle))  # insert to box

    sup_angle = abs(180 - angle)  # supplementary angle
    self.box_angle2.insert(tk.INSERT, "{0:10.6f}".format(sup_angle))  # insert to box

    main.print_stdout(self, "      ======= Summary of angular Jahn-Teller distortion =======")
    main.print_stdout(self, "")
    main.print_stdout(self, "      Supplementary angle 1 : = {0:10.6f} degree".format(angle))
    main.print_stdout(self, "      Supplementary angle 2 : = {0:10.6f} degree".format(sup_angle))
    main.print_stdout(self, "")
    main.print_stdout(self, "      =========================================================")
    main.print_stdout(self, "")

    ###############
    # Plot planes #
    ###############

    main.print_stdout(self, "Info: Display scatter plots of the lease squares planes of group A & B")
    main.print_stdout(self, "")

    fal, fcl = acf[0]

    fig = plt.figure()
    # fig = plt.figure(figsize=(5, 4), dpi=100)
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2], marker='o', linewidths=0.5, edgecolors='black', picker=5,
                   color=elements.check_color(n), label="{}".format(fal[i]), s=elements.check_radii(n) * 300)

    # Calculate distance
    bond_list = calc_bond_distance(self, fal, fcl)
    atoms_pair = []
    for i in range(len(bond_list)):
        get_atoms = bond_list[i]
        x, y, z = zip(*get_atoms)
        atoms = list(zip(x, y, z))
        atoms_pair.append(atoms)

    # Draw line
    for i in range(len(atoms_pair)):
        merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
        x, y, z = merge
        ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    # Set legend
    # Remove duplicate labels in legend.
    # Ref.https://stackoverflow.com/a/26550501/6596684
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    leg = fig.legend(handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12)
    # Fixed size of point in legend
    # Ref. https://stackoverflow.com/a/24707567/6596684
    for i in range(len(leg.legendHandles)):
        leg.legendHandles[i]._sizes = [90]

    # Set axis
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Full complex', fontsize="12")
    ax.grid(True)

    # Plot plane A
    xx, yy, z = plane_A
    ax.plot_surface(xx, yy, z, alpha=0.2, color='green')

    # Plot plane B
    xx, yy, z = plane_B
    ax.plot_surface(xx, yy, z, alpha=0.2, color='red')

    # ax.set_xlim(-10, 10)
    # ax.set_ylim(-10, 10)
    # ax.set_zlim(0, 10)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def pick_atom(self, acf, group):
    """On-mouse pick atom and get XYZ coordinate

    :param self: root
    :param acf: atom_coord_full
    :param group: group A or B
    :return:
    """
    fal, fcl = acf[0]

    main.print_stdout(self, "Info: Pick atoms for group {0}".format(group))
    main.print_stdout(self, "")

    fig = plt.figure()
    # fig = plt.figure(figsize=(5, 4), dpi=100)
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2], marker='o', linewidths=0.5, edgecolors='black', picker=5,
                   color=elements.check_color(n), label="{}".format(fal[i]), s=elements.check_radii(n) * 300)

    # Calculate distance
    bond_list = calc_bond_distance(self, fal, fcl)
    atoms_pair = []
    for i in range(len(bond_list)):
        get_atoms = bond_list[i]
        x, y, z = zip(*get_atoms)
        atoms = list(zip(x, y, z))
        atoms_pair.append(atoms)

    # Draw line
    for i in range(len(atoms_pair)):
        merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
        x, y, z = merge
        ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    # Set legend
    # Remove duplicate labels in legend.
    # Ref.https://stackoverflow.com/a/26550501/6596684
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    leg = fig.legend(handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12)
    # Fixed size of point in legend
    # Ref. https://stackoverflow.com/a/24707567/6596684
    for i in range(len(leg.legendHandles)):
        leg.legendHandles[i]._sizes = [90]

    # Set axis
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Full complex', fontsize="12")
    ax.grid(True)

    # def onpick(event):
    #     ind = event.ind
    #     print("onpick scatter:", ind, np.take(x, ind), np.take(y, ind))

    # Pick point and get XYZ data
    def onpick(event):
        ind = event.ind[0]
        x, y, z = event.artist._offsets3d
        for i in range(len(fal)):
            if x[ind] == fcl[i][0]:
                if y[ind] == fcl[i][1]:
                    if z[ind] == fcl[i][2]:
                        atom = fal[i]
                        break
        results = "{0}  {1}  :  {2} {3} {4}".format(i + 1, atom, x[ind], y[ind], z[ind])
        coord = [x[ind], y[ind], z[ind]]
        insert_text(self, results, coord, group)
        # Highlight selected atom
        index = elements.check_atom(atom)
        ax.scatter(x[ind], y[ind], z[ind], marker='o', linewidths=0.5, edgecolors='orange', picker=5, alpha=0.5,
                   color='yellow', s=elements.check_radii(index) * 400)
        # print(i+1, atom, x[ind], y[ind], z[ind])

    fig.canvas.mpl_connect('pick_event', onpick)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def calc_jahn_teller(self, acf):
    """Calculate angular Jahn-Teller distortion parameter

    :param self: master
    :param acf: atom_coord_full
    :return:
    """
    main.print_stdout(self, "Info: Calculate angular Jahn-Teller distortion parameter")
    main.print_stdout(self, "      Find least squares planes of two sets of ligands in molecule")
    main.print_stdout(self, "      A scipy.optimize.minimize package will be used to fit the plane to atoms")
    main.print_stdout(self, "")

    self.acf = acf

    if len(self.acf) == 0:
        popup.err_no_file(self)
        return 1
    elif len(self.acf) > 1:
        popup.err_many_files(self)
        return 1

    root = tk.Toplevel(self.master)
    root.title("Calculate Jahn-Teller distortion parameter")
    root.geometry("630x550")

    self.coord_A = []
    self.coord_B = []

    self.lbl = tk.Label(root, text="Group A")
    self.lbl.config(width=12)
    self.lbl.grid(padx="10", pady="5", row=0, column=0, columnspan=2)

    self.lbl = tk.Label(root, text="Group B")
    self.lbl.config(width=12)
    self.lbl.grid(padx="10", pady="5", row=0, column=2, columnspan=2)

    self.box_1 = tkscrolled.ScrolledText(root, height="12", width="40", wrap="word", undo="True")
    self.box_1.grid(padx="5", pady="5", row=1, column=0, columnspan=2)

    self.box_2 = tkscrolled.ScrolledText(root, height="12", width="40", wrap="word", undo="True")
    self.box_2.grid(padx="5", pady="5", row=1, column=2, columnspan=2)

    self.btn = tk.Button(root, text="Select ligand set A", command=lambda: pick_atom(self, self.acf, group="A"))
    self.btn.config(width=15, relief=tk.RAISED)
    self.btn.grid(padx="10", pady="5", row=2, column=0, columnspan=2)

    self.btn = tk.Button(root, text="Select ligand set B", command=lambda: pick_atom(self, self.acf, group="B"))
    self.btn.config(width=15, relief=tk.RAISED)
    self.btn.grid(padx="10", pady="5", row=2, column=2, columnspan=2)

    self.btn = tk.Button(root, text="Calculate parameter", command=lambda: plot_fit_plane(self, self.acf))
    self.btn.config(width=15, relief=tk.RAISED)
    self.btn.grid(padx="10", pady="5", row=3, column=0, columnspan=2)

    self.btn = tk.Button(root, text="Clear all", command=lambda: clear_text(self))
    self.btn.config(width=15, relief=tk.RAISED)
    self.btn.grid(padx="10", pady="5", row=3, column=2, columnspan=2)

    self.lbl = tk.Label(root, text="Supplementary angles between two planes (in degree)")
    self.lbl.grid(pady="10", row=4, columnspan=4)

    self.lbl_angle1 = tk.Label(root, text="Angle 1")
    self.lbl_angle1.grid(pady="5", row=5, column=0)
    self.box_angle1 = tk.Entry(root, width="20", justify='center')
    self.box_angle1.grid(row=5, column=1, sticky=tk.W)

    self.lbl_angle2 = tk.Label(root, text="Angle 2")
    self.lbl_angle2.grid(pady="5", row=6, column=0)
    self.box_angle2 = tk.Entry(root, width="20", justify='center')
    self.box_angle2.grid(row=6, column=1, sticky=tk.W)

    self.lbl = tk.Label(root, text="The equation of the planes")
    self.lbl.grid(pady="10", row=7, columnspan=4)

    self.lbl_eq1 = tk.Label(root, text="Plane A ")
    self.lbl_eq1.grid(pady="5", row=8, column=0)
    self.box_eq1 = tk.Entry(root, width="60", justify='center')
    self.box_eq1.grid(pady="5", row=8, column=1, columnspan=2, sticky=tk.W)

    self.lbl_eq2 = tk.Label(root, text="Plane B ")
    self.lbl_eq2.grid(pady="5", row=9, column=0)
    self.box_eq2 = tk.Entry(root, width="60", justify='center')
    self.box_eq2.grid(pady="5", row=9, column=1, columnspan=2, sticky=tk.W)

    root.mainloop()

