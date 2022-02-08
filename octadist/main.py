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

import base64
import os
import platform
import subprocess
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import webbrowser
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
from urllib.request import urlopen

import numpy as np

import octadist
from octadist.logo import Icon_Base64
from octadist.src import io, calc, draw, plot, popup, scripting, structure, tools


class OctaDist:
    """
    OctaDist class initiates main program UI and create all widgets.

    Program interface is structured as follows:

    +-------------------+
    |   Program Menu    |
    +-------------------+
    |     Frame 1       |
    +---------+---------+
    | Frame 2 | Frame 3 |
    +---------+---------+
    |     Frame 4       |
    +-------------------+

    - Frame 1 : Program name and short description
    - Frame 2 : Program console
    - Frame 3 : Textbox for showing summary output
    - Frame 4 : textbox for showing detailed output

    Examples
    --------
    >>> my_app = OctaDist()
    >>> my_app.start_app()

    """

    def __init__(self):
        self.master = tk.Tk()

        # Initialize parameters
        self.file_list = []  # Full path of input files.
        self.file_name = []  # File name.
        self.octa_index = []  # Octahedral structure index.
        self.atom_coord_full = []  # Coordinates of metal complex.
        self.atom_coord_octa = []  # Coordinates of octahedral structures.
        self.all_zeta = []  # Zeta of all octahedral structures.
        self.all_delta = []  # Delta of all octahedral structures.
        self.all_sigma = []  # Sigma of all octahedral structures.
        self.all_theta = []  # Theta of all octahedral structures.
        self.comp_result = []  # Distortion parameters.

        self.octadist_icon = None

        # Default cutoff values
        self.cutoff_metal_ligand = 2.8
        self.cutoff_global = 2.0
        self.cutoff_hydrogen = 1.2

        # Default executable of text editor
        self.text_editor = "notepad.exe"

        # Default molecular visualizer
        self.visualizer = "Matplotlib"

        # Default display settings
        self.show_title = True
        self.show_axis = True
        self.show_grid = True

        self.backup_cutoff_metal_ligand = self.cutoff_metal_ligand
        self.backup_cutoff_global = self.cutoff_global
        self.backup_cutoff_hydrogen = self.cutoff_hydrogen
        self.backup_text_editor = self.text_editor
        self.backup_visualizer = self.visualizer
        self.backup_show_title = self.show_title
        self.backup_show_axis = self.show_axis
        self.backup_show_grid = self.show_grid

        # Create master frame, sub-frames, add menu, and add widgets
        self.create_logo()
        self.start_master()
        self.add_menu()
        self.add_widgets()
        self.welcome_msg()
        self.start_app()

    def create_logo(self):
        """
        Create icon file from Base64 raw code.

        This will be used only for Windows OS.

        Other OS like Linux and macOS use default logo of Tkinter.

        Examples
        --------
        >>> if self.octadist_icon is True:
        >>>     self.create_logo()
        >>> else:
        >>>     pass

        """
        if platform.system() == "Windows":
            icon_data = base64.b64decode(Icon_Base64.icon_base64)
            temp_file = "icon.ico"
            save_path = os.path.expanduser("~/AppData/Local/Temp")
            self.octadist_icon = os.path.join(save_path, temp_file)
            icon_file = open(self.octadist_icon, "wb")
            icon_file.write(icon_data)
            icon_file.close()
            self.master.wm_iconbitmap(self.octadist_icon)

    def start_master(self):
        """
        Start application with UI settings.

        """
        self.master.title(f"OctaDist {octadist.__version__}")
        font = "Arial 10"
        self.master.option_add("*Font", font)
        center_width = (self.master.winfo_screenwidth() / 2.0) - (550 / 2.0)
        center_height = (self.master.winfo_screenheight() / 2.0) - (750 / 2.0)
        self.master.geometry("525x635+%d+%d" % (center_width, center_height))
        self.master.resizable(0, 0)

    def add_menu(self):
        """
        Add menu bar to master windows.

        """
        # Main menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(self.master, tearoff=0)
        edit_menu = tk.Menu(self.master, tearoff=0)
        disp_menu = tk.Menu(self.master, tearoff=0)
        tools_menu = tk.Menu(self.master, tearoff=0)
        help_menu = tk.Menu(self.master, tearoff=0)

        # Sub-menu
        copy_menu = tk.Menu(self.master, tearoff=0)
        data_menu = tk.Menu(self.master, tearoff=0)
        strct_menu = tk.Menu(self.master, tearoff=0)

        # File
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.clear_cache())
        file_menu.add_command(label="Open...", command=lambda: self.open_file())
        file_menu.add_command(label="Save Results", command=lambda: self.save_results())
        file_menu.add_command(label="Save Coordinates", command=lambda: self.save_coord())
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=lambda: self.settings())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: self.master.destroy())

        # Edit
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_cascade(label="Copy... to clipboard", menu=copy_menu)
        copy_menu.add_command(label="File Name", command=lambda: self.copy_name())
        copy_menu.add_command(label="File Path", command=lambda: self.copy_path())
        copy_menu.add_command(label="Computed Distortion Parameters", command=lambda: self.copy_results())
        copy_menu.add_command(label="Coordinates of Octahedral Structure", command=lambda: self.copy_octa())
        edit_menu.add_separator()
        edit_menu.add_command(label="Edit File", command=lambda: self.edit_file())
        edit_menu.add_command(label="Run Scripting Console", command=lambda: self.scripting_console())
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All Results", command=lambda: self.clear_cache())

        # Display
        menu_bar.add_cascade(label="Display", menu=disp_menu)
        disp_menu.add_command(label="Complex", command=lambda: self.draw_all_atom())
        disp_menu.add_command(label="Complex and Eight Faces", command=lambda: self.draw_all_atom_and_face())
        disp_menu.add_separator()
        disp_menu.add_command(label="Octahedron", command=lambda: self.draw_octa())
        disp_menu.add_command(label="Octahedron and Eight Faces", command=lambda: self.draw_octa_and_face())
        disp_menu.add_separator()
        disp_menu.add_command(label="Projection Planes", command=lambda: self.draw_projection())
        disp_menu.add_command(label="Twisting Triangular Faces", command=lambda: self.draw_twisting_plane())

        # Tools
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_cascade(label="Data Summary", command=lambda: self.show_data_complex())
        tools_menu.add_cascade(label="Show Structural Parameter", command=lambda: self.show_param_octa())
        tools_menu.add_command(label="Calculate Surface Area", command=lambda: self.show_surface_area())
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Relationship Plot between ζ and Σ", command=lambda: self.plot_zeta_sigma()
        )
        tools_menu.add_command(
            label="Relationship Plot between Σ and Θ", command=lambda: self.plot_sigma_theta()
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Calculate Jahn-Teller Distortion", command=lambda: self.tool_jahn_teller()
        )
        tools_menu.add_command(label="Calculate RMSD", command=lambda: self.tool_rmsd())

        # Help
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(
            label="User Documentation", command=lambda: webbrowser.open_new_tab(octadist.__help__)
        )
        example_mol = "https://github.com/OctaDist/OctaDist/tree/master/example-input"
        help_menu.add_command(label="Example molecules", command=lambda: webbrowser.open_new_tab(example_mol))
        help_menu.add_separator()
        submit_issue = "https://github.com/OctaDist/OctaDist/issues"
        help_menu.add_command(label="Report Issue", command=lambda: webbrowser.open_new_tab(submit_issue))
        help_menu.add_command(
            label="Github Repository", command=lambda: webbrowser.open_new_tab(octadist.__github__)
        )
        help_menu.add_command(label="Homepage", command=lambda: webbrowser.open_new_tab(octadist.__website__))
        help_menu.add_separator()
        help_menu.add_command(label="License", command=lambda: self.show_license())
        help_menu.add_separator()
        help_menu.add_command(label="Check for Updates...", command=self.check_update)
        help_menu.add_command(label="About Program", command=lambda: self.show_about())

    def add_widgets(self):
        """
        Add all widgets and components to master windows.

        GUI style of widgets in master windows use ttk style.

        """
        # my personal ttk style #
        gui_ttk = ttk.Style()
        gui_ttk.configure("TButton", relief="sunken", padding=5)
        gui_ttk.configure("My.TLabel", foreground="black")
        gui_ttk.configure("My.TLabelframe", foreground="brown")

        ###########
        # Frame 1 #
        ###########

        frame1 = tk.Frame(self.master)
        frame1.grid(padx=5, pady=5, row=0, column=0, columnspan=2)

        title = octadist.__title__
        lbl = tk.Label(frame1, text=title)
        lbl.configure(foreground="blue", font=("Arial", 16, "bold"))
        lbl.grid(pady="5", row=0, columnspan=4)

        description = octadist.__description__
        lbl = tk.Label(frame1, text=description)
        lbl.grid(pady="5", row=1, columnspan=4)

        ###########
        # Frame 2 #
        ###########

        frame2 = tk.LabelFrame(self.master, text="Program Console")
        frame2.grid(padx=5, pady=5, ipadx=2, ipady=2, sticky=tk.N, row=1, column=0)

        btn = ttk.Button(frame2, text="Browse file", command=self.open_file)
        btn.config(width=14)
        btn.grid(padx="10", pady="5", row=0)

        btn = ttk.Button(frame2, text="Compute", command=self.calc_distortion)
        btn.config(width=14)
        btn.grid(padx="10", pady="5", row=1)

        btn = ttk.Button(frame2, text="Clear cache", command=self.clear_cache)
        btn.config(width=14)
        btn.grid(padx="10", pady="5", row=2)

        btn = ttk.Button(frame2, text="Save Results", command=self.save_results)
        btn.config(width=14)
        btn.grid(padx="10", pady="5", row=3)

        ###########
        # Frame 3 #
        ###########

        frame3 = tk.LabelFrame(self.master, text="Distortion Parameters")
        frame3.grid(padx=5, pady=5, ipadx=3, ipady=2, sticky=tk.N, row=1, column=1)

        # D_mean
        lbl = tk.Label(frame3, text="<D>   =   ")
        lbl.grid(sticky=tk.E, pady="5", row=0, column=0)

        self.box_d_mean = tk.Entry(frame3)
        self.box_d_mean.configure(width="12", justify="center")
        self.box_d_mean.grid(row=0, column=1)

        lbl = tk.Label(frame3, text="  Angstrom")
        lbl.grid(pady="5", row=0, column=2)

        # Zeta
        lbl = tk.Label(frame3, text="ζ   =   ")
        lbl.grid(sticky=tk.E, pady="5", row=1, column=0)

        self.box_zeta = tk.Entry(frame3)
        self.box_zeta.configure(width="12", justify="center")
        self.box_zeta.grid(row=1, column=1)

        lbl = tk.Label(frame3, text="  Angstrom")
        lbl.grid(pady="5", row=1, column=2)

        # Delta
        lbl_delta = tk.Label(frame3, text="Δ   =   ")
        lbl_delta.grid(sticky=tk.E, pady="5", row=2, column=0)

        self.box_delta = tk.Entry(frame3)
        self.box_delta.configure(width="12", justify="center")
        self.box_delta.grid(row=2, column=1)

        # Sigma
        lbl = tk.Label(frame3, text="Σ   =   ")
        lbl.grid(sticky=tk.E, pady="5", row=3, column=0)

        self.box_sigma = tk.Entry(frame3)
        self.box_sigma.configure(width="12", justify="center")
        self.box_sigma.grid(row=3, column=1)

        lbl = tk.Label(frame3, text="  degree")
        lbl.grid(pady="5", row=3, column=2)

        # Theta_mean
        lbl = tk.Label(frame3, text="Θ   =   ")
        lbl.grid(sticky=tk.E, pady="5", row=4, column=0)

        self.box_theta_mean = tk.Entry(frame3)
        self.box_theta_mean.configure(width="12", justify="center")
        self.box_theta_mean.grid(row=4, column=1)

        lbl = tk.Label(frame3, text="  degree")
        lbl.grid(pady="5", row=4, column=2)

        ###########
        # Frame 4 #
        ###########

        frame4 = tk.Frame(self.master)
        frame4.grid(padx=5, pady=10, row=2, column=0, columnspan=2)

        self.box_result = tkscrolled.ScrolledText(frame4)
        self.box_result.configure(height="19", width="70", wrap="word", undo="True")
        self.box_result.grid(row=0)

    def show_text(self, text):
        """
        Insert text to result box

        Parameters
        ----------
        text : str
            Text to show in result box.

        Returns
        -------
        None : None

        """
        self.box_result.insert(tk.INSERT, text + "\n")
        self.box_result.see(tk.END)

    def welcome_msg(self):
        """
        Show welcome message in result box:

        1. Program name, version, and release.
        2. Full author names.
        3. Official website: https://octadist.github.io.

        """
        full_version = octadist.__version__ + " " + f"({octadist.__release__})"

        self.show_text(f"Welcome to OctaDist version {full_version}\n")
        self.show_text(f"Developed by {octadist.__author_full__}.\n")
        self.show_text(octadist.__website__ + "\n")

    #####################
    # Manipulating File #
    #####################

    def open_file(self):
        """
        Open file dialog where the user will browse input files.

        """
        self.clear_cache()

        input_file = filedialog.askopenfilenames(
            title="Choose input file",
            filetypes=(
                ("All Files", "*.*"),
                ("CIF File", "*.cif"),
                ("XYZ File", "*.xyz"),
                ("Gaussian Output File", "*.out"),
                ("Gaussian Output File", "*.log"),
                ("NWChem Output File", "*.out"),
                ("NWChem Output File", "*.log"),
                ("ORCA Output File", "*.out"),
                ("ORCA Output File", "*.log"),
                ("Q-Chem Output File", "*.out"),
                ("Q-Chem Output File", "*.log"),
            ),
        )

        self.file_list = list(input_file)
        self.search_coord()

    def search_coord(self):
        """
        Search and extract atomic symbols and coordinates from input file.

        See Also
        --------
        octadist.src.io.extract_coord :
            Extract atomic symbols and atomic coordinates from input file.
        octadist.src.io.extract_octa :
            Extract octahedral structure from complex.

        """
        try:
            open(self.file_list[0], "r")
        except IndexError:
            return 1

        for i in range(len(self.file_list)):

            ########################################
            # Extract atomic coordinates from file #
            ########################################

            atom_full, coord_full = io.extract_coord(self.file_list[i])
            self.atom_coord_full.append([atom_full, coord_full])

            # If either lists is empty, then continue to next file
            if len(list(atom_full)) == 0 or len(coord_full) == 0:
                continue

            #################################################
            # Extract octahedral structure from the complex #
            #################################################

            atom_metal, coord_metal, index_metal = io.find_metal(atom_full, coord_full)

            if len(atom_metal) == 0:
                popup.warn_no_metal(i + 1)

            # loop over the number of metal atoms found in the complex
            for j in range(len(atom_metal)):
                atom_octa, coord_octa = io.extract_octa(
                    atom_full, coord_full, index_metal[j], self.cutoff_metal_ligand
                )

                # If no atomic coordinates inside, raise error
                if np.any(coord_octa) == 0:
                    popup.err_no_coord(i + 1)
                    continue

                if len(coord_octa) < 7:
                    self.clear_result_box()
                    popup.err_less_ligands(i + 1)
                    continue

                # File number and file name
                file_name = self.file_list[i].split("/")[-1]
                self.file_name.append([i + 1, file_name])

                # Metal center atom
                self.octa_index.append(atom_octa[0])

                # Atomic labels and atomic coordinates
                # Example:
                #
                # atom = ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
                # coord = [[2.298354, 5.161785, 7.971898],
                #          [1.885657, 4.804777, 6.183726],
                #          [1.747515, 6.960963, 7.932784],
                #          [4.094380, 5.807257, 7.588689],
                #          [0.539005, 4.482809, 8.460004],
                #          [2.812425, 3.266553, 8.131637],
                #          [2.886404, 5.392925, 9.848966]]

                self.atom_coord_octa.append([atom_octa, coord_octa])

        self.show_coord()

    def show_coord(self):
        """
        Show coordinates in box.

        """
        # loop over complex
        for i in range(len(self.atom_coord_octa)):
            if i == 0:
                self.show_text("XYZ coordinates of extracted octahedral structure")

            self.show_text(f"File {self.file_name[i][0]}: {self.file_name[i][1]}")
            self.show_text(f"Metal center atom: {self.octa_index[i]}")
            self.show_text("Atom\t\tCartesian coordinate")

            # loop over atoms in octahedron
            for k in range(7):
                self.show_text(
                    " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}".format(
                        self.atom_coord_octa[i][0][k],
                        self.atom_coord_octa[i][1][k][0],
                        self.atom_coord_octa[i][1][k][1],
                        self.atom_coord_octa[i][1][k][2],
                    )
                )
            self.show_text("")

    def save_results(self):
        """
        Save results as output file. Default file extension is .txt.

        """
        f = filedialog.asksaveasfile(
            mode="w",
            defaultextension=".txt",
            title="Save results",
            filetypes=(("TXT File", "*.txt"), ("All Files", "*.*")),
        )

        f.write(f"{octadist.__copyright__}\n")
        f.write("=" * 60 + "\n")
        f.write("\n")
        f.write(f"OctaDist version {octadist.__version__} ({octadist.__release__})\n")
        f.write("Octahedral Distortion Calculator\n")
        f.write(f"{octadist.__website__}\n")
        today = datetime.now().strftime("%b-%d-%y %H:%M:%S")
        f.write(f"{today}\n")
        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("\n")
        get_result = self.box_result.get("1.0", tk.END + "-1c")
        f.write(get_result)
        f.write("\n")
        f.write("=" * 60 + "\n")
        f.close()

        popup.info_save_results(f.name)

    def save_coord(self):
        """
        Save atomic coordinates (Cartesian coordinate) of octahedral structure.
        Default file extension is .xyz.

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        if len(self.file_list) > 1:
            popup.err_many_files()
            return 1

        f = filedialog.asksaveasfile(
            mode="w",
            defaultextension=".xyz",
            title="Save atomic coordinates",
            filetypes=(("XYZ File", "*.xyz"), ("TXT File", "*.txt"), ("All Files", "*.*")),
        )

        file_name = self.file_list[0].split("/")[-1]
        atoms = self.atom_coord_octa[0][0]
        coord = self.atom_coord_octa[0][1]
        num_atom = 7

        f.write(f"{num_atom}\n")
        full_version = octadist.__version__ + " " + f"({octadist.__release__})"
        f.write(f"{file_name} : this file was generated by OctaDist version {full_version}.\n")
        for i in range(num_atom):
            f.write(
                "{0:2s}\t{1:9.6f}\t{2:9.6f}\t{3:9.6f}\n".format(
                    atoms[i], coord[i][0], coord[i][1], coord[i][2]
                )
            )
        f.write("\n")
        f.close()

        popup.info_save_results(f.name)

    ###################################
    # Calculate distortion parameters #
    ###################################

    def calc_distortion(self):
        """
        Calculate all distortion parameters:

        - D_mean
        - Zeta
        - Delta
        - Sigma
        - Theta

        See Also
        --------
        octadist.src.calc.CalcDistortion.calc_d_mean :
            Calculate mean metal-ligand bond length.
        octadist.src.calc.CalcDistortion.calc_zeta :
            Calculate Zeta parameter.
        octadist.src.calc.CalcDistortion.calc_delta :
            Calculate Delta parameter.
        octadist.src.calc.CalcDistortion.calc_sigma :
            Calculate Sigma parameter.
        octadist.src.calc.CalcDistortion.calc_theta :
            Calculate Theta parameter.

        """
        if len(self.atom_coord_octa) >= 1:
            self.clear_param_box()
        else:
            popup.err_no_file()
            return 1

        # if comp_result is not empty, clean it to avoid over loop.
        if self.comp_result:
            self.comp_result = []

        # loop over number of metal complexes
        for i in range(len(self.atom_coord_octa)):
            atom_octa, coord_octa = self.atom_coord_octa[i]

            # Calculate distortion parameters
            calc_dist = calc.CalcDistortion(coord_octa)

            d_mean = calc_dist.d_mean
            zeta = calc_dist.zeta
            delta = calc_dist.delta
            sigma = calc_dist.sigma
            theta = calc_dist.theta
            non_octa = calc_dist.non_octa

            if non_octa:
                popup.warn_not_octa()

            # Collect results
            self.all_zeta.append(zeta)
            self.all_delta.append(delta)
            self.all_sigma.append(sigma)
            self.all_theta.append(theta)

            self.comp_result.append([d_mean, zeta, delta, sigma, theta])

        # Print results to each unique box.

        if len(self.atom_coord_octa) == 1:
            d_mean, zeta, delta, sigma, theta = self.comp_result[0]

            self.box_d_mean.insert(tk.INSERT, f"{d_mean:3.6f}")
            self.box_zeta.insert(tk.INSERT, f"{zeta:3.6f}")
            self.box_delta.insert(tk.INSERT, f"{delta:3.6f}")
            self.box_sigma.insert(tk.INSERT, f"{sigma:3.6f}")
            self.box_theta_mean.insert(tk.INSERT, f"{theta:3.6f}")
        else:
            self.box_d_mean.insert(tk.INSERT, "See below")
            self.box_zeta.insert(tk.INSERT, "See below")
            self.box_delta.insert(tk.INSERT, "See below")
            self.box_sigma.insert(tk.INSERT, "See below")
            self.box_theta_mean.insert(tk.INSERT, "See below")

        # Print results to result box
        self.show_text("Computed octahedral distortion parameters for all complexes\n")
        self.show_text("No. - Metal\t\tD_mean\tZeta\tDelta\tSigma\tTheta")
        self.show_text("*" * 71)
        for i in range(len(self.comp_result)):
            self.show_text(
                "{0:2d}  -  {1}\t\t{2:9.4f}\t{3:9.6f}\t{4:9.6f}\t{5:9.4f}\t{6:9.4f}".format(
                    i + 1,
                    self.octa_index[i],
                    self.comp_result[i][0],
                    self.comp_result[i][1],
                    self.comp_result[i][2],
                    self.comp_result[i][3],
                    self.comp_result[i][4],
                )
            )

    ###################
    # Program Setting #
    ###################

    def settings(self):
        """
        Program settings allows the user to configure the values of variables
        that used in molecular display function.

        For example, cutoff distance for screening bond distance between atoms.

        """

        def open_exe():
            """
            Program setting: Open dialog in which the user will choose text editor.

            """
            try:
                input_file = filedialog.askopenfilename(
                    title="Choose text editor executable", filetypes=[("EXE file", "*.exe")],
                )

                file_list = str(input_file)
                entry_exe.delete(0, tk.END)
                entry_exe.insert(tk.INSERT, file_list)

            except IndexError:
                return 1

        def is_show_title():
            """
            Check if title of figure will be set to show or not.

            """
            if var_title.get():
                var_title.set(True)
            else:
                var_title.set(False)

        def is_show_axis():
            """
            Check if axis of figure will be set to show or not.

            """
            if var_axis.get():
                var_axis.set(True)
            else:
                var_axis.set(False)

        def is_show_grid():
            """
            Check if grid of figure will be set to show or not.

            """
            if var_grid.get():
                var_grid.set(True)
            else:
                var_grid.set(False)

        def restore_settings(self):
            """
            Restore all settings.

            """
            self.cutoff_metal_ligand = self.backup_cutoff_metal_ligand
            self.cutoff_global = self.backup_cutoff_global
            self.cutoff_hydrogen = self.backup_cutoff_hydrogen
            self.text_editor = self.backup_text_editor
            self.visualizer = self.backup_visualizer
            self.show_title = self.backup_show_title
            self.show_axis = self.backup_show_axis
            self.show_grid = self.backup_show_grid

            var_1.set(self.cutoff_metal_ligand)
            var_2.set(self.cutoff_global)
            var_3.set(self.cutoff_hydrogen)
            var_title.set(self.show_title)
            var_axis.set(self.show_axis)
            var_grid.set(self.show_grid)

            entry_exe.delete(0, tk.END)
            entry_exe.insert(tk.INSERT, self.text_editor)

        def click_ok(self):
            """
            If the user click OK, it will save all settings and show info in output box.

            """
            self.cutoff_metal_ligand = float(var_1.get())
            self.cutoff_global = float(var_2.get())
            self.cutoff_hydrogen = float(var_3.get())
            self.text_editor = str(entry_exe.get())
            self.visualizer = str(var_vis.get())
            self.show_title = bool(var_title.get())
            self.show_axis = bool(var_axis.get())
            self.show_grid = bool(var_grid.get())

            self.show_text("Updated program settings")
            self.show_text("************************")
            self.show_text(f"Metal-ligand bond cutoff\t\t\t{self.cutoff_metal_ligand}")
            self.show_text(f"Global bond cutoff\t\t\t{self.cutoff_global}")
            self.show_text(f"Hydrogen bond cutoff\t\t\t{self.cutoff_hydrogen}")
            self.show_text(f"Text editor\t\t\t{self.text_editor}")
            self.show_text(f"Molecular visualizer\t\t\t{self.visualizer}")
            self.show_text(f"Show Title\t\t\t{self.show_title}")
            self.show_text(f"Show Axis\t\t\t{self.show_axis}")
            self.show_text(f"Show Grid\t\t\t{self.show_grid}\n")

            wd.destroy()

        def click_cancel():
            """
            If the user click CANCEL, close window.

            """
            wd.destroy()

        ###################
        # Setting: Widget #
        ###################

        wd = tk.Toplevel(self.master)
        if self.octadist_icon is not None:
            wd.wm_iconbitmap(self.octadist_icon)
        wd.title("Program settings")
        wd.option_add("*Font", "Arial 10")

        frame = tk.Frame(wd)
        frame.grid()

        ###################
        # Setting: Cutoff #
        ###################

        frame_cutoff = tk.LabelFrame(frame, text="Bond Cutoff:")
        frame_cutoff.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky="W", row=0, columnspan=4)

        label_1 = tk.Label(frame_cutoff, text="Metal-Ligand Bond")
        label_1.grid(padx="10", pady="5", ipadx="10", row=0, column=0)

        var_1 = tk.DoubleVar()
        var_1.set(self.cutoff_metal_ligand)

        scale_1 = tk.Scale(frame_cutoff, orient="horizontal", variable=var_1, to=5, resolution=0.1)
        scale_1.configure(width=20, length=100)
        scale_1.grid(padx="10", pady="5", ipadx="10", row=1, column=0)

        label_2 = tk.Label(frame_cutoff, text="Global Distance")
        label_2.grid(padx="10", pady="5", ipadx="10", row=0, column=1)

        var_2 = tk.DoubleVar()
        var_2.set(self.cutoff_global)

        scale_2 = tk.Scale(frame_cutoff, orient="horizontal", variable=var_2, to=5, resolution=0.1)
        scale_2.configure(width=20, length=100)
        scale_2.grid(padx="10", pady="5", ipadx="10", row=1, column=1)

        label_3 = tk.Label(frame_cutoff, text="Hydrogen Distance")
        label_3.grid(padx="10", pady="5", ipadx="10", row=0, column=2)

        var_3 = tk.DoubleVar()
        var_3.set(self.cutoff_hydrogen)

        scale_3 = tk.Scale(frame_cutoff, orient="horizontal", variable=var_3, to=5, resolution=0.1)
        scale_3.configure(width=20, length=100)
        scale_3.grid(padx="10", pady="5", ipadx="10", row=1, column=2)

        ########################
        # Setting: Text editor #
        ########################

        frame_text_editor = tk.LabelFrame(frame, text="Text editor:")
        frame_text_editor.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky="W", row=1, columnspan=4)

        label = tk.Label(frame_text_editor, text="Enter the EXE:")
        label.grid(padx="5", sticky=tk.E, row=0, column=0)

        entry_exe = tk.Entry(frame_text_editor, bd=2, width=60)
        entry_exe.grid(row=0, column=1)

        button = tk.Button(frame_text_editor, text="Browse...", command=open_exe)
        button.grid(padx="5", pady="5", sticky=tk.W, row=0, column=2)

        entry_exe.insert(tk.INSERT, self.text_editor)

        ########################
        # Setting : Visualizer #
        ########################

        frame_visualizer = tk.LabelFrame(frame, text="Visualizer:")
        frame_visualizer.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky="W", row=2)

        visualizers = ["Matplotlib", "Plotly"]
        var_vis = tk.StringVar()
        var_vis.set(self.visualizer)

        vis = ttk.Combobox(frame_visualizer, textvariable=var_vis, values=visualizers)
        vis.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky="W")

        ####################
        # Setting: Figures #
        ####################

        frame_figures = tk.LabelFrame(frame, text="Displays:")
        frame_figures.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky="W", row=3, columnspan=4)

        # Show title of plot?
        var_title = tk.BooleanVar()
        var_title.set(self.show_title)

        show_title = ttk.Checkbutton(
            frame_figures,
            text="Show Figure Title",
            onvalue=True,
            offvalue=False,
            variable=var_title,
            command=lambda: is_show_title(),
        )
        show_title.grid(padx="5", pady="5", ipadx="25", sticky=tk.E, row=0, column=0)

        # Show axis?
        var_axis = tk.BooleanVar()
        var_axis.set(self.show_axis)

        show_axis = ttk.Checkbutton(
            frame_figures,
            text="Show Axis",
            onvalue=True,
            offvalue=False,
            variable=var_axis,
            command=lambda: is_show_axis(),
        )
        show_axis.grid(padx="5", pady="5", ipadx="25", sticky=tk.E, row=0, column=1)

        # Show grid?
        var_grid = tk.BooleanVar()
        var_grid.set(self.show_grid)

        show_grid = ttk.Checkbutton(
            frame_figures,
            text="Show Gridlines",
            onvalue=True,
            offvalue=False,
            variable=var_grid,
            command=lambda: is_show_grid(),
        )
        show_grid.grid(padx="5", pady="5", ipadx="5", sticky=tk.E, row=0, column=2)

        ####################
        # Setting: Console #
        ####################

        button = tk.Button(frame, text="Restore settings", command=lambda: restore_settings(self))
        button.configure(width=15)
        button.grid(padx="10", pady="10", sticky=tk.W, row=4, column=0)

        button = tk.Button(frame, text="OK", command=lambda: click_ok(self))
        button.configure(width=15)
        button.grid(padx="5", pady="10", sticky=tk.E, row=4, column=2)

        button = tk.Button(frame, text="Cancel", command=lambda: click_cancel())
        button.configure(width=15)
        button.grid(padx="5", pady="10", row=4, column=3)

        frame.mainloop()

    #################
    # Copy and Edit #
    #################

    def copy_name(self):
        """
        Copy input file name to clipboard.

        See Also
        --------
        copy_path :
            Copy absolute path of input file to clibboard.
        copy_results :
            Copy results to clibboard.
        copy_octa :
            Copy octahedral structure coordinates to clibboard.

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        name = self.file_list[0].split("/")[-1]

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(name)
        clip.destroy()

    def copy_path(self):
        """
        Copy absolute path of input file to clipboard.

        See Also
        --------
        copy_name
            Copy input file name to clibboard.
        copy_results :
            Copy results to clibboard.
        copy_octa :
            Copy octahedral structure coordinates to clibboard.

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(self.file_list[0])
        clip.destroy()

    def copy_results(self):
        """
        Copy the results and computed distortion parameters to clipboard.

        See Also
        --------
        copy_name
            Copy input file name to clibboard.
        copy_path :
            Copy absolute path of input file to clibboard.
        copy_octa :
            Copy octahedral structure coordinates to clibboard.

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        if len(self.all_zeta) == 0:
            popup.err_no_calc()
            return 1

        results = "Zeta, Delta, Sigma, Gamma\n" "{0:3.6f}, {1:3.6f}, {2:3.6f}, {3:3.6f}".format(
            self.all_zeta[0], self.all_delta[0], self.all_sigma[0], self.all_theta[0],
        )

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(results)
        clip.destroy()

    def copy_octa(self):
        """
        Copy atomic coordinates of octahedral structure to clipboard.

        See Also
        --------
        copy_name
            Copy input file name to clibboard.
        copy_path :
            Copy absolute path of input file to clibboard.
        copy_results :
            Copy results to clibboard.

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(self.atom_coord_octa[0][2])
        clip.destroy()

    def edit_file(self):
        """
        Edit file by specified text editor on Windows.

        See Also
        --------
        settings

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        if self.text_editor == "":
            popup.err_no_editor()
            return 1

        try:
            for i in range(len(self.file_list)):
                program_name = self.text_editor
                file_name = self.file_list[i]
                subprocess.Popen([program_name, file_name])

        except FileNotFoundError:
            return 1

    #########################
    # Interactive scripting #
    #########################

    def scripting_console(self):
        """
        Start scripting interface for an interactive code.

        User can access to class variable (dynamic variable).

        +------------+
        | Output box |
        +------------+
        | Input box  |
        +------------+

        See Also
        --------
        settings :
            Program settings.

        """
        my_app = scripting.ScriptingConsole(self)
        my_app.scripting_start()

    ##################
    # Visualizations #
    ##################

    def draw_all_atom(self):
        """
        Display 3D complex.

        See Also
        --------
        octadist.src.draw.DrawComplex :
            Show 3D molecule.

        """
        if len(self.atom_coord_full) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_full) > 1:
            popup.err_many_files()
            return 1

        atom_full, coord_full = self.atom_coord_full[0]

        if self.visualizer == "Matplotlib":
            my_plot = draw.DrawComplex_Matplotlib(
                atom=atom_full,
                coord=coord_full,
                cutoff_global=self.cutoff_global,
                cutoff_hydrogen=self.cutoff_hydrogen,
            )
            my_plot.add_atom()
            my_plot.add_bond()
            my_plot.add_legend()
            my_plot.config_plot(
                show_title=self.show_title, show_axis=self.show_axis, show_grid=self.show_grid,
            )
            my_plot.show_plot()

        elif self.visualizer == "Plotly":
            my_plot = draw.DrawComplex_Plotly(
                atom=atom_full,
                coord=coord_full,
                cutoff_global=self.cutoff_global,
                cutoff_hydrogen=self.cutoff_hydrogen,
            )
            my_plot.add_atom()
            my_plot.add_bond()
            my_plot.show_plot()
        else:
            popup.err_visualizer_not_found()

    def draw_all_atom_and_face(self):
        """
        Display 3D complex with the faces.

        See Also
        --------
        octadist.src.draw.DrawComplex :
            Show 3D molecule.

        """
        if len(self.atom_coord_full) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_full) > 1:
            popup.err_many_files()
            return 1

        atom_full, coord_full = self.atom_coord_full[0]

        my_plot = draw.DrawComplex_Matplotlib(
            atom=atom_full,
            coord=coord_full,
            cutoff_global=self.cutoff_global,
            cutoff_hydrogen=self.cutoff_hydrogen,
        )
        my_plot.add_atom()
        my_plot.add_bond()

        for i in range(len(self.atom_coord_octa)):
            _, coord_octa = self.atom_coord_octa[i]
            my_plot.add_face(coord_octa)

        my_plot.add_legend()
        my_plot.config_plot(
            show_title=self.show_title, show_axis=self.show_axis, show_grid=self.show_grid,
        )
        my_plot.show_plot()

    def draw_octa(self):
        """
        Display 3D octahedral structure.

        See Also
        --------
        octadist.src.draw.DrawComplex :
            Show 3D molecule.

        """
        if len(self.atom_coord_octa) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_octa) > 1:
            popup.err_many_files()
            return 1

        atom_octa, coord_octa = self.atom_coord_octa[0]

        my_plot = draw.DrawComplex_Matplotlib(
            atom=atom_octa,
            coord=coord_octa,
            cutoff_global=self.cutoff_global,
            cutoff_hydrogen=self.cutoff_hydrogen,
        )
        my_plot.add_atom()
        my_plot.add_bond()
        my_plot.add_legend()
        my_plot.config_plot(
            show_title=self.show_title, show_axis=self.show_axis, show_grid=self.show_grid,
        )
        my_plot.show_plot()

    def draw_octa_and_face(self):
        """
        Display 3D octahedral structure with the faces.

        See Also
        --------
        octadist.src.draw.DrawComplex :
            Show 3D molecule.

        """
        if len(self.atom_coord_octa) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_octa) > 1:
            popup.err_many_files()
            return 1

        atom_octa, coord_octa = self.atom_coord_octa[0]

        my_plot = draw.DrawComplex_Matplotlib(
            atom=atom_octa,
            coord=coord_octa,
            cutoff_global=self.cutoff_global,
            cutoff_hydrogen=self.cutoff_hydrogen,
        )
        my_plot.add_atom()
        my_plot.add_bond()
        my_plot.add_legend()

        for i in range(len(self.atom_coord_octa)):
            _, coord = self.atom_coord_octa[i]
            my_plot.add_face(coord)

        my_plot.config_plot(
            show_title=self.show_title, show_axis=self.show_axis, show_grid=self.show_grid,
        )
        my_plot.show_plot()

    def draw_projection(self):
        """
        Draw projection planes.

        See Also
        --------
        octadist.src.draw.DrawProjection :
            Show graphical projections.

        """
        if len(self.atom_coord_full) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_full) > 1:
            popup.err_many_files()
            return 1

        atom_full, coord_full = self.atom_coord_full[0]

        my_plot = draw.DrawProjection(atom=atom_full, coord=coord_full)
        my_plot.add_atom()
        my_plot.add_symbol()
        my_plot.add_plane()
        my_plot.show_plot()

    def draw_twisting_plane(self):
        """
        Draw twisting triangular planes.

        See Also
        --------
        octadist.src.draw.DrawTwistingPlane :
            Show graphical triangular twisting planes.

        """
        if len(self.atom_coord_full) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_full) > 1:
            popup.err_many_files()
            return 1

        atom_full, coord_full = self.atom_coord_full[0]

        my_plot = draw.DrawTwistingPlane(atom=atom_full, coord=coord_full)
        my_plot.add_plane()
        my_plot.add_symbol()
        my_plot.add_bond()
        my_plot.show_plot()

    #####################
    # Show data summary #
    #####################

    def show_data_complex(self):
        """
        Show info of input complex.

        See Also
        --------
        octadist.src.structure.DataComplex :
            Show data summary of complex.

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        my_app = structure.DataComplex(master=self.master, icon=self.octadist_icon)

        for i in range(len(self.file_list)):
            atom = self.atom_coord_full[i][0]
            coord = self.atom_coord_full[i][1]
            my_app.add_name(self.file_list[i])
            my_app.add_coord(atom, coord)

    def show_param_octa(self):
        """
        Show structural parameters of selected octahedral structure.

        See Also
        --------
        octadist.src.structure.StructParam :
            Show structural parameter symmary of complex.

        """
        if len(self.atom_coord_octa) == 0:
            popup.err_no_file()
            return 1

        my_app = structure.StructParam(master=self.master, icon=self.octadist_icon)

        for i in range(len(self.atom_coord_octa)):
            metal = self.octa_index[i]
            atom, coord = self.atom_coord_octa[i]
            my_app.add_metal(metal)
            my_app.add_coord(atom, coord)

    def show_surface_area(self):
        """
        Calculate the area of eight triangular faces of octahedral structure.

        See Also
        --------
        octadist.src.structure.SurfaceArea :
            Show the area of the faces of octahedral structure.

        """
        if len(self.atom_coord_octa) == 0:
            popup.err_no_file()
            return 1

        my_app = structure.SurfaceArea(master=self.master, icon=self.octadist_icon)

        for i in range(len(self.atom_coord_octa)):
            metal = self.octa_index[i]
            atom, coord = self.atom_coord_octa[i]
            my_app.add_metal(metal)
            my_app.add_octa(coord)

    ##############################
    # Plot between two data sets #
    ##############################

    def plot_zeta_sigma(self):
        """
        Plot relationship between zeta and sigma.

        See Also
        --------
        octadist.src.plot.Plot :
            Show relationship plot.

        """
        if len(self.all_sigma) == 0:
            popup.err_no_calc()
            return 1

        my_plot = plot.Plot(self.all_zeta, self.all_sigma, name1="zeta", name2="sigma")
        my_plot.add_point()
        my_plot.add_text()
        my_plot.add_legend()
        my_plot.show_plot()

    def plot_sigma_theta(self):
        """
        Plot relationship between sigma and theta.

        See Also
        --------
        octadist.src.plot.Plot :
            Show relationship plot.

        """
        if len(self.all_sigma) == 0:
            popup.err_no_calc()
            return 1

        my_plot = plot.Plot(self.all_sigma, self.all_theta, name1="sigma", name2="theta")
        my_plot.add_point()
        my_plot.add_text()
        my_plot.add_legend()
        my_plot.show_plot()

    ##################
    # Analysis tools #
    ##################

    def tool_jahn_teller(self):
        """
        Calculate Jahn-Teller distortion parameter.

        See Also
        --------
        octadist.src.tools.CalcJahnTeller :
            Calculate Jahn-Teller distortion parameter.

        """
        if len(self.atom_coord_full) == 0:
            popup.err_no_file()
            return 1
        elif len(self.atom_coord_full) > 1:
            popup.err_many_files()
            return 1

        atom_full, coord_full = self.atom_coord_full[0]

        run_jt = tools.CalcJahnTeller(
            atom=atom_full,
            coord=coord_full,
            cutoff_global=self.cutoff_global,
            cutoff_hydrogen=self.cutoff_hydrogen,
            master=self.master,
            icon=self.octadist_icon,
        )
        run_jt.start_app()
        run_jt.find_bond()
        run_jt.show_app()

    def tool_rmsd(self):
        """
        Calculate root mean squared displacement of atoms in complex, RMSD.

        See Also
        --------
        octadist.src.tools.CalcRMSD :
            Calculate RMSD.

        """
        if len(self.atom_coord_full) != 2:
            popup.err_only_2_files()
            return 1

        complex_1 = self.atom_coord_full[0]
        complex_2 = self.atom_coord_full[1]

        atom_complex_1, coord_complex_1 = complex_1
        atom_complex_2, coord_complex_2 = complex_2

        # Check if two complexes are consistent
        if len(atom_complex_1) != len(atom_complex_2):
            popup.err_not_equal_atom()
            return 1

        for i in range(len(atom_complex_1)):
            if atom_complex_1[i] != atom_complex_2[i]:
                popup.err_atom_not_match(i + 1)
                return 1

        run_rmsd = tools.CalcRMSD(
            coord_complex_1,
            coord_complex_2,
            atom_1=atom_complex_1,
            atom_2=atom_complex_2,
            master=self.master,
            icon=self.octadist_icon,
        )

        run_rmsd.start_app()
        run_rmsd.show_app()

    ################
    # Check Update #
    ################

    @staticmethod
    def check_update():
        """
        Check program update by comparing version of program user is using with
        that of the latest version released on github.

        References
        ----------
        File: https://www.github.com/OctaDist/OctaDist/version_update.txt.

        """
        data = urlopen("https://raw.githubusercontent.com/OctaDist/OctaDist/master/version_update.txt").read()
        # decode
        data = data.decode("utf-8")
        data = data.split()

        user_rev = float(octadist.__revision__)
        server_ver = data[1]
        server_rev = float(data[3])  # code version

        os_name = platform.system()  # find the OS name

        if server_rev > user_rev:
            popup.info_new_update()

            text = f"A new version {server_ver} is ready for download.\n\n" "Do you want to download now?"
            msg_box = messagebox.askquestion("Updates available", text, icon="warning")

            if msg_box == "yes":
                dl_link = "https://github.com/OctaDist/OctaDist/releases/download/"
                main_link = dl_link + "v." + server_ver + "/OctaDist-" + server_ver
                if os_name == "Windows":
                    link_windows = main_link + "-Win-x86-64.exe"
                    webbrowser.open_new_tab(link_windows)
                elif os_name == "Darwin" or os_name == "Linux":
                    link_linux = main_link + "-src-x86-64.tar.gz"
                    webbrowser.open_new_tab(link_linux)
                else:
                    popup.err_cannot_update()

                # Open Thank You page at the same time download the program
                webbrowser.open_new_tab("https://octadist.github.io/thanks.html")
            else:
                pass
        elif server_rev < user_rev:
            popup.info_using_dev()
        else:
            popup.info_no_update()

    #####################
    # Show program info #
    #####################

    @staticmethod
    def callback(event):
        """
        On-clink open web browser.

        Parameters
        ----------
        event : object
            Event object for callback.

        """
        webbrowser.open_new(event.widget.cget("text"))

    @staticmethod
    def show_about():
        """
        Show author details on a sub-window.

        1. Name of authors
        2. Official program website
        3. Citation

        """
        text = (
            f"OctaDist version {octadist.__version__} ({octadist.__release__})\n\n"
            f"Authors: {octadist.__author_full__}.\n\n"
            f"Website: {octadist.__website__}\n\n"
            f"Please cite this project if you use OctaDist for scientific publication:\n\n"
            "Ketkaew, R.; Tantirungrotechai, Y.; Harding, P.; Chastanet, G.; Guionneau, P.; Marchivie, M.; Harding, D. J.\n"
            "OctaDist: A Tool for Calculating Distortion Parameters in Spin Crossover and Coordination Complexes. "
            "Dalton Trans. 2021. \nhttps://doi.org/10.1039/D0DT03988H"
        )

        showinfo("About program", text)

    @staticmethod
    def show_license():
        """
        Show license details on a sub-window.

        GNU General Public License version 3.0.

        References
        ----------
        Link: https://www.gnu.org/licenses/gpl-3.0.en.html.

        """
        text = """\
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.

This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version.

This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details.

You should have received a copy of the GNU General Public License \
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

        showinfo("License", text)

    ###################
    # Clear All Cache #
    ###################

    def clear_cache(self):
        """
        Clear program cache by nullifying all default variables
        and clear both of parameter and result boxes.

        """
        for name in dir():
            if not name.startswith("_"):
                del locals()[name]

        self.file_list = []
        self.file_name = []
        self.octa_index = []
        self.atom_coord_full = []
        self.atom_coord_octa = []
        self.all_zeta = []
        self.all_delta = []
        self.all_sigma = []
        self.all_theta = []
        self.comp_result = []

        self.clear_param_box()
        self.clear_result_box()

    def clear_param_box(self):
        """
        Clear parameter box.

        """
        self.box_delta.delete(0, tk.END)
        self.box_sigma.delete(0, tk.END)
        self.box_d_mean.delete(0, tk.END)
        self.box_zeta.delete(0, tk.END)
        self.box_theta_mean.delete(0, tk.END)

    def clear_result_box(self):
        """
        Clear result box.

        """
        self.box_result.delete(1.0, tk.END)

    def start_app(self):
        """
        Start application.

        """
        self.master.mainloop()


def main():
    app = OctaDist()
    app.start_app()

    # Delete icon after closing app
    if app.octadist_icon is not None:
        os.remove(app.octadist_icon)


if __name__ == "__main__":
    main()
