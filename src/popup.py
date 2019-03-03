"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import showwarning
import webbrowser
import main


def header(self):
    """Show welcome message when program is opened
    """
    main.print_stdout(self, "==========================================================")
    main.print_stdout(self, "OctaDist {0} : https://octadist.github.io".format(main.program_version))
    main.print_stdout(self, "A Program for determining the structural distortion of the octahedral complexes")
    main.print_stdout(self, "==========================================================")
    main.print_stdout(self, "")


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def err_no_file(self):
    main.print_stdout(self, "Error: No input file. At least one input file must be loaded.")
    showerror("Error", "No input file. At least one input file must be loaded.")


def err_no_coord(self):
    main.print_stdout(self, "Error: No coordinate of a molecule.")
    showerror("Error", "No coordinate of a molecule. Please make sure the input file format is correct.")


def err_no_calc(self):
    main.print_stdout(self, "Error: No computational results.")
    showerror("Error", "No results. Click \"Compute parameters\" to calculate octahedral distortion parameters.")


def err_many_files(self):
    main.print_stdout(self, "Error: You must load only one input file.")
    showerror("Error", "You must load only one input file.")


def wrong_format_error(self):
    main.print_stdout(self, "Error: Input file format is not supported.")
    showerror("Error", "Input file format is not supported.")


def err_not_octa(self):
    main.print_stdout(self, "Error: Cannot determine the octahedral structure from your input complex.")
    showerror("Error", "Cannot determine the octahedral structure from your input complex.")


def warn_no_metal(self):
    main.print_stdout(self, "Warning: No transition metal in your input file.")
    showwarning("Warning", "No transition metal in your input file.")


def warn_many_metals(self):
    main.print_stdout(self, "Warning: The complex contains too many transition metal and/or heavy metal")
    main.print_stdout(self, "         Please clarify your complex carefully.")
    main.print_stdout(self, "         It would help OctaDist to determine the metal center atom correctly.")
    showwarning("Warning",
                "The complex contains too many transition metal and/or heavy metal.\n\n"       
                "Please clarify the complex to help OctaDist to determine metal center atom correctly.\n\n"
                "Otherwise, go to https://octadist.github.io for preparation of input file.\n")


class ShowHelp:
    def __init__(self, master):
        """Show program help
        """
        self.master = master
        self.master.title("Program Help")
        self.master.geometry("550x550")
        self.master.option_add("*Font", "Arial 10")
        self.frame = tk.Frame(self.master)
        self.frame.grid()

        # Usage
        self.lbl = tk.Label(self.frame, text="Usage:")
        self.lbl.grid(sticky=tk.W, row=0)
        msg_help_1 = "1. Browse input file\n" \
                     "2. Compute distortion parameters\n" \
                     "3. Check results\n" \
                     "4. File → Save as\n"
        self.msg = tk.Message(self.frame, text=msg_help_1, width="450")
        self.msg.grid(sticky=tk.W, row=1)

        # XYZ file format
        self.lbl = tk.Label(self.frame, text="Supported input: XYZ file format (*.xyz)")
        self.lbl.grid(sticky=tk.W, row=2)
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
        self.msg = tk.Message(self.frame, text=msg_help_2, width="450")
        self.msg.grid(sticky=tk.W, row=3, column=0)

        self.lbl = tk.Label(self.frame, text="Example of input file is available at the following website:")
        self.lbl.grid(sticky=tk.W, row=5, columnspan=2)
        link = "https://github.com/OctaDist/OctaDist/tree/master/test\n"
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


def show_about(self):
    """Show author info
    """
    main.print_stdout(self, "Info: Show program information")

    text = "OctaDist version {0}\n" \
           "\n" \
           "Authors: Rangsiman Ketkaew, Yuthana Tantirungrotechai,\n" \
           "David J. Harding, Phimphaka Harding, and Mathieu Marchivie.\n" \
           "\n" \
           "Website: https://octadist.github.io\n" \
           "\n" \
           "Please cite this project if you use OctaDist for scientific publication." \
        .format(main.program_version)
    showinfo("About program", text)


def show_license(self):
    """Show license info
    """
    main.print_stdout(self, "Info: Show program license information")

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
        .format(main.program_version)
    showinfo("License", text)
