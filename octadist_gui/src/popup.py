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


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def show_help(self):
    """
    Show program help on a sub-window.

    1. Simple usage
    2. XYZ file format
    3. References

    Returns
    -------
    None : None

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


def show_about():
    """
    Show author details on a sub-window.

    1. Name of authors
    2. Official program website
    3. Citation

    Returns
    -------
    None : None

    """
    text = f"OctaDist version {octadist_gui.__version__} ({octadist_gui.__release__})\n" \
           f"\n" \
           f"Authors: {octadist_gui.__author_full__}.\n" \
           f"\n" \
           f"Website: {octadist_gui.__website__}\n" \
           f"\n" \
           f"Please cite this project if you use OctaDist for scientific publication."

    showinfo("About program", text)


def show_license():
    """
    Show license details on a sub-window.

    GNU General Public License version 3.0.

    Returns
    -------
    None : None

    """
    text = "OctaDist {0} Copyright (C) 2019  Rangsiman Ketkaew et al.\n" \
           "\n" \
           "This program is free software: you can redistribute it " \
           "and/or modify it under the terms of the GNU General Public " \
           "License as published by the Free Software Foundation, either " \
           "version 3 of the License, or (at your option) any later version.\n" \
           "\n" \
           "This program is distributed in the hope that it will be useful, " \
           "but WITHOUT ANY WARRANTY; without even the implied warranty " \
           "of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. " \
           "See the GNU General Public License for more details.\n" \
           "\n" \
           "You should have received a copy of the GNU General Public License " \
           "along with this program. If not, see <https://www.gnu.org/licenses/>."\
        .format(octadist_gui.__version__)
    showinfo("License", text)


def err_no_file():
    """
    Show this error when having no any input files is loaded into program.

    Returns
    -------
    None : None

    """
    showerror("Error", "No input file. At least one input file must be loaded.")


def err_invalid_ftype(ftype):
    """
    Show this error popup when file type is not supported by the program.

    Parameters
    ----------
    ftype : str
        File type of submitted file.

    Returns
    -------
    None : None

    """
    showerror("Error", f"Invalid {ftype} file format.\n\n"
                       "The complex must have at least 1 metal atom and 6 ligand atoms.")


def err_no_coord():
    """
    Show this error popup when the program cannot read the atomic coordinates of complex
    inside the file or cannot extract the coordinates from the complex.

    This will happen only if the input has no the proper format of atomic coordinates.

    Returns
    -------
    None : None

    """
    showerror("Error", "No coordinate of a molecule. Please make sure the input file format is correct.")


def err_less_ligands():
    """
    Show this error popup when the complex has ligand atoms less that six.

    Returns
    -------
    None : None

    """
    showerror("Error", "Number of ligand atoms in the complex is less than six. "
                       "Please check the metal-ligand bond cutoff if the value is set properly.")


def err_no_metal():
    """
    Show this error popup when the complex has no transition metal atom.

    Returns
    -------
    None : None

    """
    showerror("Error", "Cannot proceed calculation. Your current structure has no metal atom.\n\n"
                       "The complex must have at least one metal.")


def err_no_calc():
    """
    Show this error popup when the user requests function that the results are required,
    but the results have not been computed yet.

    Returns
    -------
    None : None

    """
    showerror("Error", "No results. Click \"Compute\" to calculate octahedral distortion parameters.")


def err_only_2_files():
    """
    Show this error popup when having not uploaded two complexes
    for using the RMSD function.

    Returns
    -------
    None : None

    """
    showerror("Error", "You must load only two complexes for computing RMSD.")


def err_not_equal_atom():
    """
    Show this error popup when the total number of atoms of two complexes are not equal.

    Returns
    -------
    None : None

    """
    showerror("Error", "The number of atoms in structure 1 and structure 2 are not the same.")


def err_atom_not_match(line):
    """
    show this error popup when atomic symbol of two similar complexes does not match.

    Parameters
    ----------
    line : int
        The line number that atomic symbol does not match.

    Returns
    -------
    None : None

    """
    showerror("Error", f"Atomic symbol not match at line {line}.")


def err_many_files():
    """
    Show this error popup when user has loaded too many files.

    Returns
    -------
    None : None

    """
    showerror("Error", "You must load only one input file.")


def err_wrong_format():
    """
    Show this error popup when user has loaded the file that is not supported by OctaDist.

    Returns
    -------
    None : None

    """
    showerror("Error", "Input file format is not supported.")


def err_cannot_update():
    """
    Show this error popup when the program cannot detect the operating system of
    the machine that user is using.

    Returns
    -------
    None : None

    """
    showerror("Error", "Cannot download an installer of a new version.\n\n"
                       "Please contact OctaDist development team for further help.")


def info_save_results(file):
    """
    Show info popup:

    show this info popup when output file has been saved successfully.

    Parameters
    ----------
    file : str
        Absolute or full path of saved output file.

    Returns
    -------
    None : None

    """
    showinfo("Info", f"Data has been saved to {file}")


def info_update():
    """
    Show this info popup when new version is available for update.

    Returns
    -------
    None : None

    """
    showinfo("Info", "New updates available!")


def info_no_update():
    """
    Show this info popup if program is the latest version.

    Returns
    -------
    None : None

    """
    showinfo("Info", "You already have the latest version of OctaDist.")


def warn_no_metal():
    """
    Show this warning popup if no transition metal was found.

    Returns
    -------
    None : None

    """
    showwarning("Warning", "No transition metal in your input file.")


def warn_not_octa():
    """
    Show this warning popup if the complex is non-octahedral structure.

    Returns
    -------
    None : None

    """
    showwarning("Warning", "Non-octahedral complex detected.")
