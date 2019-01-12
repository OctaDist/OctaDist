"""
Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

----------------------------------------------------------------------
OctaDist version 1.2

Octahedral Distortion Analysis
Software website: www.github.com/rangsimanketkaew/octadist
Last modified: January 2018

This program, we use Python 3.7.2 and TkInter as GUI maker.
PyInstaller is used as executable compiler.
Written and tested on PyCharm 2018.3.3 (Community Edition) program

Author: Rangsiman Ketkaew
        Computational Chemistry Research Unit
        Department of Chemistry
        Faculty of Science and Technology
        Thammasat University, Pathum Thani, 12120 Thailand
Contact: rangsiman1993@gmail.com
         rangsiman_k@sci.tu.ac.th
Personal website: https://sites.google.com/site/rangsiman1993
"""

program_version = 1.2

import numpy as np
from math import sqrt, pow
import datetime
import webbrowser

from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class OctaDist:

    def __init__(self, masters):
        """
        "masters" is a top frame that Menubar belongs to.
        "master" is a sub-frame that all widgets belongs to.
        """

        self.masters = masters

        # Set program title
        masters.title("OctaDist")

        # Set font and text size as default setting.
        FONT = "Arial 10"
        self.masters.option_add("*Font", FONT)

        # width x height + x_offset + y_offset
        # master.geometry("350x610+400+100")
        # master.resizable(0,0)
        # master.bind('<Escape>', quit)

        # Configure frame
        master = Frame(masters, width="2", height="2")
        master.grid(padx=5, pady=5)

        """
        Create menu bar
            File
            |- New                        << clear_cache
            |- Open                       << open_file
            |- Open multiple files        << open_multiple
            |- Save as ..                 << save_file
            |-------------
            |- Exit                       << quit_program
            Tools
            |- Show structural parameters << structure_param
            Help
            |- Program help               << popup_program_help
            |- About program              << popup_about
            |- License info               << popup_license
        """

        menubar = Menu(masters)
        # add menu bar button
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)

        # sub-menu
        filemenu.add_command(label="New", command=self.clear_cache)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Open multiple files", command=self.open_multiple)
        filemenu.add_command(label="Save as ..", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit_program)

        # add menu bar button
        toolsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        # add sub-menu
        toolsmenu.add_command(label="Show structural parameters")

        # add menu bar button
        helpmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # add sub-menu
        helpmenu.add_command(label="Program help", command=self.popup_program_help)
        helpmenu.add_command(label="About program", command=self.popup_about)
        helpmenu.add_command(label="License information", command=self.popup_license)
        masters.config(menu=menubar)

        print("")
        print(" OctaDist Copyright (C) 2019  Rangsiman Ketkaew  (rangsiman1993@gmail.com)")
        print(" This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.")
        print(" This is free software, and you are welcome to redistribute it under")
        print(" certain conditions; see <https://www.gnu.org/licenses/> for details.")
        print("")
        print("       ==============================================================")
        print("                                OctaDist {}".format(program_version))
        print("")
        print("                       OCTAHEDRAL DISTORTION ANALYSIS")
        print("                       ------------------------------")
        print("           A PROGRAM FOR DETERMINING THE STRUCTURAL PARAMETERS OF")
        print("                     THE DISTORTED OCTAHEDRAL STRUCTURE")
        print("")
        print("                            by Rangsiman Ketkaew")
        print("                             January 8th, 2019")
        print("                https://github.com/rangsimanketkaew/OctaDist")
        print("       ==============================================================")
        print("")

        # program details
        program_name = "Octahedral Distortion Analysis"
        self.msg_1 = Label(master, foreground="blue", font=("Arial", 16, "bold"), text=program_name)
        self.msg_1.config()
        self.msg_1.grid(pady="5", row=0, columnspan=4)
        description = "Determine the structural distortion between two octahedral structures."
        self.msg_2 = Label(master, text=description)
        self.msg_2.grid(pady="5", row=1, columnspan=4)

        # button to browse input file
        self.btn_open_file = Button(master, command=self.open_file, text="Browse file")
        self.btn_open_file.grid(pady="5", row=2, column=0)

        # button to run
        self.btn_run = Button(master, command=self.calc_all_param, text="Compute parameters")
        # btn_run.config(font="Segoe 10")
        self.btn_run.grid(sticky=W, pady="5", row=2, column=1, columnspan=2)

        # button to clear cache
        self.btn_open_file = Button(master, command=self.clear_cache, text="Clear cache", )
        self.btn_open_file.grid(sticky=W, pady="5", row=2, column=3)

        # coordinate label
        self.lbl_1 = Label(master, text="Molecule Specifications")
        self.lbl_1.grid(sticky=W, pady="5", row=3, columnspan=4)

        # text box for showing cartesian coordinates
        self.textBox_coord = Text(master, height="14", width="65", wrap="word")
        self.textBox_coord.grid(pady="5", row=4, columnspan=4)

        # Octahedral distortion parameters
        self.lbl_2 = Label(master, text="Octahedral distortion parameters")

        # lbl_2.config(font="Segoe 10 bold")
        self.lbl_2.grid(row=6, column=1, columnspan=2)

        # Display coordinate and vector projection
        self.lbl_display = Label(master, text="Graphical Displays")
        # self.lbl_display.config(font="Segoe 10 bold")
        self.lbl_display.grid(row=6, column=0, padx="30")

        # button to draw structure
        self.btn_draw_structure = Button(master, command=self.draw_structure, text="Octahedral structure")
        self.btn_draw_structure.grid(pady="5", row=7, column=0)

        # button to draw plane
        self.btn_draw_plane = Button(master, command=self.draw_plane, text="Projection plane", width="15")
        self.btn_draw_plane.grid(pady="5", row=8, column=0)

        # button to draw vector projection
        self.btn_draw_projection = Button(master, command=self.draw_projection, text="Projected atoms", width="15")
        self.btn_draw_projection.grid(pady="5", row=9, column=0)

        # Delta
        self.lbl_dist = Label(master, text="Δ  = ")
        self.lbl_dist.grid(sticky=E, pady="5", row=7, column=1)
        self.textBox_delta = Text(master, height="1", width="15", wrap="word")
        self.textBox_delta.grid(row=7, column=2, sticky=W)

        # Sigma
        self.lbl_sigma = Label(master, text="Σ  = ")
        self.lbl_sigma.grid(sticky=E, pady="5", row=8, column=1)
        self.textBox_sigma = Text(master, height="1", width="15", wrap="word")
        self.textBox_sigma.grid(sticky=W, row=8, column=2)
        self.lbl_sigma_unit = Label(master, text="degree")
        self.lbl_sigma_unit.grid(sticky=W, pady="5", row=8, column=3)

        # Theta
        self.lbl_theta = Label(master, text="Θ  = ")
        self.lbl_theta.grid(sticky=E, pady="5", row=9, column=1)
        self.textBox_theta = Text(master, height="1", width="15", wrap="word")
        self.textBox_theta.grid(sticky=W, row=9, column=2)
        self.lbl_theta_unit = Label(master, text="degree")
        self.lbl_theta_unit.grid(sticky=W, pady="5", row=9, column=3)

        # Link
        link = "https://github.com/rangsimanketkaew/OctaDist"
        self.lbl_link = Label(master, foreground="blue", text=link, cursor="hand2")
        self.lbl_link.grid(pady="5", row=10, columnspan=4)
        self.lbl_link.bind("<Button-1>", self.callback)

    def clear_cache(self):
        """Clear all variables
        """
        global file_name, file_data, atom_list, coord_list

        print("Command: Clear cache")

        file_name = ""
        file_data = ""
        atom_list = 0
        coord_list = 0

        self.textBox_coord.delete(1.0, END)
        self.textBox_delta.delete(1.0, END)
        self.textBox_sigma.delete(1.0, END)
        self.textBox_theta.delete(1.0, END)

        self.clear_results()

    def clear_results(self):
        """Clear the computed parameters
        """
        global computed_delta, computed_sigma, computed_theta

        computed_delta = 0.0
        computed_sigma = 0.0
        computed_theta = 0.0

    def quit_program(self):
        """Quit program
        """
        print("Command: Quit program")
        print("Bye bye ...")
        
        self.masters.quit()

    def popup_open_error(self):
        """Show error message when opening file twice
        """
        print("Error: Open Error")
        
        showinfo("Error", "You already loaded input file. Please clear cache before loading a new file.")

    def popup_nofile_error(self):
        """Show error message when opening file twice
        """
        print("Error: No input file")
        
        showinfo("Error", "No input file. Click \"Browse file\" to load a new file.")

    def popup_nocalc_error(self):
        """Show error message when save file but no any parameters computed
        """
        print("Error: No results")
        
        showinfo("Error", "No results. Click \"Compute parameters\" to calculate octahedral distortion parameters.")

    def popup_wrong_format(self):
        """Show error message when opening file twice
        """
        print("Error: Wrong input format")
        
        showinfo("Error", "Your input file format is not supported.")

    def popup_program_help(self):
        """Open program help page
            - Usage
            - Input file format
            - References
        """

        print("Command: Show program help")

        hp = Tk()
        # hp.overrideredirect(1)
        hp.option_add("*Font", "Arial 10")
        hp.geometry("500x450+750+200")
        hp.title("Program Help")

        # Usage
        lbl = Label(hp, text="Usage:")
        lbl.pack(anchor=W)
        msg_help_1 = "1. Browse file\n" \
                     "2. Compute parameters\n" \
                     "3. Check results\n" \
                     "4. File → Save as ..\n"
        msg = Message(hp, text=msg_help_1, width="450")
        # msg.config(font=("Arial 10"))
        msg.pack(anchor=W)

        # Input format
        lbl = Label(hp, text="Supported input file format:")
        lbl.pack(anchor=W)
        msg_help_2 = "  <Metal center 0>  <X>  <Y>  <Z>\n" \
                     "  <Ligand atom 1>  <X>  <Y>  <Z>\n" \
                     "  <Ligand atom 2>  <X>  <Y>  <Z>\n" \
                     "  <Ligand atom 3>  <X>  <Y>  <Z>\n" \
                     "  <Ligand atom 4>  <X>  <Y>  <Z>\n" \
                     "  <Ligand atom 5>  <X>  <Y>  <Z>\n" \
                     "  <Ligand atom 6>  <X>  <Y>  <Z>\n" \
                     "  <optional>\n" \
                     "  ...\n"
        msg = Message(hp, text=msg_help_2, width="450")
        msg.config(font="Arial 10 italic")
        msg.pack(anchor=W)

        # References
        lbl = Label(hp, text="References:")
        lbl.pack(anchor=W)
        msg_help_3 = "1. J. A. Alonso, M. J. Martı´nez-Lope, M. T. Casais, M. T. Ferna´ndez-Dı´az\n" \
                     "   Inorg. Chem. 2000, 39, 917-923\n" \
                     "2. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson\n" \
                     "   Inorg. Chem. 1996, 35, 2100.\n" \
                     "3. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau\n" \
                     "   Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
        msg = Message(hp, text=msg_help_3, width="450")
        # msg.config(font=("Arial 10"))
        msg.pack(anchor=W)

        hp.mainloop()

    def popup_about(self):
        """Show author information
        """
        print("Command: Show program information")

        text = "OctaDist version {}\n" \
               "\n" \
               "Programming:\n" \
               "Rangsiman Ketkaew\n" \
               "Computational Chemistry Research Unit\n" \
               "Department of Chemistry\n" \
               "Faculty of Science and Technology\n" \
               "Thammasat University, Pathum Thani, 12120 Thailand\n" \
               "\n" \
               "Contact:\n" \
               "E-mail: rangsiman1993@gmail.com\n" \
               "Website: https://github.com/rangsimanketkaew/OctaDist" \
            .format(program_version)
        showinfo("About program", text)

    def popup_license(self):
        """Show program info
        """
        print("Command: Show program license information")

        text = "OctaDist {} Copyright (C) 2019  Rangsiman Ketkaew\n" \
               "\n" \
               "This program is free software: you can redistribute it " \
               "and/or modify it under the terms of the GNU General Public " \
               "License as published by the Free Software Foundation, either " \
               "version 3 of the License, or (at your option) any later version.\n" \
               "\n" \
               "This program is distributed in the hope that it will be useful, " \
               "but WITHOUT ANY WARRANTY; without even the implied warranty " \
               "of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. " \
               "See the GNU General Public License for more details.\n" \
               "\n" \
               "You should have received a copy of the GNU General Public License " \
               "along with this program. If not, see <https://www.gnu.org/licenses/>." \
            .format(program_version)
        showinfo("License", text)

    def callback(self, event):
        webbrowser.open_new(event.widget.cget("text"))

    def file_len(self, fname):
        """Count line in file
        
        :param fname: string 
        :return: number of line in file
        """
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def check_txt_type(self, f):
        """Check if the input file
        text file format
        ----------------
        
        <index 0> <X> <Y> <Z>
        <index 1> <X> <Y> <Z>
        <index 2> <X> <Y> <Z>
        <index 3> <X> <Y> <Z>
        <index 4> <X> <Y> <Z>
        <index 5> <X> <Y> <Z>
        <index 6> <X> <Y> <Z>

        ***The first atom must be metal center.
        
        :param f: string - filename
        :return: int 1 if file is a .txt fie format
        """

        if self.file_len(f) < 7:
            return 0
        else:
            return 1

    def get_coord_from_txt(self, f):
        """Get coordinate from .txt file
        
        :param f: string - file
        :return: atom_list and coord_list
        """
        global atom_list, coord_list

        print("Command: Get Cartesian coordinates")

        file = open(f, "r")
        line = file.readlines()
        file.close()

        atom_raw = []

        for l in line:
            # read atom on 1st column and insert to array
            lst = l.split(' ')[0]
            atom_raw.append(lst)

        # Get only first 7 atoms
        atom_list = atom_raw[0:7]

        """Read file again for getting XYZ coordinate
            We have two ways to do this, 
            1. use >> file.seek(0) <<
            2. use >> file = open(f, "r") <<
        """

        file = open(f, "r")
        coord_raw = np.loadtxt(file, skiprows=0, usecols=[1, 2, 3])
        file.close()

        # Get only first 7 atoms
        coord_list = coord_raw[0:7]

        return atom_list, coord_list

    def check_xyz_type(self, f):
        """Check if the input file is .xyz file format
        
        xyz file format
        ---------------
        
        <number of atom>
        <comment>
        <index 0> <X> <Y> <Z>
        <index 1> <X> <Y> <Z>
        <index 2> <X> <Y> <Z>
        <index 3> <X> <Y> <Z>
        <index 4> <X> <Y> <Z>
        <index 5> <X> <Y> <Z>
        <index 6> <X> <Y> <Z>

        ***The first atom must be metal center.
        :param f: string - filename
        :return: int - 1 if the file is .xyz format
        """
        file = open(f, 'r')

        first_line = file.readline()

        first = 0

        try:
            first = int(first_line)
        except ValueError:
            return 0

        if self.file_len(f) >= 9:
            return 1
        else:
            return 0

    def get_coord_from_xyz(self, f):
        """Get coordinate from .xyz file

        :param f: string - input file
        :return: atom_list and coord_list
        """
        global atom_list, coord_list
        
        print("Command: Get Cartesian coordinates")

        return print("XYZ is not supported.")

    def check_gaussian_type(self, f):
        """Check if the input file is Gaussian file format
        
        :param f: string - input file
        :return: int - 1 if file is Gaussian output file, return 0 if not.
        """
        gaussian_file = open(f, "r")
        nline = gaussian_file.readlines()

        for i in range(len(nline)):
            if "Standard orientation:" in nline[i]:
                return 1
            
        return 0

    def get_coord_from_gaussian(self, f):
        """Extract XYZ coordinate from Gaussian output file

        :param f: string - input file
        :return: atom_list and coord_list
        """
        global atom_list, coord_list

        print("Command: Get Cartesian coordinates")

        atom_raw_from_g09 = []
        coord_raw_from_g09 = []

        gaussian_file = open(f, "r")
        nline = gaussian_file.readlines()

        start = 0
        end = 0

        for i in range(len(nline)):
            if "Standard orientation:" in nline[i]:
                start = i

        for i in range(start + 5, len(nline)):
            if "---" in nline[i]:
                end = i
                break

        for line in nline[start + 5: end]:
            dat = line.split()
            dat1 = int(dat[1])
            coord_x = float(dat[3])
            coord_y = float(dat[4])
            coord_z = float(dat[5])

            if dat1 == 1:
                dat1 = "H"
            elif dat1 == 2:
                dat1 = "He"
            elif dat1 == 3:
                dat1 = "Li"
            elif dat1 == 4:
                dat1 = "Be"
            elif dat1 == 5:
                dat1 = "B"
            elif dat1 == 6:
                dat1 = "C"
            elif dat1 == 7:
                dat1 = "N"
            elif dat1 == 8:
                dat1 = "O"
            elif dat1 == 9:
                dat1 = "F"
            elif dat1 == 10:
                dat1 = "Ne"
            elif dat1 == 11:
                dat1 = "Na"
            elif dat1 == 12:
                dat1 = "Mg"
            elif dat1 == 13:
                dat1 = "Al"
            elif dat1 == 14:
                dat1 = "Si"
            elif dat1 == 15:
                dat1 = "P"
            elif dat1 == 16:
                dat1 = "S"
            elif dat1 == 17:
                dat1 = "Cl"
            elif dat1 == 18:
                dat1 = "Ar"
            elif dat1 == 19:
                dat1 = "K"
            elif dat1 == 20:
                dat1 = "Ca"
            elif dat1 == 21:
                dat1 = "Sc"
            elif dat1 == 22:
                dat1 = "Ti"
            elif dat1 == 23:
                dat1 = "V"
            elif dat1 == 24:
                dat1 = "Cr"
            elif dat1 == 25:
                dat1 = "Mn"
            elif dat1 == 26:
                dat1 = "Fe"
            elif dat1 == 27:
                dat1 = "Co"
            elif dat1 == 28:
                dat1 = "Ni"
            elif dat1 == 29:
                dat1 = "Cu"
            elif dat1 == 30:
                dat1 = "Zn"
            elif dat1 == 31:
                dat1 = "Ga"
            elif dat1 == 32:
                dat1 = "Ge"
            elif dat1 == 33:
                dat1 = "As"
            elif dat1 == 34:
                dat1 = "Se"
            elif dat1 == 35:
                dat1 = "Br"
            elif dat1 == 36:
                dat1 = "Kr"
            elif dat1 == 37:
                dat1 = "Rb"
            elif dat1 == 38:
                dat1 = "Sr"
            elif dat1 == 39:
                dat1 = "Y"
            elif dat1 == 40:
                dat1 = "Zr"
            elif dat1 == 41:
                dat1 = "Nb"
            elif dat1 == 42:
                dat1 = "Mo"
            elif dat1 == 43:
                dat1 = "Tc"
            elif dat1 == 44:
                dat1 = "Ru"
            elif dat1 == 45:
                dat1 = "Rh"
            elif dat1 == 46:
                dat1 = "Pd"
            elif dat1 == 47:
                dat1 = "Ag"
            elif dat1 == 48:
                dat1 = "Cd"
            elif dat1 == 49:
                dat1 = "In"
            elif dat1 == 50:
                dat1 = "Sn"
            elif dat1 == 51:
                dat1 = "Sb"
            elif dat1 == 52:
                dat1 = "Te"
            elif dat1 == 53:
                dat1 = "I"
            elif dat1 == 54:
                dat1 = "Xe"
            elif dat1 == 55:
                dat1 = "Cs"
            elif dat1 == 56:
                dat1 = "Ba"
            elif dat1 == 57:
                dat1 = "La"
            elif dat1 == 58:
                dat1 = "Ce"
            elif dat1 == 59:
                dat1 = "Pr"
            elif dat1 == 60:
                dat1 = "Nd"
            elif dat1 == 61:
                dat1 = "Pm"
            elif dat1 == 62:
                dat1 = "Sm"
            elif dat1 == 63:
                dat1 = "Eu"
            elif dat1 == 64:
                dat1 = "Gd"
            elif dat1 == 65:
                dat1 = "Tb"
            elif dat1 == 66:
                dat1 = "Dy"
            elif dat1 == 67:
                dat1 = "Ho"
            elif dat1 == 68:
                dat1 = "Er"
            elif dat1 == 69:
                dat1 = "Tm"
            elif dat1 == 70:
                dat1 = "Yb"

            atom_raw_from_g09.append(dat1)
            coord_raw_from_g09.append([coord_x, coord_y, coord_z])

        gaussian_file.close()

        atom_list = atom_raw_from_g09[0:7]
        coord_list = coord_raw_from_g09[0:7]
        coord_list = np.asarray(coord_list)

        return atom_list, coord_list

    def get_coord(self, f):
        """Check file type, read data, extract atom and coord from input file

        :param f: string - input file
        :return: insert atom and coord read from input file into text box
        """
        # Check file extension
        if f.endswith(".txt"):
            if self.check_txt_type(f) == 1:
                print("         File type: TXT file")
                print("")
                self.get_coord_from_txt(f)
            else:
                print("Error: Could not read data in TXT file '%s'" % f)
                print("")
        elif f.endswith(".xyz"):
            if self.check_xyz_type(f) == 1:
                print("         File type: XYZ file")
                print("")
                self.get_coord_from_xyz(f)
            else:
                print("Error: Could not read data in XYZ file '%s'" % f)
                print("")
        elif self.check_gaussian_type(f) == 1:
            print("         File type: Gaussian output")
            print("")
            self.get_coord_from_gaussian(f)
        else:
            print("Error: Could not read file '%s'" % f)
            print("")

        print("Command: Show Cartesian coordinates")

        for i in range(len(atom_list)):
            print("          Atom no. {0} : {1}   ({2:5.8f}, {3:5.8f}, {4:5.8f})"
                  .format(i + 1, atom_list[i], coord_list[i][0], coord_list[i][1], coord_list[i][2]))
        print("")

        atom_coords = []

        for i in range(len(atom_list)):
            atom_coords.append([atom_list[i], coord_list[i]])

        texts = "File: {0}\n\n" \
                "Atom     Coordinate\n" \
                " {1}      {2}\n" \
                " {3}      {4}\n" \
                " {5}      {6}\n" \
                " {7}      {8}\n" \
                " {9}      {10}\n" \
                " {11}      {12}\n" \
                " {13}      {14}\n"\
            .format(file_name,
            atom_list[0], coord_list[0],
            atom_list[1], coord_list[1],
            atom_list[2], coord_list[2],
            atom_list[3], coord_list[3],
            atom_list[4], coord_list[4],
            atom_list[5], coord_list[5],
            atom_list[6], coord_list[6])

        self.textBox_coord.insert(INSERT, texts)

    def open_file(self):
        """Open file using Open Dialog
        Atom and coordinates must be in Cartesian (XYZ) coordinate.
        Supported file extensions: .txt, .xyz, and Gaussian output file
        """
        global file_name, file_data

        print("Command: Open input file")

        if file_name != "":
            self.clear_cache()

        file_name = filedialog.askopenfilename( # initialdir="C:/Users/",
            title="Choose input file",
            filetypes=(("Text File", "*.txt"),
                       ("Gaussian Output File", "*.out"),
                       ("Gaussian Output File", "*.log"),
                       ("XYZ File", "*.xyz"),
                       ("All Files", "*.*")))

        # Using try/except in case user types in unknown file or closes without choosing a file.
        try:
            with open(file_name, 'r') as f:
                print("         Open file: " + file_name)
                # print("Command: Insert file data into coordinate box")
                # self.textBox_coord.insert(INSERT, f.read())
                f.close()

                # Check file type and get coordinate
                print("         Determine file type")
                self.get_coord(file_name)
        except:
            print("Error: No input file")

    def open_multiple(self):

        dirname = filedialog.askdirectory( # initialdir="/",
            title='Please select a directory')

        print("Command: Select a directory")
        print("         You selected directory \"{0}\"".format(dirname))

    def save_file(self):
        """Save file using Save Dialog. The result will be saved into .txt or .out file.
        """
        print("Command: Save data to output file")

        if file_name == "":
            self.popup_nofile_error()
            return 1
        if run_check == 0:
            self.popup_nocalc_error()
            return 1

        f = filedialog.asksaveasfile(mode='w',
                                     defaultextension=".txt",
                                     title="Save as",
                                     filetypes=(("Text File", "*.txt"),
                                                ("Output File", "*.out"),
                                                ("All Files", "*.*")))

        if f is None:
            print("Warning: Cancelled save file")
            return 0

        f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew\n")
        f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
        f.write("This is free software, and you are welcome to redistribute it under\n")
        f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n\n")
        f.write("OctaDist {}: Octahedral Distortion Analysis\n".format(program_version))
        f.write("https://github.com/rangsimanketkaew/OctaDist\n\n")
        f.write("By Rangsiman Ketkaew\n")
        f.write("Computational Chemistry Research Unit\n")
        f.write("Department of Chemistry, Faculty of Science and Technology\n")
        f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
        f.write("E-mail: rangsiman1993@gmail.com\n\n")
        f.write("================== Output file ==================\n\n")
        f.write("Date: Saved on {}\n\n".format(datetime.datetime.now()))
        f.write("Input file: " + file_name + "\n\n")
        f.write("Molecular specification of Octahedral structure\n")
        f.write("Atom list:\n")
        for item in atom_list:
            f.write("%s  " % item)
        f.write("\n\n")
        f.write("Coordinate list:\n")
        for item in coord_list:
            f.write("%s\n" % item)
        f.write("\n")
        f.write("Distance between atoms:\n")
        for item in distance_list:
            f.write("Distance --> %5.6f Angstrom\n" % item)
        f.write("\n")
        f.write("Angle of three cis atoms (metal center is vertex):\n")
        for item in new_angle_sigma_list:
            f.write("Angle --> %5.6f degree\n" % item)
        f.write("\n")
        f.write("The Theta parameter for each orthogonal plane:\n")
        for item in computed_theta_list:
            f.write("Angle --> %5.6f degree\n" % item)
        f.write("\n")
        f.write("Octahedral distortion parameters:\n")
        f.write(" - Delta = {0:5.10f}\n".format(computed_delta))
        f.write(" - Sigma = {0:5.10f} degree\n".format(computed_sigma))
        f.write(" - Theta = {0:5.10f} degree\n".format(computed_theta))
        f.write("\n")
        f.write("============ End of the output file. ============\n\n")
        f.close()

        print("Command: Data has been saved to ", f)

    def norm_vector(self, v):
        """Returns the unit vector of the vector v

        :param v: array - vector
        :return: array - normallized vector
        """
        if np.linalg.norm(v) == 0:
            print("Error: Norm of vector", v, "is 0.")

        return v / np.linalg.norm(v)

    def distance_between(self, x, y):
        """Find distance between two point, given points (x1,y1,z1) and (x2,y2,z2)

        :param x: array - cartesian coordinate of atom x
        :param y: array - cartesian coordinate of atom x
        :return: float - distance
        """

        return sqrt(sum([pow(x[i] - y[i], 2) for i in range(len(x))]))

    def distance_avg(self, x):
        """Calculate average M-X distance

        :param x: array - coordinate of atom x
        :return: float - average M-X distance
        """
        dist_sum = []

        for i in range(1, 7):
            results_sum = self.distance_between(x[i], x[0])
            dist_sum.append(results_sum)

        return sum([dist_sum[i] for i in range(6)]) / 6

    def angle_between(self, v0, v1, v2):
        """Compute the angle between vector <v1 - v0> and <v2 - v0>

                                    / v1_x * v2_x + v1_y * v2_y + v1_z * v2_z  \
        angle (in radian) = arccos | ----------------------------------------- |
                                   \               |v1| * |v2|                /

        :param v0, v1, v2: array - coordinate of atom 1, 2, 3
        :return: float - angle in degree unit
        """
        sub_v1 = v1 - v0
        sub_v2 = v2 - v0

        v1_u = self.norm_vector(sub_v1)
        v2_u = self.norm_vector(sub_v2)

        return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

    def rearrange_atom_order(self, v, n):
        """ Rearrange order of atoms

        :param v: array - original coordinate list of ligand atoms
        :param n: int - number of atom for that the last atom would be swapped with
        :return: row-swapped coordinate list
        """
        v[n], v[6] = v[6].copy(), v[n].copy()

        return v

    def search_plane(self, v):
        """Find the plane of octahedral complex

        1. The total number of plane defined by given any three ligand atoms is
            (5!/2!3!) = 10 planes. Then project metal center atom onto the new plane one-by-one
            The projected metal center on new plane is called m'.

        2. Find the minimum distance between metal center atom and its projected point
            d_plane_i = norm(m' - m)
            So we will get d_plane_1, d_plane_2, ..., d_plane_6

        3. Given plane_coord_list array with dimension 10 x 1 x 4.
            This array contains sequence of vertices and the minimum distance from previous step.

                         [[ [coor] [coor] [coor] distance ]  --> plane 1
                          | [coor] [coor] [coor] distance ]  --> plane 2
            plane_coord = | ...          ...           ...|
                          | ...          ...           ...|
                          [ [coor] [coor] [coor] distance ]] ---> plane 10

            where [coor] is array of coordinate (xyz) of atom i

        4. Sort plane_coord_list in ascending order of the minimum distance (column 4)
            Unwanted plane is close to metal center atom. So, delete first 6 plane out of list.
            The remaining 4 planes are the correct plane for atom projection.

        :param v: array - XYZ coordinate of one metal center and six ligand atoms
                    v[0] = metal center atom of complex
                    v[i] = ligand atom of complex
        :return: plane_atom_list and plane_coord_list
        """
        global plane_atom_list, plane_coord_list

        print("Command: Given three atoms. Find the plane (AKA the face) on octahedron.")
        print("")
        print("                   Atom i")
        print("                   /  \\")
        print("                  /    \\")
        print("                 /      \\")
        print("                /        \\")
        print("              Atom j-----Atom k")
        print("")

        plane_atom_list = []
        plane_coord_list = []

        # Find all possible faces --> 10 faces (plane)
        for i in range(1, 4):
            for j in range(i + 1, 5):
                for k in range(j + 1, 6):
                    a, b, c, d = self.eq_of_plane(v[i], v[j], v[k])
                    # Find metal center atom projection onto the new plane
                    m = self.project_atom_onto_plane(v[0], a, b, c, d)
                    # Find distance between metal center atom to its projected point
                    d_btw = self.distance_between(m, v[0])
                    # Insert the number of ligand atoms into list
                    plane_atom_list.append([i, j, k])
                    # Insert the minimum distance into list
                    plane_coord_list.append([v[i], v[j], v[k], d_btw])

        # Do not convert list to array!
        # plane_atom_list = np.asarray(plane_atom_list)
        # plane_coord_list = np.asarray(plane_coord_list)

        pal = plane_atom_list
        pcl = plane_coord_list

        print("Command: Show the given three atoms and shortest distance from metal center to the plane")
        print("         Format of list:")
        print("")
        print("         [<atom_i> <atom_j> <atom_k> <shortest_distance_from_metal_center_to_the_plane>]")
        print("")
        print("         List before sorted:")
        print("          The sequence of atom and coordinate (x,y,z):")

        for i in range(len(pcl)):
            print("          ", pal[i])
            for j in range(3):
                print("              ({0:5.6f}, {1:5.6f}, {2:5.6f})"
                      .format(pcl[i][j][0], pcl[i][j][1], pcl[i][j][2]))
        print("")

        # Sort plane_coord_list in ascending order of the minimum distance (column 4)
        i = 0
        while i < len(pcl):
            k = i
            j = i + 1
            while j < len(pcl):
                # Compare the minimum distance
                if pcl[k][3] > pcl[j][3]:
                    k = j
                j += 1
            # Reorder of atom sequence for both arrays
            pcl[i], pcl[k] = pcl[k], pcl[i]
            pal[i], pal[k] = pal[k], pal[i]
            i += 1

        print("         List after sorted:")
        print("          The sequence of atom and coordinate (x,y,z):")

        for i in range(len(pcl)):
            print("          ", pal[i])
            for j in range(3):
                print("              ({0:5.6f}, {1:5.6f}, {2:5.6f})"
                      .format(pcl[i][j][0], pcl[i][j][1], pcl[i][j][2]))
        print("")

        # Remove first 6 out of 10 planes (first 6 rows), now plane_coord_list remains 4 planes
        scl = pcl[6:]
        sal = pal[6:]

        # Remove the 4th column of distance
        coord_vertex_list = np.delete(scl, 3, 1)

        # Print new plane list after unwanted plane excluded
        print("Command: Delete 6 planes that mostly close to metal center atom")
        print("         List after unwanted plane deleted:")

        for i in range(len(scl)):
            print("          ", sal[i])
            for j in range(3):
                print("              ({0:5.6f}, {1:5.6f}, {2:5.6f})"
                      .format(scl[i][j][0], scl[i][j][1], scl[i][j][2]))
        print("")

        # Return adjusted value to the old array
        plane_atom_list = sal
        plane_coord_list = coord_vertex_list

        return coord_vertex_list

    def eq_of_plane(self, p1, p2, p3):
        """Find the equation of plane of given three ligand atoms
        The general form of plane equation is Ax + By + Cz = D

        :param p1, p2, p3: array - given three points
        :return: float - coefficient of the equation of given plane
        """
        v1 = p3 - p1
        v2 = p2 - p1

        # find the vector orthogonal to the plane using cross product method
        ortho_vector = np.cross(v1, v2)
        a, b, c = ortho_vector
        d = np.dot(ortho_vector, p3)

        return a, b, c, d

    def project_atom_onto_line(self, p, a, b):
        """Find the projected point of atom on the line that defined by another two atoms

        P(x) = x1 + (p - x1).(x2 - x1)/(x2-x1).(x2-x1) * (x2-x1)

        :param p: point to project
        :param a, b: ends of line
        :return:
        """
        ap = p - a
        ab = b - a

        return a + (np.dot(ap, ab) / np.dot(ab, ab) * ab)

    def project_atom_onto_plane(self, v, a, b, c, d):
        """Find the orthogonal vector of point onto the given plane.
        If the equation of plane is Ax + By + Cz = D and the location of point is (L, M, N),
        then the location in the plane that is closest to the point (P, Q, R) is

        (P, Q, R) = (L, M, N) + λ * (A, B, C)
            where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2)

        :param v: array - coordinate of atom
        :param a, b, c, d: float - coefficient of the equation of plane
        :return: the projected point on the othogonal plane
        """
        # Create array of coefficient of vector plane
        v_plane = np.array([a, b, c])
        # find lambda
        lambda_plane = (d - (a * v[0] + b * v[1] + c * v[2])) / np.dot(v_plane, v_plane)

        return v + (lambda_plane * v_plane)

    def find_atom_on_oppo_plane(self, x):
        """Find the atom on the parallel opposite plane. For example,

        list of the atom on plane    list of the atom on opposite plane
                [[1 2 3]                       [[4 5 6]
                 [1 2 4]         --->           [3 5 6]
                 [2 3 5]]                       [1 4 6]]

        :param x: array - three ligand atoms
        :return oppo_pal: array - list of atoms on the opposite plane
        """
        all_atom = [1, 2, 3, 4, 5, 6]
        oppo_pal = []

        print("Command: Find the atoms on the opposite plane")

        # loop for 4 planes
        for i in range(4):
            new_pal = []
            # find the list of atoms on opposite plane
            for e in all_atom:
                if e not in (x[i][0], x[i][1], x[i][2]):
                    new_pal.append(e)
            oppo_pal.append(new_pal)
        print("         List of the coordinate of atom on the opposite plane:")

        v = coord_list

        for i in range(len(oppo_pal)):
            print("         Opposite to {0}".format(x[i]))
            for j in range(3):
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})"
                      .format(oppo_pal[i][j],
                              v[int(oppo_pal[i][j])][0], v[int(oppo_pal[i][j])][1], v[int(oppo_pal[i][j])][2]))
        print("")

        return oppo_pal

    def calc_delta(self, x):
        """Calculate Delta parameter
                                          2
                     1         / d_i - d \
        delta(d) =  --- * sum | -------- |
                     6        \    d    /

        where d_i is individual M-X distance and d is mean M-X distance.
        Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

        :param x: array - coordinate of atoms
        :return computed_delta: float - delta parameter (unitless)
        """
        global distance_list, computed_delta

        print("Command: Calculate distance between metal center (M) and ligand atoms (in Ångström)")

        # Calculate and print individual distance
        distance_list = []

        for i in range(1, 7):
            distance_indi = sqrt(sum([pow(x[i][j] - x[0][j], 2) for j in range(3)]))
            print("          Distance between M and ligand atom {0} : {1:5.6f}"
                  .format(i, distance_indi))
            distance_list.append(distance_indi)

        # Print summary
        print("")
        print("         Total number of computed distance:", len(distance_list))
        print("")

        computed_distance_avg = self.distance_avg(x)

        # Calculate Delta parameter
        for i in range(6):
            diff_dist = (distance_list[i] - computed_distance_avg) / computed_distance_avg
            computed_delta = (pow(diff_dist, 2) / 6) + computed_delta

        return computed_delta

    def calc_sigma(self, v):
        """Calculate Sigma parameter
        
                      12
        Σ = sigma < 90 - angle_i >
             i=1

        Ref: J. K. McCusker et al. Inorg. Chem. 1996, 35, 2100.
        
        :param v: array - coordinate of atoms
        :return computed_sigma: float - sigma parameter in degree
        """
        global new_angle_sigma_list, computed_sigma

        print("Command: Calculate angle between ligand atoms (in degree)")
        print("         Three trans angle (three biggest angles) are excluded.")
        print("")
        print("                   Atom i")
        print("                    /")
        print("                   /")
        print("                  /")
        print("                 /")
        print("                /")
        print("              Vertex ------- Atom j")
        print("")
        print("         Metal center atom is taken as vertex.")
        print("")

        # Calculate individual angle and add to list
        angle_sigma_list = []
        ligand_atom_list = []

        for i in range(1, 7):
            for j in range(i + 1, 7):
                angle_sigma_indi = self.angle_between(v[0], v[i], v[j])
                angle_sigma_list.append(angle_sigma_indi)
                ligand_atom_list.append([i, j])
                
        # Print list of angle
        print("         List of the angles before sorted:")
        # Print list of angles before sorted
        for i in range(len(angle_sigma_list)):
            print("          Angle between atom", ligand_atom_list[i][0], "and atom", ligand_atom_list[i][1],
                  "before sorted: {0:5.6f}".format(angle_sigma_list[i]))
        print("")

        # Sort the angle from lowest to highest
        i = 0
        while i < len(angle_sigma_list):
            k = i
            j = i + 1
            while j < len(angle_sigma_list):
                if angle_sigma_list[k] > angle_sigma_list[j]:
                    k = j
                j += 1
            angle_sigma_list[i], angle_sigma_list[k] = angle_sigma_list[k], angle_sigma_list[i]
            ligand_atom_list[i], ligand_atom_list[k] = ligand_atom_list[k], ligand_atom_list[i]
            i += 1

        print("         List of the angles after sorted:")
        
        for i in range(len(angle_sigma_list)):
            print("          Angle between atom", ligand_atom_list[i][0], "and atom", ligand_atom_list[i][1],
                  "after sorted : {0:5.6f}".format(angle_sigma_list[i]))
        print("")

        # Remove last three angles (last three rows)
        new_angle_sigma_list = angle_sigma_list[:len(angle_sigma_list) - 3]

        # Print new list of angle after three trans angle deleted
        print("         List after three trans angles deleted:")

        for i in range(len(new_angle_sigma_list)):
            print("          {0:5.6f} degree".format(new_angle_sigma_list[i]))

        # Print summary
        print("")
        print("         Total number of angles before three trans angles deleted:", len(angle_sigma_list))
        print("         Total number of angles after three trans angles deleted :", len(new_angle_sigma_list))
        print("")

        # Calculate Sigma parameter
        for i in range(len(new_angle_sigma_list)):
            computed_sigma = abs(90.0 - new_angle_sigma_list[i]) + computed_sigma

        return computed_sigma

    def calc_theta(self, z):
        """Calculate octahedral distortion parameter, Θ
        4 faces, 6 angles each, thus the total number of theta angle is 24 angles.
        
          24
        Θ = sigma < 60 - angle_i >
         i=1

        where angle_i is angle between two plane defined by vector of metal center and ligand atoms.
        
        Ref: M. Marchivie et al. Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

        1. Suppose that we have an octahedron composed of one metal center atom (m)
            and six ligand atoms of which index 1-6. Given three atom of triangular plane

                        1
                    4  /\  6            [1, 3, 5]
                     \/  \/
                     /\  /\             So the rest are on another parallel plane,
                    3  \/  5
                       2                [2, 4, 6]

            m is absent for clarity.

        2. Orthogonally project [2, 4, 6] onto the plane that defined by [1, 3, 5]

            [2, 4, 6] -----> [2', 4', 6']
                    [1, 3, 5]

            The new location of projected atoms on the given plane is [2', 4', 6']

        3. Given the line that pass through two points of the projected atoms

            line1 = 2' <------> 4'
            line2 = 4' <------> 6'
            line3 = 2' <------> 6'

        4. Project another atoms onto the given line
            and Check if two vectors are parallel or anti-parallel

            Example, line1
            
                            2'                          4'
                   1 ------>|                1 ------->|
                            |                          |
                    6' ---->|                          |<------ 6'
                            4'                         2'

                        Parallel                Anti-Parallel
                   Negative dot-product     Positive dot-product

            If anti-parallel, the start and end points of line are adjacent atoms

        5. Repeat step (2) - (4) with loop the plane and reference atoms.

        6. Calculate Theta parameter
        
        :param z: array - coordinate of atom
        :return computed_theta: float - the mininum Theta parameter 
        """
        global computed_theta, computed_theta_list

        print("Command: Calculate the following items")
        print("         - The equation of plane given by three selected ligand atoms, Ax + By + Cz = D")
        print("           Use orthogonal projection to find the projection of all atoms on the given plane.")
        print("")
        print("                         Atom i")
        print("                          / \\        ")
        print("                Atom p --/---\\---- Atom r")
        print("                     \  /     \\    /")
        print("                      \\/       \\  /")
        print("                      /\\ Metal  \\/             All atoms are on the same plane.")
        print("                     /  \\       /\\")
        print("                    /    \\     /  \\")
        print("                   /      \\   /    \\")
        print("                Atom j --- \\-/ --- Atom k")
        print("                          Atom q")
        print("")
        print("         - Angle between metal and ligand atom [i, j, k, p, q, r] (in degree)")
        print("")

        # loop for swapping ligand atom 1, 2, 3, 4, & 5 with no.6 to find all possible plane
        computed_theta_list = []
        
        for i in range(1, 7):
            # Copy coord_list to v_temp without touching to original array
            # use np.array(v) or v[:]
            v_temp = np.array(z)

            print("Command: Swap each ligand atom with 6th atom for finding the plane")
            print("         Swap no. {0} with original atom no.6".format(i))

            swapped_list = self.rearrange_atom_order(v_temp, i)
            print("         Coordinate list after atom order swapped")

            for j in range(len(swapped_list)):
                s = swapped_list[j]
                if j == i:
                    print("          ({0:5.6f}, {1:5.6f}, {2:5.6f}) <- swapped atom".format(s[0], s[1], s[2]))
                if j == 6:
                    print("          ({0:5.6f}, {1:5.6f}, {2:5.6f}) <- Atom no.6".format(s[0], s[1], s[2]))
                else:
                    print("          ({0:5.6f}, {1:5.6f}, {2:5.6f})".format(s[0], s[1], s[2]))
            print("")

            v = np.array(swapped_list)

            # Find suitable plane and atom on opposite plane
            self.search_plane(v)

            pal = plane_atom_list
            pcl = plane_coord_list
            
            print("Command: Find the orthogonal projection of atom on the given plane")
            
            computed_24_angle = []
            oppo_pal = self.find_atom_on_oppo_plane(pal)

            # loop plane
            for j in range(4):
                a, b, c, d = self.eq_of_plane(pcl[j][0], pcl[j][1], pcl[j][2])
                m = self.project_atom_onto_plane(v[0], a, b, c, d)
                
                print("         Orthogonal projection onto the plane", i + 1)
                print("         The equation of plane: {1:5.6f}x + {2:5.6f}y + {3:5.6f}z = {4:5.6f}"
                      .format(i + 1, a, b, c, d))
                print("")

                o1 = int(oppo_pal[j][0])
                o2 = int(oppo_pal[j][1])
                o3 = int(oppo_pal[j][2])

                print("         Old coordinate of projected atom on the original plane")
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})".format(o1, v[o1][0], v[o1][1], v[o1][2]))
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})".format(o2, v[o2][0], v[o2][1], v[o2][2]))
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})".format(o3, v[o3][0], v[o3][1], v[o3][2]))
                print("")

                # Project the opposite atom onto the given plane
                n1 = self.project_atom_onto_plane(v[o1], a, b, c, d)
                n2 = self.project_atom_onto_plane(v[o2], a, b, c, d)
                n3 = self.project_atom_onto_plane(v[o3], a, b, c, d)

                print("         New coordinate of projected atom on the given projection plane")
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})".format(o1, n1[0], n1[1], n1[2]))
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})".format(o2, n2[0], n2[1], n2[2]))
                print("          {0} --> ({1:5.6f}, {2:5.6f}, {3:5.6f})".format(o3, n3[0], n3[1], n3[2]))
                print("")

                # Define line and find that if the two vectors are parallel or anti parallel.
                lal = [[o1, o2, o3],  # lal = line atom list
                       [o2, o3, o1],
                       [o1, o3, o2]]
                
                lcl = [[n1, n2, n3],  # lcl = line coord list
                       [n2, n3, n1],
                       [n1, n3, n2]]

                # loop three ref atoms (vertices of triangular)
                for p in range(3):
                    # Find projected point of "reference atom" and "candidate atom" on the given line
                    for q in range(3):
                        ref_on_line = self.project_atom_onto_line(pcl[j][p], lcl[q][0], lcl[q][1])
                        can_on_line = self.project_atom_onto_line(lcl[q][2], lcl[q][0], lcl[q][1])
                        # Find vector of ref. atom and 
                        vector_ref = ref_on_line - pcl[j][p]
                        vector_can = can_on_line - lcl[q][2]
                        # Check if two vectors are parallel or anti-parallel, 
                        # if the latter found, compute two angles for two adjacent atoms
                        if np.dot(vector_ref, vector_can) < 0:
                            # angle 1
                            angle = self.angle_between(m, pcl[j][p], lcl[q][0])
                            computed_24_angle.append(angle)
                            # angle 2
                            angle = self.angle_between(m, pcl[j][p], lcl[q][1])
                            computed_24_angle.append(angle)

                            print("          Angle between atom {0} and {1}: {2:5.6f}"
                                  .format(pal[j][p], lal[q][0], angle))
                            print("          Angle between atom {0} and {1}: {2:5.6f}"
                                  .format(pal[j][p], lal[q][1], angle))
                            print("")

            # Print all 24 angles
            print("Command: Show all 24 angles")
            for a in range(len(computed_24_angle)):
                print("          Angle", a + 1, ": {0:5.6f} degree".format(computed_24_angle[a]))
            print("")

            # Sum all angles
            diff_angle = 0

            for a in range(len(computed_24_angle)):
                diff_angle += abs(60.0 - computed_24_angle[a])

            computed_theta_list.append(diff_angle)

        # Print each Theta parameter angles
        print("Command: Show computed Θ parameter for each view")
        for i in range(len(computed_theta_list)):
            print("         Θ from view plane {0}: {1:5.6f} degree".format(i + 1, computed_theta_list[i]))

        print("")

        # Find the minimum Theta angle
        computed_theta = min(computed_theta_list)

        return computed_theta

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        global run_check

        if file_name == "":
            self.popup_nofile_error()
            return 1

        run_check = 1
        self.clear_results()

        self.calc_delta(coord_list)
        self.calc_sigma(coord_list)
        self.calc_theta(coord_list)

        self.textBox_delta.delete(1.0, END)
        self.textBox_sigma.delete(1.0, END)
        self.textBox_theta.delete(1.0, END)

        self.textBox_delta.insert(INSERT, '%10.8f' % computed_delta)
        self.textBox_sigma.insert(INSERT, '%10.8f' % computed_sigma)
        self.textBox_theta.insert(INSERT, '%10.8f' % computed_theta)

        print("Command: Calculate octahedral distortion parameters")
        print("")
        print("         Delta <Δ> = {0:10.8f}".format(computed_delta))
        print("         Sigma <Σ> = {0:10.8f} degree".format(computed_sigma))
        print("         Theta <Θ> = {0:10.8f} degree".format(computed_theta))
        print("")

    def draw_structure(self):
        """Display 3D structure of octahedral complex with label for each atoms
        """
        if file_name == "":
            self.popup_nofile_error()
            return 1

        print("Command: Display octahedral structure")

        # Plot and configuration
        fig = plt.figure()
        ax = Axes3D(fig)
        cl = coord_list

        # Plot metal center
        ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=300, linewidths=3, edgecolors='black')
        ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, atom_list[0], fontsize=12)

        # Plot ligand atoms
        for i in range(1, 7):
            ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=200, linewidths=2, edgecolors='black')
            ax.text(cl[i][0] + 0.1, cl[i][1] + 0.1, cl[i][2] + 0.1, "{0},{1}".format(atom_list[i], i), fontsize=12)

        ax.set_xlabel(r'X', fontsize=15)
        ax.set_ylabel(r'Y', fontsize=15)
        ax.set_zlabel(r'Z', fontsize=15)
        ax.set_title('Octahedral structure', fontsize="12")
        ax.grid(True)

        # plt.axis('equal')
        plt.show()

    def draw_plane(self):
        """Display the plane defined by three ligand atoms
        """
        if file_name == "":
            self.popup_nofile_error()
            return 1
        if run_check == 0:
            self.popup_nocalc_error()
            return 1

        print("Command: Display defined plane and orthogonal point")

        cl = coord_list
        vl = self.search_plane(cl)
        vertex_list = []
        color_list = ["red", "blue", "green", "yellow"]

        ##########################################################
        # This function is hard coding. Waiting for improvement
        ##########################################################

        plane_1_x, plane_1_y, plane_1_z = [], [], []
        plane_2_x, plane_2_y, plane_2_z = [], [], []
        plane_3_x, plane_3_y, plane_3_z = [], [], []
        plane_4_x, plane_4_y, plane_4_z = [], [], []

        for i in range(3):
            plane_1_x.append(vl[0][i][0])
            plane_1_y.append(vl[0][i][1])
            plane_1_z.append(vl[0][i][2])
        for i in range(3):
            plane_2_x.append(vl[1][i][0])
            plane_2_y.append(vl[1][i][1])
            plane_2_z.append(vl[1][i][2])
        for i in range(3):
            plane_3_x.append(vl[2][i][0])
            plane_3_y.append(vl[2][i][1])
            plane_3_z.append(vl[2][i][2])
        for i in range(3):
            plane_4_x.append(vl[3][i][0])
            plane_4_y.append(vl[3][i][1])
            plane_4_z.append(vl[3][i][2])

        vertex_set_1 = [list(zip(plane_1_x, plane_1_y, plane_1_z))]
        vertex_set_2 = [list(zip(plane_2_x, plane_2_y, plane_2_z))]
        vertex_set_3 = [list(zip(plane_3_x, plane_3_y, plane_3_z))]
        vertex_set_4 = [list(zip(plane_4_x, plane_4_y, plane_4_z))]

        vertex_list.append(vertex_set_1)
        vertex_list.append(vertex_set_2)
        vertex_list.append(vertex_set_3)
        vertex_list.append(vertex_set_4)

        fig = plt.figure()

        # Display four planes
        for i in range(4):
            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Plane {}".format(i + 1))
            ax.scatter(cl[0][0], cl[0][1], cl[0][2],
                       color='yellow', marker='o', s=100, linewidths=1, edgecolors='black')
            ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, atom_list[0], fontsize=9)

            for j in range(1, 7):
                ax.scatter(cl[j][0], cl[j][1], cl[j][2],
                           color='red', marker='o', s=50, linewidths=1, edgecolors='black')
                ax.text(cl[j][0] + 0.1, cl[j][1] + 0.1, cl[j][2] + 0.1,
                        "{0},{1}".format(atom_list[j], j), fontsize=9)

            # Draw plane
            ax.add_collection3d(Poly3DCollection(vertex_list[i], alpha=0.5, color=color_list[i]))

            ax.set_xlabel(r'X', fontsize=10)
            ax.set_ylabel(r'Y', fontsize=10)
            ax.set_zlabel(r'Z', fontsize=10)
            ax.grid(True)

        # plt.axis('equal')
        plt.show()

    def draw_projection(self):
        """Display the vector projection of all atoms onto the given plane
        """
        if file_name == "":
            self.popup_nofile_error()
            return 1
        if run_check == 0:
            self.popup_nocalc_error()
            return 1

        print("Command: Display the orthogonal projection onto the given plane")

        cl = coord_list
        vl = self.search_plane(cl)
        color_list = ["red", "blue", "green", "yellow"]

        x_range, y_range = [], []
        pl_x, pl_y, pl_z = [], [], []
        l = []

        fig = plt.figure()

        for i in range(4):
            # Figure configuration
            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Orthogonal projection onto the plane {}".format(i + 1), fontsize='10')

            # Plot plane : Given three points, the plane is a*x + b*y + c*z + d = 0
            a, b, c, d = self.eq_of_plane(vl[i][0], vl[i][1], vl[i][2])
            print("         The equation of plane {0} is {1:5.6f}x + {2:5.6f}y + {3:5.6f}z + {4:5.6f} = 0"
                  .format(i + 1, a, b, c, d))

            m = self.project_atom_onto_plane(cl[0], a, b, c, d)

            point = m
            normal = np.array([a, b, c])
            d = -np.sum(point * normal)

            # Parameters for plotting the surface
            for j in range(len(cl)):
                x_range.append(cl[j][0])
                y_range.append(cl[j][1])

            x_limit = min(x_range) - 1, max(x_range) + 1
            y_limit = min(y_range) - 1, max(y_range) + 1
            xx, yy = np.meshgrid((x_limit), (y_limit))
            # xx, yy = np.meshgrid(range(10), range(10))
            z = (- (normal[0] * xx + normal[1] * yy + d)) / normal[2]

            ax.plot_surface(xx, yy, z, alpha='0.5', color=color_list[i])

            # Plot original location of atoms
            # Metal center atom
            ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=100, linewidths=1,
                       edgecolors='black',
                       label="Metal center")
            ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, atom_list[0], fontsize=9)

            # Ligand atoms
            for k in range(1, 7):
                ax.scatter(cl[k][0], cl[k][1], cl[k][2], color='red', marker='o', s=50, linewidths=1,
                           edgecolors='black',
                           label="Ligand atom")
                ax.text(cl[k][0] + 0.1, cl[k][1] + 0.1, cl[k][2] + 0.1, "{0}".format(k), fontsize=9)

            # Plot the location of atoms on the given plane
            # Projected Metal center atom
            ax.scatter(m[0], m[1], m[2], color='orange', marker='o', s=100, linewidths=1, edgecolors='black',
                       label="Projected metal center")
            ax.text(m[0] + 0.1, m[1] + 0.1, m[2] + 0.1, "{}*".format(atom_list[0]), fontsize=9)

            # Ligand atom projected onto the plane
            # Projected Ligand atom
            for n in range(1, 7):
                l.append(self.project_atom_onto_plane(cl[n], a, b, c, d))
                pl_x.append(self.project_atom_onto_plane(cl[n], a, b, c, d)[0])
                pl_y.append(self.project_atom_onto_plane(cl[n], a, b, c, d)[0])
                pl_z.append(self.project_atom_onto_plane(cl[n], a, b, c, d)[0])
            for p in range(6):
                ax.scatter(l[p][0], l[p][1], l[p][2], color='blue', marker='o', s=50, linewidths=1, edgecolors='black',
                           label="Projected ligand atom")
                ax.text(l[p][0] + 0.1, l[p][1] + 0.1, l[p][2] + 0.1, "{0}".format(p + 1), fontsize=9)

            ax.set_xlabel(r'X', fontsize=10)
            ax.set_ylabel(r'Y', fontsize=10)
            ax.set_zlabel(r'Z', fontsize=10)
            ax.grid(True)

        print("")

        # ax.legend()

        # Draw line
        # x, y, z = [], [], []
        # for i in range(1, 7):
        #     x.append(cl[i][0])
        #     y.append(cl[i][1])
        #     z.append(cl[i][2])
        # ax.plot(x, y, z, 'k-')

        # plt.axis('equal')
        plt.show()


def main():
    masters = Tk()
    MainProgram = OctaDist(masters)

    global file_name, file_data, run_check
    global computed_delta, computed_sigma, computed_theta

    file_name = ""
    file_data = ""
    run_check = 0
    computed_delta = 0.0
    computed_sigma = 0.0
    computed_theta = 0.0

    # activate program windows
    masters.mainloop()


if __name__ == '__main__':
    main()
