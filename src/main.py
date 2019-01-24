"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

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

OctaDist version 2.0

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

program_version = 2.0

import numpy as np
import datetime
import popup
import coord
import plane
import proj
import calc
import tools

import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class OctaDist:

    def __init__(self, masters):
        self.masters = masters
        masters.title("OctaDist")
        FONT = "Arial 10"
        self.masters.option_add("*Font", FONT)
        master = tk.Frame(masters, width="2", height="2")
        master.grid(padx=5, pady=5, row=0, column=0)

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
            |- Program help               << help
            |- About program              << about
            |- License info               << license
        """

        menubar = tk.Menu(masters)
        # add menu bar button
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)

        # sub-menu
        filemenu.add_command(label="New", command=self.clear_cache)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Open multiple files", command=self.open_multiple)
        filemenu.add_command(label="Save as ..", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.masters.quit)

        # add menu bar button
        toolsmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=toolsmenu)

        # add sub-menu
        toolsmenu.add_command(label="Show structural parameters", command=self.show_strct_param)

        # add menu bar button
        helpmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # add sub-menu
        helpmenu.add_command(label="Program help", command=popup.help)
        helpmenu.add_command(label="About program", command=popup.about)
        helpmenu.add_command(label="License information", command=popup.license)
        masters.config(menu=menubar)

        popup.welcome()

        # program details
        program_name = "Octahedral Distortion Analysis"
        self.msg_1 = tk.Label(master, foreground="blue", font=("Arial", 16, "bold"), text=program_name)
        self.msg_1.config()
        self.msg_1.grid(pady="5", row=0, columnspan=4)
        description = "Determine the structural distortion between two octahedral structures."
        self.msg_2 = tk.Label(master, text=description)
        self.msg_2.grid(pady="5", row=1, columnspan=4)

        # button to browse input file
        self.btn_open_file = tk.Button(master, command=self.open_file, text="Browse file", relief=tk.RAISED)
        self.btn_open_file.grid(pady="5", row=2, column=0)

        # button to run
        self.btn_run = tk.Button(master, command=self.calc_all_param, text="Compute parameters")
        # btn_run.config(font="Segoe 10")
        self.btn_run.grid(sticky=tk.W, pady="5", row=2, column=1, columnspan=2)

        # button to clear cache
        self.btn_open_file = tk.Button(master, command=self.clear_cache, text="Clear cache", )
        self.btn_open_file.grid(sticky=tk.W, pady="5", row=2, column=3)

        # coordinate label
        self.lbl_1 = tk.Label(master, text="Molecule Specifications")
        self.lbl_1.grid(sticky=tk.W, pady="5", row=3, columnspan=4)

        # text box for showing cartesian coordinates
        self.textBox_coord = tkscrolled.ScrolledText(master, height="14", width="70", wrap="word", undo="True")
        self.textBox_coord.grid(pady="5", row=4, columnspan=4)

        # Octahedral distortion parameters
        self.lbl_2 = tk.Label(master, text="Octahedral distortion parameters")

        # lbl_2.config(font="Segoe 10 bold")
        self.lbl_2.grid(row=6, column=1, columnspan=2)

        # Display coordinate and vector projection
        self.lbl_display = tk.Label(master, text="Graphical Displays")
        # self.lbl_display.config(font="Segoe 10 bold")
        self.lbl_display.grid(row=6, column=0, padx="30")

        # button to draw structure
        self.btn_draw_structure = tk.Button(master, command=self.display_structure, text="Octahedral structure",
                                            width="18")
        self.btn_draw_structure.grid(pady="5", row=7, column=0)

        # button to draw plane
        self.btn_draw_plane = tk.Button(master, command=self.display_3D_plane, text="Pair of opposite faces",
                                        width="18")
        self.btn_draw_plane.grid(pady="5", row=8, column=0)

        # button to draw vector projection
        self.btn_draw_projection = tk.Button(master, command=self.display_projection, text="Projection planes",
                                             width="18")
        self.btn_draw_projection.grid(pady="5", row=9, column=0)

        # Delta
        self.lbl_dist = tk.Label(master, text="Δ  = ")
        self.lbl_dist.grid(sticky=tk.E, pady="5", row=7, column=1)
        self.textBox_delta = tk.Text(master, height="1", width="15", wrap="word")
        self.textBox_delta.grid(row=7, column=2, sticky=tk.W)

        # Sigma
        self.lbl_sigma = tk.Label(master, text="Σ  = ")
        self.lbl_sigma.grid(sticky=tk.E, pady="5", row=8, column=1)
        self.textBox_sigma = tk.Text(master, height="1", width="15", wrap="word")
        self.textBox_sigma.grid(sticky=tk.W, row=8, column=2)
        self.lbl_sigma_unit = tk.Label(master, text="degree")
        self.lbl_sigma_unit.grid(sticky=tk.W, pady="5", row=8, column=3)

        # Theta
        self.lbl_theta = tk.Label(master, text="Θ  = ")
        self.lbl_theta.grid(sticky=tk.E, pady="5", row=9, column=1)
        self.textBox_theta = tk.Text(master, height="1", width="15", wrap="word")
        self.textBox_theta.grid(sticky=tk.W, row=9, column=2)
        self.lbl_theta_unit = tk.Label(master, text="degree")
        self.lbl_theta_unit.grid(sticky=tk.W, pady="5", row=9, column=3)

        # Link
        link = "https://github.com/rangsimanketkaew/OctaDist"
        self.lbl_link = tk.Label(master, foreground="blue", text=link, cursor="hand2")
        self.lbl_link.grid(pady="5", row=10, columnspan=4)
        self.lbl_link.bind("<Button-1>", popup.callback)

    def clear_cache(self):
        """Clear all variables
        """
        global file_name, file_data, atom_list, coord_list, mult, strct
        global computed_delta, computed_sigma, computed_theta

        print("Command: Clear cache")

        file_name = ""
        file_data = ""
        atom_list = []
        coord_list = []
        mult = 0
        strct = 0

        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        self.textBox_coord.delete(1.0, tk.END)

        computed_delta = 0.0
        computed_sigma = 0.0
        computed_theta = 0.0

        self.clear_results()

    def clear_results(self):
        """Clear the computed parameters
        """
        self.textBox_delta.delete(1.0, tk.END)
        self.textBox_sigma.delete(1.0, tk.END)
        self.textBox_theta.delete(1.0, tk.END)

    def open_file(self):
        """Open file using Open Dialog
        Atom and coordinates must be in Cartesian (XYZ) coordinate.
        Supported file extensions: .txt, .xyz, and Gaussian output file
        """
        global file_name, file_data, atom_list, coord_list, full_atom_list, full_coord_list

        print("Command: Open input file")

        if file_name != "" or mult == 1:
            self.clear_cache()

        file_name = filedialog.askopenfilename(title="Choose input file",
                                               filetypes=(("XYZ File", "*.xyz"),
                                                          ("Text File", "*.txt"),
                                                          ("Gaussian Output File", "*.out"),
                                                          ("Gaussian Output File", "*.log"),
                                                          ("NWChem Output File", "*.out"),
                                                          ("NWChem Output File", "*.log"),
                                                          ("ORCA Output File", "*.out"),
                                                          ("ORCA Output File", "*.log"),
                                                          ("All Files", "*.*")))

        # Using try/except in case user types in unknown file or closes without choosing a file.
        try:
            with open(file_name, 'r') as f:
                print("         File full path: " + file_name)
                print("         File name: " + file_name.split('/')[-1])

                # Check file type and get coordinate
                print("")
                print("Command: Determine file type")
                full_atom_list, full_coord_list = coord.get_coord(file_name)

                if len(full_coord_list) != 0:
                    atom_list, coord_list = coord.cut_coord(full_atom_list, full_coord_list)
                else:
                    return 1

                texts = "File: {0}\n\n" \
                        "Atom                       Cartesian coordinate".format(file_name.split('/')[-1])
                self.textBox_coord.insert(tk.INSERT, texts)

                for i in range(len(atom_list)):
                    texts = " {A:>2}      {Lx:14.9f}  {Ly:14.9f}  {Lz:14.9f}" \
                        .format(A=atom_list[i], Lx=coord_list[i][0], Ly=coord_list[i][1], Lz=coord_list[i][2])
                    self.textBox_coord.insert(tk.END, "\n" + texts)

                return atom_list, coord_list

        except:
            print("Error: No input file")
            atom_list, coord_list = 0, 0

            return atom_list, coord_list

    def open_multiple(self):
        """Open multiple input files
        """
        global file_name, list_file, mult, atom_coord_mult

        print("Command: Open multiple files")

        if file_name != "" or list_file != "":
            self.clear_cache()

        file_name = filedialog.askopenfilenames(title="Choose input file",
                                                filetypes=(("XYZ File", "*.xyz"),
                                                           ("Text File", "*.txt"),
                                                           ("Gaussian Output File", "*.out"),
                                                           ("Gaussian Output File", "*.log"),
                                                           ("NWChem Output File", "*.out"),
                                                           ("NWChem Output File", "*.log"),
                                                           ("ORCA Output File", "*.out"),
                                                           ("ORCA Output File", "*.log"),
                                                           ("All Files", "*.*")))

        list_file = list(file_name)

        try:
            open(file_name[0], 'r')
            print("Command: %s input files selected" % len(list_file))
            mult = 1
            atom_coord_mult = []

            for i in range(len(list_file)):
                print("         File {0:2d} : \"{1}\"".format(i + 1, list_file[i]))

                texts = "File {0}: {1}\n\n" \
                        "Atom                       Cartesian coordinate".format(i + 1, list_file[i].split('/')[-1])
                self.textBox_coord.insert(tk.INSERT, texts)

                # Get and show coordinate
                full_atom_list, full_coord_list = coord.get_coord(list_file[i])

                if len(full_coord_list) != 0:
                    atom_list, coord_list = coord.cut_coord(full_atom_list, full_coord_list)

                for j in range(len(atom_list)):
                    texts = " {A:>2}      {Lx:14.9f}  {Ly:14.9f}  {Lz:14.9f}" \
                        .format(A=atom_list[j], Lx=coord_list[j][0], Ly=coord_list[j][1], Lz=coord_list[j][2])
                    self.textBox_coord.insert(tk.END, "\n" + texts)
                self.textBox_coord.insert(tk.END, "\n\n---------------------------------\n\n")

                atom_coord_mult.append([full_atom_list, full_coord_list])
            print("")

            return atom_coord_mult

        except:
            print("Error: No input file")

    def save_file(self):
        """Save file using Save Dialog. The result will be saved into .txt or .out file.
        """
        print("Command: Save data to output file")

        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.cannot_show_param()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        f = filedialog.asksaveasfile(mode='w',
                                     defaultextension=".out",
                                     title="Save as",
                                     filetypes=(("Output File", "*.out"),
                                                ("Text File", "*.txt"),
                                                ("All Files", "*.*")))

        if f is None:
            print("Warning: Save file cancelled")
            return 0

        f.write("OctaDist {}: Octahedral Distortion Analysis\n".format(program_version))
        f.write("https://github.com/rangsimanketkaew/OctaDist\n\n")
        f.write("By Rangsiman Ketkaew\n")
        f.write("Computational Chemistry Research Unit\n")
        f.write("Department of Chemistry\n")
        f.write("Faculty of Science and Technology\n")
        f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
        f.write("E-mail: rangsiman1993@gmail.com\n\n")
        f.write("Date: {}\n\n".format(datetime.datetime.now()))
        f.write("Input file: " + file_name.split('/')[-1] + "\n")
        f.write("Output file: " + f.name.split('/')[-1] + "\n\n")
        f.write("Cartesian coordinates:\n")
        for i in range(len(coord_list)):
            f.write("{0:2}  {1:10.6f}  {2:10.6f}  {3:10.6f}\n"
                    .format(atom_list[i], coord_list[i][0], coord_list[i][1], coord_list[i][2]))
        f.write("\n")
        f.write("Distance between metal center and 6 ligand atoms:\n")
        for i in range(len(unique_delta_list)):
            f.write("Distance {0} --> {1:10.6f} Angstrom\n".format(i+1, unique_delta_list[i]))
        f.write("\n")
        f.write("12 cis angle (metal center is a vertex):\n")
        for i in range(len(unique_sigma_list)):
            f.write("Angle {0:2} --> {1:10.6f} degree\n".format(i+1, unique_sigma_list[i]))
        f.write("\n")
        f.write("24 unique angle for all 70 sets of 4 faces:\n")
        for i in range(len(unique_theta_list)):
            f.write("Angle {0:2} --> {1:10.6f} degree\n".format(i+1, unique_theta_list[i]))
        f.write("\n")
        f.write("Selected 4 optimal faces for orthogonal projection:\n")
        for i in range(len(ref_pal)):
            f.write("Face {0} --> {1}\n".format(i + 1, ref_pal[i]))
            for j in range(3):
                f.write("  [{0:10.6f}, {1:10.6f}, {2:10.6f}]\n"
                        .format(ref_pcl[i][j][0], ref_pcl[i][j][1], ref_pcl[i][j][2]))
        f.write("\n")
        f.write("Octahedral distortion parameters:\n")
        f.write(" - Delta = %10.6f\n" % computed_delta)
        f.write(" - Sigma = %10.6f degree\n" % computed_sigma)
        f.write(" - Theta = %10.6f degree\n" % computed_theta)
        f.write("\n")
        f.close()

        print("Command: Data has been saved to \"%s\"" % f.name)

    def show_strct_param(self):
        """Show structural parameters: bond distance and bond angle
        """
        global strct

        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.cannot_show_param()
            return 1
        if strct == 1:
            popup.redundant_strct()
            return 1

        strct = 1
        tools.show_strct_param(full_atom_list, full_coord_list)

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        global run_check, computed_delta, computed_sigma, computed_theta
        global unique_delta_list, unique_sigma_list, unique_theta_list
        global pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl

        if mult == 1:
            self.clear_results()
            calc.calc_mult(list_file, atom_coord_mult)
            return 0

        if file_name == "":
            popup.nofile_error()
            return 1

        run_check = 1
        self.clear_results()

        if np.any(coord_list) != 0:
            print("Command: Calculate octahedral distortion parameters")
            computed_delta, unique_delta_list = calc.calc_delta(coord_list)
            computed_sigma, unique_sigma_list = calc.calc_sigma(coord_list)
            computed_theta, unique_theta_list, selected_plane_lists = calc.calc_theta(coord_list)

            pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl = selected_plane_lists

            print("Command: Show computed octahedral distortion parameters")
            print("")
            print("         Δ = %11.6f" % computed_delta)
            print("         Σ = %11.6f degree" % computed_sigma)
            print("         Θ = %11.6f degree" % computed_theta)
            print("")

            self.textBox_delta.insert(tk.INSERT, '%3.6f' % computed_delta)
            self.textBox_sigma.insert(tk.INSERT, '%3.6f' % computed_sigma)
            self.textBox_theta.insert(tk.INSERT, '%3.6f' % computed_theta)

        else:
            popup.nocoord_error()

        return ref_pal, ref_pcl, oppo_pal, oppo_pcl

    def display_structure(self):
        """Display 3D structure of octahedral complex with label for each atoms
        """
        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.cannot_display()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        print("Command: Display octahedral structure")
        print("         Scattering plot of all atoms")
        print("         Draw surface for all 8 faces")

        # Plot and configuration
        fig = plt.figure()
        ax = Axes3D(fig)
        al, cl = atom_list, coord_list
        vertices_list = []

        # Create array of vertices for 8 faces
        for i in range(8):
            get_vertices = pcl[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]
            vertices_list.append(vertices)

        # The following is for showing only 4 faces whose the minimum Theta value
        # for i in range(4):
        #     get_vertices = ref_pcl[i].tolist()
        #     x, y, z = zip(*get_vertices)
        #     vertices = [list(zip(x, y, z))]
        #     vertices_list.append(vertices)

        # Plot metal center
        ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=300, linewidths=2, edgecolors='black')
        ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, al[0], fontsize=12)

        # Plot ligand atoms
        for i in range(1, 7):
            ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=200, linewidths=2, edgecolors='black')
            ax.text(cl[i][0] + 0.1, cl[i][1] + 0.1, cl[i][2] + 0.1, "{0},{1}".format(al[i], i), fontsize=10)

        # Draw plane
        color_list = ["red", "blue", "green", "yellow", "violet", "cyan", "brown", "grey"]

        for i in range(len(vertices_list)):
            ax.add_collection3d(Poly3DCollection(vertices_list[i], alpha=0.5, color=color_list[i]))

        # Set axis
        ax.set_xlabel(r'X', fontsize=15)
        ax.set_ylabel(r'Y', fontsize=15)
        ax.set_zlabel(r'Z', fontsize=15)
        ax.set_title('Octahedral structure', fontsize="12")
        ax.grid(True)

        # plt.axis('equal')
        # plt.axis('off')
        plt.show()

    def display_3D_plane(self):
        """Display the selected 4 faces of octahedral complex
        """
        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.cannot_display()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        print("Command: Display the selected 4 pairs of opposite faces")
        print("         Scattering plot of all atoms")
        print("         Draw surface for 4 pairs of reference and opposite faces")

        al, cl, vl, ovl = atom_list, coord_list, ref_pcl, oppo_pcl

        # reference face
        ref_vertices_list = []

        for i in range(4):
            get_vertices = vl[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]
            ref_vertices_list.append(vertices)

        # opposite face
        oppo_vertices_list = []

        for i in range(4):
            x, y, z = zip(*ovl[i])
            vertices = [list(zip(x, y, z))]
            oppo_vertices_list.append(vertices)

        fig = plt.figure()
        st = fig.suptitle("4 pairs of opposite faces", fontsize="x-large")

        # Display four planes
        color_list_1 = ["red", "blue", "orange", "magenta"]
        color_list_2 = ["green", "yellow", "cyan", "brown"]

        for i in range(4):
            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Plane {}".format(i + 1))
            ax.scatter(cl[0][0], cl[0][1], cl[0][2],
                       color='yellow', marker='o', s=100, linewidths=1, edgecolors='black', label="Metal center")
            ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1, al[0], fontsize=9)

            for j in range(1, 7):
                ax.scatter(cl[j][0], cl[j][1], cl[j][2],
                           color='red', marker='o', s=50, linewidths=1, edgecolors='black', label="Ligand atoms")
                ax.text(cl[j][0] + 0.1, cl[j][1] + 0.1, cl[j][2] + 0.1, "{0},{1}".format(al[j], j), fontsize=9)

            # Draw plane
            ax.add_collection3d(Poly3DCollection(ref_vertices_list[i], alpha=0.5, color=color_list_1[i]))
            ax.add_collection3d(Poly3DCollection(oppo_vertices_list[i], alpha=0.5, color=color_list_2[i]))

            # Set axis
            ax.set_xlabel(r'X', fontsize=10)
            ax.set_ylabel(r'Y', fontsize=10)
            ax.set_zlabel(r'Z', fontsize=10)
            ax.grid(True)

        # Shift subplots down
        st.set_y(1.0)
        fig.subplots_adjust(top=0.25)

        # plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def display_projection(self):
        """Display twisting triangular faces vector projection of all atoms onto the given plane
        """
        if file_name == "":
            popup.nofile_error()
            return 1
        if mult == 1:
            popup.cannot_display()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        print("Command: Display the reference and projected atoms")
        print("         Scattering plot of reference atom and projected atoms on the reference plane")
        print("         Draw surface for 4 pairs of two twisting triangular faces")

        al, cl, vl, ovl = atom_list, coord_list, ref_pcl, oppo_pcl

        ref_vertices_list = []

        for i in range(4):
            get_vertices = vl[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]
            ref_vertices_list.append(vertices)

        fig = plt.figure()
        st = fig.suptitle("Projected twisting triangular faces", fontsize="x-large")

        for i in range(4):
            a, b, c, d = plane.eq_of_plane(vl[i][0], vl[i][1], vl[i][2])
            m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

            ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
            ax.set_title("Projection plane {0}".format(i + 1), fontsize='10')

            # Projected metal center atom
            ax.scatter(m[0], m[1], m[2], color='orange', s=100, marker='o', linewidths=1, edgecolors='black',
                       label="Metal center")
            ax.text(m[0] + 0.1, m[1] + 0.1, m[2] + 0.1, "{0}'".format(al[0]), fontsize=9)

            # Reference atoms
            pl = []

            for j in range(3):
                ax.scatter(vl[i][j][0], vl[i][j][1], vl[i][j][2], color='red', s=50, marker='o', linewidths=1,
                           edgecolors='black', label="Reference atom")
                ax.text(vl[i][j][0] + 0.1, vl[i][j][1] + 0.1, vl[i][j][2] + 0.1, "{0}".format(j+1), fontsize=9)
                # Project ligand atom onto the reference face
                pl.append(proj.project_atom_onto_plane(ovl[i][j], a, b, c, d))

            # Projected opposite atoms
            for j in range(3):
                ax.scatter(pl[j][0], pl[j][1], pl[j][2], color='blue', s=50, marker='o', linewidths=1,
                           edgecolors='black', label="Projected ligand atom")
                ax.text(pl[j][0] + 0.1, pl[j][1] + 0.1, pl[j][2] + 0.1, "{0}'".format(j + 1), fontsize=9)

            # Draw plane
            x, y, z = zip(*pl)
            projected_oppo_vertices_list = [list(zip(x, y, z))]

            ax.add_collection3d(Poly3DCollection(ref_vertices_list[i], alpha=0.5, color="yellow"))
            ax.add_collection3d(Poly3DCollection(projected_oppo_vertices_list, alpha=0.5, color="blue"))

            # Draw line
            for j in range(3):
                merge = list(zip(m.tolist(), vl[i][j].tolist()))
                x, y, z = merge
                ax.plot(x, y, z, 'k-', color="black")

            for j in range(3):
                merge = list(zip(m.tolist(), pl[j].tolist()))
                x, y, z = merge
                ax.plot(x, y, z, 'k->', color="black")

            # Set axis
            ax.set_xlabel(r'X', fontsize=10)
            ax.set_ylabel(r'Y', fontsize=10)
            ax.set_zlabel(r'Z', fontsize=10)
            ax.grid(True)

        # Shift subplots down
        st.set_y(1.0)
        fig.subplots_adjust(top=0.25)

        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
        # plt.axis('equal')
        plt.tight_layout()
        plt.show()


def main():
    masters = tk.Tk()
    MainProgram = OctaDist(masters)

    global file_name, file_data, list_file, run_check, mult, strct
    file_name = ""
    file_data = ""
    list_file = ""
    run_check = 0
    mult = 0
    strct = 0

    masters.mainloop()


if __name__ == '__main__':
    main()
