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
            |  |- Octahedron
            |  |- Full complex 
            |-------------
            |- Calculate surface area 
            |-------------
            |- Relationship plot between Σ and Θ
            |-------------
            |- Display full complex and faces
            |- Display only octahedron and faces
            |- Display projection planes
            |- Display twisting triangular faces
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
        filemenu.add_command(label="Save as", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=masters.quit)

        # Tools
        menubar.add_cascade(menu=toolsmenu, label="Tools")
        toolsmenu.add_cascade(menu=datamenu, label="Data summary")
        datamenu.add_cascade(label="Complex info",
                             command=show_data_summary)
        toolsmenu.add_cascade(menu=structuremenu, label="Show structural parameter")
        structuremenu.add_command(label="Octahedron",
                                  command=show_param_octa)
        structuremenu.add_command(label="Full complex",
                                  command=show_param_full)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Calculate surface area",
                              command=show_surface_area)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Relationship plot between Σ and Θ",
                              command=show_plot_angle)
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Display full complex and faces",
                              command=display_full_complex_and_faces)
        toolsmenu.add_command(label="Display only octahedron and faces",
                              command=display_octahedron_and_faces)
        toolsmenu.add_command(label="Display projection planes",
                              command=display_projection_planes)
        toolsmenu.add_command(label="Display twisting triangular faces",
                              command=display_twisting_faces)

        # Help
        menubar.add_cascade(menu=helpmenu, label="Help")
        helpmenu.add_command(label="Program help",
                             command=popup.show_help)
        helpmenu.add_command(label="About program",
                             command=popup.show_about)
        helpmenu.add_command(label="License information",
                             command=popup.show_license)
        masters.config(menu=menubar)

        popup.welcome()

        # program details
        program_name = "Octahedral Distortion Analysis"
        self.lbl1 = tk.Label(master, foreground="blue",
                             font=("Arial", 16, "bold"), text=program_name)
        self.lbl1.config()
        self.lbl1.grid(pady="5", row=0, columnspan=4)
        description = "Determine the structural distortion " \
                      "between two octahedral structures."
        self.lbl2 = tk.Label(master, text=description)
        self.lbl2.grid(pady="5", row=1, columnspan=4)

        # button to browse input file
        self.btn_open_file = tk.Button(master, command=self.open_file,
                                       text="Browse file", relief=tk.RAISED)
        self.btn_open_file.grid(pady="5", row=2, column=0)

        # button to run
        self.btn_run = tk.Button(master, command=self.calc_all_param,
                                 text="Compute parameters")
        # btn_run.config(font="Segoe 10")
        self.btn_run.grid(sticky=tk.W, pady="5", row=2, column=1, columnspan=2)

        # button to clear cache
        self.btn_clear = tk.Button(master, command=self.clear_cache,
                                   text="Clear cache", )
        self.btn_clear.grid(sticky=tk.W, pady="5", row=2, column=3)

        # coordinate label
        self.lbl3 = tk.Label(master, text="Molecule Specifications")
        self.lbl3.grid(sticky=tk.W, pady="5", row=3, columnspan=4)

        # text box for showing cartesian coordinates
        self.box_coord = tkscrolled.ScrolledText(master,
                                                 height="14", width="70",
                                                 wrap="word", undo="True")
        self.box_coord.grid(pady="5", row=4, columnspan=4)

        # Octahedral distortion parameters
        self.lbl4 = tk.Label(master, text="Octahedral distortion parameters")

        # lbl_2.config(font="Segoe 10 bold")
        self.lbl4.grid(row=6, column=1, columnspan=2)

        # Display coordinate and vector projection
        self.lbl5 = tk.Label(master, text="Graphical Displays")
        # self.lbl_display.config(font="Segoe 10 bold")
        self.lbl5.grid(row=6, column=0, padx="30")

        # button to draw structure
        self.btn_complex = tk.Button(master, command=display_full_complex,
                                     text="Full complex", width="18")
        self.btn_complex.grid(pady="5", row=7, column=0)

        # button to draw plane
        self.btn_octa = tk.Button(master, command=display_octahedron,
                                  text="Only Octahedron", width="18")
        self.btn_octa.grid(pady="5", row=8, column=0)

        # button to draw vector projection
        self.btn_4faces = tk.Button(master, command=display_octahedron_and_opt_faces,
                                    text="Octahedron with 4 faces", width="18")
        self.btn_4faces.grid(pady="5", row=9, column=0)

        # Delta
        self.lbl6 = tk.Label(master, text="Δ  = ")
        self.lbl6.grid(sticky=tk.E, pady="5", row=7, column=1)
        self.box_delta = tk.Text(master, height="1",
                                 width="15", wrap="word")
        self.box_delta.grid(row=7, column=2, sticky=tk.W)

        # Sigma
        self.lbl7 = tk.Label(master, text="Σ  = ")
        self.lbl7.grid(sticky=tk.E, pady="5", row=8, column=1)
        self.box_sigma = tk.Text(master, height="1",
                                 width="15", wrap="word")
        self.box_sigma.grid(sticky=tk.W, row=8, column=2)
        self.lbl8 = tk.Label(master, text="degree")
        self.lbl8.grid(sticky=tk.W, pady="5", row=8, column=3)

        # Theta
        self.lbl_theta = tk.Label(master, text="Θ  = ")
        self.lbl_theta.grid(sticky=tk.E, pady="5", row=9, column=1)
        self.box_theta = tk.Text(master, height="1",
                                 width="15", wrap="word")
        self.box_theta.grid(sticky=tk.W, row=9, column=2)
        self.lbl9 = tk.Label(master, text="degree")
        self.lbl9.grid(sticky=tk.W, pady="5", row=9, column=3)

        # Link
        link = "https://github.com/rangsimanketkaew/OctaDist"
        self.lbl10 = tk.Label(master, foreground="blue",
                              text=link, cursor="hand2")
        self.lbl10.grid(pady="5", row=10, columnspan=4)
        self.lbl10.bind("<Button-1>", popup.callback)

    def clear_cache(self):
        """Clear all variables
        """

        global file_list, atom_octa, coord_octa, \
            atom_coord_full, atom_coord_sel, \
            comp_delta, comp_sigma, comp_theta

        print("Info: Clear cache")

        file_list = ""
        atom_octa = []
        coord_octa = []
        atom_coord_full = []
        atom_coord_sel = []

        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        self.box_coord.delete(1.0, tk.END)

        comp_delta = 0.0
        comp_sigma = 0.0
        comp_theta = 0.0

        self.clear_results()

    def clear_results(self):
        """Clear the computed parameters
        """
        self.box_delta.delete(1.0, tk.END)
        self.box_sigma.delete(1.0, tk.END)
        self.box_theta.delete(1.0, tk.END)

    def open_file(self):
        """Open input files
        """

        global file_list, atom_octa, coord_octa, atom_coord_full, atom_coord_sel

        print("Info: Browse input file")

        if file_list != "":
            self.clear_cache()

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
            print("Info: The total number of file: %s \n"
                  % len(file_list))

            atom_coord_full, atom_coord_sel = [], []

            for i in range(len(file_list)):
                # Print coordinates
                print("Info: Open file no. {0:d} : \"{1}\"".format(i + 1, file_list[i]))

                texts = "File {0}: {1}\n\n" \
                        "Atom                       Cartesian coordinate" \
                    .format(i + 1, file_list[i].split('/')[-1])
                self.box_coord.insert(tk.INSERT, texts)

                # Get atom and coordinate
                atom_full, coord_full = coord.get_coord(file_list[i])

                # Print atom and coordinate, and get only first 7 atoms
                atom_octa, coord_octa = coord.cut_coord(atom_full, coord_full)

                # Check if input file has coordinate inside
                if np.any(coord_octa) == 0:
                    popup.nocoord_error()
                    return 1

                for j in range(len(atom_octa)):
                    texts = " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}" \
                        .format(atom_octa[j],
                                coord_octa[j][0],
                                coord_octa[j][1],
                                coord_octa[j][2])
                    self.box_coord.insert(tk.END, "\n" + texts)

                self.box_coord.insert(tk.END, "\n\n---------------------------------\n\n")

                # Store all data into following arrays
                atom_coord_full.append([atom_full, coord_full])
                atom_coord_sel.append([atom_octa, coord_octa])
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

        f = filedialog.asksaveasfile(mode='w',
                                     defaultextension=".out",
                                     title="Save as",
                                     filetypes=(("Output File", "*.out"),
                                                ("Text File", "*.txt"),
                                                ("All Files", "*.*")))

        if f is None:
            print("Warning: Save file cancelled")
            return 0

        f.write("OctaDist %s: Octahedral Distortion Analysis\n"
                % program_version)
        f.write("https://github.com/rangsimanketkaew/OctaDist\n\n")
        f.write("By Rangsiman Ketkaew\n")
        f.write("Computational Chemistry Research Unit\n")
        f.write("Department of Chemistry\n")
        f.write("Faculty of Science and Technology\n")
        f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
        f.write("E-mail: rangsiman1993@gmail.com\n\n")
        f.write("Date: %s\n\n" % (datetime.datetime.now()))

        for i in range(len(file_list)):
            f.write("File       :  %2d\n" % int(i+1))
            f.write("Input file : " + file_list[i].split('/')[-1] + "\n")
            f.write("Output file: " + f.name.split('/')[-1] + "\n\n")
            f.write("Cartesian coordinates:\n")
            for j in range(len(coord_octa)):
                f.write("{0:2}  {1:10.6f}  {2:10.6f}  {3:10.6f}\n"
                        .format(atom_octa[j],
                                coord_octa[j][0],
                                coord_octa[j][1],
                                coord_octa[j][2]))
            f.write("\nOctahedral distortion parameters:\n")
            f.write(" - Delta = %10.6f\n" % comp_delta)
            f.write(" - Sigma = %10.6f degree\n" % comp_sigma)
            f.write(" - Theta = %10.6f degree\n\n" % comp_theta)
            f.write("--------------------------------------\n\n")

        f.close()

        print("Info: Data has been saved to \"%s\"" % f.name)

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """

        global run_check, \
            comp_delta, comp_sigma, comp_theta, \
            all_delta, all_sigma, all_theta, comp_result, \
            all_comp, pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl

        if file_list == "":
            popup.nofile_error()
            return 1

        run_check = 1
        self.clear_results()

        # Ready to compute all parameters
        all_delta = []
        all_sigma = []
        all_theta = []
        comp_result = []

        for i in range(len(file_list)):
            print("      ====================== Complex %s ======================\n"
                  % int(i + 1))
            print("Info: Show coordinate and compute Δ, Σ, and Θ parameters")

            atom_list, coord_list = atom_coord_sel[i]
            coord.show_7_atoms(atom_list, coord_list)

            comp_delta = calc.calc_delta(coord_list)
            comp_sigma = calc.calc_sigma(coord_list)
            comp_theta, all_comp = calc.calc_theta(coord_list)

            print("Info: Show computed octahedral distortion parameters\n")
            print("      Δ = {0:10.6f}".format(comp_delta))
            print("      Σ = {0:10.6f} degree".format(comp_sigma))
            print("      Θ = {0:10.6f} degree\n".format(comp_theta))

            all_delta.append(comp_delta)
            all_sigma.append(comp_sigma)
            all_theta.append(comp_theta)

            comp_result.append([comp_delta, comp_sigma, comp_theta])

        print("      ===================== Overall Summary =====================\n")
        print("Info: Show computed octahedral distortion parameters of all files")

        for i in range(len(comp_result)):
            print("      Complex {0:2d} : {1}".format(i + 1,
                                                         file_list[i].split('/')[-1]))

        print("\n                         Δ           Σ (°)         Θ (°)")
        print("                     --------    ----------    ----------")
        for i in range(len(comp_result)):
            print("      Complex {0:2d} : {1:10.6f}    {2:10.6f}    {3:10.6f}"
                  .format(i + 1,
                          comp_result[i][0],
                          comp_result[i][1],
                          comp_result[i][2]))

        print("\n      ===========================================================\n")

        if len(file_list) == 1:
            self.box_delta.insert(tk.INSERT, '%3.6f' % comp_delta)
            self.box_sigma.insert(tk.INSERT, '%3.6f' % comp_sigma)
            self.box_theta.insert(tk.INSERT, '%3.6f' % comp_theta)

        else:
            tools.show_results_mult(comp_result)

        if len(file_list) == 1:
            pal, pcl, ref_pal, ref_pcl, oppo_pal, oppo_pcl = all_comp


def show_data_summary():
    if file_list == "":
        popup.nofile_error()
        return 1

    tools.show_data_summary(file_list, atom_coord_full)


def show_param_octa():
    """Show structural parameters for octahedral structure (7 atoms):
    bond distance and bond angle between metal center and ligand atoms
    """

    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1

    tools.calc_param_octa(atom_octa, coord_octa)


def show_param_full():
    """Show structural parameters for full complex:
    bond distance and bond angle between metal center and ligand atoms
    """

    if file_list == "":
        popup.nofile_error()
        return 1
    if len(file_list) > 1:
        popup.only_single_file_error()
        return 1

    atom_full, coord_full = atom_coord_full[0]

    tools.calc_param_full(atom_full, coord_full)


def show_surface_area():
    """Show surface area of selected 8 faces
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

    tools.calc_surface_area(pal, pcl)


def show_plot_angle():
    """Plot Sigma versus Theta angles
    Relation plot between Sigma and Theta
    """

    if file_list == "":
        popup.nofile_error()
        return 1
    if run_check == 0:
        popup.nocalc_error()
        return 1

    draw.show_plot_angles(all_sigma, all_theta)


def display_full_complex():
    """Display full structure
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

    draw.draw_full_complex(atom_full, coord_full)


def display_full_complex_and_faces():
    """Display full structure with the projection plane
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

    draw.draw_full_complex_and_faces(atom_full, coord_full, pcl)


def display_octahedron():
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


def display_octahedron_and_faces():
    """Display the octahedral structure with 8 faces
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

    draw.draw_octahedron_and_faces(atom_octa, coord_octa, pcl)


def display_octahedron_and_opt_faces():
    """Display the octahedral structure with optimal 4 faces which give the lowest Theta value
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

    draw.draw_octahedron_and_opt_faces(atom_octa, coord_octa, ref_pcl)


def display_projection_planes():
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


def display_twisting_faces():
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
    MainProgram = OctaDist(masters)

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
