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

import platform
import subprocess
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import webbrowser
from tkinter import filedialog
from tkinter import messagebox
from urllib.request import urlopen

import numpy as np

import octadist_gui
import octadist_gui.src.draw
from octadist_gui.src import (
    echo_outs, calc, coord, draw, plot, popup, tools, util
)


class OctaDist:
    def __init__(self, master):
        """
        Program interface is structured as below:

        +-------------------+
        +   Program menu    +
        +-------------------+
        +     Frame 1       +
        +-------------------+
        + Frame 2 + Frame 3 +
        +-------------------+
        +     Frame 4       +
        +-------------------+

        Parameters
        ----------
        master
            Master frame of program GUI.

        Returns
        -------
        None

        Notes
        -----
        Initialize default parameters.

        file_list : list of str
            Input files
        atom_coord_full : array
            Atomic labels and coordinates of metal complex.
        atom_coord_octa : array
            Atomic labels and coordinates of octahedral structures.
        all_zeta : list of float
            Computed zeta of all octahedral structures.
        all_delta : list of float
            Computed delta of all octahedral structures.
        all_sigma : list of float
            Computed sigma of all octahedral structures.
        all_theta : list of float
            Computed theta of all octahedral structures.
        all_face : list of str
            Atomic labels and coordinates of 8 faces and their opposite faces.
        check_metal : bool
            True if the structure is octahedron or not, False if it does not.

        """
        # Default settings
        self.file_list = []
        self.atom_coord_full = []
        self.atom_coord_octa = []
        self.all_zeta = []
        self.all_delta = []
        self.all_sigma = []
        self.all_theta = []
        self.all_face = []
        self.check_metal = True

        # Default cutoff values
        self.cutoff_metal_ligand = 2.8
        self.cutoff_global = 2.0
        self.cutoff_hydrogen = 1.2

        # Default executable
        self.text_editor = "notepad.exe"

        # Backup default setting values
        self.backup_1 = self.cutoff_metal_ligand
        self.backup_2 = self.cutoff_global
        self.backup_3 = self.cutoff_hydrogen
        self.backup_4 = self.text_editor

        # Master frame configuration
        self.master = master
        self.master.title("OctaDist {0}".format(octadist_gui.__version__))
        font = "Arial 10"
        self.master.option_add("*Font", font)
        self.master.geometry("520x605")

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
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=lambda: self.settings())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: master.destroy())

        # Edit
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_cascade(label="Copy... to clipboard", menu=copy_menu)
        copy_menu.add_command(label="File Name", command=lambda: self.copy_name())
        copy_menu.add_command(label="File Path", command=lambda: self.copy_path())
        copy_menu.add_command(label="Computed Distortion Parameters", command=lambda: self.copy_results())
        copy_menu.add_command(label="Coordinates of Octahedral Structure", command=lambda: self.copy_octa())
        edit_menu.add_separator()
        edit_menu.add_command(label="Edit File", command=lambda: self.edit_file())
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All Results", command=lambda: self.clear_cache())

        # Display
        menu_bar.add_cascade(label="Display", menu=disp_menu)
        disp_menu.add_command(label="All Atoms",
                              command=lambda: draw.all_atom(self, self.atom_coord_full))
        disp_menu.add_command(label="All Atoms and Faces",
                              command=lambda: draw.all_atom_and_face(self, self.atom_coord_full,
                                                                     self.all_face))
        disp_menu.add_command(label="Octahedral Complex",
                              command=lambda: draw.octa(self.atom_coord_octa))
        disp_menu.add_command(label="Octahedron and 8 Faces",
                              command=lambda: draw.octa_and_face(self.atom_coord_octa,
                                                                 self.all_face))
        disp_menu.add_separator()
        disp_menu.add_command(label="Projection Planes",
                              command=lambda: octadist_gui.src.draw.proj_planes(self.atom_coord_octa,
                                                                                self.all_face))
        disp_menu.add_command(label="Twisting Triangular Faces",
                              command=lambda: octadist_gui.src.draw.twisting_faces(self.atom_coord_octa,
                                                                                   self.all_face))

        # Tools
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_cascade(label="Data Summary", menu=data_menu)
        data_menu.add_cascade(label="Complex Info",
                              command=lambda: tools.data_complex(self, self.file_list,
                                                                 self.atom_coord_full))
        tools_menu.add_cascade(menu=strct_menu, label="Show Structural Parameter")
        strct_menu.add_command(label="All Atoms",
                               command=lambda: tools.param_complex(self, self.atom_coord_full))
        strct_menu.add_command(label="Octahedral Structure",
                               command=lambda: tools.param_octa(self, self.atom_coord_octa))
        tools_menu.add_separator()
        tools_menu.add_command(label="Relationship Plot between ζ and Σ",
                               command=lambda: plot.plot_zeta_sigma(self.all_zeta, self.all_sigma))
        tools_menu.add_command(label="Relationship Plot between Σ and Θ",
                               command=lambda: plot.plot_sigma_theta(self.all_sigma, self.all_theta))
        tools_menu.add_separator()
        tools_menu.add_command(label="Calculate Surface Area",
                               command=lambda: tools.find_surface_area(self, self.all_face))
        tools_menu.add_command(label="Calculate Jahn-Teller Distortion Parameter",
                               command=lambda: util.calc_jahn_teller(self, self.atom_coord_full))
        tools_menu.add_command(label="Calculate RMSD", command=lambda: util.calc_rmsd(self, self.atom_coord_full))

        # Help
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Quick Help", command=lambda: popup.show_help(self.master))
        help_menu.add_command(label="Getting Started",
                              command=lambda: webbrowser.open_new_tab(octadist_gui.__website__ + "/manual.html"))
        help_menu.add_separator()
        submit_issue = "https://github.com/OctaDist/OctaDist/issues"
        help_menu.add_command(label="Report Issue", command=lambda: webbrowser.open_new_tab(submit_issue))
        help_menu.add_command(label="Github Repository",
                              command=lambda: webbrowser.open_new_tab(octadist_gui.__github__))
        help_menu.add_command(label="Homepage", command=lambda: webbrowser.open_new_tab(octadist_gui.__website__))
        help_menu.add_separator()
        help_menu.add_command(label="License", command=lambda: popup.show_license())
        help_menu.add_separator()
        help_menu.add_command(label="Check for Updates...", command=self.check_update)
        help_menu.add_command(label="About Program", command=lambda: popup.show_about())

        # Setting layout under master
        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(padx=5, pady=5, row=0, column=0, columnspan=2)
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(padx=5, pady=5, row=1, column=0)
        self.frame3 = tk.Frame(self.master)
        self.frame3.grid(padx=5, pady=5, row=1, column=1)
        self.frame4 = tk.Frame(self.master)
        self.frame4.grid(padx=5, pady=5, row=2, column=0, columnspan=2)

        ###########
        # Frame 1 #
        ###########

        title = octadist_gui.__title__
        self.lbl = tk.Label(self.frame1, foreground="blue", font=("Arial", 16, "bold"), text=title)
        self.lbl.grid(pady="5", row=0, columnspan=4)
        description = octadist_gui.__description__

        self.lbl = tk.Label(self.frame1, text=description)
        self.lbl.grid(pady="5", row=1, columnspan=4)

        self.show_stdout = tk.BooleanVar()
        self.show_stdout.set(False)

        ###########
        # Frame 2 #
        ###########

        self.lbl = tk.Label(self.frame2, text="Program console")
        self.lbl.grid(sticky=tk.N, pady="5", row=0)

        self.btn_openfile = tk.Button(self.frame2, text="Browse file", command=self.open_file)
        self.btn_openfile.config(width=14, relief=tk.RAISED)
        self.btn_openfile.grid(padx="10", pady="5", row=1)

        self.btn_run = tk.Button(self.frame2, text="Compute", command=self.calc_all_param)
        self.btn_run.config(width=14, relief=tk.RAISED)
        self.btn_run.grid(padx="10", pady="5", row=2)

        self.btn_clear = tk.Button(self.frame2, text="Clear cache", command=self.clear_cache)
        self.btn_clear.config(width=14, relief=tk.RAISED)
        self.btn_clear.grid(padx="10", pady="5", row=3)

        self.btn_save = tk.Button(self.frame2, text="Save Results", command=self.save_results)
        self.btn_save.config(width=14, relief=tk.RAISED)
        self.btn_save.grid(padx="10", pady="5", row=4)

        ###########
        # Frame 3 #
        ###########

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

        ###########
        # Frame 4 #
        ###########

        self.box_result = tkscrolled.ScrolledText(self.frame4, height="19", width="70",
                                                  wrap="word", undo="True")
        self.box_result.grid(row=0)

        ###########
        # Welcome #
        ###########

        echo_outs(self, "Welcome to OctaDist {0} {1}".format(octadist_gui.__version__,
                                                             octadist_gui.__release__))
        echo_outs(self, "")
        echo_outs(self, "Developed by " + octadist_gui.__author_full__ + ".")
        echo_outs(self, "")
        echo_outs(self, octadist_gui.__website__)
        echo_outs(self, "")

    def cutoff_metal_ligand(self):
        return self.cutoff_metal_ligand

    def cutoff_global(self):
        return self.cutoff_global

    def cutoff_hydrogen(self):
        return self.cutoff_hydrogen

    def text_editor(self):
        return self.text_editor

    def copy_name(self):
        """
        Copy input file name to clipboard.

        Returns
        -------
        None

        See Also
        --------
        copy_path
        copy_results
        copy_octa

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        name = self.file_list[0].split('/')[-1]

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(name)
        clip.destroy()

    def copy_path(self):
        """
        Copy absolute path of input file to clipboard.

        Returns
        -------
        None

        See Also
        --------
        copy_name
        copy_results
        copy_octa

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

        Returns
        -------
        None

        See Also
        --------
        copy_name
        copy_path
        copy_octa

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        if len(self.all_zeta) == 0:
            popup.err_no_calc()
            return 1

        results = "Zeta, Delta, Sigma, Gamma\n" \
                  "{0:3.6f}, {1:3.6f}, {2:3.6f}, {3:3.6f}"\
            .format(self.all_zeta[0], self.all_delta[0], self.all_sigma[0], self.all_theta[0])

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(results)
        clip.destroy()

    def copy_octa(self):
        """
        Copy atomic coordinates of octahedral structure to clipboard.

        Returns
        -------
        None

        See Also
        --------
        copy_name
        copy_path
        copy_results

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        clip = tk.Tk()
        clip.withdraw()
        clip.clipboard_clear()
        clip.clipboard_append(self.atom_coord_octa[0][3])
        clip.destroy()

    def edit_file(self):
        """
        Edit file by specified text editor on Windows

        Returns
        -------
        None

        See Also
        --------
        settings

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        try:
            for i in range(len(self.file_list)):
                program_name = self.text_editor
                file_name = self.file_list[i]
                subprocess.Popen([program_name, file_name])

        except FileNotFoundError:
            return 1

    def settings(self):
        """
        Program settings. User can set and adjust default values of distance parameters
        for example, distance cutoff for screening out bond distance between atoms.

        Returns
        -------
        None

        """
        def open_exe():
            try:
                input_file = filedialog.askopenfilename(
                    title="Choose text editor executable",
                    filetypes=[("EXE file", "*.exe")]
                )

                file_list = str(input_file)
                entry_exe.delete(0, tk.END)
                entry_exe.insert(tk.INSERT, file_list)

            except IndexError:
                return 1

        def restore_settings(self):
            self.cutoff_metal_ligand = self.backup_1
            self.cutoff_global = self.backup_2
            self.cutoff_hydrogen = self.backup_3
            self.text_editor = self.backup_4

            var_1.set(self.cutoff_metal_ligand)
            var_2.set(self.cutoff_global)
            var_3.set(self.cutoff_hydrogen)

            entry_exe.delete(0, tk.END)
            entry_exe.insert(tk.INSERT, self.text_editor)

        def commit_ok(self):
            self.cutoff_metal_ligand = float(var_1.get())
            self.cutoff_global = float(var_2.get())
            self.cutoff_hydrogen = float(var_3.get())
            self.text_editor = str(entry_exe.get())

            echo_outs(self, "Updated program settings")
            echo_outs(self, "************************")
            echo_outs(self, "Metal-Ligand bond cutoff : {0}".format(self.cutoff_metal_ligand))
            echo_outs(self, "Global bond cutoff       : {0}".format(self.cutoff_global))
            echo_outs(self, "Hydrogen bond cutoff     : {0}".format(self.cutoff_hydrogen))
            echo_outs(self, "------------------------")
            echo_outs(self, "Text editor : {0}".format(self.text_editor))
            echo_outs(self, "")

            master.destroy()

        def commit_cancel():
            master.destroy()

        master = tk.Toplevel(self.master)
        master.title("Program settings")
        master.geometry("650x240")
        master.option_add("*Font", "Arial 10")
        frame = tk.Frame(master)
        frame.grid()

        #######################
        # Metal-Ligand cutoff #
        #######################

        label = tk.Label(frame, text="Metal-Ligand Bond cutoff")
        label.grid(padx="10", pady="5", row=0, column=0)
        var_1 = tk.DoubleVar()
        var_1.set(self.cutoff_metal_ligand)
        scale_1 = tk.Scale(frame, orient="horizontal", variable=var_1, to=5,
                           resolution=0.1, width=20, length=100)
        scale_1.grid(padx="10", pady="5", row=1, column=0)

        ##########################
        # Global distance cutoff #
        ##########################

        label = tk.Label(frame, text="Global distance cutoff")
        label.grid(padx="10", pady="5", row=0, column=1)
        var_2 = tk.DoubleVar()
        var_2.set(self.cutoff_global)
        scale_2 = tk.Scale(frame, orient="horizontal", variable=var_2, to=5,
                           resolution=0.1, width=20, length=100)
        scale_2.grid(padx="10", pady="5", row=1, column=1)

        ############################
        # Hydrogen distance cutoff #
        ############################

        label = tk.Label(frame, text="Hydrogen distance cutoff")
        label.grid(padx="10", pady="5", row=0, column=2)
        var_3 = tk.DoubleVar()
        var_3.set(self.cutoff_hydrogen)
        scale_3 = tk.Scale(frame, orient="horizontal", variable=var_3, to=5,
                           resolution=0.1, width=20, length=100)
        scale_3.grid(padx="10", pady="5", row=1, column=2)

        ######
        label = tk.Label(frame, text="")
        label.grid(row=2)
        ######

        ###############
        # Text editor #
        ###############

        label = tk.Label(frame, text="Text editor executable:")
        label.grid(padx="10", sticky=tk.W, row=6, column=0)
        entry_exe = tk.Entry(frame, bd=2, width=60)
        entry_exe.grid(row=6, column=1, columnspan=2)
        button = tk.Button(frame, text="...", command=open_exe)
        button.grid(padx="5", pady="10", row=6, column=3)

        entry_exe.insert(tk.INSERT, self.text_editor)

        ######
        label = tk.Label(frame, text="")
        label.grid(row=7)
        ######

        ###########
        # Console #
        ###########

        button = tk.Button(frame, text="Restore settings", width=15,
                           command=lambda: restore_settings(self))
        button.grid(padx="10", pady="10", sticky=tk.W, row=8, column=0)
        button = tk.Button(frame, text="OK", width=10,
                           command=lambda: commit_ok(self))
        button.grid(padx="5", pady="10", sticky=tk.E, row=8, column=1)
        button = tk.Button(frame, text="Cancel", width=10,
                           command=lambda: commit_cancel())
        button.grid(padx="5", pady="10", row=8, column=2)

        frame.mainloop()

    def clear_cache(self):
        """
        Clear program cache by nullifying all default variables
        and clear both of parameter and result boxes.

        Returns
        -------
        None

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
        self.check_metal = True

        self.clear_param_box()
        self.clear_result_box()

    def clear_param_box(self):
        """
        Clear parameter box.

        Returns
        -------
        None

        """
        self.box_delta.delete(0, tk.END)
        self.box_sigma.delete(0, tk.END)
        self.box_d_mean.delete(0, tk.END)
        self.box_zeta.delete(0, tk.END)
        self.box_theta_mean.delete(0, tk.END)

    def clear_result_box(self):
        """
        Clear result box.

        Returns
        -------
        None

        """
        self.box_result.delete(1.0, tk.END)

    def check_update(self):
        """
        Check program update.

        Compare version of program user is using with that of the latest release on github.

        Returns
        -------
        None

        References
        ----------
        File: "www.github.com/OctaDist/OctaDist/version_update.txt".

        """
        data = urlopen("https://raw.githubusercontent.com/OctaDist/OctaDist/master/version_update.txt").read()
        # decode
        data = data.decode('utf-8')
        data = data.split()

        user_rev = float(octadist_gui.__revision__)
        server_ver = data[1]
        server_rev = float(data[3])  # code version

        os_name = platform.system()  # find the OS name

        if server_rev > user_rev:
            popup.info_update()

            text = "A new version {0} is ready for download.\n\n" \
                   "Do you want to download now?".format(server_ver)
            MsgBox = messagebox.askquestion("Updates available", text, icon="warning")

            if MsgBox == 'yes':

                dl_link = "https://github.com/OctaDist/OctaDist/releases/download/"
                main_link = dl_link + "v." + server_ver + "/OctaDist-" + server_ver

                if os_name == "Windows":
                    link_windows = main_link + "-Win-x86-64.exe"
                    webbrowser.open_new_tab(link_windows)

                elif os_name == "Darwin":
                    link_mac = main_link + "-macOS-x86-64"
                    webbrowser.open_new_tab(link_mac)

                elif os_name == "Linux":
                    link_linux = main_link + "-Linux-x86-64.tar.gz"
                    webbrowser.open_new_tab(link_linux)

                else:
                    popup.err_cannot_update()

                # Open Thank You page at the same time download the program
                webbrowser.open_new_tab("https://octadist.github.io/thanks.html")

            else:
                pass
        else:
            popup.info_no_update()

    def open_file(self):
        """
        Open file dialog in which user can browse to input file
        and upload it to program.

        Returns
        -------
        None

        """
        self.clear_cache()

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

                for i in range(len(self.file_list)):
                    file_name = self.file_list[i].split('/')[-1]

                    ###########################
                    # Read file and pull data #
                    ###########################

                    atom_full, coord_full = coord.get_coord(self, self.file_list[i])
                    self.atom_coord_full.append([atom_full, coord_full])

                    # If atom_full or coord_full is empty, it will continue to next file
                    if len(atom_full) == 0 or len(coord_full) == 0:
                        continue

                    #########################################
                    # Count the number of metal center atom #
                    #########################################

                    count, atom_metal, coord_metal = coord.count_metal(atom_full, coord_full)

                    # If molecule has no transition metal, insert full atomic coordinates into result box.
                    if count == 0:
                        popup.warn_no_metal()
                        self.check_metal = False

                        if i == 0:
                            echo_outs(self, "XYZ coordinates of extracted octahedral structure")

                        echo_outs(self, "File {0}: {1}".format(i + 1, file_name))
                        echo_outs(self, "Atom                       Cartesian coordinate")
                        for k in range(len(atom_full)):
                            echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                      .format(atom_full[k],
                                              coord_full[k][0],
                                              coord_full[k][1],
                                              coord_full[k][2]))
                        echo_outs(self, "")

                        continue  # continue to next file

                    ########################################################
                    # 1. Extract octahedral structure                      #
                    # 2. Show atomic symbols and coordinates of octahedron #
                    ########################################################

                    if i == 0:
                        echo_outs(self, "XYZ coordinates of extracted octahedral structure")

                    # loop over metal center atoms
                    for j in range(count):
                        # Extract the octahedral structure from the complex
                        atom_octa, coord_octa = coord.search_octa(self, atom_full, coord_full, coord_metal[j - 1])

                        # If no atomic coordinates inside, it will return error
                        if np.any(coord_octa) == 0:
                            popup.err_no_coord()
                            return 1

                        # gather octahedral structure into atom_coord_octa
                        # [ number of file, metal atom, atomic labels, and atomic coordinates ]
                        self.atom_coord_octa.append([i + 1, atom_octa[0], atom_octa, coord_octa])

                        # Print octahedral structure to coord box and stdout box (on request)
                        if count == 1:
                            echo_outs(self, "File {0}: {1}".format(i + 1, file_name))
                            echo_outs(self, "Atom                       Cartesian coordinate")
                            for k in range(len(atom_octa)):
                                echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                          .format(atom_octa[k],
                                                  coord_octa[k][0],
                                                  coord_octa[k][1],
                                                  coord_octa[k][2]))
                            echo_outs(self, "")

                        elif count > 1:
                            echo_outs(self, "File {0}: {1}".format(i + 1, file_name))
                            echo_outs(self, "Metal center atom no. {0} : {1}".format(j + 1, atom_octa[0]))
                            echo_outs(self, "Atom                       Cartesian coordinate")
                            for k in range(len(atom_octa)):
                                echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                          .format(atom_octa[k],
                                                  coord_octa[k][0],
                                                  coord_octa[k][1],
                                                  coord_octa[k][2]))
                            echo_outs(self, "")

            except UnboundLocalError:
                return 1

        except IndexError:
            return 1

    def save_results(self):
        """
        Save results as output file (*txt).

        Returns
        -------
        None

        """
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt", title="Save results",
                                     filetypes=(("TXT File", "*.txt"),
                                                ("All Files", "*.*")))

        if f is None:
            return 0

        f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.\n")
        f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
        f.write("This is free software, and you are welcome to redistribute it under\n")
        f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n")
        f.write("\n")
        f.write("OctaDist {0} {1}: Octahedral Distortion Analysis\n".
                format(octadist_gui.__version__, octadist_gui.__release__))
        f.write("https://octadist.github.io\n")
        f.write("\n")
        f.write("================ Start of the Output file =================\n")
        f.write("\n")
        get_result = self.box_result.get('1.0', tk.END + '-1c')
        f.write(get_result)
        f.write("\n")
        f.write("================= End of the output file ==================\n")
        f.write("\n")
        f.close()

        popup.info_save_results(f.name)

    def calc_all_param(self):
        """
        Calculate all distortion parameters:
        Zeta, Delta, Sigma, and Theta_mean parameters.

        Returns
        -------
        None

        """
        if not self.check_metal:
            popup.err_no_metal()
            return 1

        if len(self.atom_coord_octa) >= 1:
            self.clear_param_box()
        else:
            popup.err_no_file()
            return 1

        comp_result = []

        # loop over number of metal complexes
        for i in range(len(self.atom_coord_octa)):
            num_file, num_metal, atom_octa, coord_octa = self.atom_coord_octa[i]

            # Calculate distortion parameters
            d_mean = calc.calc_d_mean(coord_octa)
            zeta = calc.calc_zeta(coord_octa)
            delta = calc.calc_delta(coord_octa)
            sigma = calc.calc_sigma(coord_octa)
            theta_mean = calc.calc_theta(atom_octa, coord_octa)

            # Find 8 reference faces and 8 opposite faces
            a_ref_f, c_ref_f, a_oppo_f, c_oppo_f = tools.find_faces_octa(coord_octa)
            face_data = [a_ref_f, c_ref_f, a_oppo_f, c_oppo_f]

            # Collect results
            self.all_zeta.append(zeta)
            self.all_delta.append(delta)
            self.all_sigma.append(sigma)
            self.all_theta.append(theta_mean)
            self.all_face.append(face_data)

            comp_result.append([num_file, num_metal,
                                d_mean,
                                zeta,
                                delta,
                                sigma,
                                theta_mean])

        # Print results to each unique box
        if len(self.atom_coord_octa) == 1:
            self.box_d_mean.insert(tk.INSERT, "{0:3.6f}".format(d_mean))
            self.box_zeta.insert(tk.INSERT, "{0:3.6f}".format(zeta))
            self.box_delta.insert(tk.INSERT, "{0:3.6f}".format(delta))
            self.box_sigma.insert(tk.INSERT, "{0:3.6f}".format(sigma))
            self.box_theta_mean.insert(tk.INSERT, "{0:3.6f}".format(theta_mean))
        else:
            self.box_d_mean.insert(tk.INSERT, "See below")
            self.box_zeta.insert(tk.INSERT, "See below")
            self.box_delta.insert(tk.INSERT, "See below")
            self.box_sigma.insert(tk.INSERT, "See below")
            self.box_theta_mean.insert(tk.INSERT, "See below")

        # Print results to result box
        echo_outs(self, "Computed octahedral distortion parameters for all complexes")
        echo_outs(self, "")
        echo_outs(self, "Complex - Metal :    <D>      Zeta      Delta      Sigma      Theta")
        echo_outs(self, "*******************************************************************")
        echo_outs(self, "")
        for i in range(len(comp_result)):
            echo_outs(self, "{0:2d} - {1} : {2:9.4f}  {3:9.6f}  {4:9.6f}  {5:9.4f}  {6:9.4f}"
                      .format(comp_result[i][0],
                              comp_result[i][1],
                              comp_result[i][2],
                              comp_result[i][3],
                              comp_result[i][4],
                              comp_result[i][5],
                              comp_result[i][6]))
        echo_outs(self, "")


def main():
    masters = tk.Tk()
    App = OctaDist(masters)
    masters.mainloop()


if __name__ == '__main__':
    main()
