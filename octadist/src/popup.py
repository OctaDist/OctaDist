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

from tkinter.messagebox import showinfo, showerror, showwarning


def err_no_file():
    """
    Show this error when having no any input files is loaded into program.

    """
    showerror("Error", "No input file. At least one input file must be loaded.")


def err_invalid_ftype(ftype):
    """
    Show this error popup when file type is not supported by the program.

    Parameters
    ----------
    ftype : str
        File type of submitted file.

    """
    showerror("Error", f"Invalid {ftype} file format.\n\n"
                       "The complex must have at least 1 metal atom and 6 ligand atoms.")


def err_no_coord():
    """
    Show this error popup when the program cannot read the atomic coordinates of complex
    inside the file or cannot extract the coordinates from the complex.

    This will happen only if the input has no the proper format of atomic coordinates.

    """
    showerror("Error", "No coordinate of a molecule. Please make sure the input file format is correct.")


def err_less_ligands():
    """
    Show this error popup when the complex has ligand atoms less that six.

    """
    showerror("Error", "Number of ligand atoms in the complex is less than six. "
                       "Please check the metal-ligand bond cutoff if the value is set properly.")


def err_no_metal():
    """
    Show this error popup when the complex has no transition metal atom.

    """
    showerror("Error", "Cannot proceed calculation. Your current structure has no transition metal.\n\n"
                       "The complex must have at least one transition metal.")


def err_no_calc():
    """
    Show this error popup when the user requests function that the results are required,
    but the results have not been computed yet.

    """
    showerror("Error", "No results. Click \"Compute\" to calculate octahedral distortion parameters.")


def err_only_2_files():
    """
    Show this error popup when having not uploaded two complexes
    for using the RMSD function.

    """
    showerror("Error", "You must load only two complexes for computing RMSD.")


def err_not_equal_atom():
    """
    Show this error popup when the total number of atoms of two complexes are not equal.

    """
    showerror("Error", "The number of atoms in structure 1 and structure 2 are not the same.")


def err_atom_not_match(line):
    """
    show this error popup when atomic symbol of two similar complexes does not match.

    Parameters
    ----------
    line : int
        The line number that atomic symbol does not match.

    """
    showerror("Error", f"Atomic symbol not match at line {line}.")


def err_many_files():
    """
    Show this error popup when user has loaded too many files.

    """
    showerror("Error", "You must load only one input file.")


def err_wrong_format():
    """
    Show this error popup when user has loaded the file that is not supported by OctaDist.

    """
    showerror("Error", "Could not read file.\n\n"
                       "Input file format is not supported by the current version of OctaDist.")


def err_no_editor():
    """
    Show this error popup if text editor path is empty.

    """
    showerror("Error", "No text editor.\n\n"
                       "Text editor path is empty. Go to setting and browse a new text editor.")


def err_cannot_update():
    """
    Show this error popup when the program cannot detect the operating system of
    the machine that user is using.

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

    """
    showinfo("Info", f"Data has been saved to {file}")


def info_new_update():
    """
    Show this info popup when new version is available for update.

    """
    showinfo("Info", "New updates available!")


def info_using_dev():
    """
    Show this info popup if user is using a development build version.

    """
    showinfo("Info", "You are using a development build version!")


def info_no_update():
    """
    Show this info popup if program is the latest version.

    """
    showinfo("Info", "You already have the latest version.")


def warn_no_metal():
    """
    Show this warning popup if no transition metal was found.

    """
    showwarning("Warning", "No transition metal in your input file.")


def warn_not_octa():
    """
    Show this warning popup if the complex is non-octahedral structure.

    """
    showwarning("Warning", "Non-octahedral complex detected.")
