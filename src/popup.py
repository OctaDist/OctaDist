"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import tkinter as tk
from tkinter.messagebox import showinfo
import webbrowser
from main import program_version


def welcome():
    """Show welcome message
    """
    print("\n OctaDist Copyright (C) 2019  Rangsiman Ketkaew  (rangsiman1993@gmail.com)")
    print(" This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.")
    print(" This is free software, and you are welcome to redistribute it under")
    print(" certain conditions; see <https://www.gnu.org/licenses/> for details.\n")
    print("     ==============================================================")
    print("                              OctaDist %s\n" % program_version)
    print("                     OCTAHEDRAL DISTORTION ANALYSIS")
    print("                     ------------------------------")
    print("          A PROGRAM FOR DETERMINING THE STRUCTURAL DISTORTION")
    print("                       OF THE OCTAHEDRAL STRUCTURE\n")
    print("              https://github.com/rangsimanketkaew/OctaDist")
    print("     ==============================================================\n")


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def nofile_error():
    """Show error when opening file twice
    """
    print("Error: No input file")
    showinfo("Error", "No input file.")


def nocoord_error():
    """Show error when opening file twice
    """
    print("Error: No coordinate of a molecule")
    showinfo("Error", "No coordinate of a molecule. Please make sure the input file format is correct.")


def nocalc_error():
    """Show error when save file but no any parameters computed
    """
    print("Error: No results")
    showinfo("Error", "No results. Click \"Compute parameters\" to calculate octahedral distortion parameters.")


def only_single_file_error():
    """Show error when user request function that not supported for multiple files mode
    """
    print("Error: This function only supports single file mode")
    showinfo("Error", "This function only supports single input file.")


def only_mult_file_error():
    """Show error when user request function that not supported for single file mode
    """
    print("Error: This function only supports multiple files mode")
    showinfo("Error", "This function only supports multiple input files.")


def wrong_format_error():
    """Show error when opening file twice
    """
    print("Error: Input file format is not supported")
    showinfo("Error", "Input file format is not supported.")


class ShowHelp:
    def __init__(self, master):
        """Show program help
        """
        self.master = master
        self.master.title("Program Help")
        self.master.geometry("550x600")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        print("Info: Show program help")

        # Usage
        self.lbl = tk.Label(self.frame, text="Usage:")
        self.lbl.grid(sticky=tk.W, row=0)
        msg_help_1 = "1. Browse file\n" \
                     "2. Compute parameters\n" \
                     "3. Check results\n" \
                     "4. File → Save as\n"
        self.msg = tk.Message(self.frame, text=msg_help_1, width="450")
        self.msg.grid(sticky=tk.W, row=1)

        # XYZ file format
        self.lbl = tk.Label(self.frame, text="Supported input formats:")
        self.lbl.grid(sticky=tk.W, row=2)
        self.lbl = tk.Label(self.frame, text="XYZ file format (*.xyz):")
        self.lbl.grid(sticky=tk.W, row=3, column=0)
        msg_help_2 = " <number of atoms\n" \
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
        self.msg = tk.Message(self.frame, text=msg_help_2, width="450")
        self.msg.grid(sticky=tk.W, row=4, column=0)

        self.lbl = tk.Label(self.frame, text="Example of input file is available at the following website:")
        self.lbl.grid(sticky=tk.W, row=5, columnspan=2)
        link = "https://github.com/rangsimanketkaew/OctaDist/tree/master/test\n"
        self.lbl_link = tk.Label(self.frame, foreground="blue", text=link, cursor="hand2")
        self.lbl_link.grid(sticky=tk.W, pady="5", row=6, columnspan=2)
        self.lbl_link.bind("<Button-1>", callback)

        # References
        self.lbl = tk.Label(self.frame, text="References:")
        self.lbl.grid(sticky=tk.W, row=7, columnspan=2)
        msg_help_3 = "1. J. A. Alonso, M. J. Martı´nez-Lope, M. T. Casais, M. T. Ferna´ndez-Dı´az\n" \
                     "   Inorg. Chem. 2000, 39, 917-923\n" \
                     "2. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson\n" \
                     "   Inorg. Chem. 1996, 35, 2100.\n" \
                     "3. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau\n" \
                     "   Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
        self.msg = tk.Message(self.frame, text=msg_help_3, width="450")
        self.msg.grid(sticky=tk.W, row=8, columnspan=2)


def show_about():
    """Show author info
    """
    print("Info: Show program information")

    text = "OctaDist version {}\n" \
           "\n" \
           "Programming:\n" \
           "Rangsiman Ketkaew\n" \
           "Computational Chemistry Research Unit\n" \
           "Department of Chemistry\n" \
           "Faculty of Science and Technology\n" \
           "Thammasat University, Pathum Thani, 12120 Thailand\n" \
           "\n" \
           "Contact:\n" \
           "E-mail: rangsiman1993@gmail.com\n" \
           "Website: https://github.com/rangsimanketkaew/OctaDist" \
        .format(program_version)
    showinfo("About program", text)


def show_license():
    """Show license info
    """
    print("Info: Show program license information")

    text = "OctaDist {} Copyright (C) 2019  Rangsiman Ketkaew\n\n" \
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
        .format(program_version)
    showinfo("License", text)
