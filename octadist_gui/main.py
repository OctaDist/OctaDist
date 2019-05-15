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
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import webbrowser
from tkinter import filedialog
from tkinter import messagebox
from urllib.request import urlopen

import numpy as np

import octadist_gui
from octadist_gui.src import (
    echo_logs, echo_outs, calc, coord,
    draw, plane, plot, popup, tools, util
)


class OctaDist:
    def __init__(self, master):
        """
        Program interface component is organized as follows:

        |-------------------|---------------|
        |     Frame 1       |               |
        |-------------------|               |
        | Frame 2 | Frame 3 |    Frame 5    |
        |-------------------|               |
        |     Frame 4       |               |
        |-------------------|---------------|

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

        Parameters
        ----------
        master
            Master frame of program GUI.

        Returns
        -------
        None

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

        # Master frame configuration
        self.master = master
        self.master.title("OctaDist {0}".format(octadist_gui.__version__))
        font = "Arial 10"
        self.master.option_add("*Font", font)
        self.master.geometry("520x535")

        # Main menu
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(self.master, tearoff=0)
        disp_menu = tk.Menu(self.master, tearoff=0)
        tools_menu = tk.Menu(self.master, tearoff=0)
        help_menu = tk.Menu(self.master, tearoff=0)

        # Sub-menu
        data_menu = tk.Menu(self.master, tearoff=0)
        strct_menu = tk.Menu(self.master, tearoff=0)

        # File
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.clear_cache())
        file_menu.add_command(label="Open", command=lambda: self.open_file())
        file_menu.add_command(label="Save Results", command=lambda: self.save_results())
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: master.destroy())

        # Display
        menu_bar.add_cascade(label="Display", menu=disp_menu)
        disp_menu.add_command(label="All Atoms",
                              command=lambda: draw.all_atom(self, self.atom_coord_full))
        disp_menu.add_command(label="All Atoms and Faces",
                              command=lambda: draw.all_atom_and_face(self, self.atom_coord_full, self.all_face))
        disp_menu.add_command(label="Octahedral Complex",
                              command=lambda: draw.octa(self, self.atom_coord_octa))
        disp_menu.add_command(label="Octahedron and 8 Faces",
                              command=lambda: draw.octa_and_face(self, self.atom_coord_octa, self.all_face))
        disp_menu.add_separator()
        disp_menu.add_command(label="Projection Planes",
                              command=lambda: plane.proj_planes(self, self.atom_coord_octa, self.all_face))
        disp_menu.add_command(label="Twisting Triangular Faces",
                              command=lambda: plane.twisting_faces(self, self.atom_coord_octa, self.all_face))

        # Tools
        menu_bar.add_cascade(menu=tools_menu, label="Tools")
        tools_menu.add_cascade(menu=data_menu, label="Data Summary")
        data_menu.add_cascade(label="Complex Info",
                              command=lambda: tools.data_complex(self, self.file_list, self.atom_coord_full))
        tools_menu.add_cascade(menu=strct_menu, label="Show Structural Parameter")
        strct_menu.add_command(label="All Atoms",
                               command=lambda: tools.param_complex(self, self.atom_coord_full))
        strct_menu.add_command(label="Octahedral Structure",
                               command=lambda: tools.param_octa(self, self.atom_coord_octa))
        tools_menu.add_separator()
        tools_menu.add_command(label="Relationship Plot between ζ and Σ",
                               command=lambda: plot.plot_zeta_sigma(self, self.all_zeta, self.all_sigma))
        tools_menu.add_command(label="Relationship Plot between Σ and Θ",
                               command=lambda: plot.plot_sigma_theta(self, self.all_sigma, self.all_theta))
        tools_menu.add_separator()
        tools_menu.add_command(label="Calculate Surface Area",
                               command=lambda: tools.find_surface_area(self, self.all_face))
        tools_menu.add_command(label="Calculate Jahn-Teller Distortion Parameter",
                               command=lambda: util.calc_jahn_teller(self, self.atom_coord_full))
        tools_menu.add_command(label="Calculate RMSD", command=lambda: util.calc_rmsd(self, self.atom_coord_full))

        # Help
        menu_bar.add_cascade(menu=help_menu, label="Help")
        help_menu.add_command(label="Quick Help", command=lambda: popup.show_help(self.master))
        help_menu.add_command(label="Getting Started",
                              command=lambda: webbrowser.open_new_tab(octadist_gui.__website__ + "/manual.html"))
        help_menu.add_separator()
        submit_issue = "https://github.com/OctaDist/OctaDist/issues"
        help_menu.add_command(label="Submit a Bug Report", command=lambda: webbrowser.open_new_tab(submit_issue))
        help_menu.add_command(label="Github Repository",
                              command=lambda: webbrowser.open_new_tab(octadist_gui.__github__))
        help_menu.add_command(label="Homepage", command=lambda: webbrowser.open_new_tab(octadist_gui.__website__))
        help_menu.add_separator()
        help_menu.add_command(label="Check for Updates", command=self.check_update)
        help_menu.add_command(label="License", command=lambda: popup.show_license(self))
        help_menu.add_command(label="About Program", command=lambda: popup.show_about(self))

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

        def select_stdout_window():
            if self.show_stdout.get():
                self.master.geometry("1050x535")
            else:
                self.master.geometry("520x535")

        ###########
        # Frame 2 #
        ###########

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

        self.box_result = tkscrolled.ScrolledText(self.frame4, height="14", width="70", wrap="word", undo="True")
        self.box_result.grid(row=0)

        ###########
        # Frame 5 #
        ###########

        self.lbl = tk.Label(self.frame5, text="Standard Output/Error Information")
        self.lbl.grid(row=0)

        self.box_stdout = tkscrolled.ScrolledText(self.frame5, height="30", width="70", wrap="word", undo="True")
        self.box_stdout.grid(sticky=tk.N, pady="5", row=1)

        echo_outs(self, "Welcome to OctaDist {0} {1}".format(octadist_gui.__version__, octadist_gui.__release__))
        echo_outs(self, "")
        echo_outs(self, "Created by " + octadist_gui.__author_full__)
        echo_outs(self, "")
        echo_outs(self, octadist_gui.__website__)

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

        echo_logs(self, "Clear cache")

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
        self.box_stdout.delete(1.0, tk.END)

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
            popup.info_update(self)

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
                    popup.err_cannot_update(self)

                # Open Thank You page at the same time download the program
                webbrowser.open_new_tab("https://octadist.github.io/thanks.html")

            else:
                pass
        else:
            popup.info_no_update(self)

    def open_file(self):
        """
        Open file dialog in which user can browse to input file
        and upload it to program.

        Returns
        -------
        None

        """
        self.clear_cache()

        echo_logs(self, "Info: Browse input file")

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
                echo_logs(self, "Info: Total number of file: {0}".format(len(self.file_list)))

                for i in range(len(self.file_list)):
                    file_name = self.file_list[i].split('/')[-1]
                    echo_logs(self, "Info: Open file no. {0}: {1}".format(i + 1, file_name))

                    ###########################
                    # Read file and pull data #
                    ###########################

                    atom_full, coord_full = coord.get_coord(self, self.file_list[i])
                    self.atom_coord_full.append([atom_full, coord_full])

                    # If atom_full or coord_full is empty, continue to next file
                    if len(atom_full) == 0 or len(coord_full) == 0:
                        continue

                    # Print full structure to stdout box
                    echo_logs(self, "Info: Show Cartesian coordinates of all {0} atoms".format(len(atom_full)))
                    echo_logs(self, "")
                    echo_logs(self, "      Atom        X             Y             Z")
                    echo_logs(self, "      ----    ----------    ----------    ----------")
                    for j in range(len(atom_full)):
                        echo_logs(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                  .format(atom_full[j], coord_full[j][0], coord_full[j][1], coord_full[j][2]))
                    echo_logs(self, "")

                    #########################################
                    # Count the number of metal center atom #
                    #########################################

                    count, atom_metal, coord_metal = coord.count_metal(self, atom_full, coord_full)

                    # If molecule has no transition metal, insert full atomic coordinates into result box.
                    if count == 0:
                        popup.warn_no_metal(self)
                        self.check_metal = False

                        if i == 0:
                            echo_outs(self, "XYZ coordinates of extracted octahedral structure")

                        echo_outs(self, "File {0}: {1}".format(i + 1, file_name))
                        echo_outs(self, "Atom                       Cartesian coordinate")
                        for k in range(len(atom_full)):
                            echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                      .format(atom_full[k], coord_full[k][0], coord_full[k][1], coord_full[k][2]))
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
                        atom_octa, coord_octa = coord.search_octa(atom_full, coord_full, coord_metal[j - 1])

                        # If no atomic coordinates inside, it will return error
                        if np.any(coord_octa) == 0:
                            popup.err_no_coord(self)
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
                                          .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1], coord_octa[k][2]))
                            echo_outs(self, "")

                            echo_logs(self, "Info: Show Cartesian coordinates of extracted octahedral structure")
                            echo_logs(self, "")
                            echo_logs(self, "      Atom        X             Y             Z")
                            echo_logs(self, "      ----    ----------    ----------    ----------")
                            for k in range(len(atom_octa)):
                                echo_logs(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                          .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1], coord_octa[k][2]))
                            echo_logs(self, "")

                        elif count > 1:
                            echo_outs(self, "File {0}: {1}".format(i + 1, file_name))
                            echo_outs(self, "Metal center atom no. {0} : {1}".format(j + 1, atom_octa[0]))
                            echo_outs(self, "Atom                       Cartesian coordinate")
                            for k in range(len(atom_octa)):
                                echo_outs(self, " {0:>2}      {1:14.9f}  {2:14.9f}  {3:14.9f}"
                                          .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1], coord_octa[k][2]))
                            echo_outs(self, "")

                            echo_logs(self, "File {0}: {1}".format(i + 1, file_name))
                            echo_logs(self, "Info: Show Cartesian coordinates of extracted octahedral structure")
                            echo_logs(self, "")
                            echo_logs(self, "      Atom        X             Y             Z")
                            echo_logs(self, "      ----    ----------    ----------    ----------")
                            for k in range(len(atom_octa)):
                                echo_logs(self, "       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                                          .format(atom_octa[k], coord_octa[k][0], coord_octa[k][1], coord_octa[k][2]))
                            echo_logs(self, "")

            except UnboundLocalError:
                echo_logs(self, "Error: No input file")
                return 1

        except IndexError:
            echo_logs(self, "Error: No input file")
            return 1

    def save_results(self):
        """
        Save results as output file (*txt).

        Returns
        -------
        None

        """
        echo_logs(self, "Info: Save results as an output file")

        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt", title="Save results",
                                     filetypes=(("TXT File", "*.txt"),
                                                ("All Files", "*.*")))

        if f is None:
            echo_logs(self, "Warning: Cancelled save file")
            return 0

        f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.\n")
        f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
        f.write("This is free software, and you are welcome to redistribute it under\n")
        f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n")
        f.write("\n")
        f.write("OctaDist {0} {1}: Octahedral Distortion Analysis\n".format(octadist_gui.__version__,
                                                                            octadist_gui.__release__))
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

        popup.info_save_results(self, f.name)

    def calc_all_param(self):
        """
        Calculate distortion parameters.

        Returns
        -------
        None

        """
        if not self.check_metal:
            popup.err_no_metal(self)
            return 1

        if len(self.atom_coord_octa) >= 1:
            self.clear_param_box()
        else:
            popup.err_no_file(self)
            return 1

        self.all_zeta, self.all_delta, self.all_sigma, self.all_theta, self.all_face = \
            calc.calc_all(self, self.atom_coord_octa)


def main():
    masters = tk.Tk()
    App = OctaDist(masters)
    masters.mainloop()


if __name__ == '__main__':
    main()
