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

OctaDist version 2.1

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

program_version = "2.1"

import numpy as np
import datetime
import popup
import coord
import calc
import tools
import draw
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled


def show_data_summary():
    if list_file == "":
        popup.nofile_error()
        return 1

    tools.show_data_summary(list_file, full_atom_coord_list)


def show_strct_param_octa():
    """Show structural parameters for octahedral structure (7 atoms):
    bond distance and bond angle between metal center and ligand atoms
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1

    tools.calc_strct_param_octa(atom_list, coord_list)


def show_strct_param_full():
    """Show structural parameters for full complex:
    bond distance and bond angle between metal center and ligand atoms
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1

    full_atom_list, full_coord_list = full_atom_coord_list[0]

    tools.calc_strct_param_full(full_atom_list, full_coord_list)


def show_surface_area():
    """Show surface area of selected 8 faces
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    tools.calc_surface_area(pal, pcl)


def show_plot_angle():
    """Plot Sigma versus Theta angles
    Relation plot between Sigma and Theta
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.show_plot_angles(sigma_list, theta_list)


def display_full_complex():
    """Display full structure
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    full_atom_list, full_coord_list = full_atom_coord_list[0]

    draw.draw_full_complex(full_atom_list, full_coord_list)


def display_full_complex_with_face():
    """Display full structure with the projection plane
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    full_atom_list, full_coord_list = full_atom_coord_list[0]

    draw.draw_full_complex_with_face(full_atom_list, full_coord_list, pcl)


def display_octahedron():
    """Display the octahedral structure
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_octahedron(atom_list, coord_list)


def display_octahedron_with_face():
    """Display the octahedral structure with 8 faces
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_octahedron_with_face(atom_list, coord_list, pcl)


def display_octahedron_with_optimal_face():
    """Display the octahedral structure with optimal 4 faces which give the lowest Theta value
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_octahedron_with_optimal_face(atom_list, coord_list, ref_pcl)


def display_projection_planes():
    """Display the projection planes
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_projection_planes(atom_list, coord_list, ref_pcl, oppo_pcl)


def display_twisting_faces():
    """Display the twisting triangular faces
    """

    if list_file == "":
        popup.nofile_error()
        return 1
    if len(list_file) > 1:
        popup.only_single_file()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_twisting_faces(atom_list, coord_list, ref_pcl, oppo_pcl)


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
            |- New 
            |- Open 
            |- Save as .. 
            |-------------
            |- Exit
            | 
            Tools
            |- Data summary
            |  |- Complex info
            |- Show structural parameters 
            |  |- Truncated octahedron 
            |  |- Full complex 
            |-------------
            |- Calculate surface area 
            |-------------
            |- Relationship plot between Σ and Θ
            |-------------
            |- Display full complex
            |- Display full complex with projection planes
            |
            Help
            |- Program help 
            |- About program 
            |- License info
        """

        # Main menu
        menubar = tk.Menu(masters)
        filemenu = tk.Menu(masters, tearoff=0)
        toolsmenu = tk.Menu(masters, tearoff=0)
        helpmenu = tk.Menu(masters, tearoff=0)

        # Sub-menu
        datamenu = tk.Menu(masters, tearoff=0)
        structuremenu = tk.Menu(masters, tearoff=0)

        # File
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.clear_cache)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save as ..", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=masters.quit)

        # Tools
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        toolsmenu.add_cascade(label="Data summary", menu=datamenu)
        datamenu.add_cascade(label="Complex info", command=show_data_summary)
        toolsmenu.add_cascade(label="Show structural parameter", menu=structuremenu)
        structuremenu.add_command(label="Octahedral structure", command=show_strct_param_octa)
        structuremenu.add_command(label="Full complex", command=show_strct_param_full)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Calculate surface area", command=show_surface_area)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Relationship plot between Σ and Θ", command=show_plot_angle)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Display full complex with faces",
                              command=display_full_complex_with_face)
        toolsmenu.add_command(label="Display only octahedron with faces",
                              command=display_octahedron_with_face)
        toolsmenu.add_command(label="Display Projection planes", command=display_projection_planes)
        toolsmenu.add_command(label="Display Twisting triangular faces", command=display_twisting_faces)

        # Help
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Program help", command=popup.show_help)
        helpmenu.add_command(label="About program", command=popup.show_about)
        helpmenu.add_command(label="License information", command=popup.show_license)
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
        self.btn_draw_structure = tk.Button(master, command=display_full_complex,
                                            text="Full complex", width="18")
        self.btn_draw_structure.grid(pady="5", row=7, column=0)

        # button to draw plane
        self.btn_draw_plane = tk.Button(master, command=display_octahedron,
                                        text="Only Octahedron", width="18")
        self.btn_draw_plane.grid(pady="5", row=8, column=0)

        # button to draw vector projection
        self.btn_draw_projection = tk.Button(master, command=display_octahedron_with_optimal_face,
                                             text="Octahedron with 4 faces", width="18")
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
        global list_file, atom_list, coord_list, computed_delta, computed_sigma, computed_theta
        global full_atom_coord_list, sel_atom_coord_list

        print("Command: Clear cache")

        list_file = ""
        atom_list = []
        coord_list = []
        full_atom_coord_list = []
        sel_atom_coord_list = []

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
        """Open input files
        """

        global list_file, atom_list, coord_list, full_atom_coord_list, sel_atom_coord_list

        print("Command: Browse input file(s)")

        if list_file != "":
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
            open(list_file[0], 'r')
            print("Command: The total number of file(s) selected: %s \n" % len(list_file))

            full_atom_coord_list, sel_atom_coord_list = [], []

            for i in range(len(list_file)):
                # Print coordinates
                print("Command: Open file no. {0:2d} : \"{1}\"".format(i + 1, list_file[i]))

                texts = "File {0}: {1}\n\n" \
                        "Atom                       Cartesian coordinate"\
                        .format(i + 1, list_file[i].split('/')[-1])
                self.textBox_coord.insert(tk.INSERT, texts)

                # Get atom and coordinate
                full_atom_list, full_coord_list = coord.get_coord(list_file[i])

                # Print atom and coordinate, and get only first 7 atoms
                atom_list, coord_list = coord.cut_coord(full_atom_list, full_coord_list)

                # Check if input file has coordinate inside
                if np.any(coord_list) == 0:
                    popup.nocoord_error()
                    return 1

                for j in range(len(atom_list)):
                    texts = " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}" \
                            .format(atom_list[j], coord_list[j][0], coord_list[j][1], coord_list[j][2])
                    self.textBox_coord.insert(tk.END, "\n" + texts)

                self.textBox_coord.insert(tk.END, "\n\n---------------------------------\n\n")

                # Store all data into following arrays
                full_atom_coord_list.append([full_atom_list, full_coord_list])
                sel_atom_coord_list.append([atom_list, coord_list])

        except:
            print("Error: No input file")
            list_file = ""

    def save_file(self):
        """Save computed data to file. The result will be saved into .txt or .out file.
        """

        print("Command: Save data to output file")

        if list_file == "":
            popup.nofile_error()
            return 1
        if len(list_file) > 1:
            popup.only_single_file()
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
        f.write("Input file: " + list_file.split('/')[-1] + "\n")
        f.write("Output file: " + f.name.split('/')[-1] + "\n\n")
        f.write("Cartesian coordinates:\n")
        for i in range(len(coord_list)):
            f.write("{0:2}  {1:10.6f}  {2:10.6f}  {3:10.6f}\n"
                    .format(atom_list[i], coord_list[i][0], coord_list[i][1], coord_list[i][2]))
        f.write("\n")
        f.write("Distance between metal center and 6 ligand atoms:\n")
        for i in range(len(unique_delta_list)):
            f.write("Distance {0} --> {1:10.6f} Angstrom\n".format(i + 1, unique_delta_list[i]))
        f.write("\n")
        f.write("12 cis angle (metal center is a vertex):\n")
        for i in range(len(unique_sigma_list)):
            f.write("Angle {0:2} --> {1:10.6f} degree\n".format(i + 1, unique_sigma_list[i]))
        f.write("\n")
        f.write("24 unique angle for all 70 sets of 4 faces:\n")
        for i in range(len(unique_theta_list)):
            f.write("Angle {0:2} --> {1:10.6f} degree\n".format(i + 1, unique_theta_list[i]))
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

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """

        global run_check, computed_delta, computed_sigma, computed_theta
        global sigma_list, theta_list, computed_results
        global unique_delta_list, unique_sigma_list, unique_theta_list
        global selected_plane_lists, pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl

        if list_file == "":
            popup.nofile_error()
            return 1

        run_check = 1
        self.clear_results()

        # Ready to compute all parameters
        delta_list, sigma_list, theta_list, computed_results = [], [], [], []

        for i in range(len(list_file)):
            print("         ====================== Complex %s ======================\n" % int(i + 1))
            print("Command: Show coordinate and compute Δ, Σ, and Θ parameters")

            atom_list, coord_list = sel_atom_coord_list[i]
            coord.show_7_atoms(atom_list, coord_list)

            computed_delta, unique_delta_list = calc.calc_delta(coord_list)
            computed_sigma, unique_sigma_list = calc.calc_sigma(coord_list)
            computed_theta, unique_theta_list, selected_plane_lists = calc.calc_theta(coord_list)

            print("Command: Show computed octahedral distortion parameters\n")
            print("         Δ = {0:10.6f}".format(computed_delta))
            print("         Σ = {0:10.6f} degree".format(computed_sigma))
            print("         Θ = {0:10.6f} degree\n".format(computed_theta))

            delta_list.append(computed_delta)
            sigma_list.append(computed_sigma)
            theta_list.append(computed_theta)

            computed_results.append([computed_delta, computed_sigma, computed_theta])

        print("         ==========================================================\n")
        print("Command: Show the names of all files")

        for i in range(len(computed_results)):
            print("         Complex {0:2d} : {1}".format(i + 1, list_file[i].split('/')[-1]))
        print("")

        print("Command: Show computed octahedral distortion parameters of all complexes\n")
        print("                            Δ            Σ             Θ")
        print("                        --------    ----------    ----------")
        for i in range(len(computed_results)):
            print("         Complex {0:2d} : {1:10.6f}    {2:10.6f}    {3:10.6f}"
                  .format(i + 1, computed_results[i][0], computed_results[i][1], computed_results[i][2]))
        print("")

        if len(list_file) == 1:
            self.textBox_delta.insert(tk.INSERT, '%3.6f' % computed_delta)
            self.textBox_sigma.insert(tk.INSERT, '%3.6f' % computed_sigma)
            self.textBox_theta.insert(tk.INSERT, '%3.6f' % computed_theta)

        else:
            tools.show_results_mult(computed_results)

        if len(list_file) == 1:
            pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl = selected_plane_lists


def main():
    masters = tk.Tk()
    MainProgram = OctaDist(masters)

    global list_file, run_check
    list_file = ""
    run_check = 0

    def on_closing():
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            masters.destroy()

    masters.protocol("WM_DELETE_WINDOW", on_closing)
    masters.mainloop()


if __name__ == '__main__':
    main()
