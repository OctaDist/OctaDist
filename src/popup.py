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
from src import main


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


def info_save_results(self, file):
    main.print_stdout(self, "Info: Data has been saved to \"{0}\"".format(file))
    showinfo("Info", "Data has been saved to {0}".format(file))


def err_no_file(self):
    main.print_stdout(self, "Error: No input file. At least one input file must be loaded.")
    showerror("Error", "No input file. At least one input file must be loaded.")


def err_no_coord(self):
    main.print_stdout(self, "Error: No coordinate of a molecule.")
    showerror("Error", "No coordinate of a molecule. Please make sure the input file format is correct.")


def err_no_calc(self):
    main.print_stdout(self, "Error: No computational results.")
    showerror("Error", "No results. Click \"Compute\" to calculate octahedral distortion parameters.")


def err_many_files(self):
    main.print_stdout(self, "Error: You must load only one input file.")
    showerror("Error", "You must load only one input file.")


def error_wrong_format(self):
    main.print_stdout(self, "Error: Input file format is not supported.")
    showerror("Error", "Input file format is not supported.")


def warn_no_metal(self):
    main.print_stdout(self, "Warning: No transition metal in your input file.")
    showwarning("Warning", "No transition metal in your input file.")


def show_help(self):
    """Show program help
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
    link = "https://github.com/OctaDist/OctaDist/tree/master/test\n"
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
    """Show author info
    """
    main.print_stdout(self, "Info: Show program information")

    text = "OctaDist version {0} {1}\n" \
           "\n" \
           "Authors: Rangsiman Ketkaew, Yuthana Tantirungrotechai,\n" \
           "David J. Harding, Phimphaka Harding, and Mathieu Marchivie.\n" \
           "\n" \
           "Website: https://octadist.github.io\n" \
           "\n" \
           "Please cite this project if you use OctaDist for scientific publication." \
        .format(main.program_version, main.program_revision)
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
