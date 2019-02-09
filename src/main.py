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

OctaDist version 2.2

Octahedral Distortion Analysis
Software website: https://octadist.github.io
Last modified: February 2019

This program has been written in Python 3 binding to TkInter GUI platform.
Written and tested on PyCharm (Community Edition) program.
Program executable is compiled by PyInstaller package.


Author: Rangsiman Ketkaew (Department of Chemistry, Thammasat University, Thailand)
Contact: rangsiman1993@gmail.com & rangsiman_k@sci.tu.ac.th
Personal website: https://sites.google.com/site/rangsiman1993
"""

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

program_version = "2.2"


class OctaDist:
    def __init__(self, master):
        self.master = master
        self.master.title("OctaDist")
        FONT = "Arial 10"
        self.master.option_add("*Font", FONT)
        self.frame = tk.Frame(self.master, width="2", height="2")
        self.frame.grid(padx=5, pady=5, row=0, column=0)

        """
        Create menu bar
            File
            |- New 
            |- Open 
            |- Save as
            |-------------
            |- Exit
            Display
            |- Display octahedron and 8 faces
            |- Display octahedron and selected 4 faces
            |- Display projection planes
            |- Display twisting triangular faces
            Tools
            |- Data summary
            |  |- Complex info
            |  |- Selected 4 faces
            |- Show structural parameters 
            |  |- Octahedron
            |  |- All atoms 
            |-------------
            |- Calculate surface area 
            |- Relationship plot between Σ and Θ
            Preference
            |- Auto-search octahedron
            Help
            |- Program help 
            |- About program 
            |- License info
        """

        # Main menu
        menu_bar = tk.Menu(self.frame)
        file_menu = tk.Menu(self.frame, tearoff=0)
        display_menu = tk.Menu(self.frame, tearoff=0)
        tools_menu = tk.Menu(self.frame, tearoff=0)
        pref_menu = tk.Menu(self.frame, tearoff=0)
        help_menu = tk.Menu(self.frame, tearoff=0)

        # Sub-menu
        data_menu = tk.Menu(self.frame, tearoff=0)
        structure_menu = tk.Menu(self.frame, tearoff=0)

        # File
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.clear_cache)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save as", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.destroy)

        # Display
        menu_bar.add_cascade(label="Display", menu=display_menu)
        display_menu.add_command(label="Display octahedron and 8 faces", command=show_octa_and_face)
        display_menu.add_command(label="Display octahedron and selected 4 faces", command=show_octa_and_opt_face)
        display_menu.add_command(label="Display projection planes", command=show_projection_plane)
        display_menu.add_command(label="Display twisting triangular faces", command=show_twisting_face)

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
        tools_menu.add_command(label="Relationship plot between Σ and Θ", command=show_plot_angle)

        # Setting check_button
        self.check_search_octa = tk.BooleanVar()
        self.check_search_octa.set(False)

        def auto_search_status():
            if self.check_search_octa.get():
                print("Info: Auto-search octahedron enabled")
            else:
                print("Info: Auto-search octahedron disabled")

        # Preference
        menu_bar.add_cascade(menu=pref_menu, label="Preference")
        pref_menu.add_checkbutton(label="Auto-search octahedron", onvalue=True, offvalue=False,
                                  variable=self.check_search_octa, command=auto_search_status)

        # Help
        menu_bar.add_cascade(menu=help_menu, label="Help")
        help_menu.add_command(label="Program help", command=self.show_help)
        help_menu.add_command(label="About program", command=popup.show_about)
        help_menu.add_command(label="License information", command=popup.show_license)
        self.master.config(menu=menu_bar)

        popup.welcome()

        program_name = "Octahedral Distortion Analysis"
        self.lbl1 = tk.Label(self.frame, foreground="blue", font=("Arial", 16, "bold"), text=program_name)
        self.lbl1.config()
        self.lbl1.grid(pady="5", row=0, columnspan=4)
        description = "A program for determining the structural distortion of octahedral complexes"
        self.lbl2 = tk.Label(self.frame, text=description)
        self.lbl2.grid(pady="5", row=1, columnspan=4)

        self.btn_open_file = tk.Button(self.frame, text="Browse file", relief=tk.RAISED, command=self.open_file)
        self.btn_open_file.grid(pady="5", row=2, column=0)

        self.btn_run = tk.Button(self.frame, text="Compute parameters", command=self.calc_all_param)
        self.btn_run.grid(sticky=tk.W, pady="5", row=2, column=1, columnspan=2)

        self.btn_clear = tk.Button(self.frame, text="Clear cache", command=self.clear_cache)
        self.btn_clear.grid(sticky=tk.W, pady="5", row=2, column=3)

        self.lbl3 = tk.Label(self.frame, text="Molecule Specifications")
        self.lbl3.grid(sticky=tk.W, pady="5", row=3, columnspan=4)

        self.box_coord = tkscrolled.ScrolledText(self.frame, height="14", width="70", wrap="word", undo="True")
        self.box_coord.grid(pady="5", row=4, columnspan=4)

        self.lbl4 = tk.Label(self.frame, text="Octahedral distortion parameters")
        self.lbl4.grid(row=6, column=1, columnspan=2)

        self.lbl5 = tk.Label(self.frame, text="Graphical Displays")
        self.lbl5.grid(row=6, column=0, padx="30")

        self.btn_complex = tk.Button(self.frame, text="All atoms", width="18", command=show_all_atom)
        self.btn_complex.grid(pady="5", row=7, column=0)

        self.btn_octa = tk.Button(self.frame, text="All atoms and faces", width="18", command=show_all_atom_and_face)
        self.btn_octa.grid(pady="5", row=8, column=0)

        self.btn_4faces = tk.Button(self.frame, text="Octahedral complex", width="18", command=show_octa)
        self.btn_4faces.grid(pady="5", row=9, column=0)

        self.lbl6 = tk.Label(self.frame, text="Δ  = ")
        self.lbl6.grid(sticky=tk.E, pady="5", row=7, column=1)
        self.box_delta = tk.Text(self.frame, height="1", width="15", wrap="word")
        self.box_delta.grid(row=7, column=2, sticky=tk.W)

        self.lbl7 = tk.Label(self.frame, text="Σ  = ")
        self.lbl7.grid(sticky=tk.E, pady="5", row=8, column=1)
        self.box_sigma = tk.Text(self.frame, height="1", width="15", wrap="word")
        self.box_sigma.grid(sticky=tk.W, row=8, column=2)
        self.lbl8 = tk.Label(self.frame, text="degree")
        self.lbl8.grid(sticky=tk.W, pady="5", row=8, column=3)

        self.lbl_theta = tk.Label(self.frame, text="Θ  = ")
        self.lbl_theta.grid(sticky=tk.E, pady="5", row=9, column=1)
        self.box_theta = tk.Text(self.frame, height="1", width="15", wrap="word")
        self.box_theta.grid(sticky=tk.W, row=9, column=2)
        self.lbl9 = tk.Label(self.frame, text="degree")
        self.lbl9.grid(sticky=tk.W, pady="5", row=9, column=3)

        link = "https://octadist.github.io"
        self.lbl10 = tk.Label(self.frame, foreground="blue", text=link, cursor="hand2")
        self.lbl10.grid(pady="5", row=10, columnspan=4)
        self.lbl10.bind("<Button-1>", popup.callback)

    def clear_cache(self):
        """Clear all variables
        """
        global file_list, atom_octa, coord_octa, atom_coord_full, \
            atom_coord_octa, comp_delta, comp_sigma, comp_theta

        print("Info: Clear cache")

        file_list = ""
        atom_octa = []
        coord_octa = []
        atom_coord_full = []
        atom_coord_octa = []

        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        comp_delta = 0
        comp_sigma = 0
        comp_theta = 0

        self.box_coord.delete(1.0, tk.END)
        self.clear_results()

    def clear_results(self):
        """Clear box of computed octahedral distortion parameters
        """
        self.box_delta.delete(1.0, tk.END)
        self.box_sigma.delete(1.0, tk.END)
        self.box_theta.delete(1.0, tk.END)

    def open_file(self):
        """Open input files
        """
        global file_list, atom_octa, coord_octa, atom_coord_full, atom_coord_octa

        if file_list != "":
            self.clear_cache()

        print("Info: Browse input file")

        file_name = filedialog.askopenfilenames(
            title="Choose input file",
            filetypes=(("XYZ File", "*.xyz"),
                       ("Text File", "*.txt"),
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
            print("Info: The total number of file: %s\n" % len(file_list))

            atom_coord_full = []
            atom_coord_octa = []

            for i in range(len(file_list)):
                # Extract atoms and coordinates from input file
                atom_full, coord_full = coord.get_coord(file_list[i])

                # Use auto-search octahedron if requested
                if self.check_search_octa.get():
                    atom_octa, coord_octa = coord.auto_search_octa(atom_full, coord_full)
                else:
                    atom_octa = list(atom_full[:7])
                    coord_octa = np.asarray(coord_full[:7])

                # Check if input file has coordinate inside
                if np.any(coord_octa) == 0:
                    popup.nocoord_error()
                    return 1

                # Print atoms and coordinates
                get_name = file_list[i].split('/')[-1]
                print("Info: Open file no. {0}: {1}".format(i + 1, get_name))

                if len(coord_full) > 7:
                    coord.list_all_atom(atom_full, coord_full)
                coord.list_octahedron_atom(atom_octa, coord_octa)

                # Insert coordinates into text box
                texts = "File {0}: {1}\n\n" \
                        "Atom                       Cartesian coordinate".format(i + 1, get_name)
                self.box_coord.insert(tk.INSERT, texts)

                for j in range(len(atom_octa)):
                    texts = " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}" \
                        .format(atom_octa[j], coord_octa[j][0], coord_octa[j][1], coord_octa[j][2])
                    self.box_coord.insert(tk.END, "\n" + texts)

                self.box_coord.insert(tk.END, "\n\n---------------------------------\n\n")

                # Store all data into following arrays
                atom_coord_full.append([atom_full, coord_full])
                atom_coord_octa.append([atom_octa, coord_octa])
        except:
            print("Error: No input file")
            file_list = ""

    def save_file(self):
        """Save computed data to file. The result will be saved into .txt or .out file.
        """
        print("Info: Save data to output file")

        if file_list == "":
            popup.nofile_error()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt", title="Save as",
                                     filetypes=(("Text File", "*.txt"),
                                                ("Output File", "*.out"),
                                                ("All Files", "*.*")))

        if f is None:
            print("Warning: Save file cancelled")
            return 0

        f.write("OctaDist %s: Octahedral Distortion Analysis\n" % program_version)
        f.write("https://octadist.github.io\n\n")
        f.write("By Rangsiman Ketkaew\n")
        f.write("Computational Chemistry Research Unit\n")
        f.write("Department of Chemistry\n")
        f.write("Faculty of Science and Technology\n")
        f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
        f.write("E-mail: rangsiman1993@gmail.com\n\n")
        f.write("Date: %s\n\n" % (datetime.datetime.now()))
        for i in range(len(file_list)):
            f.write("File       : %s\n" % int(i + 1))
            f.write("Input file : " + file_list[i].split('/')[-1] + "\n")
            f.write("Output file: " + f.name.split('/')[-1] + "\n\n")
            f.write("Cartesian coordinates:\n")
            for j in range(len(coord_octa)):
                f.write("{0:2}  {1:10.6f}  {2:10.6f}  {3:10.6f}\n"
                        .format(atom_octa[j], coord_octa[j][0], coord_octa[j][1], coord_octa[j][2]))
            f.write("\nOctahedral distortion parameters:\n")
            f.write(" - Delta = %10.6f\n" % comp_result[i][0])
            f.write(" - Sigma = %10.6f degree\n" % comp_result[i][1])
            f.write(" - Theta = %10.6f degree\n\n" % comp_result[i][2])
            f.write("--------------------------------------\n\n")

        f.close()

        print("Info: Data has been saved to \"%s\"" % f.name)

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        global run_check, comp_delta, comp_sigma, comp_theta, all_sigma, all_theta, \
            comp_result, all_comp, pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl

        if file_list == "":
            popup.nofile_error()
            return 1

        run_check = 1
        self.clear_results()

        all_sigma = []
        all_theta = []
        comp_result = []

        for i in range(len(file_list)):
            print("      ********************** Complex %s **********************\n" % int(i + 1))
            print("Info: Show coordinate and compute Δ, Σ, and Θ parameters")

            atom_list, coord_list = atom_coord_octa[i]
            coord.list_octahedron_atom(atom_list, coord_list)

            comp_delta = calc.calc_delta(atom_list, coord_list)
            comp_sigma = calc.calc_sigma(atom_list, coord_list)
            comp_theta, all_comp = calc.calc_theta(coord_list)

            all_sigma.append(comp_sigma)
            all_theta.append(comp_theta)
            comp_result.append([comp_delta, comp_sigma, comp_theta])

        print("Info: Show computed octahedral distortion parameters of all files\n")
        print("      ===================== Overall Summary ====================\n")

        for i in range(len(comp_result)):
            print("      Complex {0:2d} : {1}".format(i + 1, file_list[i].split('/')[-1]))

        print("\n      Complex          Δ           Σ (°)         Θ (°)")
        print("      -------      --------    ----------    ----------")

        for i in range(len(comp_result)):
            print("         {0:2d}      {1:10.6f}    {2:10.6f}    {3:10.6f}"
                  .format(i + 1, comp_result[i][0], comp_result[i][1], comp_result[i][2]))

        print("\n      ==========================================================")

        if len(file_list) == 1:
            pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl = all_comp
            self.box_delta.insert(tk.INSERT, '%3.6f' % comp_delta)
            self.box_sigma.insert(tk.INSERT, '%3.6f' % comp_sigma)
            self.box_theta.insert(tk.INSERT, '%3.6f' % comp_theta)

        else:
            self.show_results_mult()

    def show_help(self):
        """Open program help page
        """
        self.newWindow = tk.Toplevel(self.master)
        self.app = popup.ShowHelp(self.newWindow)

    def show_results_mult(self):
        """Open program help page
        """
        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowResults(self.newWindow, comp_result)

    def show_data_summary(self):
        """Show information of complex/structure
        """
        if file_list == "":
            popup.nofile_error()
            return 1

        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowData(self.newWindow, file_list, atom_coord_full)

    def show_face_summary(self):
        """Show information of selected 4 faces
        """
        if file_list == "":
            popup.nofile_error()
            return 1
        if len(file_list) > 1:
            popup.only_single_file_error()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowFaceSet(self.newWindow, ref_pal, ref_pcl, oppo_pal, oppo_pcl)

    def show_param_octa(self):
        """Show selected structural parameters of octahedral structure:
        bond distance and bond angle between metal center and ligand atoms
        """
        if file_list == "":
            popup.nofile_error()
            return 1
        if len(file_list) > 1:
            popup.only_single_file_error()
            return 1

        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowParamOcta(self.newWindow, atom_octa, coord_octa)

    def show_param_full(self):
        """Show structural parameters of full complex:
        bond distance and bond angle between metal center and ligand atoms
        """
        if file_list == "":
            popup.nofile_error()
            return 1
        if len(file_list) > 1:
            popup.only_single_file_error()
            return 1

        atom_full, coord_full = atom_coord_full[0]

        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowParamFull(self.newWindow, atom_full, coord_full)

    def show_surface_area(self):
        """Show surface area of 8 faces of octahedron
        """
        if file_list == "":
            popup.nofile_error()
            return 1
        if len(file_list) > 1:
            popup.only_single_file_error()
            return 1
        if run_check == 0:
            popup.nocalc_error()
            return 1

        self.newWindow = tk.Toplevel(self.master)
        self.app = tools.ShowSurfaceArea(self.newWindow, pal, pcl)


def show_plot_angle():
    """Show relationship plot Sigma and Theta parameters
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.show_plot_angles(all_sigma, all_theta)


def show_all_atom():
    """Display full complex
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    atom_full, coord_full = atom_coord_full[0]

    draw.draw_all_atom(atom_full, coord_full)


def show_all_atom_and_face():
    """Display full complex and 8 faces of octahedron
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    atom_full, coord_full = atom_coord_full[0]

    draw.draw_all_atom_and_face(atom_full, coord_full, pcl)


def show_octa():
    """Display the octahedral structure
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_octahedron(atom_octa, coord_octa)


def show_octa_and_face():
    """Display the octahedral structure and its 8 faces
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_octahedron_and_face(atom_octa, coord_octa, pcl)


def show_octa_and_opt_face():
    """Display the octahedral structure and selected optimal 4 faces
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_octahedron_and_opt_face(atom_octa, coord_octa, ref_pcl)


def show_projection_plane():
    """Display the projection planes
    """
    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_projection_planes(atom_octa, coord_octa, ref_pcl, oppo_pcl)


def show_twisting_face():
    """Display the twisting triangular faces
    """

    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.draw_twisting_faces(atom_octa, coord_octa, ref_pcl, oppo_pcl)


def main():
    masters = tk.Tk()
    App = OctaDist(masters)

    global file_list, run_check
    file_list = ""
    run_check = 0

    def on_closing():
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            masters.destroy()

    masters.protocol("WM_DELETE_WINDOW", on_closing)
    masters.mainloop()


if __name__ == '__main__':
    main()
