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

import tkinter as tk
import webbrowser
from tkinter.messagebox import showinfo, showerror, showwarning

import octadist_gui
from octadist_gui.src import echo_logs


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def show_help(self):
    """
    Show program help.

    1. Simple usage
    2. XYZ file format
    3. References

    """
    master = tk.Toplevel(self)
    master.title("Program Help")
    master.geometry("550x600")
    master.option_add("*Font", "Arial 10")
    frame = tk.Frame(master)
    frame.grid()

    # Usage
    lbl = tk.Label(frame, text="Usage:")
    lbl.grid(sticky=tk.W, row=0)
    msg_help_1 = "1. Browse input file\n" \
                 "2. Compute distortion parameters\n" \
                 "3. Check results\n" \
                 "4. File → Save results\n"
    msg = tk.Message(frame, text=msg_help_1, width="450")
    msg.grid(sticky=tk.W, row=1)

    # XYZ file format
    lbl = tk.Label(frame, text="Supported input: XYZ file format (*.xyz)")
    lbl.grid(sticky=tk.W, row=2)
    msg_help_2 = " <number of atoms>\n" \
                 " comment line\n" \
                 " <Metal center 0>  <X>  <Y>  <Z>\n" \
                 " <Ligand atom 1>  <X>  <Y>  <Z>\n" \
                 " <Ligand atom 2>  <X>  <Y>  <Z>\n" \
                 " <Ligand atom 3>  <X>  <Y>  <Z>\n" \
                 " <Ligand atom 4>  <X>  <Y>  <Z>\n" \
                 " <Ligand atom 5>  <X>  <Y>  <Z>\n" \
                 " <Ligand atom 6>  <X>  <Y>  <Z>\n" \
                 " <optional>\n" \
                 " ...\n"
    msg = tk.Message(frame, text=msg_help_2, width="450")
    msg.grid(sticky=tk.W, row=3, column=0)

    lbl = tk.Label(frame, text="Example of input file is available at the following website:")
    lbl.grid(sticky=tk.W, row=5, columnspan=2)
    link = "https://github.com/OctaDist/OctaDist/tree/master/example-input\n"
    lbl_link = tk.Label(frame, foreground="blue", text=link, cursor="hand2")
    lbl_link.grid(sticky=tk.W, pady="5", row=6, columnspan=2)
    lbl_link.bind("<Button-1>", callback)

    # References
    lbl = tk.Label(frame, text="References:")
    lbl.grid(sticky=tk.W, row=7, columnspan=2)
    msg_help_3 = "1. M. Buron-Le Cointe, J. H´ebert, C. Bald´e, N. Moisan, L. Toupet,\n" \
                 "   P. Guionneau, J. F. L´etard, E. Freysz, H. Cailleau, and E. Collet\n" \
                 "   Physical Review B 2012, 85, 064114.\n" \
                 "2. J. A. Alonso, M. J. Martı´nez-Lope, M. T. Casais, M. T. Ferna´ndez-Dı´az\n" \
                 "   Inorg. Chem. 2000, 39, 917-923.\n" \
                 "3. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson\n" \
                 "   Inorg. Chem. 1996, 35, 2100.\n" \
                 "4. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau\n" \
                 "   Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
    msg = tk.Message(frame, text=msg_help_3, width="450")
    msg.grid(sticky=tk.W, row=8, columnspan=2)


def show_about(self):
    """
    Show author info

    1. Name of authors
    2. Official program website
    3. Citation

    """
    echo_logs(self, "Info: Show program information")
    text = "OctaDist version {0} ({1})\n" \
           "\n" \
           "Authors: {2}\n" \
           "\n" \
           "Website: {3}\n" \
           "\n" \
           "Please cite this project if you use OctaDist for scientific publication."\
        .format(octadist_gui.__version__, octadist_gui.__release__,
                octadist_gui.__author_full__, octadist_gui.__website__)
    showinfo("About program", text)


def show_license(self):
    """
    Show license info.

    GNU General Public License version 3.0.

    """
    echo_logs(self, "Info: Show program license information")

    text = "OctaDist {0} Copyright (C) 2019  Rangsiman Ketkaew et al.\n\n" \
           "This program is free software: you can redistribute it " \
           "and/or modify it under the terms of the GNU General Public " \
           "License as published by the Free Software Foundation, either " \
           "version 3 of the License, or (at your option) any later version.\n\n" \
           "This program is distributed in the hope that it will be useful, " \
           "but WITHOUT ANY WARRANTY; without even the implied warranty " \
           "of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. " \
           "See the GNU General Public License for more details.\n\n" \
           "You should have received a copy of the GNU General Public License " \
           "along with this program. If not, see <https://www.gnu.org/licenses/>." \
        .format(octadist_gui.__version__)
    showinfo("License", text)


def err_no_file(self):
    echo_logs(self, "Error: No input file. At least one input file must be loaded.")
    showerror("Error", "No input file. At least one input file must be loaded.")


def err_invalid_ftype(self, ftype):
    """
    Show error popup:

    Show this error popup when file type is not supported by the program.

    Parameters
    ----------
    ftype : str
        File type of submitted file.

    Returns
    -------
    None

    """
    echo_logs(self, "Error: Invalid XYZ file format")
    showerror("Error", "Invalid {0} file format.\n\n"
                       "The complex must have at least 1 metal atom and 6 ligand atoms.".format(ftype))


def err_no_coord(self):
    echo_logs(self, "Error: No coordinate of a molecule.")
    showerror("Error", "No coordinate of a molecule. Please make sure the input file format is correct.")


def err_no_metal(self):
    echo_logs(self, "Error: Cannot calculate parameters.")
    showerror("Error", "Cannot calculate parameters. Your current structure has no metal atom.\n\n"
                       "Please upload new input structure that has at least one metal to proceed the calculation.")


def err_no_calc(self):
    echo_logs(self, "Error: No computational results.")
    showerror("Error", "No results. Click \"Compute\" to calculate octahedral distortion parameters.")


def err_only_2_files(self):
    echo_logs(self, "Error: You must load only two complexes for computing RMSD.")
    showerror("Error", "You must load only two complexes for computing RMSD.")


def err_not_equal_atom(self):
    echo_logs(self, "Error: The number of atoms in structure 1 and structure 2 are not the same.")
    showerror("Error", "The number of atoms in structure 1 and structure 2 are not the same.")


def err_atom_not_match(self, line):
    """
    Show error popup:

    show this error popup when atomic symbol of two similar complexes does not match.

    Parameters
    ----------
    line : int
        The line number that atomic symbol does not match.

    Returns
    -------
    None

    """
    echo_logs(self, "Error: Atomic symbol not match at line {0}.".format(line))
    showerror("Error", "Atomic symbol not match at line {0}.".format(line))


def err_many_files(self):
    echo_logs(self, "Error: You must load only one input file.")
    showerror("Error", "You must load only one input file.")


def err_wrong_format(self):
    echo_logs(self, "Error: Input file format is not supported.")
    showerror("Error", "Input file format is not supported.")


def err_cannot_update(self):
    echo_logs(self, "Error: Cannot download an installer of a new version.")
    showerror("Error", "Cannot download an installer of a new version.\n\n"
                       "Please contact OctaDist development team for further help.")


def info_save_results(self, file):
    """
    Show info popup:

    show this info popup when output file has been saved successfully.

    Parameters
    ----------
    file : str
        Absolute or full path of saved output file.

    Returns
    -------
    None

    """
    echo_logs(self, "Info: Data has been saved to \"{0}\"".format(file))
    showinfo("Info", "Data has been saved to {0}".format(file))


def info_update(self):
    echo_logs(self, "Info: New version of OctaDist is available for update now!")
    echo_logs(self, "      Visit {0} for downloading a new version of OctaDist.".format(octadist_gui.__website__))
    showinfo("Info", "New updates available!")


def info_no_update(self):
    echo_logs(self, "Info: You already have the latest version of OctaDist.")
    showinfo("Info", "You already have the latest version of OctaDist.")


def warn_no_metal(self):
    echo_logs(self, "Warning: No transition metal in your input file.")
    showwarning("Warning", "No transition metal in your input file.")


def warn_not_octa(self):
    echo_logs(self, "Warning: The complex is non-octahedral complex")
    showwarning("Warning", "Non-octahedral complex detected.")
