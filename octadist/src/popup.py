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
    """Show this error when no input files uploaded/opened.
    """
    showerror("Error", "No input file. You need to upload at least one input file.")


def err_invalid_ftype():
    """Show this error popup when file type is not supported by the program.
    """
    showerror(
        "Error", f"Invalid input file format.\n\n"
        "Supported formats are *.cif, *.xyz, *.out, *.log.\n"
        "Also note that molecule must contain one metal atom and six ligand atoms.",
    )


def err_no_coord(i):
    """Show this error popup when the program cannot read the atomic coordinates of complex
    inside the file or cannot extract the coordinates from the complex.

    This will happen only if the input has no the proper format of atomic coordinates.

    Parameters
    ----------
    i : int
        Number of file.
    """
    showerror(
        "Error", f"File no. {i} Atomic coordinates not found.\n\n"
        "Please make sure that the input file is correct.",
    )


def err_less_ligands(i):
    """Show this error popup when the complex has ligand atoms less that six atoms.

    Parameters
    ----------
    i : int
        Number of file.

    """
    showerror(
        "Error", f"File no. {i} has ligand atoms less than six atoms.\n\n"
        "Please check if some ligand atoms are too far away from metal atom,"
        "if so, please check the metal-ligand bond cutoff and set this parameter properly.",
    )


def err_no_metal():
    """Show this error popup when the complex has no transition metal atom.
    """
    showerror(
        "Error", "Cannot proceed calculation. Transition metal not found in your current structure.\n\n"
        "Molecule must contain at least one transition metal.",
    )


def err_no_calc():
    """Show this error popup when the user requests function that the results are required,
    but the results have not been computed yet.
    """
    showerror(
        "Error", 'No results. Click "Compute" to calculate distortion parameters of the molecule.',
    )


def err_only_2_files():
    """Show this error popup when having not uploaded two complexes
    for using the RMSD function.
    """
    showerror("Error", "You must load only two complexes for computing RMSD.")


def err_not_equal_atom():
    """Show this error popup when the total number of atoms of two complexes are not equal.
    """
    showerror(
        "Error", "The number of atoms in structure 1 and structure 2 are not equal."
    )


def err_atom_not_match(line):
    """show this error popup when atomic symbol of two similar complexes does not match.

    Parameters
    ----------
    line : int
        The line number that atomic symbol does not match.
    """
    showerror("Error", f"Atomic symbol not match at line {line}.")


def err_many_files():
    """Show this error popup when user has loaded too many files.
    """
    showerror("Error", "Too many input files. You can load only one input file.")


def err_wrong_format():
    """Show this error popup when user has loaded the file that is not supported by OctaDist.
    """
    showerror(
        "Error", "Could not read file. Input file format is not supported yet by the current version of OctaDist.\n\n"
        "However, please contact OctaDist developer if you have any further questions or need help."
    )


def err_no_editor():
    """Show this error popup if text editor path is empty.
    """
    showerror("Error", "Text editor path is empty. Go to program setting and browse a new text editor.")


def err_visualizer_not_found():
    """Show this error popup if user-defined visualizer is not available.
    """
    showerror("Error", "Molecular visualizer that you specified is not supported. "
    "Please choose either Matplotlib or Plotly.")


def err_cannot_update():
    """Show this error popup when the program cannot detect the operating system that the user is using.
    """
    showerror(
        "Error", "Cannot download an installer of a new version.\n\n"
        "Please contact OctaDist developer for further help."
    )


def info_save_results(file):
    """show this info popup when an output file has been saved successfully.

    Parameters
    ----------
    file : str
        Absolute or full path of saved output file.
    """
    showinfo("Info", f"Data has been saved to {file}")


def info_new_update():
    """Show this info popup when new version is available for update.
    """
    showinfo("Info", "New release available! Please upgrade your OctaDist. :)")


def info_using_dev():
    """Show this info popup if user is using a development build version.
    """
    showinfo("Info", "You are using a development build version!")


def info_no_update():
    """Show this info popup if program is the latest version.
    """
    showinfo("Info", "You already have the latest version.")


def warn_no_metal(i):
    """Show this warning popup if no transition metal was found.

    Parameters
    ----------
    i : int
        Number of file.
    """
    showwarning("Warning", f"File no. {i} transition metal not found in your molecule.")


def warn_not_octa():
    """Show this warning popup if the complex is non-octahedral structure.
    """
    showwarning("Warning", "Non-octahedral structure detected!")
