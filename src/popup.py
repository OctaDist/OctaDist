"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from tkinter import *
from tkinter.messagebox import showinfo
import webbrowser


program_version = 2.0


def welcome():

    print("")
    print(" OctaDist Copyright (C) 2019  Rangsiman Ketkaew  (rangsiman1993@gmail.com)")
    print(" This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.")
    print(" This is free software, and you are welcome to redistribute it under")
    print(" certain conditions; see <https://www.gnu.org/licenses/> for details.")
    print("")
    print("       ==============================================================")
    print("                                OctaDist {}".format(program_version))
    print("")
    print("                       OCTAHEDRAL DISTORTION ANALYSIS")
    print("                       ------------------------------")
    print("           A PROGRAM FOR DETERMINING THE STRUCTURAL PARAMETERS OF")
    print("                     THE DISTORTED OCTAHEDRAL STRUCTURE")
    print("")
    print("                            by Rangsiman Ketkaew")
    print("                             January 22nd, 2019")
    print("                https://github.com/rangsimanketkaew/OctaDist")
    print("       ==============================================================")
    print("")


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def nofile_error():
    """Show error message when opening file twice
    """
    print("Error: No input file")

    showinfo("Error", "No input file. Click \"Browse file\" to load a new file.")


def nocoord_error():
    """Show error message when opening file twice
    """
    print("Error: No coordinate of a molecule")

    showinfo("Error", "No coordinate of a molecule. Please make sure that the input file format is correct. "
                      "Click \"Browse file\" to load a new file.")


def nocalc_error():
    """Show error message when save file but no any parameters computed
    """
    print("Error: No results")

    showinfo("Error", "No results. Click \"Compute parameters\" to calculate octahedral distortion parameters.")


def nosupport_mult():
    """Show error message when multiple files are selected and call draw function
    """
    print("Error: Cannot use graphical drawing function if multiple files are selected")

    showinfo("Error", "Cannot use graphical drawing function if multiple files are selected.")


def wrong_format():
    """Show error message when opening file twice
    """
    print("Error: Wrong input format")

    showinfo("Error", "Your input file format is not supported.")


def help():
    """Open program help page
        - Usage
        - Input file format
        - References
    """

    print("Command: Show program help")

    hp = Tk()
    # hp.overrideredirect(1)
    hp.option_add("*Font", "Arial 10")
    hp.geometry("650x570")
    hp.title("Program Help")

    # Usage
    lbl = Label(hp, text="Usage:")
    lbl.grid(sticky=W, row=0)
    msg_help_1 = "1. Browse file\n" \
                 "2. Compute parameters\n" \
                 "3. Check results\n" \
                 "4. File → Save as ..\n"
    msg = Message(hp, text=msg_help_1, width="450")
    # msg.config(font=("Arial 10"))
    msg.grid(sticky=W, row=1)

    # XYZ file format
    lbl = Label(hp, text="Supported input formats:")
    lbl.grid(sticky=W, row=2)
    lbl = Label(hp, text="XYZ file format (*.xyz):")
    lbl.grid(sticky=W, row=3, column=0)
    msg_help_2 = " <number of atoms\n" \
                 " comment line\n" \
                 " <Metal center 0>  <X>  <Y>  <Z>      \n" \
                 " <Ligand atom 1>  <X>  <Y>  <Z>      \n" \
                 " <Ligand atom 2>  <X>  <Y>  <Z>      \n" \
                 " <Ligand atom 3>  <X>  <Y>  <Z>      \n" \
                 " <Ligand atom 4>  <X>  <Y>  <Z>      \n" \
                 " <Ligand atom 5>  <X>  <Y>  <Z>      \n" \
                 " <Ligand atom 6>  <X>  <Y>  <Z>      \n" \
                 " <optional>\n" \
                 " ...\n"
    msg = Message(hp, text=msg_help_2, width="450")
    msg.grid(sticky=W, row=4, column=0)

    lbl = Label(hp, text="Example: the Fe(H2O)6 can be described in XYZ by following:")
    lbl.grid(sticky=W, row=3, column=1)
    msg_help_2 = " 56\n" \
                 "\n" \
                 " Fe    0.20069808   0.70680627   0.00000000\n" \
                 "  O    1.66069810   0.70680627   0.00000000\n" \
                 "  O    0.20069808   2.16680630   0.00000000\n" \
                 "  O    0.20069808   0.70680627   1.46000000\n" \
                 "  O   -1.25930190   0.70680627   0.00000000\n" \
                 "  O    0.20069808  -0.75319373   0.00000000\n" \
                 "  O    0.20069808   0.70680627  -1.46000000\n" \
                 " ..."
    msg = Message(hp, text=msg_help_2)
    msg.grid(sticky=W, row=4, column=1)

    lbl = Label(hp, text="Example of input file is available at the following website:")
    lbl.grid(sticky=W, row=5, columnspan=2)
    link = "https://github.com/rangsimanketkaew/OctaDist/tree/master/test\n"
    lbl_link = Label(hp, foreground="blue", text=link, cursor="hand2")
    lbl_link.grid(sticky=W, pady="5", row=6, columnspan=2)
    lbl_link.bind("<Button-1>", callback)

    # References
    lbl = Label(hp, text="References:")
    lbl.grid(sticky=W, row=7, columnspan=2)
    msg_help_3 = "1. J. A. Alonso, M. J. Martı´nez-Lope, M. T. Casais, M. T. Ferna´ndez-Dı´az\n" \
                 "   Inorg. Chem. 2000, 39, 917-923\n" \
                 "2. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson\n" \
                 "   Inorg. Chem. 1996, 35, 2100.\n" \
                 "3. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau\n" \
                 "   Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
    msg = Message(hp, text=msg_help_3, width="450")
    msg.grid(sticky=W, row=8, columnspan=2)

    hp.mainloop()


def about():
    """Show author information
    """
    print("Command: Show program information")

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


def license():
    """Show program info
    """
    print("Command: Show program license information")

    text = "OctaDist {} Copyright (C) 2019  Rangsiman Ketkaew\n" \
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
           "along with this program. If not, see <https://www.gnu.org/licenses/>." \
        .format(program_version)
    showinfo("License", text)

