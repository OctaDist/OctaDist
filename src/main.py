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
    if self.show_stdout.get():
        self.box_stdout.insert(tk.INSERT, text + "\n")
        self.box_stdout.see(tk.END)
    else:
        return 0


def print_coord(self, text):
    """Insert text to Coordinate box
    """
    self.box_coord.insert(tk.INSERT, text + "\n")
    self.box_coord.see(tk.END)


class OctaDist:
    def __init__(self, master):
        # Default settings
        self.file_list = ""
        self.atom_octa = []
        self.coord_octa = []
        self.atom_coord_full = []
        self.atom_coord_octa = []
        self.pal = []
        self.pcl = []
        self.ref_pal = []
        self.ref_pcl = []
        self.oppo_pal = []
        self.oppo_pcl = []
        self.comp_result = []
        self.all_sigma = []
        self.all_theta = []
        self.delta = 0
        self.sigma = 0
        self.theta_min = 0
        self.theta_max = 0
        self.theta_mean = 0

        # Windows GUI
        self.master = master
        self.master.title("OctaDist {0}".format(program_version))
        font = "Arial 10"
        self.master.option_add("*Font", font)
        self.master.geometry("520x535")

        # Main menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(self.master, tearoff=0)
        display_menu = tk.Menu(self.master, tearoff=0)
        tools_menu = tk.Menu(self.master, tearoff=0)
        help_menu = tk.Menu(self.master, tearoff=0)

        # Sub-menu
        data_menu = tk.Menu(self.master, tearoff=0)
        structure_menu = tk.Menu(self.master, tearoff=0)

        # File
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.clear_cache())
        file_menu.add_command(label="Open", command=lambda: self.open_file())
        file_menu.add_command(label="Save as", command=lambda: self.save_file())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: master.destroy())

        # Display
        menu_bar.add_cascade(label="Display", menu=display_menu)
        display_menu.add_command(label="All atoms",
                                 command=lambda: draw.all_atom(self, self.atom_coord_full))
        display_menu.add_command(label="All atoms and faces",
                                 command=lambda: draw.all_atom_and_face(self, self.atom_coord_full, self.pcl))
        display_menu.add_command(label="Octahedral complex",
                                 command=lambda: draw.octahedron(self, self.atom_octa, self.coord_octa))
        display_menu.add_command(label="Octahedron and 8 faces",
                                 command=lambda: draw.octa_and_face(self, self.atom_octa,
                                                                    self.coord_octa, self.pcl))
        display_menu.add_command(label="Octahedron and selected 4 faces",
                                 command=lambda: draw.octa_and_4_face(self, self.atom_octa,
                                                                      self.coord_octa, self.ref_pcl))
        display_menu.add_command(label="Projection planes",
                                 command=lambda: draw.proj_planes(self, self.atom_octa, self.coord_octa,
                                                                  self.ref_pcl, self.oppo_pcl))
        display_menu.add_command(label="Twisting triangular faces",
                                 command=lambda: draw.twisting_faces(self, self.atom_octa, self.coord_octa,
                                                                     self.ref_pcl, self.oppo_pcl))

        # Tools
        menu_bar.add_cascade(menu=tools_menu, label="Tools")
        tools_menu.add_cascade(menu=data_menu, label="Data summary")
        data_menu.add_cascade(label="Complex info",
                              command=lambda: tools.data_complex(self, self.file_list, self.atom_coord_full))
        data_menu.add_cascade(label="Selected 4 faces",
                              command=lambda: tools.data_face(self, self.ref_pal, self.ref_pcl,
                                                              self.oppo_pal, self.oppo_pcl))
        tools_menu.add_cascade(menu=structure_menu, label="Show structural parameter")
        structure_menu.add_command(label="All atoms",
                                   command=lambda: tools.param_complex(self, self.atom_coord_full))
        structure_menu.add_command(label="Octahedron",
                                   command=lambda: tools.param_octa(self, self.atom_octa, self.coord_octa))
        tools_menu.add_separator()
        tools_menu.add_command(label="Calculate surface area",
                               command=lambda: tools.show_surface_area(self, self.pal, self.pcl))
        tools_menu.add_command(label="Relationship plot between Σ and Θ",
                               command=lambda: tools.show_plot_angles(self, self.all_sigma, self.all_theta))

        # Help
        menu_bar.add_cascade(menu=help_menu, label="Help")
        help_menu.add_command(label="Program help", command=lambda: popup.show_help(self.master))
        help_menu.add_command(label="About program", command=lambda: popup.show_about(self))
        help_menu.add_command(label="License information", command=lambda: popup.show_license(self))

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

        self.show_stdout = tk.BooleanVar()
        self.show_stdout.set(False)

        def select_stdout_window():
            if self.show_stdout.get():
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
        self.btn_show_stdout = tk.Checkbutton(self.frame2, text="STDOUT logs", onvalue=True, offvalue=False,
                                              variable=self.show_stdout, command=select_stdout_window)
        self.btn_show_stdout.config(width=12, relief="raised")
        self.btn_show_stdout.grid(padx="10", pady="5", row=4)

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

        print_coord(self, "Welcome to OctaDist {0}".format(program_version))
        popup.header(self)

    def clear_cache(self):
        """Clear all variables
        """
        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        self.file_list = ""
        self.atom_octa = []
        self.coord_octa = []
        self.atom_coord_full = []
        self.atom_coord_octa = []
        self.all_sigma = []
        self.all_theta = []
        self.comp_result = []
        self.delta = 0
        self.sigma = 0
        self.theta_min = 0
        self.theta_max = 0
        self.theta_mean = 0

        self.clear_results_box()
        self.clear_info_box()

        print_stdout(self, "Clear cache")

    def clear_results_box(self):
        """Clear result box
        """
        self.box_delta.delete(1.0, tk.END)
        self.box_sigma.delete(1.0, tk.END)
        self.box_theta_min.delete(1.0, tk.END)
        self.box_theta_max.delete(1.0, tk.END)
        self.box_theta_mean.delete(1.0, tk.END)

    def clear_info_box(self):
        self.box_coord.delete(1.0, tk.END)
        self.box_stdout.delete(1.0, tk.END)

    def open_file(self):
        """Open input files
        """
        # self.clear_results_box()
        # self.clear_info_box()
        self.clear_cache()
        print_stdout(self, "Info: Browse input file")

        try:
            input_file = filedialog.askopenfilenames(
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

            self.file_list = list(input_file)

            try:
                open(self.file_list[0], 'r')
                print_stdout(self, "Info: Total number of file: {0}".format(len(self.file_list)))

                self.atom_coord_full = []
                self.atom_coord_octa = []
                for i in range(len(self.file_list)):
                    file_name = self.file_list[i].split('/')[-1]
                    print_stdout(self, "Info: Open file no. {0}: {1}".format(i+1, file_name))

                    # Extract the atoms and the coordinates from input file
                    atom_full, coord_full = coord.get_coord(self, self.file_list[i])

                    # Print full structure on stdout box
                    print_stdout(self, "Info: Show Cartesian coordinates of all {0} atoms".format(len(atom_full)))
                    print_stdout(self, "")
                    print_stdout(self, "      Atom        X             Y             Z")
                    print_stdout(self, "      ----    ----------    ----------    ----------")
                    for j in range(len(atom_full)):
                        print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                     .format(atom_full[j], coord_full[j][0], coord_full[j][1], coord_full[j][2]))
                    print_stdout(self, "")

                    self.atom_octa, self.coord_octa = coord.search_octa(self, self.file_list[i], atom_full, coord_full)

                    # Check if input file has coordinate inside
                    if np.any(self.coord_octa) == 0:
                        popup.err_no_coord(self)
                        return 1

                    self.atom_coord_full.append([atom_full, coord_full])
                    self.atom_coord_octa.append([self.atom_octa, self.coord_octa])

                    if i == 0:
                        print_coord(self, "XYZ coordinate of extracted octahedral structure")
                    # Print octahedral structure on coord box
                    print_coord(self, "File {0}: {1}".format(i+1, file_name))
                    print_coord(self, "Atom                       Cartesian coordinate")
                    for j in range(len(self.atom_octa)):
                        print_coord(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                    .format(self.atom_octa[j],
                                            self.coord_octa[j][0], self.coord_octa[j][1], self.coord_octa[j][2]))
                    print_coord(self, "")

                    # Print octahedral structure on stdout box
                    print_stdout(self, "Info: Show Cartesian coordinates of extracted octahedral structure")
                    print_stdout(self, "")
                    print_stdout(self, "      Atom        X             Y             Z")
                    print_stdout(self, "      ----    ----------    ----------    ----------")
                    for j in range(len(self.atom_octa)):
                        print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                     .format(self.atom_octa[j],
                                             self.coord_octa[j][0], self.coord_octa[j][1], self.coord_octa[j][2]))
                    print_stdout(self, "")

            except UnboundLocalError:
                print_stdout(self, "Error: No input file")
                # self.clear_cache()
                print_coord(self, "Error: Could not open file \"{0}\"".format(file_name))
                print_coord(self, "Please carefully check the accuracy of the complex again!")
                return 1

        except IndexError:
            print_stdout(self, "Error: No input file")
            return 1

    def save_file(self):
        """Save structures as .xyz or .out file.
        """
        print_stdout(self, "Info: Save data as an output file")

        f = filedialog.asksaveasfile(mode='w', defaultextension=".xyz", title="Save as",
                                     filetypes=(("XYZ File", "*.xyz"),
                                                ("All Files", "*.*")))

        if f is None:
            print_stdout(self, "Warning: Cancelled save file")
            return 0

        f.write("7\n")
        f.write("XYZ coordinate generated by OctaDist {0} < https://octadist.github.io >\n".format(program_version))

        get_text = self.box_coord.get(1.0, tk.END)
        # split and get only xyz
        split_text = get_text.split('\n')[3:10]
        # join text in list
        xyz_coord = '\n'.join(split_text)
        f.write(xyz_coord)
        f.close()

        print_stdout(self, "Info: Data has been saved to \"{0}\"".format(f.name))

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        if len(self.atom_coord_octa) >= 1:
            self.clear_results_box()
        else:
            popup.err_no_file(self)
            return 1

        self.all_sigma, self.all_theta, self.comp_result, self.all_comp = \
            calc.calc_all(self, self.file_list, self.atom_coord_octa)

        self.pal, self.pcl, self.ref_pal, self.ref_pcl, self.oppo_pal, self.oppo_pcl = self.all_comp


if __name__ == '__main__':
    masters = tk.Tk()
    App = OctaDist(masters)
    masters.mainloop()
