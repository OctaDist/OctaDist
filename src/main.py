"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.

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

OctaDist version 2.3

Octahedral Distortion Analysis
Software website: https://octadist.github.io
Last modified: February 2019

This program was written in Python 3 binding to TkInter GUI platform,
tested on PyCharm (Community Edition) program, and compiled by PyInstaller.

Authors:
Rangsiman Ketkaew            Thammasat University, Thailand    rangsiman1993@gmail.com
Yuthana Tantirungrotechai    Thammasat University, Thailand    yt203y@gmail.com
David J. Harding             Walailak University, Thailand     hdavid@mail.wu.ac.th
Phimphaka Harding            Walailak University, Thailand     kphimpha@mail.wu.ac.th
Mathieu Marchivie            Université de Bordeaux, France    mathieu.marchivie@icmcb.cnrs.fr
"""

import numpy as np
import popup
import coord
import calc
import tools
import draw
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled

program_version = "2.3"


def print_stdout(self, text):
    """Insert stdout & stderr to Log text box
    """
    self.box_stdout.insert(tk.INSERT, text + "\n")


class OctaDist:
    def show_all_atom(self):
        """Display all atom
        """
        try:
            if len(atom_coord_full) == 1:
                draw.draw_all_atom(self, atom_coord_full[0])
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_plot_angle(self):
        """Show relationship plot between Sigma and Theta parameters
        """
        try:
            if len(atom_coord_full) > 0:
                try:
                    draw.show_plot_angles(self, all_sigma, all_theta)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_all_atom_and_face(self):
        """Display all atom and 8 faces of octahedron
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    draw.draw_all_atom_and_face(self, atom_coord_full[0], pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_octa(self):
        """Display the octahedral structure
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    draw.draw_octahedron(self, atom_octa, coord_octa)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_octa_and_face(self):
        """Display the octahedral structure and its 8 faces
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    draw.draw_octahedron_and_face(self, atom_octa, coord_octa, pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_octa_and_opt_face(self):
        """Display the octahedral structure and selected optimal 4 faces
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    draw.draw_octahedron_and_opt_face(self, atom_octa, coord_octa, ref_pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_projection_plane(self):
        """Display the projection planes
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    draw.draw_projection_planes(self, atom_octa, coord_octa, ref_pcl, oppo_pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_twisting_face(self):
        """Display the twisting triangular faces
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    draw.draw_twisting_faces(self, atom_octa, coord_octa, ref_pcl, oppo_pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_help(self):
        """Open program help page
        """
        self.newWindow = tk.Toplevel(self.master)
        self.app = popup.ShowHelp(self.newWindow)

    def show_about(self):
        """Open about page
        """
        popup.show_about(self)

    def show_license(self):
        """Open about page
        """
        popup.show_license(self)

    def show_results_mult(self):
        """Show results
        """
        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowResults(self.newWindow, comp_result)

    def show_data_summary(self):
        """Show information of complex/structure
        """
        try:
            if len(atom_coord_full) >= 1:
                self.newWindow = tk.Toplevel(self.master)
                self.app = tools.ShowData(self.newWindow, file_list, atom_coord_full)
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_face_summary(self):
        """Show information of selected 4 faces
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    self.newWindow = tk.Toplevel(self.master)
                    self.app = tools.ShowFaceSet(self.newWindow, ref_pal, ref_pcl, oppo_pal, oppo_pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_param_octa(self):
        """Show selected structural parameters of octahedral structure:
        bond distance and bond angle between metal center and ligand atoms
        """
        try:
            if len(atom_coord_full) == 1:
                self.newWindow = tk.Toplevel(self.master)
                self.app = tools.ShowParamOcta(self.newWindow, atom_octa, coord_octa)
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_param_full(self):
        """Show structural parameters of full complex:
        bond distance and bond angle between metal center and ligand atoms
        """
        try:
            if len(atom_coord_full) == 1:
                self.newWindow = tk.Toplevel(self.master)
                self.app = tools.ShowParamFull(self.newWindow, atom_coord_full[0])
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def show_surface_area(self):
        """Show surface area of 8 faces of octahedron
        """
        try:
            if len(atom_coord_full) == 1:
                try:
                    self.newWindow = tk.Toplevel(self.master)
                    self.app = tools.ShowSurfaceArea(self.newWindow, pal, pcl)
                except NameError:
                    popup.no_calc_error(self)
                    return 1
            elif len(atom_coord_full) > 1:
                popup.only_one_file_error(self)
                return 1
            elif len(atom_coord_full) == 0:
                popup.no_file_error(self)
                return 1
        except NameError:
            popup.no_file_error(self)
            return 1

    def clear_cache(self):
        """Clear all variables
        """
        global file_list, atom_octa, coord_octa, atom_coord_full, atom_coord_octa, \
            all_sigma, all_theta, comp_result, comp_delta, comp_sigma, \
            comp_theta_min, comp_theta_max, comp_theta_mean

        file_list = ""
        atom_octa = []
        coord_octa = []
        atom_coord_full = []
        atom_coord_octa = []
        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        all_sigma = 0
        all_theta = []
        comp_result = []
        comp_delta = 0
        comp_sigma = 0
        comp_theta_min = 0
        comp_theta_max = 0
        comp_theta_mean = 0

        self.box_coord.delete(1.0, tk.END)
        self.box_stdout.delete(1.0, tk.END)
        print_stdout(self, "Clear cache")
        self.clear_results()

    def clear_results(self):
        """Clear box of computed octahedral distortion parameters
        """
        self.box_delta.delete(1.0, tk.END)
        self.box_sigma.delete(1.0, tk.END)
        self.box_theta_min.delete(1.0, tk.END)
        self.box_theta_max.delete(1.0, tk.END)
        self.box_theta_mean.delete(1.0, tk.END)

    def open_file(self):
        """Open input files
        """
        global file_list, atom_octa, coord_octa, atom_coord_full, atom_coord_octa

        self.box_coord.delete(1.0, tk.END)
        self.box_stdout.insert(tk.INSERT, "Info: Browse input file\n")

        try:
            file_name = filedialog.askopenfilenames(
                title="Choose input file",
                filetypes=(("XYZ File", "*.xyz"),
                           ("Gaussian Output File", "*.out"),
                           ("Gaussian Output File", "*.log"),
                           ("NWChem Output File", "*.out"),
                           ("NWChem Output File", "*.log"),
                           ("ORCA Output File", "*.out"),
                           ("ORCA Output File", "*.log"),
                           ("Q-Chem Output File", "*.out"),
                           ("Q-Chem Output File", "*.log"),
                           ("All Files", "*.*")))

            file_list = list(file_name)
            try:
                open(file_list[0], 'r')
                self.box_stdout.insert(tk.INSERT, "Info: Total number of file: {0}\n\n".format(len(file_list)))

                atom_coord_full = []
                atom_coord_octa = []
                for i in range(len(file_list)):
                    get_name = file_list[i].split('/')[-1]
                    self.box_stdout.insert(tk.INSERT, "Info: Open file no. {0}: {1}\n".format(i + 1, get_name))

                    # Extract the atoms and the coordinates from input file
                    atom_full, coord_full = coord.get_coord(self, file_list[i])

                    print_stdout(self, "Info: Show Cartesian coordinates of all {0} atoms".format(len(atom_full)))
                    print_stdout(self, "")
                    print_stdout(self, "      Atom        X             Y             Z")
                    print_stdout(self, "      ----    ----------    ----------    ----------")
                    for j in range(len(atom_full)):
                        print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                     .format(atom_full[j], coord_full[j][0], coord_full[j][1], coord_full[j][2]))
                    print_stdout(self, "")

                    # Check if the total number of atom is more than 7.
                    # If so, turn-on auto-search octahedron function
                    if len(atom_full) > 7:
                        atom_octa, coord_octa = coord.auto_search_octa(self, atom_full, coord_full)
                    elif len(atom_full) == 7:
                        atom_octa, coord_octa = atom_full, coord_full

                    # Check if input file has coordinate inside
                    if np.any(coord_octa) == 0:
                        popup.no_coord_error(self)
                        return 1

                    # Show extracted octahedral structure
                    print_stdout(self, "Info: Show Cartesian coordinates of extracted octahedral structure")
                    print_stdout(self, "")
                    print_stdout(self, "      Atom        X             Y             Z")
                    print_stdout(self, "      ----    ----------    ----------    ----------")

                    num_atom = len(atom_octa)
                    for j in range(num_atom):
                        print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                     .format(atom_octa[j], coord_octa[j][0], coord_octa[j][1], coord_octa[j][2]))
                    print_stdout(self, "")
                    self.box_stdout.see(tk.END)

                    num_atom = len(atom_full)
                    self.box_coord.insert(tk.END, "File {0}: {1}\n".format(i + 1, get_name))
                    self.box_coord.insert(tk.END, "No. of atom: {0}\n".format(num_atom))
                    self.box_coord.insert(tk.END, "Atom                       Cartesian coordinate")

                    for j in range(num_atom):
                        self.box_coord.insert(tk.END, "\n" + " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                              .format(atom_full[j], coord_full[j][0], coord_full[j][1],
                                                      coord_full[j][2]))
                    self.box_coord.insert(tk.END, "\n\n\n")

                    atom_coord_full.append([atom_full, coord_full])
                    atom_coord_octa.append([atom_octa, coord_octa])

            except UnboundLocalError:
                print_stdout(self, "Error: No input file")
                self.clear_cache()
                self.box_coord.insert(tk.END, "Error: Could not open file \"{0}\"".format(get_name))
                self.box_coord.insert(tk.END, "\n\n")
                self.box_coord.insert(tk.END, "Please check the complex and the coordinates carefully!")

        except IndexError:
            print_stdout(self, "Error: No input file")
            return 1

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        global comp_delta, comp_sigma, comp_theta_min, comp_theta_max, comp_theta_mean, all_sigma, all_theta, \
            comp_result, all_comp, pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl

        if file_list == "":
            popup.no_file_error(self)
            return 1
        self.clear_results()

        print_stdout(self, "Info: Calculate the Δ, Σ, and Θ parameters")
        print_stdout(self, "")

        all_sigma = []
        all_theta = []
        comp_result = []
        for i in range(len(file_list)):
            print_stdout(self, "      *********************** Complex {0} ***********************".format(i + 1))
            print_stdout(self, "")

            # Calculate distortion parameters
            atom_octa, coord_octa = atom_coord_octa[i]
            comp_delta = calc.calc_delta(self, atom_octa, coord_octa)
            comp_sigma = calc.calc_sigma(self, atom_octa, coord_octa)
            comp_theta_min, comp_theta_max, comp_theta_mean, all_comp = calc.calc_theta(self, coord_octa)
            all_sigma.append(comp_sigma)
            all_theta.append(comp_theta_min)
            comp_result.append([comp_delta, comp_sigma, comp_theta_min])

        print_stdout(self, "Info: Show computed octahedral distortion parameters of all files")
        print_stdout(self, "")
        print_stdout(self, "      ==================== Overall Summary ====================")
        print_stdout(self, "")
        for i in range(len(comp_result)):
            print_stdout(self, "      Complex {0:2d} : {1}".format(i + 1, file_list[i].split('/')[-1]))
        print_stdout(self, "")
        print_stdout(self, "      Complex          Δ           Σ (°)         Θ (°)")
        print_stdout(self, "      -------      --------    ----------    ----------")
        for i in range(len(comp_result)):
            print_stdout(self, "      {0:2d}      {1:10.6f}    {2:10.6f}    {3:10.6f}"
                         .format(i + 1, comp_result[i][0], comp_result[i][1], comp_result[i][2]))
        print_stdout(self, "")
        print_stdout(self, "      =========================================================")
        print_stdout(self, "")

        if len(file_list) == 1:
            pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl = all_comp
            self.box_delta.insert(tk.INSERT, "{0:3.6f}".format(comp_delta))
            self.box_sigma.insert(tk.INSERT, "{0:3.6f}".format(comp_sigma))
            self.box_theta_min.insert(tk.INSERT, "{0:3.6f}".format(comp_theta_min))
            self.box_theta_max.insert(tk.INSERT, "{0:3.6f}".format(comp_theta_max))
            self.box_theta_mean.insert(tk.INSERT, "{0:3.6f}".format(comp_theta_mean))
        else:
            self.show_results_mult()

        self.box_stdout.see(tk.END)

    def save_file(self):
        """Save computed data to file. The result will be saved as .txt or .out file.
        """
        print_stdout(self, "Info: Save data as an output file")

        try:
            if len(atom_coord_full) > 0:

                try:
                    if comp_result:
                        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt", title="Save as",
                                                     filetypes=(("Text File", "*.txt"),
                                                                ("Output File", "*.out"),
                                                                ("All Files", "*.*")))

                        if f is None:
                            print_stdout(self, "Warning: Cancelled save file")
                            return 0

                        f.write("OctaDist {0}: Octahedral Distortion Analysis\n".format(program_version))
                        f.write("https://octadist.github.io\n")
                        f.write("\n")
                        for i in range(len(file_list)):
                            f.write("File no.   : {0}\n".format(i + 1))
                            f.write("Input file : " + file_list[i].split('/')[-1] + "\n")
                            f.write("Output file: " + f.name.split('/')[-1] + "\n")
                            f.write("\n")
                            f.write("Cartesian coordinates:\n")
                            for j in range(len(coord_octa)):
                                f.write("{0:2}  {1:10.6f}  {2:10.6f}  {3:10.6f}\n"
                                        .format(atom_octa[j], coord_octa[j][0], coord_octa[j][1], coord_octa[j][2]))
                            f.write("\n")
                            f.write("Octahedral distortion parameters:\n")
                            f.write(" - Delta = {0:10.6f}\n".format(comp_result[i][0]))
                            f.write(" - Sigma = {0:10.6f} degree\n".format(comp_result[i][1]))
                            f.write(" - Theta = {0:10.6f} degree\n".format(comp_result[i][2]))
                            f.write("\n")
                            f.write("--------------------------------------\n")
                            f.write("\n")
                        f.close()

                        print_stdout(self, "Info: Data has been saved to \"{0}\"".format(f.name))

                except NameError:
                    popup.no_calc_error(self)
                    return 1

        except NameError:
            popup.no_file_error(self)
            return 1

    def __init__(self, master):
        self.master = master
        self.master.title("OctaDist {0}".format(program_version))
        FONT = "Arial 10"
        self.master.option_add("*Font", FONT)
        self.master.geometry("520x535")

        # Main menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(self.master, tearoff=0)
        display_menu = tk.Menu(self.master, tearoff=0)
        tools_menu = tk.Menu(self.master, tearoff=0)
        pref_menu = tk.Menu(self.master, tearoff=0)
        help_menu = tk.Menu(self.master, tearoff=0)

        # Sub-menu
        data_menu = tk.Menu(self.master, tearoff=0)
        structure_menu = tk.Menu(self.master, tearoff=0)
        algorithm_selection = tk.Menu(self.master, tearoff=0)

        # File
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.clear_cache)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save as", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.destroy)

        # Display
        menu_bar.add_cascade(label="Display", menu=display_menu)
        display_menu.add_command(label="All atoms", command=self.show_all_atom)
        display_menu.add_command(label="All atoms and faces", command=self.show_all_atom_and_face)
        display_menu.add_command(label="Octahedral complex", command=self.show_octa)
        display_menu.add_command(label="Octahedron and 8 faces", command=self.show_octa_and_face)
        display_menu.add_command(label="Octahedron and selected 4 faces", command=self.show_octa_and_opt_face)
        display_menu.add_command(label="Projection planes", command=self.show_projection_plane)
        display_menu.add_command(label="Twisting triangular faces", command=self.show_twisting_face)

        # Tools
        menu_bar.add_cascade(menu=tools_menu, label="Tools")
        tools_menu.add_cascade(menu=data_menu, label="Data summary")
        data_menu.add_cascade(label="Complex info", command=self.show_data_summary)
        data_menu.add_cascade(label="Selected 4 faces", command=self.show_face_summary)
        tools_menu.add_cascade(menu=structure_menu, label="Show structural parameter")
        structure_menu.add_command(label="Octahedron", command=self.show_param_octa)
        structure_menu.add_command(label="All atoms", command=self.show_param_full)
        tools_menu.add_separator()
        tools_menu.add_command(label="Calculate surface area", command=self.show_surface_area)
        tools_menu.add_command(label="Relationship plot between Σ and Θ", command=self.show_plot_angle)

        # Preference
        # menu_bar.add_cascade(menu=pref_menu, label="Preference")

        # Setting check_button for Theta algorithm # Turn off for now
        """
        self.check_algorithm_1 = tk.BooleanVar()
        self.check_algorithm_1.set(True)
        self.check_algorithm_2 = tk.BooleanVar()
        self.check_algorithm_2.set(False)
        self.theta_algorithm = 1

        def select_algorithm_1():
            self.theta_algorithm = 1
            self.check_algorithm_1.set(True)
            self.check_algorithm_2.set(False)
            print_stdout(self, "Warning: Algorithm 1 enabled")

        def select_algorithm_2():
            self.theta_algorithm = 2
            self.check_algorithm_1.set(False)
            self.check_algorithm_2.set(True)
            print_stdout(self, "Warning: Algorithm 2 enabled")

        pref_menu.add_cascade(menu=algorithm_selection, label="Algorithm for computing Θ")
        algorithm_selection.add_checkbutton(label="Algorithm 1 (default)", onvalue=True, offvalue=False,
                                            variable=self.check_algorithm_1, command=select_algorithm_1)
        algorithm_selection.add_checkbutton(label="Algorithm 2", onvalue=True, offvalue=False,
                                            variable=self.check_algorithm_2, command=select_algorithm_2)
        """
        # Help
        menu_bar.add_cascade(menu=help_menu, label="Help")
        help_menu.add_command(label="Program help", command=self.show_help)
        help_menu.add_command(label="About program", command=self.show_about)
        help_menu.add_command(label="License information", command=self.show_license)

        # Setting layout under master
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(padx=5, pady=5, row=0, column=0, columnspan=2)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(padx=5, pady=5, row=1, column=0)
        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(padx=5, pady=5, row=1, column=1)
        self.frame4 = tk.Frame(self.master)
        self.frame4.grid(padx=5, pady=5, row=2, column=0, columnspan=2)
        self.frame5 = tk.Frame(self.master)
        self.frame5.grid(padx=5, pady=5, row=0, column=2, rowspan=3)

        # Frame 1
        title = "Octahedral Distortion Analysis"
        self.lbl1 = tk.Label(self.frame1, foreground="blue", font=("Arial", 16, "bold"), text=title)
        self.lbl1.grid(pady="5", row=0, columnspan=4)
        description = "A program for determining the structural distortion of the octahedral complexes"
        self.lbl2 = tk.Label(self.frame1, text=description)
        self.lbl2.grid(pady="5", row=1, columnspan=4)

        self.show_details = tk.BooleanVar()
        self.show_details.set(False)

        def select_details_window():
            if self.show_details.get():
                self.master.geometry("1050x535")
            else:
                self.master.geometry("520x535")

        # Frame 2
        self.lbl = tk.Label(self.frame2, text="Program console")
        self.lbl.grid(sticky=tk.N, pady="5", row=0)
        self.btn_openfile = tk.Button(self.frame2, text="Browse file", command=self.open_file)
        self.btn_openfile.config(width=12, relief=tk.RAISED)
        self.btn_openfile.grid(padx="10", pady="5", row=1)
        self.btn_run = tk.Button(self.frame2, text="Compute", command=self.calc_all_param)
        self.btn_run.config(width=12, relief=tk.RAISED)
        self.btn_run.grid(padx="10", pady="5", row=2)
        self.btn_clear = tk.Button(self.frame2, text="Clear cache", command=self.clear_cache)
        self.btn_clear.config(width=12, relief=tk.RAISED)
        self.btn_clear.grid(padx="10", pady="5", row=3)
        self.btn_show_details = tk.Checkbutton(self.frame2, text="Show details", onvalue=True, offvalue=False,
                                               variable=self.show_details, command=select_details_window, )
        self.btn_show_details.config(width=12, relief="raised")
        self.btn_show_details.grid(padx="10", pady="5", row=4)

        # Frame 3
        self.lbl1 = tk.Label(self.frame3, text="Octahedral distortion parameters")
        self.lbl1.grid(pady="5", row=0, columnspan=3)
        # Delta
        self.lbl2 = tk.Label(self.frame3, text="Δ = ")
        self.lbl2.grid(sticky=tk.E, pady="5", row=1, column=0)
        self.box_delta = tk.Text(self.frame3, height="1", width="15", wrap="word")
        self.box_delta.grid(row=1, column=1)
        # Sigma
        self.lbl3 = tk.Label(self.frame3, text="Σ = ")
        self.lbl3.grid(sticky=tk.E, pady="5", row=2, column=0)
        self.box_sigma = tk.Text(self.frame3, height="1", width="15", wrap="word")
        self.box_sigma.grid(row=2, column=1)
        self.lbl4 = tk.Label(self.frame3, text="degree")
        self.lbl4.grid(pady="5", row=2, column=2)
        # Min theta
        self.lbl_theta_min = tk.Label(self.frame3, text="Θ (min) = ")
        self.lbl_theta_min.grid(sticky=tk.E, pady="5", row=3, column=0)
        self.box_theta_min = tk.Text(self.frame3, height="1", width="15", wrap="word")
        self.box_theta_min.grid(row=3, column=1)
        self.lbl_theta_mean = tk.Label(self.frame3, text="degree")
        self.lbl_theta_mean.grid(pady="5", row=3, column=2)
        # Max theta
        self.lbl_theta_max = tk.Label(self.frame3, text="Θ (max) = ")
        self.lbl_theta_max.grid(sticky=tk.E, pady="5", row=4, column=0)
        self.box_theta_max = tk.Text(self.frame3, height="1", width="15", wrap="word")
        self.box_theta_max.grid(row=4, column=1)
        self.lbl_theta_mean = tk.Label(self.frame3, text="degree")
        self.lbl_theta_mean.grid(pady="5", row=4, column=2)
        # Mean theta
        self.lbl_theta_mean = tk.Label(self.frame3, text="Θ (mean) = ")
        self.lbl_theta_mean.grid(sticky=tk.E, pady="5", row=5, column=0)
        self.box_theta_mean = tk.Text(self.frame3, height="1", width="15", wrap="word")
        self.box_theta_mean.grid(row=5, column=1)
        self.lbl_theta_mean = tk.Label(self.frame3, text="degree")
        self.lbl_theta_mean.grid(pady="5", row=5, column=2)

        # Frame 4
        self.box_coord = tkscrolled.ScrolledText(self.frame4, height="14", width="70", wrap="word", undo="True")
        self.box_coord.grid(row=0)

        # Frame 5
        self.lbl = tk.Label(self.frame5, text="Standard Output/Error Information")
        self.lbl.grid(row=0)
        self.box_stdout = tkscrolled.ScrolledText(self.frame5, height="30", width="70", wrap="word", undo="True")
        self.box_stdout.grid(sticky=tk.N, pady="5", row=1)

        self.box_coord.insert(tk.INSERT, "Welcome to OctaDist {0}\n\n".format(program_version))
        popup.header(self)


if __name__ == '__main__':
    masters = tk.Tk()
    App = OctaDist(masters)
    masters.mainloop()
