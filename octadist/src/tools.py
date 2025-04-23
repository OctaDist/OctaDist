# OctaDist  Copyright (C) 2019-2024  Rangsiman Ketkaew et al.
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
import rmsd

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from octadist.src import linear, elements, plane, util


class CalcJahnTeller:
    """
    Calculate angular Jahn-Teller distortion parameter [1]_.

    Parameters
    ----------
    atom : array_like
        Atomic labels of full complex.
    coord : array_like
        Atomic coordinates of full complex.
    master : None, object
        If None, use tk.Tk().
        If not None, use tk.Toplevel(master).
    cutoff_global : int or float
        Global cutoff for screening bonds.
        Default is 2.0.
    cutoff_hydrogen : int or float
        Cutoff for screening hydrogen bonds.
        Default is 1.2.
    icon : str, optional
        If None, use tkinter default icon.
        If not None, use user-defined icon.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> test = CalcJahnTeller(atom=atom, coord=coord)
    >>> test.start_app()
    >>> test.find_bond()
    >>> test.show_app()

    References
    ----------
    .. [1] J. M. Holland, J. A. McAllister, C. A. Kilner,
        M. Thornton-Pett, A. J. Bridgeman, M. A. Halcrow.
        Stereochemical effects on the spin-state transition
        shown by salts of [FeL2]2+ [L = 2,6-di(pyrazol-1-yl)pyridine].
        J. Chem. Soc., Dalton Trans., 2002, 548-554.
        DOI: 10.1039/B108468M.

    """

    def __init__(
        self,
        atom,
        coord,
        cutoff_global=2.0,
        cutoff_hydrogen=1.2,
        master=None,
        icon=None,
    ):
        self.atom = atom
        self.coord = coord
        self.cutoff_global = cutoff_global
        self.cutoff_hydrogen = cutoff_hydrogen

        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

        self.icon = icon

        self.bond_list = []
        self.coord_A = []
        self.coord_B = []

    def start_app(self):
        """
        Start application.

        """
        if self.icon is not None:
            self.wd.wm_iconbitmap(self.icon)
        self.wd.title("Calculate Jahn-Teller distortion parameter")
        self.wd.geometry("630x550")
        self.wd.resizable(0, 0)

        self.lbl = tk.Label(self.wd, text="Group A")
        self.lbl.config(width=12)
        self.lbl.grid(padx="10", pady="5", row=0, column=0, columnspan=2)

        self.lbl = tk.Label(self.wd, text="Group B")
        self.lbl.config(width=12)
        self.lbl.grid(padx="10", pady="5", row=0, column=2, columnspan=2)

        self.box_1 = tkscrolled.ScrolledText(
            self.wd, height="12", width="40", wrap="word", undo="True"
        )
        self.box_1.grid(padx="5", pady="5", row=1, column=0, columnspan=2)

        self.box_2 = tkscrolled.ScrolledText(
            self.wd, height="12", width="40", wrap="word", undo="True"
        )
        self.box_2.grid(padx="5", pady="5", row=1, column=2, columnspan=2)

        self.btn = tk.Button(
            self.wd,
            text="Select ligand set A",
            command=lambda: self.pick_atom(group="A"),
        )
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=2, column=0, columnspan=2)

        self.btn = tk.Button(
            self.wd,
            text="Select ligand set B",
            command=lambda: self.pick_atom(group="B"),
        )
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=2, column=2, columnspan=2)

        self.btn = tk.Button(
            self.wd, text="Calculate parameter", command=lambda: self.plot_fit_plane()
        )
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=3, column=0, columnspan=2)

        self.btn = tk.Button(
            self.wd, text="Clear all", command=lambda: self.clear_text()
        )
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="5", row=3, column=2, columnspan=2)

        self.lbl = tk.Label(
            self.wd, text="Supplementary angles between two planes (in degree)"
        )
        self.lbl.grid(pady="10", row=4, columnspan=4)

        self.lbl_angle1 = tk.Label(self.wd, text="Angle 1")
        self.lbl_angle1.grid(pady="5", row=5, column=0)
        self.box_angle1 = tk.Entry(self.wd, width="20", justify="center")
        self.box_angle1.grid(row=5, column=1, sticky=tk.W)

        self.lbl_angle2 = tk.Label(self.wd, text="Angle 2")
        self.lbl_angle2.grid(pady="5", row=6, column=0)
        self.box_angle2 = tk.Entry(self.wd, width="20", justify="center")
        self.box_angle2.grid(row=6, column=1, sticky=tk.W)

        self.lbl = tk.Label(self.wd, text="The equation of the planes")
        self.lbl.grid(pady="10", row=7, columnspan=4)

        self.lbl_eq1 = tk.Label(self.wd, text="Plane A ")
        self.lbl_eq1.grid(pady="5", row=8, column=0)
        self.box_eq1 = tk.Entry(self.wd, width="60", justify="center")
        self.box_eq1.grid(pady="5", row=8, column=1, columnspan=2, sticky=tk.W)

        self.lbl_eq2 = tk.Label(self.wd, text="Plane B ")
        self.lbl_eq2.grid(pady="5", row=9, column=0)
        self.box_eq2 = tk.Entry(self.wd, width="60", justify="center")
        self.box_eq2.grid(pady="5", row=9, column=1, columnspan=2, sticky=tk.W)

    def find_bond(self):
        """
        Find bonds.

        See Also
        --------
        octadist.src.util.find_bonds :
            Find atomic bonds.

        """
        _, self.bond_list = util.find_bonds(
            self.atom, self.coord, self.cutoff_global, self.cutoff_hydrogen
        )

    #################
    # Picking atoms #
    #################

    def pick_atom(self, group):
        """
        On-mouse pick atom and get XYZ coordinate.

        Parameters
        ----------
        group : str
            Group A or B.

        """
        fig = plt.figure()
        # fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = Axes3D(fig)
        # ax = fig.add_subplot(111, projection='3d')

        # Plot all atoms
        for i in range(len(self.coord)):
            # Determine atomic number
            n = elements.number_to_symbol(self.atom[i])
            ax.scatter(
                self.coord[i][0],
                self.coord[i][1],
                self.coord[i][2],
                marker="o",
                linewidths=0.5,
                edgecolors="black",
                picker=5,
                color=elements.number_to_color(n),
                label=f"{self.atom[i]}",
                s=elements.number_to_radii(n) * 300,
            )

        atoms_pair = []
        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            atoms_pair.append(atoms)

        # Draw line
        for i in range(len(atoms_pair)):
            merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
            x, y, z = merge
            ax.plot(x, y, z, "-", color="black", linewidth=2)

        # Set legend
        # Remove duplicate labels in legend.
        # Ref.https://stackoverflow.com/a/26550501/6596684
        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        leg = fig.legend(
            handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12
        )
        # Fixed size of point in legend
        # Ref. https://stackoverflow.com/a/24707567/6596684
        for i in range(len(leg.legend_handles)):
            leg.legend_handles[i]._sizes = [90]

        # Set axis
        ax.set_xlabel(r"X", fontsize=15)
        ax.set_ylabel(r"Y", fontsize=15)
        ax.set_zlabel(r"Z", fontsize=15)
        ax.set_title("Full complex", fontsize="12")
        ax.grid(True)

        def insert_text(text, coord, group):
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

            """
            if group == "A":
                self.box_1.insert(tk.INSERT, text + "\n")
                self.box_1.see(tk.END)

                self.coord_A.append(coord)

            elif group == "B":
                self.box_2.insert(tk.INSERT, text + "\n")
                self.box_2.see(tk.END)

                self.coord_B.append(coord)

        def on_pick(event):
            """
            Pick point and get XYZ data

            Parameters
            ----------
            event : object
                Event object for on-pick function.

            Examples
            --------
            >>> def on_pick(event):
            >>> ... ind = event.ind
            >>> ... print("on_pick scatter:", ind, np.take(x, ind), np.take(y, ind))

            """
            ind = event.ind[0]
            x, y, z = event.artist._offsets3d
            for i in range(len(self.atom)):
                if x[ind] == self.coord[i][0]:
                    if y[ind] == self.coord[i][1]:
                        if z[ind] == self.coord[i][2]:
                            atom = self.atom[i]
                            break

            results = f"{i + 1}  {atom}  :  {x[ind]} {y[ind]} {z[ind]}"
            coord = [x[ind], y[ind], z[ind]]
            insert_text(results, coord, group)
            # Highlight selected atom
            index = elements.number_to_symbol(atom)
            ax.scatter(
                x[ind],
                y[ind],
                z[ind],
                marker="o",
                linewidths=0.5,
                edgecolors="orange",
                picker=5,
                alpha=0.5,
                color="yellow",
                s=elements.number_to_radii(index) * 400,
            )
            # print(i+1, atom, x[ind], y[ind], z[ind])

        fig.canvas.mpl_connect("pick_event", on_pick)

        # plt.axis('equal')
        # plt.axis('off')
        plt.show()

    ########################################
    # Plot fit plant to the selected atoms #
    ########################################

    def plot_fit_plane(self):
        """
        Display complex and two fit planes of two sets of ligand in molecule.

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

        xx, yy, z, abcd = plane.find_fit_plane(self.coord_A)
        plane_a = (xx, yy, z)
        a1, b1, c1, d1 = abcd

        self.box_eq1.insert(
            tk.INSERT, f"{a1:8.5f}x {b1:+8.5f}y {c1:+8.5f}z {d1:+8.5f} = 0"
        )

        xx, yy, z, abcd = plane.find_fit_plane(self.coord_B)
        plane_b = (xx, yy, z)
        a2, b2, c2, d2 = abcd

        self.box_eq2.insert(
            tk.INSERT, f"{a2:8.5f}x {b2:+8.5f}y {c2:+8.5f}z {d2:+8.5f} = 0"
        )

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

        fig = plt.figure()
        # fig = plt.figure(figsize=(5, 4), dpi=100)
        ax = Axes3D(fig)
        # ax = fig.add_subplot(111, projection='3d')

        # Plot all atoms
        for i in range(len(self.coord)):
            # Determine atomic number
            n = elements.number_to_symbol(self.atom[i])
            ax.scatter(
                self.coord[i][0],
                self.coord[i][1],
                self.coord[i][2],
                marker="o",
                linewidths=0.5,
                edgecolors="black",
                picker=5,
                color=elements.number_to_color(n),
                label=f"{self.atom[i]}",
                s=elements.number_to_radii(n) * 300,
            )

        atoms_pair = []
        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            atoms_pair.append(atoms)

        # Draw line
        for i in range(len(atoms_pair)):
            merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
            x, y, z = merge
            ax.plot(x, y, z, "-", color="black", linewidth=2)

        # Set legend
        # Remove duplicate labels in legend.
        # Ref.https://stackoverflow.com/a/26550501/6596684
        handles, labels = ax.get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        leg = fig.legend(
            handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12
        )
        # Fixed size of point in legend
        # Ref. https://stackoverflow.com/a/24707567/6596684
        for i in range(len(leg.legend_handles)):
            leg.legend_handles[i]._sizes = [90]

        # Set axis
        ax.set_xlabel(r"X", fontsize=15)
        ax.set_ylabel(r"Y", fontsize=15)
        ax.set_zlabel(r"Z", fontsize=15)
        ax.set_title("Full complex", fontsize="12")
        ax.grid(True)

        # Plot plane A
        xx, yy, z = plane_a
        ax.plot_surface(xx, yy, z, alpha=0.2, color="green")

        # Plot plane B
        xx, yy, z = plane_b
        ax.plot_surface(xx, yy, z, alpha=0.2, color="red")

        # ax.set_xlim(-10, 10)
        # ax.set_ylim(-10, 10)
        # ax.set_zlim(0, 10)

        # plt.axis('equal')
        # plt.axis('off')
        plt.show()

    ##################
    # Clear text box #
    ##################

    def clear_text(self):
        """
        Clear text in box A & B.

        """
        self.box_1.delete(1.0, tk.END)
        self.box_2.delete(1.0, tk.END)

        self.box_angle1.delete(0, tk.END)
        self.box_angle2.delete(0, tk.END)

        self.box_eq1.delete(0, tk.END)
        self.box_eq2.delete(0, tk.END)

        self.coord_A = []
        self.coord_B = []

        try:
            plt.close("all")
        except AttributeError:
            pass

    def show_app(self):
        """
        Show application.

        """
        self.wd.mainloop()


class CalcRMSD:
    """
    Calculate root mean squared displacement of atoms in complex, RMSD [2]_.

    Parameters
    ----------
    coord_1 : array_like
        Atomic coordinates of structure 1.
    coord_2 : array_like
        Atomic coordinates of structure 2.
    atom_1 : list or tuple, optional
        Atomic symbols of structure 1.
    atom_2 : list or tuple, optional
        Atomic symbols of structure 2.
        If no atom_2 specified, assign it with None.

    Returns
    -------
    rmsd_normal : float
        Normal RMSD.
    rmsd_translate : float
        Translate RMSD (re-centered).
    rmsd_rotate : float
        Kabsch RMSD (rotated).

    References
    ----------
    .. [2] J. C. Kromann. https://github.com/charnley/rmsd.

    Examples
    --------
    >>> # Example of structure 1
    >>> comp1 = [[10.1873, 5.7463, 5.615],
                 [8.494, 5.9735, 4.8091],
                 [9.6526, 6.4229, 7.3079],
                 [10.8038, 7.5319, 5.1762],
                 [9.6229, 3.9221, 6.0083],
                 [12.0065, 5.5562, 6.3497],
                 [10.8046, 4.9471, 3.9219]]

    >>> # Example of structure 1
    >>> comp2 = [[12.0937, 2.4505, 3.4207],
                 [12.9603, 2.2952, 1.7286],
                 [13.4876, 1.6182, 4.4230],
                 [12.8522, 4.3174, 3.9894],
                 [10.9307, 0.7697, 2.9315],
                 [10.7878, 2.2987, 5.1071],
                 [10.6773, 3.7960, 2.5424]]

    >>> test = CalcRMSD(coord_1=comp1, coord_2=comp2)
    >>> test.calc_rmsd()
    >>> test.rmsd_normal
    6.758144
    >>> test.rmsd_translate
    0.305792
    >>> test.rmsd_rotate
    0.277988

    """

    def __init__(
        self, coord_1, coord_2, atom_1=None, atom_2=None, master=None, icon=None
    ):
        self.coord_1 = np.asarray(coord_1, dtype=np.float64)
        self.coord_2 = np.asarray(coord_2, dtype=np.float64)

        self.atom_1 = atom_1
        self.atom_2 = atom_2

        if self.atom_2 is None:
            self.atom_2 = self.atom_1

        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

        self.icon = icon

        self.rmsd_normal = 0
        self.rmsd_translate = 0
        self.rmsd_rotate = 0

    def start_app(self):
        if self.icon is not None:
            self.wd.wm_iconbitmap(self.icon)
        self.wd.title("Calculate RMSD")
        self.wd.geometry("700x440")
        self.wd.resizable(0, 0)

        self.lbl = tk.Label(
            self.wd, text="Calculate root-mean-square deviation of atomic positions"
        )
        # self.lbl.config(width=12)
        self.lbl.grid(padx="5", pady="5", row=0, column=0, columnspan=2)

        self.lbl = tk.Label(self.wd, text="Structure A")
        self.lbl.config(width=12)
        self.lbl.grid(padx="10", pady="5", row=1, column=0)

        self.lbl = tk.Label(self.wd, text="Structure B")
        self.lbl.config(width=12)
        self.lbl.grid(padx="10", pady="5", row=1, column=1)

        self.box_1 = tkscrolled.ScrolledText(
            self.wd, height="12", width="45", wrap="word", undo="True"
        )
        self.box_1.grid(padx="5", pady="5", row=2, column=0)

        self.box_2 = tkscrolled.ScrolledText(
            self.wd, height="12", width="45", wrap="word", undo="True"
        )
        self.box_2.grid(padx="5", pady="5", row=2, column=1)

        self.lbl = tk.Label(self.wd, text="Normal RMSD")
        self.lbl.grid(padx="5", pady="5", row=3, column=0, sticky=tk.E)
        self.box_3 = tk.Entry(self.wd, width="20", justify="center")
        self.box_3.grid(padx="5", row=3, column=1, sticky=tk.W)

        self.lbl = tk.Label(self.wd, text="Re-centered RMSD")
        self.lbl.grid(padx="5", pady="5", row=4, column=0, sticky=tk.E)
        self.box_4 = tk.Entry(self.wd, width="20", justify="center")
        self.box_4.grid(padx="5", row=4, column=1, sticky=tk.W)

        self.lbl = tk.Label(self.wd, text="Rotated RMSD")
        self.lbl.grid(padx="5", pady="5", row=5, column=0, sticky=tk.E)
        self.box_5 = tk.Entry(self.wd, width="20", justify="center")
        self.box_5.grid(padx="5", row=5, column=1, sticky=tk.W)

        self.btn = tk.Button(
            self.wd, text="Calculate RMSD", command=lambda: self.calc_and_show()
        )
        self.btn.config(width=15, relief=tk.RAISED)
        self.btn.grid(padx="10", pady="15", row=6, column=0, columnspan=2)

        # When app starts, show atomic coordinates in box.
        self.show_coord()

    def show_coord(self):
        """
        Show atomic coordinates in box.

        """
        num_atoms = len(self.coord_1)

        self.box_1.insert(tk.INSERT, f"Total atoms: {num_atoms}\n\n")
        self.box_2.insert(tk.INSERT, f"Total atoms: {num_atoms}\n\n")

        if self.atom_1 is None or self.atom_2 is None:
            self.atom_1 = ["N/A"] * num_atoms
            self.atom_2 = ["N/A"] * num_atoms

        for i in range(num_atoms):
            self.box_1.insert(
                tk.INSERT, f"{i+1}.  {self.atom_1[i]}\t{self.coord_1[i]}\n"
            )
            self.box_2.insert(
                tk.INSERT, f"{i+1}.  {self.atom_2[i]}\t{self.coord_2[i]}\n"
            )

    def calc_rmsd(self):
        """
        Calculate normal, translated, and rotated RMSD.

        """
        tmp_1, tmp_2 = self.coord_1.copy(), self.coord_2.copy()

        self.rmsd_normal = rmsd.rmsd(self.coord_1, self.coord_2)

        # Manipulate recenter
        self.coord_1 -= rmsd.centroid(self.coord_1)
        self.coord_2 -= rmsd.centroid(self.coord_2)

        self.rmsd_translate = rmsd.rmsd(self.coord_1, self.coord_2)

        # Rotate
        rotation_matrix = rmsd.kabsch(self.coord_1, self.coord_2)
        self.coord_1 = np.dot(self.coord_1, rotation_matrix)

        self.rmsd_rotate = rmsd.rmsd(self.coord_1, self.coord_2)

        self.coord_1, self.coord_2 = tmp_1, tmp_2

    def calc_and_show(self):
        """
        Execute calc_rmsd function to calculate RMSD
        and show results in box.

        """
        self.calc_rmsd()

        self.box_3.delete(0, tk.END)
        self.box_4.delete(0, tk.END)
        self.box_5.delete(0, tk.END)

        self.box_3.insert(tk.INSERT, f"{self.rmsd_normal: 3.6f}")
        self.box_4.insert(tk.INSERT, f"{self.rmsd_translate: 3.6f}")
        self.box_5.insert(tk.INSERT, f"{self.rmsd_rotate: 3.6f}")

    def show_app(self):
        """
        Show application.

        """
        self.wd.mainloop()
