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

import octadist
from octadist.src import linear, popup, util


class DataComplex:
    """
    Show info of input complex.

    Parameters
    ----------
    master : None, object
        If None, use tk.Tk().
        If not None, use tk.Toplevel(master).

    Examples
    --------
    >>> atom
    ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']

    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]

    >>> my_app = DataComplex()
    >>> my_app.add_coord(atom, coord)

    """
    def __init__(self, master=None):
        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

        self.start_app()

    def start_app(self):
        """
        Start application.

        """
        self.wd.wm_iconbitmap(rf"{octadist.__path__[0]}\logo\molecule.ico")
        self.wd.title("Complex info")
        self.wd.geometry("550x500")
        self.wd.option_add("*Font", "Arial 10")
        self.wd.resizable(0, 0)

        self.frame = tk.Frame(self.wd)
        self.frame.grid()
        self.box = tkscrolled.ScrolledText(self.frame, wrap="word", undo="True",
                                           width="75", height="30")
        self.box.grid(row=0, pady="5", padx="5")

    def add_name(self, file_name):
        """
        Add file name to box.

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
            self.box.insert(tk.END, f"{atom[i]:>2}  "
                                    f"{coord[i][0]:9.6f}  "
                                    f"{coord[i][1]:9.6f}  "
                                    f"{coord[i][2]:9.6f}")
            self.box.insert(tk.END, "\n")
        self.box.insert(tk.END, "\n\n")


class StructParam:
    """
    Show structural parameters of structure.

    Parameters
    ----------
    master : None, object
        If None, use tk.Tk().
        If not None, use tk.Toplevel(master).

    Examples
    --------
    >>> atom
    ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']

    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]

    >>> my_app = DataComplex()
    >>> my_app.add_coord(atom, coord)

    """
    def __init__(self, master=None):
        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

        self.start_app()

    def start_app(self):
        """
        Start application.

        """
        self.wd.wm_iconbitmap(rf"{octadist.__path__[0]}\logo\molecule.ico")
        self.wd.title("Results")
        self.wd.geometry("380x530")
        self.wd.option_add("*Font", "Arial 10")
        self.wd.resizable(0, 0)
        
        self.frame = tk.Frame(self.wd)
        self.frame.grid()
        self.lbl = tk.Label(self.frame, text="Structural parameters")
        self.lbl.grid(row=0, pady="5", padx="5", sticky=tk.W)
        self.box = tkscrolled.ScrolledText(self.frame, wrap="word", undo="True",
                                           width="50", height="30")
        self.box.grid(row=1, pady="5", padx="5")
        
    def add_number(self, number):
        """
        Add file number to box.
        
        Parameters
        ----------
        number : int
            File number.
            
        """
        self.box.insert(tk.INSERT, f"Number : {number}\n")
        
    def add_metal(self, metal):
        """
        Add metal atom to box:
        
        Parameters
        ----------
        metal : str
            Metal atom.
        
        """
        self.box.insert(tk.END, f"Metal: {metal}\n")

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
        self.box.insert(tk.END, "Bond distance (Å)")

        # Bond distance
        for i in range(len(coord)):
            for j in range(i + 1, len(coord)):
                dist = distance.euclidean(coord[i], coord[j])

                if i == 0:
                    texts = f"{atom[i]}-{atom[j]}{j} {dist:10.6f}"
                else:
                    texts = f"{atom[i]}{i}-{atom[j]}{j} {dist:10.6f}"

                self.box.insert(tk.END, "\n" + texts)

        self.box.insert(tk.END, "\n\nBond angle (°)")

        # Bond angle.
        for i in range(len(coord)):
            for j in range(i + 1, len(coord)):
                for k in range(j + 1, 7):
                    vec1 = coord[i] - coord[j]
                    vec2 = coord[k] - coord[j]
                    angle = linear.angle_btw_vectors(vec1, vec2)

                    if i == 0:
                        texts = f"{atom[k]}{k}-{atom[i]}-{atom[j]}{j} {angle:10.6f}"
                    else:
                        texts = f"{atom[k]}{k}-{atom[i]}{i}-{atom[j]}{j} {angle:10.6f}"

                    self.box.insert(tk.END, "\n" + texts)

        self.box.insert(tk.END, "\n\n=================================\n\n")


class SurfaceArea:
    """
    Find the area of the faces of octahedral structure.

    Three ligand atoms are vertices of triangular face

    Parameters
    ----------
    master : None, object
        If None, use tk.Tk().
        If not None, use tk.Toplevel(master).

        Examples
    --------
    >>> coord
    [[2.298354000, 5.161785000, 7.971898000],
     [1.885657000, 4.804777000, 6.183726000],
     [1.747515000, 6.960963000, 7.932784000],
     [4.094380000, 5.807257000, 7.588689000],
     [0.539005000, 4.482809000, 8.460004000],
     [2.812425000, 3.266553000, 8.131637000],
     [2.886404000, 5.392925000, 9.848966000]]

    >>> my_app = SurfaceArea(master=self.master)
    >>> my_app.add_coord(coord)

    """
    def __init__(self, master=None):
        if master is None:
            self.wd = tk.Tk()
        else:
            self.wd = tk.Toplevel(master)

        self.start_app()

    def start_app(self):
        """
        Start application.

        """
        self.wd.wm_iconbitmap(rf"{octadist.__path__[0]}\logo\molecule.ico")
        self.wd.title("The area of triangular face")
        self.wd.geometry("380x500")
        self.wd.option_add("*Font", "Arial 10")
        self.wd.resizable(0, 0)

        self.frame = tk.Frame(self.wd)
        self.frame.grid()
        self.box = tkscrolled.ScrolledText(self.frame, wrap="word", undo="True",
                                           width="50", height="30")
        self.box.grid(row=0, pady="5", padx="5")

    def add_number(self, number):
        """
        Add file number to box.

        Parameters
        ----------
        number : int
            File number.

        """
        self.box.insert(tk.INSERT, f"Number : {number}\n")

    def add_metal(self, metal):
        """
        Add metal atom to box:

        Parameters
        ----------
        metal : str
            Metal atom.

        """
        self.box.insert(tk.END, f"Metal: {metal}\n")

    def add_coord(self, coord):
        a_ref, c_ref, a_oppo, c_oppo = util.find_faces_octa(coord)

        self.box.insert(tk.END, "                 Atoms*        Area (Å³)\n")

        totalArea = 0
        for i in range(8):
            area = linear.triangle_area(c_ref[i][0], c_ref[i][1], c_ref[i][2])
            self.box.insert(tk.END, f"Face no. {i + 1}:  {a_ref[i]}      {area:10.6f}\n")
            totalArea += area

        self.box.insert(tk.END, f"\nThe total surface area:   {totalArea:10.6f}\n")

        self.box.insert(tk.END, "\n==============================\n\n")