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
from tkinter import ttk
from urllib.request import urlopen

import numpy as np

import octadist_gui
from octadist_gui.src import (
    echo_outs, calc, coord, draw, plot, popup, tools, util
)


class OctaDist:
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
    None : None

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
    def __init__(self, master):
        # Initialize parameters
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

        # Default display settings
        self.show_title = True
        self.show_axis = True
        self.show_grid = True

        # Backup default setting values
        self.backup_1 = self.cutoff_metal_ligand
        self.backup_2 = self.cutoff_global
        self.backup_3 = self.cutoff_hydrogen
        self.backup_4 = self.text_editor
        self.backup_5 = self.show_title
        self.backup_6 = self.show_axis
        self.backup_7 = self.show_grid

        ##############################
        # Master frame configuration #
        ##############################

        self.master = master
        self.master.wm_iconbitmap(r"..\images\molecule.ico")
        self.master.title(f"OctaDist {octadist_gui.__version__}")
        font = "Arial 10"
        self.master.option_add("*Font", font)

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
        edit_menu.add_command(label="Run Program Scripting", command=lambda: self.script_start())
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All Results", command=lambda: self.clear_cache())

        # Display
        menu_bar.add_cascade(label="Display", menu=disp_menu)
        disp_menu.add_command(label="All Atoms",
                              command=lambda: draw.all_atom(self, self.atom_coord_full))
        disp_menu.add_command(label="All Atoms and Faces",
                              command=lambda: draw.all_atom_and_face(self, self.atom_coord_full, self.atom_coord_octa))
        disp_menu.add_separator()
        disp_menu.add_command(label="Octahedral Complex",
                              command=lambda: draw.octa(self, self.atom_coord_octa))
        disp_menu.add_command(label="Octahedron and 8 Faces",
                              command=lambda: draw.octa_and_face(self, self.atom_coord_octa))
        disp_menu.add_separator()
        disp_menu.add_command(label="Projection Planes",
                              command=lambda: draw.proj_planes(self, self.atom_coord_octa))
        disp_menu.add_command(label="Twisting Triangular Faces",
                              command=lambda: draw.twisting_faces(self, self.atom_coord_octa))

        # Tools
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_cascade(label="Data Summary", menu=data_menu)
        data_menu.add_cascade(label="Complex",
                              command=lambda: tools.data_complex(self, self.file_list, self.atom_coord_full))
        data_menu.add_cascade(label="Faces of Octahedral Structure",
                              command=lambda: tools.data_face(self, self.atom_coord_octa))
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
                               command=lambda: tools.find_surface_area(self, self.atom_coord_octa))
        tools_menu.add_command(label="Calculate Jahn-Teller Distortion Parameter",
                               command=lambda: util.CalcJahnTeller(self, self.master, self.atom_coord_full))
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

        ####################
        # my own ttk style #
        ####################

        gui_ttk = ttk.Style()
        gui_ttk.configure("TButton", relief="sunken", padding=5)
        gui_ttk.configure("My.TLabel", foreground="black")
        gui_ttk.configure("My.TLabelframe", foreground="brown")

        ###########
        # Frame 1 #
        ###########

        self.frame1 = tk.Frame(self.master)
        self.frame1.grid(padx=5, pady=5, row=0, column=0, columnspan=2)

        title = octadist_gui.__title__
        self.lbl = tk.Label(self.frame1, text=title)
        self.lbl.configure(foreground="blue", font=("Arial", 16, "bold"))
        self.lbl.grid(pady="5", row=0, columnspan=4)

        description = octadist_gui.__description__
        self.lbl = tk.Label(self.frame1, text=description)
        self.lbl.grid(pady="5", row=1, columnspan=4)

        ###########
        # Frame 2 #
        ###########

        self.frame2 = tk.LabelFrame(self.master, text="Program Console")
        self.frame2.grid(padx=5, pady=5, ipadx=2, ipady=2, sticky=tk.N, row=1, column=0)

        self.btn_openfile = ttk.Button(self.frame2, text="Browse file", command=self.open_file)
        self.btn_openfile.config(width=14)
        self.btn_openfile.grid(padx="10", pady="5", row=0)

        self.btn_run = ttk.Button(self.frame2, text="Compute", command=self.calc_all_param)
        self.btn_run.config(width=14)
        self.btn_run.grid(padx="10", pady="5", row=1)

        self.btn_clear = ttk.Button(self.frame2, text="Clear cache", command=self.clear_cache)
        self.btn_clear.config(width=14)
        self.btn_clear.grid(padx="10", pady="5", row=2)

        self.btn_save = ttk.Button(self.frame2, text="Save Results", command=self.save_results)
        self.btn_save.config(width=14)
        self.btn_save.grid(padx="10", pady="5", row=3)

        ###########
        # Frame 3 #
        ###########

        self.frame3 = tk.LabelFrame(self.master, text="Distortion Parameters")
        self.frame3.grid(padx=5, pady=5, ipadx=3, ipady=2, sticky=tk.N, row=1, column=1)

        # D_mean
        self.lbl_d_mean = tk.Label(self.frame3, text="<D>   =   ")
        self.lbl_d_mean.grid(sticky=tk.E, pady="5", row=0, column=0)

        self.box_d_mean = tk.Entry(self.frame3)
        self.box_d_mean.configure(width="12", justify='center')
        self.box_d_mean.grid(row=0, column=1)

        self.lbl_unit = tk.Label(self.frame3, text="  Angstrom")
        self.lbl_unit.grid(pady="5", row=0, column=2)

        # Zeta
        self.lbl_zeta = tk.Label(self.frame3, text="ζ   =   ")
        self.lbl_zeta.grid(sticky=tk.E, pady="5", row=1, column=0)

        self.box_zeta = tk.Entry(self.frame3)
        self.box_zeta.configure(width="12", justify='center')
        self.box_zeta.grid(row=1, column=1)

        self.lbl_unit = tk.Label(self.frame3, text="  Angstrom")
        self.lbl_unit.grid(pady="5", row=1, column=2)

        # Delta
        self.lbl_delta = tk.Label(self.frame3, text="Δ   =   ")
        self.lbl_delta.grid(sticky=tk.E, pady="5", row=2, column=0)

        self.box_delta = tk.Entry(self.frame3)
        self.box_delta.configure(width="12", justify='center')
        self.box_delta.grid(row=2, column=1)

        # Sigma
        self.lbl_sigma = tk.Label(self.frame3, text="Σ   =   ")
        self.lbl_sigma.grid(sticky=tk.E, pady="5", row=3, column=0)

        self.box_sigma = tk.Entry(self.frame3)
        self.box_sigma.configure(width="12", justify='center')
        self.box_sigma.grid(row=3, column=1)

        self.lbl_unit = tk.Label(self.frame3, text="  degree")
        self.lbl_unit.grid(pady="5", row=3, column=2)

        # Theta_mean
        self.lbl_theta_mean = tk.Label(self.frame3, text="Θ   =   ")
        self.lbl_theta_mean.grid(sticky=tk.E, pady="5", row=4, column=0)

        self.box_theta_mean = tk.Entry(self.frame3)
        self.box_theta_mean.configure(width="12", justify='center')
        self.box_theta_mean.grid(row=4, column=1)

        self.lbl_unit = tk.Label(self.frame3, text="  degree")
        self.lbl_unit.grid(pady="5", row=4, column=2)

        ###########
        # Frame 4 #
        ###########

        self.frame4 = tk.Frame(self.master)
        self.frame4.grid(padx=5, pady=10, row=2, column=0, columnspan=2)

        self.box_result = tkscrolled.ScrolledText(self.frame4)
        self.box_result.configure(height="19", width="70", wrap="word", undo="True")
        self.box_result.grid(row=0)

        ###########
        # Welcome #
        ###########

        full_version = octadist_gui.__version__ + octadist_gui.__release__

        echo_outs(self, f"Welcome to OctaDist {full_version}")
        echo_outs(self, "")
        echo_outs(self, f"Developed by {octadist_gui.__author_full__}.")
        echo_outs(self, "")
        echo_outs(self, octadist_gui.__website__)
        echo_outs(self, "")

    def get_cutoff_metal_ligand(self):
        """
        Fetch cutoff_metal_ligand and return value.

        Returns
        -------
        cutoff_metal_ligand : float
            Cutoff distance for metal-ligand bond screening.

        """
        return self.cutoff_metal_ligand

    def get_cutoff_global(self):
        """
        Fetch cutoff_global and return value.

        Returns
        -------
        cutoff_global : float
            Cutoff global distance for bond screening.

        """
        return self.cutoff_global

    def get_cutoff_hydrogen(self):
        """
        Fetch cutoff_hydrogen and return value.

        Returns
        -------
        cutoff_hydrogen : float
            Cutoff distance for hydrogen bond screening.

        """
        return self.cutoff_hydrogen

    def text_editor(self):
        """
        Text editor for editing file.

        Returns
        -------
        text_editor : str
            Name or absolute path of text editor that user specified.

        """
        return self.text_editor

    def show_title(self):
        """
        Show figure title.

        Returns
        -------
        show_title : bool
            True if user want matplotlib to show figure title.
            False if user does not.

        """
        return self.show_title

    def show_axis(self):
        """
        Show figure axes.

        Returns
        -------
        show_axis : bool
            True if user want matplotlib to show figure axis.
            False if user does not.

        """
        return self.show_axis

    def show_grid(self):
        """
        Show figure gridlines.

        Returns
        -------
        show_grid : bool
            True if user want matplotlib to show figure gridlines.
            False if user does not.

        """
        return self.show_grid

    #################
    # Copy and Edit #
    #################

    def copy_name(self):
        """
        Copy input file name to clipboard.

        Returns
        -------
        None : None

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
        None : None

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
        None : None

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
                  "{0:3.6f}, {1:3.6f}, {2:3.6f}, {3:3.6f}" \
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
        None : None

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
        None : None

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

    #############
    # Scripting #
    #############

    def script_show_var(self, args):
        for i in range(len(args)):
            self.box_script.insert(tk.INSERT, f">>> {args[i]}")

    def script_set_var(self, param, new_value):
        self.all_var = {'cutoff_metal_ligand': self.cutoff_metal_ligand,
                        'cutoff_global': self.cutoff_global,
                        'cutoff_hydrogen': self.cutoff_hydrogen
                        }

        for key, value in self.all_var.items():
            print(key, value)
            if param == key:
                self.all_var[key] = new_value

    def script_run_command(self, event):
        self.get_var = self.entry_script.get().strip().split()

        if len(self.get_var) == 0:
            self.box_script.insert(tk.INSERT, ">>>\n")
            self.box_script.see(tk.END)
            return 1

        self.entry_script.delete(0, tk.END)

        command = self.get_var[0].lower()
        args = self.get_var[1:]

        if command == "help":
            help_msg = ">>> This is an interactive code console for internal scripting.\n" \
                       ">>> \n" \
                       ">>> Commands\n" \
                       ">>> --------\n" \
                       ">>> help     - Show this help info.\n" \
                       ">>> list     - List all commands.\n" \
                       ">>> info     - Show info of program.\n" \
                       ">>> doc      - Show docstring of this function.\n" \
                       ">>> show     - Show values of parameter.\n" \
                       "               Usage: show arg1 [arg2] [arg3] [..]\n" \
                       ">>> set      - Set new value to parameter.\n" \
                       "               Usage: set param new_value\n" \
                       ">>> clear    - Clear stdout/stderr.\n" \
                       ">>> clean    - Clear stdout/stderr.\n" \
                       ">>> restore  - Restore program settings.\n"
            self.box_script.insert(tk.INSERT, help_msg + "\n")
        elif command == "list":
            all_command = "help, list, info, doc, show, set, clear, clean, restore"
            self.box_script.insert(tk.INSERT, f">>> {all_command}\n")
        elif command == "info":
            self.box_script.insert(tk.INSERT, f">>> {octadist_gui.__description__}\n")
        elif command == "doc":
            self.box_script.insert(tk.INSERT, f">>> {self.__doc__ }\n")
        elif command == "show":
            try:
                self.script_show_var(self, args)
            except TypeError:
                self.box_script.insert(tk.INSERT, f">>> show command needs 1 parameter\n")
        elif command == "set":
            try:
                self.script_set_var(self, args[0], args[1])
            except TypeError:
                self.box_script.insert(tk.INSERT, f">>> set command needs 2 parameters\n")
        elif command == "clear" or command == "clean":
            self.box_script.delete(1.0, tk.END)
        elif command == "restore" or command == "clean":
            self.box_script.insert(tk.INSERT, f">>> Restore all settings")
        else:
            self.box_script.insert(tk.INSERT, f">>> Command \"{command}\" not found\n")

        self.box_script.see(tk.END)

    def script_start(self):
        wd = tk.Toplevel(self.master)
        wd.wm_iconbitmap(r"..\images\molecule.ico")
        wd.title("Run Scripting")
        wd.bind('<Return>', self.script_run_command)

        self.lbl = tk.Label(wd, text="Output:")
        self.lbl.grid(padx="5", pady="5", sticky=tk.W, row=0, column=0)
        self.box_script = tk.Text(wd, width=70, height=20)
        self.box_script.grid(padx="5", pady="5", row=1, column=0, columnspan=2)
        self.lbl = tk.Label(wd, text="Input:")
        self.lbl.grid(padx="5", pady="5", sticky=tk.W, row=2, column=0)
        self.entry_script = tk.Entry(wd, width=62)
        self.entry_script.grid(padx="5", pady="5", sticky=tk.W, row=3, column=0)
        self.btn_script = tk.Button(wd, text="Run")
        self.btn_script.bind('<Button-1>', self.script_run_command)
        self.btn_script.grid(padx="5", pady="5", row=3, column=1)

        self.box_script.insert(tk.INSERT, ">>> Enter your script commands\n")
        self.box_script.insert(tk.INSERT, ">>> If you have no idea about scripting, "
                                          "type \"help\" for getting started.\n")

        wd.mainloop()

    ###################
    # Program Setting #
    ###################

    def settings(self):
        """
        Program settings. User can set and adjust default values of distance parameters
        for example, distance cutoff for screening out bond distance between atoms.

        Returns
        -------
        None : None

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

        def check_title():
            if var_title.get():
                var_title.set(True)
            else:
                var_title.set(False)

        def check_axis():
            if var_axis.get():
                var_axis.set(True)
            else:
                var_axis.set(False)

        def check_grid():
            if var_grid.get():
                var_grid.set(True)
            else:
                var_grid.set(False)

        def restore_settings(self):
            self.cutoff_metal_ligand = self.backup_1
            self.cutoff_global = self.backup_2
            self.cutoff_hydrogen = self.backup_3
            self.text_editor = self.backup_4
            self.show_title = self.backup_5
            self.show_axis = self.backup_6
            self.show_grid = self.backup_7

            var_1.set(self.cutoff_metal_ligand)
            var_2.set(self.cutoff_global)
            var_3.set(self.cutoff_hydrogen)
            var_title.set(self.show_title)
            var_axis.set(self.show_axis)
            var_grid.set(self.show_grid)

            entry_exe.delete(0, tk.END)
            entry_exe.insert(tk.INSERT, self.text_editor)

        def commit_ok(self):
            self.cutoff_metal_ligand = float(var_1.get())
            self.cutoff_global = float(var_2.get())
            self.cutoff_hydrogen = float(var_3.get())
            self.text_editor = str(entry_exe.get())
            self.show_title = bool(var_title.get())
            self.show_axis = bool(var_axis.get())
            self.show_grid = bool(var_grid.get())

            echo_outs(self, "Updated program settings")
            echo_outs(self, "************************")
            echo_outs(self, f"Metal-Ligand bond cutoff : {self.cutoff_metal_ligand}")
            echo_outs(self, f"Global bond cutoff       : {self.cutoff_global}")
            echo_outs(self, f"Hydrogen bond cutoff     : {self.cutoff_hydrogen}")
            echo_outs(self, "------------------------")
            echo_outs(self, f"Text editor : {self.text_editor}")
            echo_outs(self, "------------------------")
            echo_outs(self, f"Show Title  : {self.show_title}")
            echo_outs(self, f"Show Axis   : {self.show_axis}")
            echo_outs(self, f"Show Grid   : {self.show_grid}")
            echo_outs(self, "")

            wd.destroy()

        def commit_cancel():
            wd.destroy()

        ###################
        # Setting: Widget #
        ###################

        wd = tk.Toplevel(self.master)
        wd.wm_iconbitmap(r"..\images\molecule.ico")
        wd.title("Program settings")
        wd.option_add("*Font", "Arial 10")

        frame = tk.Frame(wd)
        frame.grid()

        ###################
        # Setting: Cutoff #
        ###################

        cutoff = tk.LabelFrame(frame, text="Bond Cutoff:")
        cutoff.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky='W', row=0, columnspan=4)

        label_1 = tk.Label(cutoff, text="Metal-Ligand Bond")
        label_1.grid(padx="10", pady="5", ipadx="10", row=0, column=0)

        var_1 = tk.DoubleVar()
        var_1.set(self.cutoff_metal_ligand)

        scale_1 = tk.Scale(cutoff, orient="horizontal", variable=var_1, to=5, resolution=0.1)
        scale_1.configure(width=20, length=100)
        scale_1.grid(padx="10", pady="5", ipadx="10", row=1, column=0)

        label_2 = tk.Label(cutoff, text="Global Distance")
        label_2.grid(padx="10", pady="5", ipadx="10", row=0, column=1)

        var_2 = tk.DoubleVar()
        var_2.set(self.cutoff_global)

        scale_2 = tk.Scale(cutoff, orient="horizontal", variable=var_2, to=5, resolution=0.1)
        scale_2.configure(width=20, length=100)
        scale_2.grid(padx="10", pady="5", ipadx="10", row=1, column=1)

        label_3 = tk.Label(cutoff, text="Hydrogen Distance")
        label_3.grid(padx="10", pady="5", ipadx="10", row=0, column=2)

        var_3 = tk.DoubleVar()
        var_3.set(self.cutoff_hydrogen)

        scale_3 = tk.Scale(cutoff, orient="horizontal", variable=var_3, to=5, resolution=0.1)
        scale_3.configure(width=20, length=100)
        scale_3.grid(padx="10", pady="5", ipadx="10", row=1, column=2)

        ########################
        # Setting: Text editor #
        ########################

        text_editor = tk.LabelFrame(frame, text="Text editor:")
        text_editor.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky='W', row=1, columnspan=4)

        label = tk.Label(text_editor, text="Enter the EXE:")
        label.grid(padx="5", sticky=tk.E, row=0, column=0)

        entry_exe = tk.Entry(text_editor, bd=2, width=60)
        entry_exe.grid(row=0, column=1)

        button = tk.Button(text_editor, text="Browse...", command=open_exe)
        button.grid(padx="5", pady="5", sticky=tk.W, row=0, column=2)

        entry_exe.insert(tk.INSERT, self.text_editor)

        #####################
        # Setting: Displays #
        #####################

        displays = tk.LabelFrame(frame, text="Displays:")
        displays.grid(padx=5, pady=5, ipadx=5, ipady=5, sticky='W', row=2, columnspan=4)

        # Show title of plot?
        var_title = tk.BooleanVar()
        var_title.set(self.show_title)

        show_title = ttk.Checkbutton(displays, text="Show Figure Title", onvalue=True, offvalue=False,
                                     variable=var_title, command=lambda: check_title())
        show_title.grid(padx="5", pady="5", ipadx="25", sticky=tk.E, row=0, column=0)

        # Show axis?
        var_axis = tk.BooleanVar()
        var_axis.set(self.show_axis)

        show_axis = ttk.Checkbutton(displays, text="Show Axes", onvalue=True, offvalue=False,
                                    variable=var_axis, command=lambda: check_axis())
        show_axis.grid(padx="5", pady="5", ipadx="25", sticky=tk.E, row=0, column=1)

        # Show grid?
        var_grid = tk.BooleanVar()
        var_grid.set(self.show_grid)

        show_grid = ttk.Checkbutton(displays, text="Show Gridlines", onvalue=True, offvalue=False,
                                    variable=var_grid, command=lambda: check_grid())
        show_grid.grid(padx="5", pady="5", ipadx="5", sticky=tk.E, row=0, column=2)

        ####################
        # Setting: Console #
        ####################

        button = tk.Button(frame, text="Restore settings", command=lambda: restore_settings(self))
        button.configure(width=15)
        button.grid(padx="10", pady="10", sticky=tk.W, row=3, column=0)

        button = tk.Button(frame, text="OK", command=lambda: commit_ok(self))
        button.configure(width=15)
        button.grid(padx="5", pady="10", sticky=tk.E, row=3, column=2)

        button = tk.Button(frame, text="Cancel", command=lambda: commit_cancel())
        button.configure(width=15)
        button.grid(padx="5", pady="10", row=3, column=3)

        frame.mainloop()

    ###################
    # Clear All Cache #
    ###################

    def clear_cache(self):
        """
        Clear program cache by nullifying all default variables
        and clear both of parameter and result boxes.

        Returns
        -------
        None : None

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
        None : None

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
        None : None

        """
        self.box_result.delete(1.0, tk.END)

    ################
    # Check Update #
    ################

    def check_update(self):
        """
        Check program update by comparing version of program user is using with
        that of the latest version released on github.

        Returns
        -------
        None : None

        References
        ----------
        File: www.github.com/OctaDist/OctaDist/version_update.txt

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
            popup.info_new_update()

            text = f"A new version {server_ver} is ready for download.\n\n" \
                   "Do you want to download now?"
            msg_box = messagebox.askquestion("Updates available", text, icon="warning")

            if msg_box == 'yes':

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

        elif server_rev < user_rev:
            popup.info_using_dev()

        else:
            popup.info_no_update()

    #####################
    # Manipulating File #
    #####################

    def open_file(self):
        """
        Open file dialog in which user can browse to input file and upload it to program.

        Returns
        -------
        None : None

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

                    ###########################
                    # Read file and pull data #
                    ###########################

                    file_name = self.file_list[i].split('/')[-1]

                    atom_full, coord_full = coord.get_coord(self, self.file_list[i])
                    self.atom_coord_full.append([atom_full, coord_full])

                    # If either lists is empty, then continue to next file
                    if len(atom_full) == 0 or len(coord_full) == 0:
                        continue

                    ###############################################
                    # Determine metal center atoms in the complex #
                    ###############################################

                    count, atom_metal, coord_metal = coord.count_metal(atom_full, coord_full)

                    # If molecule has no transition metal, show full atomic coordinates instead
                    if count == 0:
                        popup.warn_no_metal()
                        self.check_metal = False

                        if i == 0:
                            echo_outs(self, "XYZ coordinates of extracted octahedral structure")

                        echo_outs(self, f"File {i + 1}: {file_name}")
                        echo_outs(self, "Atom                       Cartesian coordinate")
                        for k in range(len(atom_full)):
                            echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                      .format(atom_full[k],
                                              coord_full[k][0],
                                              coord_full[k][1],
                                              coord_full[k][2]))
                        echo_outs(self, "")

                        continue  # continue to next file

                    #################################################
                    # Extract octahedral structure from the complex #
                    #################################################

                    if i == 0:
                        echo_outs(self, "XYZ coordinates of extracted octahedral structure")

                    # loop over metal center atoms
                    for j in range(count):
                        atom_octa, coord_octa = coord.search_octa(self, atom_full, coord_full, coord_metal[j - 1])

                        # If no atomic coordinates inside, it will return error
                        if np.any(coord_octa) == 0:
                            popup.err_no_coord()
                            return 1

                        if len(coord_octa) < 7:
                            self.clear_result_box()
                            popup.err_less_ligands()
                            return 1

                        # Gather octahedral structure into atom_coord_octa
                        # [ number of file, metal atom, atomic labels, and atomic coordinates ]
                        self.atom_coord_octa.append([i + 1, atom_octa[0], atom_octa, coord_octa])

                        if count == 1:
                            echo_outs(self, f"File {i + 1}: {file_name}")
                            echo_outs(self, "Atom                       Cartesian coordinate")
                            for k in range(len(atom_octa)):
                                echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                          .format(atom_octa[k],
                                                  coord_octa[k][0],
                                                  coord_octa[k][1],
                                                  coord_octa[k][2]))
                            echo_outs(self, "")

                        elif count > 1:
                            echo_outs(self, f"File {i + 1}: {file_name}")
                            echo_outs(self, f"Metal center atom no. {j + 1} : {atom_octa[0]}")
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
        None : None

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
        f.write(f"OctaDist {octadist_gui.__version__} {octadist_gui.__release__}.\n")
        f.write("Octahedral Distortion Calculator\n")
        f.write(f"{octadist_gui.__website__}\n")
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

    def save_coord(self):
        """
        Save atomic coordinates (Cartesian coordinate) of octahedral structure
        as XYZ file.

        Returns
        -------
        None : None

        """
        if len(self.file_list) == 0:
            popup.err_no_file()
            return 1

        if len(self.file_list) > 1:
            popup.err_many_files()
            return 1

        f = filedialog.asksaveasfile(mode='w', defaultextension=".xyz", title="Save atomic coordinates",
                                     filetypes=(("XYZ File", "*.xyz"),
                                                ("TXT File", "*.txt"),
                                                ("All Files", "*.*")))

        if f is None:
            return 0

        file_name = self.file_list[0].split('/')[-1]
        atoms = self.atom_coord_octa[0][2]
        coord = self.atom_coord_octa[0][3]

        full_version = octadist_gui.__version__ + octadist_gui.__release__

        f.write("7\n")
        f.write(f"{file_name} : this file was generated by OctaDist {full_version}.\n")
        for i in range(7):
            f.write("{0:2s}   {1:9.6f}  {2:9.6f}  {3:9.6f}\n"
                    .format(atoms[i], coord[i][0], coord[i][1], coord[i][2]))
        f.write("\n")
        f.close()

        popup.info_save_results(f.name)

    def calc_all_param(self):
        """
        Calculate all distortion parameters:
        Zeta, Delta, Sigma, and Theta_mean parameters.

        Returns
        -------
        None : None

        """
        if not self.check_metal:
            popup.err_no_metal()
            return 1

        if len(self.atom_coord_octa) >= 1:
            self.clear_param_box()
        else:
            popup.err_no_file()
            return 1

        d_mean = 0
        zeta = 0
        delta = 0
        sigma = 0
        theta_mean = 0
        comp_result = []

        # loop over number of metal complexes
        for i in range(len(self.atom_coord_octa)):
            num_file, num_metal, atom_octa, coord_octa = self.atom_coord_octa[i]

            # Calculate distortion parameters
            d_mean = calc.calc_d_mean(coord_octa)
            zeta = calc.calc_zeta(coord_octa)
            delta = calc.calc_delta(coord_octa)
            sigma = calc.calc_sigma(coord_octa)
            theta_mean = calc.calc_theta(coord_octa)

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
                                d_mean, zeta, delta, sigma, theta_mean
                                ])

        # Print results to each unique box
        if len(self.atom_coord_octa) == 1:
            self.box_d_mean.insert(tk.INSERT, f"{d_mean:3.6f}")
            self.box_zeta.insert(tk.INSERT, f"{zeta:3.6f}")
            self.box_delta.insert(tk.INSERT, f"{delta:3.6f}")
            self.box_sigma.insert(tk.INSERT, f"{sigma:3.6f}")
            self.box_theta_mean.insert(tk.INSERT, f"{theta_mean:3.6f}")
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
    root = tk.Tk()
    app = OctaDist(root)
    root.mainloop()


if __name__ == '__main__':
    main()
