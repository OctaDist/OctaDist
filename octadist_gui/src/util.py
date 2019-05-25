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

import functools
import tkinter as tk
from tkinter import scrolledtext as tkscrolled

import numpy as np
import rmsd
import scipy.optimize
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from octadist_gui.src import echo_outs, elements, linear, popup, tools


def insert_text(self, text, coord, group):
    """
    Insert text in boxes.

    Parameters
    ----------
    text : str
        Text.
    coord : list or array
        Coordinates.
    group : str
        Group A or B.

    Returns
    -------
    None : None

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
    """
    Clear text in box A & B.

    Returns
    -------
    None : None

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
    """
    Find best fit plane to the given data points (atoms).

    scipy.optimize.minimize is used to find the least-square plane.

    Parameters
    ----------
    coord : list or array
        Coordinates of selected atom chunk.

    Returns
    -------
    xx, yy, z : float
        Coefficient of the surface.
    abcd : tuple
        Coefficient of the equation of the plane.

    Notes
    -----


    Examples
    --------
    Example of set of coordinate of atoms.

    points = [(1.1, 2.1, 8.1),
              (3.2, 4.2, 8.0),
              (5.3, 1.3, 8.2),
              (3.4, 2.4, 8.3),
              (1.5, 4.5, 8.0),
              (5.5, 6.7, 4.5)]
    
    To plot the plane, run following commands:
              
    >> map coordinates for scattering plot
    >> xs, ys, zs = zip(*points)
    >> ax.scatter(xs, ys, zs)

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

    points = coord

    fun = functools.partial(error, points=points)
    params0 = [0, 0, 0]
    res = scipy.optimize.minimize(fun, params0)

    a = res.x[0]
    b = res.x[1]
    c = res.x[2]

    point = np.array([0.0, 0.0, c])
    normal = np.array(cross([1, 0, a], [0, 1, b]))
    d = -point.dot(normal)
    xx, yy = np.meshgrid([-5, 10], [-5, 10])
    z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

    abcd = (a, b, c, d)

    return xx, yy, z, abcd


def plot_fit_plane(self, acf):
    """
    Display complex and two fit planes of two sets of ligand in molecule.

    Parameters
    ----------
    acf : list
        Atomic labels and coordinates of full complex.
    
    Returns
    -------
    None : None
    
    """
    ###############
    # Clear boxes #
    ###############
    self.box_angle1.delete(0, tk.END)
    self.box_angle2.delete(0, tk.END)

    self.box_eq1.delete(0, tk.END)
    self.box_eq2.delete(0, tk.END)

    ########################
    # Find eq of the plane #
    ########################

    xx, yy, z, abcd = calc_fit_plane(self.coord_A)
    plane_A = (xx, yy, z)
    a1, b1, c1, d1 = abcd

    self.box_eq1.insert(tk.INSERT, f"{a1:8.5f}x {b1:+8.5f}y {c1:+8.5f}z {d1:+8.5f} = 0")

    xx, yy, z, abcd = calc_fit_plane(self.coord_B)
    plane_B = (xx, yy, z)
    a2, b2, c2, d2 = abcd

    self.box_eq2.insert(tk.INSERT, f"{a2:8.5f}x {b2:+8.5f}y {c2:+8.5f}z {d2:+8.5f} = 0")

    ####################################
    # Calculate angle between 2 planes #
    ####################################

    angle = linear.angle_btw_planes(a1, b1, c1, a2, b2, c2)
    self.box_angle1.insert(tk.INSERT, f"{angle:10.6f}")  # insert to box

    sup_angle = abs(180 - angle)  # supplementary angle
    self.box_angle2.insert(tk.INSERT, f"{sup_angle:10.6f}")  # insert to box

    ###############
    # Plot planes #
    ###############

    fal, fcl = acf[0]

    fig = plt.figure()
    # fig = plt.figure(figsize=(5, 4), dpi=100)
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black', picker=5,
                   color=elements.check_color(n), label=f"{fal[i]}",
                   s=elements.check_radii(n) * 300)

    # Calculate distance
    bond_list = tools.find_bonds(self, fal, fcl)
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
    leg = fig.legend(handle_list, label_list,
                     loc="lower left", scatterpoints=1, fontsize=12)
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
    """
    On-mouse pick atom and get XYZ coordinate.

    Parameters
    ----------
    acf : list
        Atomic labels and coordinates of full complex.
    group : str
        Group A or B.
    
    Returns
    -------
    None : None
    
    """
    fal, fcl = acf[0]

    fig = plt.figure()
    # fig = plt.figure(figsize=(5, 4), dpi=100)
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black', picker=5,
                   color=elements.check_color(n), label=f"{fal[i]}",
                   s=elements.check_radii(n) * 300)

    # Calculate distance
    bond_list = tools.find_bonds(self, fal, fcl)
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
    leg = fig.legend(handle_list, label_list,
                     loc="lower left", scatterpoints=1, fontsize=12)
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

    # def on_pick(event):
    #     ind = event.ind
    #     print("on_pick scatter:", ind, np.take(x, ind), np.take(y, ind))

    # Pick point and get XYZ data
    def on_pick(event):
        ind = event.ind[0]
        x, y, z = event.artist._offsets3d
        for i in range(len(fal)):
            if x[ind] == fcl[i][0]:
                if y[ind] == fcl[i][1]:
                    if z[ind] == fcl[i][2]:
                        atom = fal[i]
                        break

        results = f"{i + 1}  {atom}  :  {x[ind]} {y[ind]} {z[ind]}"
        coord = [x[ind], y[ind], z[ind]]
        insert_text(self, results, coord, group)
        # Highlight selected atom
        index = elements.check_atom(atom)
        ax.scatter(x[ind], y[ind], z[ind],
                   marker='o', linewidths=0.5,
                   edgecolors='orange', picker=5, alpha=0.5,
                   color='yellow', s=elements.check_radii(index) * 400)
        # print(i+1, atom, x[ind], y[ind], z[ind])

    fig.canvas.mpl_connect('pick_event', on_pick)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def calc_jahn_teller(self, acf):
    """
    Calculate angular Jahn-Teller distortion parameter.

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

    self.btn = tk.Button(root, text="Select ligand set A", command=lambda: pick_atom(self, acf, group="A"))
    self.btn.config(width=15, relief=tk.RAISED)
    self.btn.grid(padx="10", pady="5", row=2, column=0, columnspan=2)

    self.btn = tk.Button(root, text="Select ligand set B", command=lambda: pick_atom(self, acf, group="B"))
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


def calc_rmsd(self, acf):
    """
    Calculate root mean squared displacement of atoms in complex, RMSD.

    Parameters
    ----------
    acf : list
        Atomic labels and coordinates of full complex.
        
    Returns
    -------
    rmsd_normal : int or float
        Normal RMSD,
    rmsd_translate : int or float
        Translate RMSD (re-centered),
    rmsd_rotate : int or float
        Kabsch RMSD (rotated),
    
    References
    ----------
    https://github.com/charnley/rmsd

    Examples
    --------
    >>> comp1.xyz
    Fe        10.187300000     5.746300000     5.615000000
    O         8.494000000     5.973500000     4.809100000
    O         9.652600000     6.422900000     7.307900000
    N        10.803800000     7.531900000     5.176200000
    N         9.622900000     3.922100000     6.008300000
    N        12.006500000     5.556200000     6.349700000
    N        10.804600000     4.947100000     3.921900000
    >>> comp2.xyz
    Fe        12.093762780     2.450541280     3.420711630
    O        12.960362780     2.295241280     1.728611630
    O        13.487662780     1.618241280     4.423011630
    N        12.852262780     4.317441280     3.989411630
    N        10.930762780     0.769741280     2.931511630
    N        10.787862780     2.298741280     5.107111630
    N        10.677362780     3.796041280     2.542411630
    >>> complex = [comp1, comp2]  # comp1 and comp2 are lists of coordinates of two complex
    >>> calc_rmsd(complex)
    RMSD between two complexes
    **************************
    Normal RMSD       : 5.015001
    Re-centered RMSD  : 2.665076
    Rotated RMSD      : 1.592468

    """
    if len(acf) != 2:
        popup.err_only_2_files()
        return 1

    strct_1 = acf[0]
    strct_2 = acf[1]

    atom_strc_1, coord_strct_1 = strct_1
    atom_strc_2, coord_strct_2 = strct_2

    if len(atom_strc_1) != len(atom_strc_2):
        popup.err_not_equal_atom()
        return 1

    for i in range(len(atom_strc_1)):
        if atom_strc_1[i] != atom_strc_2[i]:
            popup.err_atom_not_match(i + 1)
            return 1

    rmsd_normal = rmsd.rmsd(coord_strct_1, coord_strct_2)

    # Manipulate recenter
    coord_strct_1 -= rmsd.centroid(coord_strct_1)
    coord_strct_2 -= rmsd.centroid(coord_strct_2)

    rmsd_translate = rmsd.rmsd(coord_strct_1, coord_strct_2)

    # Rotate
    U = rmsd.kabsch(coord_strct_1, coord_strct_2)
    coord_strct_1 = np.dot(coord_strct_1, U)

    rmsd_rotate = rmsd.rmsd(coord_strct_1, coord_strct_2)

    echo_outs(self, "RMSD between two complexes")
    echo_outs(self, "**************************")
    echo_outs(self, f"Normal RMSD       : {rmsd_normal:3.6f}")
    echo_outs(self, f"Re-centered RMSD  : {rmsd_translate:3.6f}")
    echo_outs(self, f"Rotated RMSD      : {rmsd_rotate:3.6f}")
    echo_outs(self, "")

    return rmsd_normal, rmsd_translate, rmsd_rotate
