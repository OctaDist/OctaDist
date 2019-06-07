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

from scipy.spatial import distance

from octadist_gui.src import linear, popup, util


class DataComplex:
    """
    Show info of input complex.

    Parameters
    ----------
    master : None, object
        If None, use tk.Tk().
        If not None, use tk.Toplevel(master).

    """
    def __init__(self, master=None):
        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

    def start_app(self):
        self.wd.wm_iconbitmap(r"..\images\molecule.ico")
        self.wd.title("Complex info")
        self.wd.geometry("550x500")
        self.wd.option_add("*Font", "Arial 10")
        self.wd.resizable(0, 0)
        self.frame = tk.Frame(self.wd)
        self.frame.grid()

        self.box = tkscrolled.ScrolledText(self.frame, wrap="word", width="75", height="30", undo="True")
        self.box.grid(row=0, pady="5", padx="5")
        self.box.delete(1.0, tk.END)

    def add_name(self, file_name):
        """
        Add file name to bix.

        Parameters
        ----------
        file_name : array_like
            List containing the names of all input files.

        """
        self.box.insert(tk.END, f"File: {file_name.split('/')[-1]}\n")

    def add_coord(self, atom, coord):
        """
        Add atomic symbols and coordinates to box.

        Parameters
        ----------
        atom : array_like
            Atomic labels of full complex.
        coord : array_like
            Atomic coordinates of full complex.

        """
        self.box.insert(tk.END, "========================\n")
        self.box.insert(tk.END, f"{len(atom)}\n")
        atoms = list(set(atom))
        self.box.insert(tk.END, f"List of atoms: {atoms}\n")

        for i in range(len(coord)):
            self.box.insert(tk.END, f"{atom[i]:>2}  {coord[i][0]:9.6f}  {coord[i][1]:9.6f}  {coord[i][2]:9.6f}")
            self.box.insert(tk.END, "\n")
        self.box.insert(tk.END, "\n\n")


def data_face(self, aco):
    """
    Show info of selected 4 octahedral faces.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

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
        a_ref, c_ref, a_oppo, c_oppo = util.find_faces_octa(coord)

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
            dist = distance.euclidean(fcl[i], fcl[j])

            if i == 0:
                texts = f"{fal[i]}-{fal[j]}{j} {dist:10.6f}"

            else:
                texts = f"{fal[i]}{i}-{fal[j]}{j} {dist:10.6f}"

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
                dist = distance.euclidean(aco[n][3][i], aco[n][3][j])

                if i == 0:
                    texts = f"{aco[n][2][i]}-{aco[n][2][j]}{j} {dist:10.6f}"

                else:
                    texts = f"{aco[n][2][i]}{i}-{aco[n][2][j]}{j} {dist:10.6f}"

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


def surface_area(self, aco):
    """
    Find the area of the faces of octahedral structure.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    """
    wd = tk.Toplevel(self.master)
    wd.wm_iconbitmap(r"..\images\molecule.ico")
    wd.title("The area of triangular face")
    wd.geometry("380x500")
    wd.option_add("*Font", "Arial 10")
    frame = tk.Frame(wd)
    frame.grid()
    box = tkscrolled.ScrolledText(frame, wrap="word", width="50", height="30", undo="True")
    box.grid(row=0, pady="5", padx="5")

    for n in range(len(self.atom_coord_octa)):
        if n > 0:
            box.insert(tk.END, "\n==============================\n\n")

        num, metal, _, coord = self.atom_coord_octa[n]
        a_ref, c_ref, a_oppo, c_oppo = util.find_faces_octa(coord)

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

