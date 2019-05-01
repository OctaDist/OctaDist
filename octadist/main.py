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

OctaDist version 2.5.1 (GUI version)

Octahedral Distortion Analysis
Software website: https://octadist.github.io
Last modified: May 1st, 2019

This program was written in Python 3 binding to TkInter GUI platform,
tested on PyCharm (Community Edition) program, and compiled by PyInstaller.

Authors:
Rangsiman Ketkaew            Thammasat University, Thailand    rangsiman1993@gmail.com
Yuthana Tantirungrotechai    Thammasat University, Thailand    yt203y@gmail.com
David J. Harding             Walailak University, Thailand     hdavid@mail.wu.ac.th
Phimphaka Harding            Walailak University, Thailand     kphimpha@mail.wu.ac.th
Mathieu Marchivie            Université de Bordeaux, France    mathieu.marchivie@icmcb.cnrs.fr
"""

from octadist import draw, calc, coord, tools, popup

import numpy as np
import tkinter as tk
from tkinter import filedialog
import tkinter.scrolledtext as tkscrolled

program_version = "2.5.1"
program_revision = "May 2019"


def print_stdout(self, text):
    """Insert stdout & stderr to Log text box
    """
    if self.show_stdout.get():
        self.box_stdout.insert(tk.INSERT, text + "\n")
        self.box_stdout.see(tk.END)
    else:
        return 0


def print_result(self, text):
    """Insert text to Coordinate box
    """
    self.box_result.insert(tk.INSERT, text + "\n")
    self.box_result.see(tk.END)


class OctaDist:
    def __init__(self, master):

        # Default settings
        self.file_list = []             # input files
        self.atom_coord_full = []       # atomic labels and coordinates of metal complex
        self.atom_coord_octa = []       # atomic labels and coordinates of octahedral structures
        self.all_zeta = []              # computed zeta of all octahedral structures
        self.all_delta = []             # computed delta of all octahedral structures
        self.all_sigma = []             # computed sigma of all octahedral structures
        self.all_theta = []             # computed theta of all octahedral structures
        self.all_face = []              # atomic labels and coordinates of 8 faces and their opposite faces

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
        file_menu.add_command(label="Save results", command=lambda: self.save_results())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: master.destroy())

        # Display
        menu_bar.add_cascade(label="Display", menu=display_menu)
        display_menu.add_command(label="All atoms",
                                 command=lambda: draw.all_atom(self, self.atom_coord_full))
        display_menu.add_command(label="All atoms and faces",
                                 command=lambda: draw.all_atom_and_face(self, self.atom_coord_full, self.all_face))
        display_menu.add_command(label="Octahedral complex",
                                 command=lambda: draw.octahedron(self, self.atom_coord_octa))
        display_menu.add_command(label="Octahedron and 8 faces",
                                 command=lambda: draw.octa_and_face(self, self.atom_coord_octa, self.all_face))
        display_menu.add_separator()
        display_menu.add_command(label="Projection planes",
                                 command=lambda: draw.proj_planes(self, self.atom_coord_octa, self.all_face))
        display_menu.add_command(label="Twisting triangular faces",
                                 command=lambda: draw.twisting_faces(self, self.atom_coord_octa, self.all_face))

        # Tools
        menu_bar.add_cascade(menu=tools_menu, label="Tools")
        tools_menu.add_cascade(menu=data_menu, label="Data summary")
        data_menu.add_cascade(label="Complex info",
                              command=lambda: tools.data_complex(self, self.file_list, self.atom_coord_full))
        tools_menu.add_cascade(menu=structure_menu, label="Show structural parameter")
        structure_menu.add_command(label="All atoms",
                                   command=lambda: tools.param_complex(self, self.atom_coord_full))
        structure_menu.add_command(label="Octahedron",
                                   command=lambda: tools.param_octa(self, self.atom_coord_octa))
        tools_menu.add_separator()
        tools_menu.add_command(label="Relationship plot between Σ and Θ",
                               command=lambda: tools.plot_sigma_theta(self, self.all_sigma, self.all_theta))
        tools_menu.add_separator()
        tools_menu.add_command(label="Calculate surface area",
                               command=lambda: tools.calc_surface_area(self, self.all_face))
        tools_menu.add_command(label="Calculate Jahn-Teller distortion parameter",
                               command=lambda: tools.calc_jahn_teller(self, self.atom_coord_full))

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

        ######### Frame 1 #########

        title = "Octahedral Distortion Analysis"
        self.lbl = tk.Label(self.frame1, foreground="blue", font=("Arial", 16, "bold"), text=title)
        self.lbl.grid(pady="5", row=0, columnspan=4)
        description = "A program for determining the structural distortion of the octahedral complexes"
        self.lbl = tk.Label(self.frame1, text=description)
        self.lbl.grid(pady="5", row=1, columnspan=4)

        self.show_stdout = tk.BooleanVar()
        self.show_stdout.set(False)

        def select_stdout_window():
            if self.show_stdout.get():
                self.master.geometry("1050x535")
            else:
                self.master.geometry("520x535")

        ######### Frame 2 #########

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

        ######### Frame 3 #########

        self.lbl = tk.Label(self.frame3, text="Octahedral distortion parameters")
        self.lbl.grid(pady="5", row=0, columnspan=3)

        # D_mean
        self.lbl_d_mean = tk.Label(self.frame3, text="<D>   =   ")
        self.lbl_d_mean.grid(sticky=tk.E, pady="5", row=1, column=0)
        self.box_d_mean = tk.Entry(self.frame3, width="12", justify='center')
        self.box_d_mean.grid(row=1, column=1)
        self.lbl_unit = tk.Label(self.frame3, text="  Angstrom")
        self.lbl_unit.grid(pady="5", row=1, column=2)

        # Zeta
        self.lbl_zeta = tk.Label(self.frame3, text="ζ   =   ")
        self.lbl_zeta.grid(sticky=tk.E, pady="5", row=2, column=0)
        self.box_zeta = tk.Entry(self.frame3, width="12", justify='center')
        self.box_zeta.grid(row=2, column=1)
        self.lbl_unit = tk.Label(self.frame3, text="  Angstrom")
        self.lbl_unit.grid(pady="5", row=2, column=2)

        # Delta
        self.lbl_delta = tk.Label(self.frame3, text="Δ   =   ")
        self.lbl_delta.grid(sticky=tk.E, pady="5", row=3, column=0)
        self.box_delta = tk.Entry(self.frame3, width="12", justify='center')
        self.box_delta.grid(row=3, column=1)

        # Sigma
        self.lbl_sigma = tk.Label(self.frame3, text="Σ   =   ")
        self.lbl_sigma.grid(sticky=tk.E, pady="5", row=4, column=0)
        self.box_sigma = tk.Entry(self.frame3, width="12", justify='center')
        self.box_sigma.grid(row=4, column=1)
        self.lbl_unit = tk.Label(self.frame3, text="  degree")
        self.lbl_unit.grid(pady="5", row=4, column=2)

        # Theta_mean
        self.lbl_theta_mean = tk.Label(self.frame3, text="Θ   =   ")
        self.lbl_theta_mean.grid(sticky=tk.E, pady="5", row=5, column=0)
        self.box_theta_mean = tk.Entry(self.frame3, width="12", justify='center')
        self.box_theta_mean.grid(row=5, column=1)
        self.lbl_unit = tk.Label(self.frame3, text="  degree")
        self.lbl_unit.grid(pady="5", row=5, column=2)

        ######### Frame 4 #########

        self.box_result = tkscrolled.ScrolledText(self.frame4, height="14", width="70", wrap="word", undo="True")
        self.box_result.grid(row=0)

        ######### Frame 5 #########

        self.lbl = tk.Label(self.frame5, text="Standard Output/Error Information")
        self.lbl.grid(row=0)

        self.box_stdout = tkscrolled.ScrolledText(self.frame5, height="30", width="70", wrap="word", undo="True")
        self.box_stdout.grid(sticky=tk.N, pady="5", row=1)

        print_result(self, "Welcome to OctaDist {0} {1}".format(program_version, program_revision))
        print_result(self, "")
        print_result(self, "Created by Rangsiman Ketkaew, Yuthana Tantirungrotechai, David J. Harding, "
                           "Phimphaka Harding, and Mathieu Marchivie.")
        print_result(self, "")
        print_result(self, "https://octadist.github.io")
        popup.header(self)

    def clear_cache(self):
        """Clear all variables
        """
        for name in dir():
            if not name.startswith('_'):
                del locals()[name]

        self.file_list = []
        self.atom_coord_full = []
        self.atom_coord_octa = []
        self.all_zeta = []
        self.all_delta = []
        self.all_sigma = []
        self.all_theta = []
        self.all_face = []

        self.clear_results_box()
        self.clear_info_box()

        print_stdout(self, "Clear cache")

    def clear_results_box(self):
        """Clear result box
        """
        self.box_delta.delete(0, tk.END)
        self.box_sigma.delete(0, tk.END)
        self.box_d_mean.delete(0, tk.END)
        self.box_zeta.delete(0, tk.END)
        self.box_theta_mean.delete(0, tk.END)

    def clear_info_box(self):
        self.box_result.delete(1.0, tk.END)
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

                for i in range(len(self.file_list)):
                    file_name = self.file_list[i].split('/')[-1]
                    print_stdout(self, "Info: Open file no. {0}: {1}".format(i + 1, file_name))

                    # Check and read the atoms and coordinates of full complex
                    atom_full, coord_full = coord.get_coord(self, self.file_list[i])
                    self.atom_coord_full.append([atom_full, coord_full])

                    # Print full structure to stdout box
                    print_stdout(self, "Info: Show Cartesian coordinates of all {0} atoms".format(len(atom_full)))
                    print_stdout(self, "")
                    print_stdout(self, "      Atom        X             Y             Z")
                    print_stdout(self, "      ----    ----------    ----------    ----------")
                    for j in range(len(atom_full)):
                        print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                     .format(atom_full[j], coord_full[j][0], coord_full[j][1], coord_full[j][2]))
                    print_stdout(self, "")

                    # Count the number of metal center atom
                    count, coord_metal = coord.count_metal(self, atom_full, coord_full)

                    if count == 0:
                        popup.warn_no_metal(self)
                        continue

                    if i == 0:
                        print_result(self, "XYZ coordinates of extracted octahedral structure")

                    # loop over metal center atoms
                    for j in range(count):
                        # Extract the octahedral structure from the complex
                        atom_octa, coord_octa = coord.search_octa(atom_full, coord_full, coord_metal[j - 1])

                        # Check if input file has coordinate inside
                        if np.any(coord_octa) == 0:
                            popup.err_no_coord(self)
                            return 1

                        # gather octahedral structure into atom_coord_octa
                        # [ number of file, metal atom, atomic labels, and atomic coordinates ]
                        self.atom_coord_octa.append([i + 1, atom_octa[0], atom_octa, coord_octa])

                        # Print octahedral structure to coord box and stdout box (on request)
                        if count == 1:
                            print_result(self, "File {0}: {1}".format(i + 1, file_name))
                            print_result(self, "Atom                       Cartesian coordinate")
                            for k in range(len(atom_octa)):
                                print_result(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                             .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1],
                                                     coord_octa[k][2]))
                            print_result(self, "")

                            print_stdout(self, "Info: Show Cartesian coordinates of extracted octahedral structure")
                            print_stdout(self, "")
                            print_stdout(self, "      Atom        X             Y             Z")
                            print_stdout(self, "      ----    ----------    ----------    ----------")
                            for k in range(len(atom_octa)):
                                print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                             .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1],
                                                     coord_octa[k][2]))
                            print_stdout(self, "")

                        elif count > 1:
                            print_result(self, "File {0}: {1}".format(i + 1, file_name))
                            print_result(self, "Metal center atom no. {0} : {1}".format(j + 1, atom_octa[0]))
                            print_result(self, "Atom                       Cartesian coordinate")
                            for k in range(len(atom_octa)):
                                print_result(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                             .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1],
                                                     coord_octa[k][2]))
                            print_result(self, "")

                            print_stdout(self, "File {0}: {1}".format(i + 1, file_name))
                            print_stdout(self, "Info: Show Cartesian coordinates of extracted octahedral structure")
                            print_stdout(self, "")
                            print_stdout(self, "      Atom        X             Y             Z")
                            print_stdout(self, "      ----    ----------    ----------    ----------")
                            for k in range(len(atom_octa)):
                                print_stdout(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                             .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1],
                                                     coord_octa[k][2]))
                            print_stdout(self, "")

            except UnboundLocalError:
                print_stdout(self, "Error: No input file")
                # self.clear_cache()
                print_result(self, "Error: Could not open file \"{0}\"".format(file_name))
                print_result(self, "Please carefully check the accuracy of the complex again!")
                return 1

        except IndexError:
            print_stdout(self, "Error: No input file")
            return 1

    def save_results(self):
        """Save results as output file
        """
        print_stdout(self, "Info: Save results as an output file")

        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt", title="Save results",
                                     filetypes=(("TXT File", "*.txt"),
                                                ("All Files", "*.*")))

        if f is None:
            print_stdout(self, "Warning: Cancelled save file")
            return 0

        f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.\n")
        f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
        f.write("This is free software, and you are welcome to redistribute it under\n")
        f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n")
        f.write("\n")
        f.write("OctaDist {0} {1}: Octahedral Distortion Analysis\n".format(program_version, program_revision))
        f.write("https://octadist.github.io\n")
        f.write("\n")
        f.write("================ Start of the Output file =================\n")
        f.write("\n")
        get_result = self.box_result.get('1.0', tk.END+'-1c')
        f.write(get_result)
        f.write("\n")
        f.write("================= End of the output file ==================\n")
        f.write("\n")
        f.close()

        popup.info_save_results(self, f.name)

    def calc_all_param(self):
        """Calculate octahedral distortion parameters
        """
        if len(self.atom_coord_octa) >= 1:
            self.clear_results_box()
        else:
            popup.err_no_file(self)
            return 1

        self.all_zeta, self.all_delta, self.all_sigma, self.all_theta, self.all_face = \
            calc.calc_all(self, self.atom_coord_octa)


if __name__ == '__main__':
    masters = tk.Tk()
    App = OctaDist(masters)
    masters.mainloop()
