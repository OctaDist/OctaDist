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
        FONT = "Segoe-UI 10"
        self.masters.option_add("*Font", FONT)

        # width x height + x_offset + y_offset
        # master.geometry("350x610+400+100")
        # master.resizable(0,0)
        # master.bind('<Escape>', quit)

        # Configure frame
        master = Frame(masters, highlightbackground="Grey", highlightthickness=1, bd="5", width="2", height="2")
        master.grid(padx=5, pady=5)

        """
        Create menu bar
            File
            |- New                        << clear_cache
            |- Open                       << open_file
            |- Save as ..                 << save_file
            |-------------
            |- Exit                       << quit_program
            Tools
            |- Draw octahedral structure  << draw_structure
            |- Draw projection plane      << draw_plane
            |- Draw orthogonal projection << draw_projection
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
        filemenu.add_command(label="Save as ..", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit_program)

        # add menu bar button
        toolsmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        # add sub-menu
        toolsmenu.add_command(label="Draw octahedral structure", command=self.draw_structure)
        toolsmenu.add_command(label="Draw projection plane", command=self.draw_plane)
        toolsmenu.add_command(label="Draw orthogonal projection", command=self.draw_projection)

        # add menu bar button
        helpmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # add sub-menu
        helpmenu.add_command(label="Program help", command=self.popup_program_help)
        helpmenu.add_command(label="About program", command=self.popup_about)
        helpmenu.add_command(label="License information", command=self.popup_license)
        masters.config(menu=menubar)

        print("")
        print("OctaDist (Octahedral Distortion Analysis) Copyright (C) 2019  Rangsiman Ketkaew")
        print("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.")
        print("This is free software, and you are welcome to redistribute it under")
        print("certain conditions; see <https://www.gnu.org/licenses/> for details.")
        print("")
        print("     ==============================================================")
        print("                              OctaDist {}".format(program_version))
        print("")
        print("                     OCTAHEDRAL DISTORTION ANALYSIS")
        print("                     ------------------------------")
        print("         A PROGRAM FOR DETERMINING THE STRUCTURAL PARAMETERS OF")
        print("                   THE DISTORTED OCTAHEDRAL STRUCTURE")
        print("")
        print("                          by Rangsiman Ketkaew")
        print("                           January 8th, 2019")
        print("              https://github.com/rangsimanketkaew/OctaDist")
        print("     ==============================================================")
        print("")

        # program details
        program_name = "Octahedral Distortion Analysis"
        self.msg_1 = Label(master, font=("Segoe-UI", 16, "bold"), text=program_name)
        self.msg_1.config(fg="Blue")
        self.msg_1.grid(pady="5", row=0, columnspan=4)
        description = "Determine the structural distortion between two octahedral structures."
        self.msg_2 = Label(master, text=description)
        self.msg_2.grid(pady="5", row=1, columnspan=4)

        # button to browse input file
        self.btn_open_file = Button(master, command=self.open_file, text="Browse file", )
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

        # lbl_display.config(font="Segoe 10 bold")
        self.lbl_display.grid(row=6, column=0)

        # button to draw structure
        self.btn_draw_structure = Button(master, command=self.draw_structure, text="Octahedral structure")
        self.btn_draw_structure.grid(pady="5", row=7, column=0)

        # button to draw plane
        self.btn_draw_plane = Button(master, command=self.draw_plane, text="Projection plane")
        self.btn_draw_plane.grid(pady="5", row=8, column=0)

        # button to draw vector projection
        self.btn_draw_projection = Button(master, command=self.draw_projection, text="Projected atoms")
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
        self.lbl_link = Label(master, text=link, fg="blue", cursor="hand2")
        self.lbl_link.grid(pady="5", row=10, columnspan=4)
        self.lbl_link.bind("<Button-1>", self.callback)

    def clear_cache(self):
        """Clear all variables
        """

        print("Command: Clear cache")

        global file_name, file_data, atom_list, coord_list

        file_name = ""
        file_data = ""
        atom_list = 0
        coord_list = 0

        # Clear text box
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
        hp.option_add("*Font", "Segoe-UI 10")
        hp.geometry("500x450+750+200")
        hp.title("Program Help")

        # frame1 = Frame(hp, highlightbackground="Black", highlightthickness=10, bd="20")
        # frame1.pack()

        # Usage
        lbl = Label(hp, text="Usage:")
        lbl.pack(anchor=W)

        msg_help_1 = "1. Browse file\n" \
                     "2. Compute parameters\n" \
                     "3. Check results\n" \
                     "4. File → Save as ..\n"
        msg = Message(hp, text=msg_help_1, width="450")
        # msg.config(font=("Segoe-UI 10"))
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
        msg.config(font="Segoe-UI 10 italic")
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
        # msg.config(font=("Segoe-UI 10"))
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

    def check_gaussian_type(self, f):
        """Check if the input file is Gaussian output file

        Parameter
        ---------
        f : string
            File name

        Return
        ------
        0 : int
            Return 0 if file is Gaussian output file
        """

        gaussian_file = open(f, "r")

        numline = gaussian_file.readlines()

        for i in range(len(numline)):
            if "Standard orientation:" in numline[i]:
                return 1
        return 0

    def get_coord_from_gaussian(self, f):
        """Extract XYZ coordinate from Gaussian output file
        """

        print("Command: Get cartesian coordinates")

        global atom_list, coord_list

        atom_raw_from_g09 = []
        coord_raw_from_g09 = []

        gaussian_file = open(f, "r")

        numline = gaussian_file.readlines()

        start = 0
        end = 0

        for i in range(len(numline)):
            if "Standard orientation:" in numline[i]:
                start = i

        for i in range(start + 5, len(numline)):
            if "---" in numline[i]:
                end = i
                break

        for line in numline[start + 5: end]:
            words = line.split()
            word1 = int(words[1])
            coord_x = float(words[3])
            coord_y = float(words[4])
            coord_z = float(words[5])

            if word1 == 1:
                word1 = "H"
            elif word1 == 2:
                word1 = "He"
            elif word1 == 3:
                word1 = "Li"
            elif word1 == 4:
                word1 = "Be"
            elif word1 == 5:
                word1 = "B"
            elif word1 == 6:
                word1 = "C"
            elif word1 == 7:
                word1 = "N"
            elif word1 == 8:
                word1 = "O"
            elif word1 == 9:
                word1 = "F"
            elif word1 == 10:
                word1 = "Ne"
            elif word1 == 11:
                word1 = "Na"
            elif word1 == 12:
                word1 = "Mg"
            elif word1 == 13:
                word1 = "Al"
            elif word1 == 14:
                word1 = "Si"
            elif word1 == 15:
                word1 = "P"
            elif word1 == 16:
                word1 = "S"
            elif word1 == 17:
                word1 = "Cl"
            elif word1 == 18:
                word1 = "Ar"
            elif word1 == 19:
                word1 = "K"
            elif word1 == 20:
                word1 = "Ca"
            elif word1 == 21:
                word1 = "Sc"
            elif word1 == 22:
                word1 = "Ti"
            elif word1 == 23:
                word1 = "V"
            elif word1 == 24:
                word1 = "Cr"
            elif word1 == 25:
                word1 = "Mn"
            elif word1 == 26:
                word1 = "Fe"
            elif word1 == 27:
                word1 = "Co"
            elif word1 == 28:
                word1 = "Ni"
            elif word1 == 29:
                word1 = "Cu"
            elif word1 == 30:
                word1 = "Zn"
            elif word1 == 31:
                word1 = "Ga"
            elif word1 == 32:
                word1 = "Ge"
            elif word1 == 33:
                word1 = "As"
            elif word1 == 34:
                word1 = "Se"
            elif word1 == 35:
                word1 = "Br"
            elif word1 == 36:
                word1 = "Kr"
            elif word1 == 37:
                word1 = "Rb"
            elif word1 == 38:
                word1 = "Sr"
            elif word1 == 39:
                word1 = "Y"
            elif word1 == 40:
                word1 = "Zr"
            elif word1 == 41:
                word1 = "Nb"
            elif word1 == 42:
                word1 = "Mo"
            elif word1 == 43:
                word1 = "Tc"
            elif word1 == 44:
                word1 = "Ru"
            elif word1 == 45:
                word1 = "Rh"
            elif word1 == 46:
                word1 = "Pd"
            elif word1 == 47:
                word1 = "Ag"
            elif word1 == 48:
                word1 = "Cd"
            elif word1 == 49:
                word1 = "In"
            elif word1 == 50:
                word1 = "Sn"
            elif word1 == 51:
                word1 = "Sb"
            elif word1 == 52:
                word1 = "Te"
            elif word1 == 53:
                word1 = "I"
            elif word1 == 54:
                word1 = "Xe"
            elif word1 == 55:
                word1 = "Cs"
            elif word1 == 56:
                word1 = "Ba"
            elif word1 == 57:
                word1 = "La"
            elif word1 == 58:
                word1 = "Ce"
            elif word1 == 59:
                word1 = "Pr"
            elif word1 == 60:
                word1 = "Nd"
            elif word1 == 61:
                word1 = "Pm"
            elif word1 == 62:
                word1 = "Sm"
            elif word1 == 63:
                word1 = "Eu"
            elif word1 == 64:
                word1 = "Gd"
            elif word1 == 65:
                word1 = "Tb"
            elif word1 == 66:
                word1 = "Dy"
            elif word1 == 67:
                word1 = "Ho"
            elif word1 == 68:
                word1 = "Er"
            elif word1 == 69:
                word1 = "Tm"
            elif word1 == 70:
                word1 = "Yb"

            # collect atom
            atom_raw_from_g09.append(word1)
            # collect coordinate
            coord_raw_from_g09.append([coord_x, coord_y, coord_z])

        gaussian_file.close()

        # delete row 8, 9, 10, ...
        atom_list = atom_raw_from_g09[0:7]

        # delete row 8, 9, 10, ...
        coord_list = coord_raw_from_g09[0:7]
        coord_list = np.asarray(coord_list)

        for i in range(len(coord_list)):
            print(coord_list[i])

        for i in range(len(coord_list)):
            print(coord_list[i][0])

        return atom_list, coord_list

    def check_xyz_type(self, f):
        """Check if the input file is Gaussian output file

        Parameter
        ---------
        f : string
            File name

        Return
        ------
        0 : int
            Return 0 if file is Gaussian output file
        """

        file = open(f, 'r')

        first_line = file.readline()

        # print(first_line)

        return 0

    def get_coord_from_xyz(self, f):
        """In case the coordinate is in XYZ file format

        XYZ file format
        ----------------

            <number of atom>
            <comment>                                4
            <index 0> <X> <Y> <Z>                2   |      6
            <index 1> <X> <Y> <Z>                 \  |    /
            <index 2> <X> <Y> <Z>                  \ |  /
            <index 3> <X> <Y> <Z>                    0
            <index 4> <X> <Y> <Z>                  / | \
            <index 5> <X> <Y> <Z>                //  |  \\
            <index 6> <X> <Y> <Z>               1    |   5
                                                     3
        The first atom must be metal center.
        """

        print("Command: Get cartesian coordinates")

        global atom_list, coord_list

        return f

    def get_coord_from_txt(self, f):
        """In case the coordinate is in TXT file format

        text file format
        ----------------
                                                     4
            <index 0> <X> <Y> <Z>                2   |      6
            <index 1> <X> <Y> <Z>                 \  |    /
            <index 2> <X> <Y> <Z>                  \ |  /
            <index 3> <X> <Y> <Z>                    0
            <index 4> <X> <Y> <Z>                  / | \
            <index 5> <X> <Y> <Z>                //  |  \\
            <index 6> <X> <Y> <Z>               1    |   5
                                                     3
        The first atom must be metal center.
        """

        # check if input file is correct format
        # check_format()

        print("Command: Get cartesian coordinates")

        global atom_list, coord_list

        file = open(f, "r")
        line = file.readlines()
        file.close()

        # line = self.textBox_coord.get('1.0', END).splitlines()

        atom_raw = []

        for l in line:
            # read only the 1st column, elements, and pass into array
            lst = l.split(' ')[0]
            atom_raw.append(lst)

        # Get only first 7 atoms
        # delete row 8, 9, 10, ...
        atom_list = atom_raw[0:7]

        """Read file again for getting XYZ coordinate
            We have two ways to do this, 
            1. use >> file.seek(0) <<
            2. use >> file = open(f, "r") <<
        """

        file = open(f, "r")
        coord_raw = np.loadtxt(file, skiprows=0, usecols=[1, 2, 3])
        file.close()

        # delete row 8, 9, 10, ...
        coord_list = coord_raw[0:7]

        return atom_list, coord_list

    def get_coord(self, f):
        """Determine file type and call specific function to extract XYZ coordinates
        """

        # Get coordinate from Gaussian output file
        if self.check_gaussian_type(f) == 1:
            print("         File type: Gaussian output")
            self.get_coord_from_gaussian(f)

        elif self.check_xyz_type(f) == 1:
            print("         File type: XYZ file")
            self.get_coord_from_xyz(f)

        else:
            print("         File type: TXT file")
            self.get_coord_from_txt(f)

        #######################################

        print("Command: Show Cartesian coordinates")
        for i in range(len(atom_list)):
            print("         Atom no.", i + 1, "--> ", atom_list[i], "", coord_list[i])

        # Form list of atom and coordinate
        atom_coords = []
        for i in range(len(atom_list)):
            atom_coords.append([atom_list[i], coord_list[i]])

        # print(atom_coords[0])

        texts = "File: {14}\n\n" \
                "Atom     Coordinate\n" \
                " {0}      {1}\n" \
                " {2}      {3}\n" \
                " {4}      {5}\n" \
                " {6}      {7}\n" \
                " {8}      {9}\n" \
                " {10}      {11}\n" \
                " {12}      {13}\n".format(atom_list[0], coord_list[0],
                                           atom_list[1], coord_list[1],
                                           atom_list[2], coord_list[2],
                                           atom_list[3], coord_list[3],
                                           atom_list[4], coord_list[4],
                                           atom_list[5], coord_list[5],
                                           atom_list[6], coord_list[6],
                                           file_name)

        self.textBox_coord.insert(INSERT, texts)

    def open_file(self):
        """Open file using Open Dialog
        Molecular coordinates must be cartesian coordinate format.
        File extensions supported are *.txt, *.xyz, and *.com
        """

        print("Command: Open input file")

        global file_name, file_data

        # check if filename is empty
        if file_name != "":
            self.clear_cache()

        """
        # check if filename is empty
        if filename != "":
            popup_open_error()
            return 1
        """

        # Open text file
        file_name = filedialog.askopenfilename(  # initialdir="C:/Users/",
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
            print("         No input file")

    def save_file(self):
        """Save file using Save Dialog
        All results is saved into text file (*.txt)
        """

        print("Command: Save data to output file")

        # check if input file exist
        if file_name == "":
            self.popup_nofile_error()
            return 1

        # check if parameters are computed
        if run_check == 0:
            self.popup_nocalc_error()
            return 1

        f = filedialog.asksaveasfile(mode='w',
                                     defaultextension=".txt",
                                     title="Save as",
                                     filetypes=(("Text File", "*.txt"),
                                                ("Output File", "*.out"),
                                                ("All Files", "*.*")))

        # asksaveasfile return `None` if dialog closed with "cancel".
        if f is None:
            print("Warning: Cancelled save file")
            return 0

        f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew\n")
        f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
        f.write("This is free software, and you are welcome to redistribute it under\n")
        f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n\n")
        #########################

        f.write("OctaDist {}: Octahedral Distortion Analysis\n".format(program_version))
        f.write("https://github.com/rangsimanketkaew/OctaDist\n\n")
        f.write("By Rangsiman Ketkaew\n")
        f.write("Computational Chemistry Research Unit\n")
        f.write("Department of Chemistry, Faculty of Science and Technology\n")
        f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
        f.write("E-mail: rangsiman1993@gmail.com\n\n")
        #########################

        f.write("Output file\n")
        f.write("===========\n")
        f.write("Date: Saved on {}\n\n".format(datetime.datetime.now()))
        f.write("Input file: " + file_name + "\n\n")
        #########################

        f.write("Molecular specification of Octahedral structure\n")
        f.write("Atom list:\n")
        for item in atom_list:
            f.write("%s  " % item)
        f.write("\n\n")

        f.write("Coordinate list:\n")
        for item in coord_list:
            f.write("%s\n" % item)
        f.write("\n")
        #########################

        f.write("Distance between atoms:\n")
        for item in distance_list:
            f.write("Distance --> %5.5f Angstrom\n" % item)
        f.write("\n")

        f.write("Angle of three cis atoms (metal center is vertex):\n")
        for item in new_angle_sigma_list:
            f.write("Angle --> %5.5f degree\n" % item)
        f.write("\n")

        f.write("Angle of three projected atoms on the same orthogonal plane:\n")
        for item in angle_theta_list:
            f.write("Angle --> %5.5f degree\n" % item)
        f.write("\n")
        #########################

        f.write("Octahedral distortion parameters:\n")
        f.write(" - Delta = {0:5.10f}\n".format(computed_delta))
        f.write(" - Sigma = {0:5.10f} degree\n".format(computed_sigma))
        f.write(" - Theta = {0:5.10f} degree\n".format(computed_theta))
        f.write("\n")
        f.write("============ End of the output file. ============\n\n")
        #########################

        f.close()  # `()` was missing.

        print("Command: Data has been saved to ", f)

    def dist_btw(self, x, y):
        """Find distance between two point

        Parameter
        ---------
        x, y : array
            cartesian coordinate of two atoms (two points)

        Return
        ------
        individual distance : float
        """

        return sqrt(sum([pow(x[i] - y[i], 2) for i in range(3)]))

    def distance_avg(self, x):
        """Calculate mean M-X distance by averaging the distance between
        metal center and ligand atom, d_i

                ----------------------------------------
        d_i = \/ (x - x_0)^2 + (y - y_0)^2 + (z - z_0)^2

        where x_0, y_0, and z_0 are component vector of metal center

        Parameter
        ---------
        x : array
            cartesian coordinate of atom (point)

        Return
        ------
        average distance : float
        """

        dist_sum = []

        for i in range(1, 7):
            results_sum = self.dist_btw(x[i], x[0])
            dist_sum.append(results_sum)

        return sum([dist_sum[i] for i in range(6)]) / 6

    def calc_delta(self, x):
        """Calculate 1st octahedral distortion parameter, delta.

                                          2
                     1         / d_i - d \
        delta(d) =  --- * sum | -------- |
                     6        \    d    /

                    where d_i is individual M-X distance and d is mean M-X distance.

        Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20

        Parameter
        ---------
        x : array
            cartesian coordinate of atom (point)

        Return
        ------
        computed_delta : float
            delta parameter (unitless)
        """

        global distance_list, computed_delta

        print("Command: Calculate distance between atoms (in Ångström)")

        # Calculate and print individual distance
        distance_list = []

        for i in range(1, 7):
            distance_indi = sqrt(sum([pow(x[i][j] - x[0][j], 2) for j in range(3)]))
            print("         Distance between metal center and ligand atom", i, "is {0:5.5f}".format(distance_indi))
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

    def normalize_vector(self, v):
        """Returns the unit vector of the vector v: normalizing

        Parameter
        ---------
        v : array
            vector

        Return
        ------
        normalized vector : array
        """

        if np.linalg.norm(v) == 0:
            print("Error: norm of vector", v, "is 0. Thus function normalize_vector returns a wrong value.")

        return v / np.linalg.norm(v)

    def angle_between(self, v0, v1, v2):
        """Compute the angle between vector <v1 - v0> and <v2 - v0>
        and returns the angle in degree.

                                    / v1_x * v2_x + v1_y * v2_y + v1_z * v2_z  \
        angle (in radian) = arccos | ----------------------------------------- |
                                   \               |v1| * |v2|                /

        Ex.
                >> angle_between((1, 0, 0), (0, 1, 0), (0, 0, 0))
                1.5707963267948966 (radian)
                90.0 (degree)

        Parameter
        ---------
        v0, v1, v2 : array
                    coordinate of three atoms

        Return
        ------
        angle : float
            angle in degree unit
        """

        # Find ray 1 and ray 2 by subtracting vectors
        sub_v1 = v1 - v0
        sub_v2 = v2 - v0

        v1_u = self.normalize_vector(sub_v1)
        v2_u = self.normalize_vector(sub_v2)

        return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

    def calc_sigma(self, v):
        """Calculate octahedral distortion parameter, Σ

              12
        Σ = sigma < 90 - angle_i >
             i=1

        For more details, please refer to following article.
        J. K. McCusker, A. L. Rheingold, D. N. Hendrickson, Inorg. Chem. 1996, 35, 2100.

        Parameter
        ---------
        v : array
            coordinate of ligand atoms

        Return
        ------
        computed_sigma : float
            sigma parameter in degree
        """

        global new_angle_sigma_list, computed_sigma

        print("Command: Calculate angle between ligand atoms (in degree)")
        print("         Three trans angle (three biggest angles) are excluded.")
        print("")
        print("                   Atom i\n"
              "                    /\n"
              "                   /\n"
              "                  /\n"
              "                 /\n"
              "                /\n"
              "              Vertex ------- Atom j")
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

        # Backup the before sorted angle
        bf_angle_sigma_list = angle_sigma_list

        # Sort the angle from lowest to highest
        # Two loops is used to sort the distance from lowest to greatest numbers
        i = 0
        while i < len(angle_sigma_list):
            k = i
            j = i + 1
            while j < len(angle_sigma_list):
                if angle_sigma_list[k] > angle_sigma_list[j]:
                    k = j
                j += 1
            angle_sigma_list[i], angle_sigma_list[k] = angle_sigma_list[k], angle_sigma_list[i]
            i += 1

        # Backup the after sorted angle
        af_angle_sigma_list = angle_sigma_list

        # Print list of angle
        print("         List of the angles:")

        # Print list of angles before sorted
        for i in range(len(bf_angle_sigma_list)):
            print("         Angle between atom", ligand_atom_list[i][0], "and atom", ligand_atom_list[i][1],
                  "before sorted: {0:5.5f}".format(bf_angle_sigma_list[i]))
        print("")

        # Print list of angles after sorted
        for i in range(len(af_angle_sigma_list)):
            print("         Angle after sorted: {0:5.5f}".format(af_angle_sigma_list[i]))
        print("")

        # Remove last three angles (last three rows)
        new_angle_sigma_list = af_angle_sigma_list[:len(af_angle_sigma_list) - 3]

        # Print new list of angle after three trans angle deleted
        print("         List after three trans angles deleted:")

        for i in range(len(new_angle_sigma_list)):
            print("         ", new_angle_sigma_list[i])

        # Print summary
        print("")
        print("         Total number of angles before three trans angles deleted:", len(af_angle_sigma_list))
        print("         Total number of angles after three trans angles deleted :", len(new_angle_sigma_list))
        print("")

        # Calculate Sigma parameter
        for i in range(len(new_angle_sigma_list)):
            computed_sigma = abs(90.0 - new_angle_sigma_list[i]) + computed_sigma

        return computed_sigma

    def find_plane(self, v):
        """Find plane of given octahedral complex

        v = XYZ coordinate of complex
        v[0] = metal center atom of complex
        v[i] = ligand atom of complex

        Parameter
        ---------
        v : array
            coordinate of ligand atoms

        Return
        ------
        final_plane_list : array - int
            the possible 4 plane
        """

        global final_plane_list

        print("Command: Find the plane (AKA the face on octahedron). Given three atoms as vertices")
        print("")
        print("                   Atom i\n"
              "                   /  \\\n"
              "                  /    \\\n"
              "                 /      \\\n"
              "                /        \\\n"
              "              Atom j-----Atom k")
        print("")
        print("         Total number of the selected plane is 10")
        print("")

        # list of vertex of triangle (face of octahedral)
        plane_list = []

        # Find four possible faces --> This would result 10 plane
        for i in range(1, 4):
            for j in range(i + 1, 5):
                for k in range(j + 1, 6):
                    self.find_plane_eq(v[i], v[j], v[k])

                    # Find distance between metal center atom and its projected point on plane
                    # and store the vertex of triangle (face/plane) and distance btw metal to plane into array
                    m = self.project_atom_onto_plane(v[0], a, b, c, d)
                    d_btw = self.dist_btw(m, v[0])
                    plane_list.append(np.array([i, j, k, d_btw]))

        # Print plane list before sorted
        print("Command: Show the list of given three atoms and shortest distance from metal center to the plane")
        print("         Format of list:\n")
        print("         [<atom_i> <atom_j> <atom_k> <shortest_distance_from_metal_center_to_the_plane>]\n")
        print("         List before sorted:")

        for i in range(len(plane_list)):
            print("         ", plane_list[i])
        print("")

        # Use distance between metal center and its projected point to sort list (array)
        # Two loops is used to sort the distance from lowest to greatest numbers
        i = 0

        while i < len(plane_list):
            k = i
            j = i + 1

            while j < len(plane_list):
                if plane_list[k][3] > plane_list[j][3]:
                    k = j
                j += 1

            plane_list[i], plane_list[k] = plane_list[k], plane_list[i]

            i += 1

        # Print plane list after sorted
        print("         List after sorted:")
        for i in range(len(plane_list)):
            print("         ", plane_list[i])
        print("")

        # Remove first six planes from list (first six rows)
        excluded_plane_list = plane_list[6:]

        # Print new plane list after unwanted plane excluded
        print("Command: Delete six planes that mostly closest to metal center atom")
        print("         List after unwanted plane deleted:")

        for i in range(len(excluded_plane_list)):
            print("         ", excluded_plane_list[i])
        print("")

        # Remove the 4th column of distance
        final_plane_list = np.delete(excluded_plane_list, 3, 1)

        # Show final plane list
        print("         Final list of the number of atoms for four selected plane:")

        for i in range(len(final_plane_list)):
            print("         ", final_plane_list[i].astype(int))
        print("")

        # Return 2D string array
        return final_plane_list.astype(int)

    def convert_atom_to_point(self, v):
        """Find 4 correct plane of octahedral complex
        For example,

        list of atom                    list of XYZ coordinate of atom
         [[1 2 3]          [[[0.00 0.00 0.00]  [1.22 2.34 1.23]  [3.21 1.09 -0.43]
          [1 2 4]    --->   [[0.00 0.00 0.00]  [1.22 2.34 1.23]  [-0.56 2.65 0.45]
          [2 3 5]]          [[1.22 2.34 1.23]  [3.21 1.09 -0.43] [2.32 -0.54 -0.23]]

        Parameter
        ---------
        v : array
            coordinate of ligand atoms

        Return
        ------
        coord_vertex_list : array
            list of coordinate of three atoms for each the defined plane
        """

        global coord_vertex_list

        # Generate list of coordinate of selected point
        coord_vertex_list = []
        f = self.find_plane(v)

        for i in range(len(f)):
            coord_vertex_list.append(np.array([v[f[i][0]], v[f[i][1]], v[f[i][2]]]))

        # Print list of coordinate of three selected atoms
        print("Command: Show coordinate list of selected three ligand atoms for defining the plane")

        for i in range(len(coord_vertex_list)):
            print("         Plane", i + 1)
            for j in range(3):
                print("         ", coord_vertex_list[i][j])
        print("")

        return coord_vertex_list

    def find_plane_eq(self, p1, p2, p3):
        """Find the equation of plane that defined by three points (ligand atoms)
        The general form of plane equation is Ax + By + Cz = D

        Input arguments are vertex of plane (triangle)

        Parameter
        ---------
        p1, p2, p3 : array
            the given points

        Return
        ------
        a, b, c, d : float
            coefficient of the equation
        """

        global a, b, c, d

        # subtract vector
        v1 = p3 - p1
        v2 = p2 - p1

        # find the vector orthogonal to the plane using cross product method
        norm_p = np.cross(v1, v2)
        a, b, c = norm_p
        d = np.dot(norm_p, p3)

        return a, b, c, d

    def project_atom_onto_plane(self, v, a, b, c, d):
        """Find the orthogonal vector of point onto the given plane.
        If the equation of plane is Ax + By + Cz = D and the location of point is (L, M, N),
        then the location in the plane that is closest to the point (P, Q, R) is

        (P, Q, R) = (L, M, N) + λ * (A, B, C)

        where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2)

        Input argument: v is vector
                        a, b, and c are A, B, and C
                        d is D

        Parameter
        ---------
        v : array
            the given atom coordinates

        a, b, c, d : float
            coefficient of the equation of plane

        Return
        ------
        projected_point : array
            new location of atom on the given plane (a projected point)
        """

        # Create array of coefficient of vector plane
        v_plane = np.array([a, b, c])

        # find lambda
        lambda_plane = (d - (a * v[0] + b * v[1] + c * v[2])) / np.dot(v_plane, v_plane)

        projected_point = v + (lambda_plane * v_plane)

        return projected_point

    def calc_theta(self, v):
        """Calculate octahedral distortion parameter, Θ

              24
        Θ = sigma < 60 - angle_i >
             i=1

        where angle_i is angle between two plane defined by vector of
        metal center and ligand atoms.

        4 faces, 6 angles each, thus the total number of theta angle is 24 angles.

        For more details, please refer to following article.
        M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau,
        Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.

        Parameter
        ---------
        v : array
            cartesian coordinate of atoms

        Return
        ------
        computed_theta : float
            computed theta angle
        """

        global angle_theta_list, computed_theta

        print("Command: Calculate the following items")
        print("         - The equation of plane given by three selected ligand atoms, Ax + By + Cz = D")
        print("           Use orthogonal projection to find the projection of all atoms on the given plane.")
        print("")
        print("                             Atom i\n"
              "                              / \\        \n"
              "                    Atom p --/---\\---- Atom r\n"
              "                         \  /     \\    /\n"
              "                          \\/       \\  /\n"
              "                          /\\ Metal  \\/\n"
              "                         /  \\       /\\\n"
              "                        /    \\     /  \\\n"
              "                       /      \\   /    \\\n"
              "                    Atom j --- \\-/ --- Atom k\n"
              "                              Atom q")
        print("")
        print("           All atoms are on the same plane.")
        print("")
        print("         - Compute the angle between Metal and ligand atom [i, j, k, p, q, r] (in degree)")
        print("")
        print("         - Default settings:")
        print("           1. If the angle is greater than", angle_cutoff_for_theta_max, ", it will be set to 60.0")
        print("           2. If the angle is less than", angle_cutoff_for_theta_min, ", it will be set to 60.0")
        print("")
        print("         ------------------------------------")
        print("")

        angle_theta_list = []

        cv = self.convert_atom_to_point(v)
        count = 0

        for i in range(4):
            # Find coefficient of plane equation
            a, b, c, d = self.find_plane_eq(cv[i][0], cv[i][1], cv[i][2])

            print("         Orthogonal projection onto the plane", i + 1)
            print("          The equation of plane: {1:5.5f}x + {2:5.5f}y + {3:5.5f}z = {4:5.5f}"
                  .format(i + 1, a, b, c, d))

            # Project metal center onto the given plane
            m = self.project_atom_onto_plane(v[0], a, b, c, d)
            print("          The point of metal center atom on the given plane: "
                  "({0:5.5f}, {1:5.5f}, {2:5.5f})".format(m[0], m[1], m[2]))

            for j in range(1, 6):
                for k in range(2, 7):
                    ##################################################
                    # Not print the projected points of ligand atoms
                    ##################################################
                    l_1 = self.project_atom_onto_plane(v[j], a, b, c, d)
                    # print("          The point of ligand atom {0} onto given plane: "
                    #       "({1:5.5f}, {2:5.5f}, {3:5.5f})".format(j, l_1[0], l_1[1], l_1[2]))
                    l_2 = self.project_atom_onto_plane(v[k], a, b, c, d)
                    # print("          The point of ligand atom {0} onto given plane: "
                    #       "({1:5.5f}, {2:5.5f}, {3:5.5f})".format(k, l_2[0], l_2[1], l_2[2]))

                    angle_theta_indi = self.angle_between(m, l_1, l_2)

                    if angle_theta_indi > angle_cutoff_for_theta_max \
                            or angle_theta_indi <= angle_cutoff_for_theta_min:

                        angle_theta_indi = 60.0
                        angle_theta_list.append(angle_theta_indi)

                        count += 1

                    else:
                        angle_theta_list.append(angle_theta_indi)

                    print("          Angle between atom {0} and {1}: {2:5.5f}".format(j, k, angle_theta_indi))

            print("")

        # Print summary
        print("         Total number of all angles      :", len(angle_theta_list))
        print("         Total number of deleted angles  :", count)
        print("         Total number of remaining angles:", len(angle_theta_list) - count)
        print("")

        # Sum up all individual theta angle
        for i in range(len(angle_theta_list)):
            computed_theta += abs(60.0 - angle_theta_list[i])

        return computed_theta

    def calc_all_param(self):
        """Calculate octahedral distortion parameters including
        Delta, Sigma, and Theta parameters
        """

        global run_check

        # check if input file exist
        if file_name == "":
            self.popup_nofile_error()
            return 1

        run_check = 1

        self.clear_results()

        self.calc_delta(coord_list)
        self.calc_sigma(coord_list)
        self.calc_theta(coord_list)

        formatted_computed_delta = "{0:10.8f}".format(computed_delta)
        formatted_computed_sigma = "{0:10.8f}".format(computed_sigma)
        formatted_computed_theta = "{0:10.8f}".format(computed_theta)

        print("Command: Calculate octahedral distortion parameters")
        print("         Delta  <Δ> =", formatted_computed_delta)
        print("         Sigma  <Σ> =", formatted_computed_sigma, "degree")
        print("         Theta  <Θ> =", formatted_computed_theta, "degree")
        print("")

        self.textBox_delta.delete(1.0, END)
        self.textBox_delta.insert(INSERT, formatted_computed_delta)

        self.textBox_sigma.delete(1.0, END)
        self.textBox_sigma.insert(INSERT, formatted_computed_sigma)

        self.textBox_theta.delete(1.0, END)
        self.textBox_theta.insert(INSERT, formatted_computed_theta)

    def draw_structure(self):
        """Display 3D structure of octahedral complex with label for each atoms
        """

        # check if input file exist
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

        # Draw line
        # x, y, z = [], [], []
        # for i in range(1, 7):
        #     x.append(cl[i][0])
        #     y.append(cl[i][1])
        #     z.append(cl[i][2])
        # ax.plot(x, y, z, 'k-')

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

        # check if input file exist
        if file_name == "":
            self.popup_nofile_error()
            return 1

        # check if the orthogonal projection is computed
        if run_check == 0:
            self.popup_nocalc_error()
            return 1

        print("Command: Display defined plane and orthogonal point")

        cl = coord_list
        vl = coord_vertex_list
        vertex_list = []
        color_list = ["red", "blue", "green", "yellow"]

        # This function is hard coding. Waiting for improvement

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
            ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=100, linewidths=1,
                       edgecolors='black')
            ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, atom_list[0], fontsize=9)

            for j in range(1, 7):
                ax.scatter(cl[j][0], cl[j][1], cl[j][2], color='red', marker='o', s=50, linewidths=1,
                           edgecolors='black')
                ax.text(cl[j][0] + 0.1, cl[j][1] + 0.1, cl[j][2] + 0.1, "{0},{1}".format(atom_list[j], j), fontsize=9)

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

        # check if input file exist
        if file_name == "":
            self.popup_nofile_error()
            return 1

        # check if the orthogonal projection is computed
        if run_check == 0:
            self.popup_nocalc_error()
            return 1

        print("Command: Display the orthogonal projection onto the given plane")

        cl = coord_list
        vl = coord_vertex_list
        color_list = ["red", "blue", "green", "yellow"]

        x_range, y_range = [], []
        pl_x, pl_y, pl_z = [], [], []
        l = []

        fig = plt.figure()

        for i in range(4):
            # Figure configuration
            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Orthogonal projection onto the plane {}".format(i + 1), fontsize='10')

            # Plot plane
            # Given three points, the plane is a*x + b*y + c*z + d = 0
            a, b, c, d = self.find_plane_eq(vl[i][0], vl[i][1], vl[i][2])
            print("         The equation of plane {0} is {1:5.5f}x + {2:5.5f}y + {3:5.5f}z + {4:5.5f} = 0" \
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

            z = (-normal[0] * xx - normal[1] * yy - d) / normal[2]

            ax.plot_surface(xx, yy, z, alpha='0.5', color=color_list[i])

            #################################
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

            #################################
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

    """
    Global variables are set here
    """

    global file_name, file_data, run_check
    global computed_delta, computed_sigma, computed_theta, angle_cutoff_for_theta_min, angle_cutoff_for_theta_max

    file_name = ""
    file_data = ""

    run_check = 0

    computed_delta = 0.0
    computed_sigma = 0.0
    computed_theta = 0.0

    angle_cutoff_for_theta_max = 60.0  # degree
    angle_cutoff_for_theta_min = 1.0  # degree

    # activate program windows
    masters.mainloop()


if __name__ == '__main__':
    main()
