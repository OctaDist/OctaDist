from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo

program_version = 1.3


def nofile_error():
    """Show error message when opening file twice
    """
    print("Error: No input file")

    showinfo("Error", "No input file. Click \"Browse file\" to load a new file.")


def nocalc_error():
    """Show error message when save file but no any parameters computed
    """
    print("Error: No results")

    showinfo("Error", "No results. Click \"Compute parameters\" to calculate octahedral distortion parameters.")


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
    hp.geometry("500x450+750+200")
    hp.title("Program Help")

    # Usage
    lbl = Label(hp, text="Usage:")
    lbl.pack(anchor=W)
    msg_help_1 = "1. Browse file\n" \
                 "2. Compute parameters\n" \
                 "3. Check results\n" \
                 "4. File → Save as ..\n"
    msg = Message(hp, text=msg_help_1, width="450")
    # msg.config(font=("Arial 10"))
    msg.pack(anchor=W)

    # Input format
    lbl = Label(hp, text="Supported input file format:")
    lbl.pack(anchor=W)
    msg_help_2 = "  <Metal center 0>  <X>  <Y>  <Z>\n" \
                 "  <Ligand atom 1>  <X>  <Y>  <Z>\n" \
                 "  <Ligand atom 2>  <X>  <Y>  <Z>\n" \
                 "  <Ligand atom 3>  <X>  <Y>  <Z>\n" \
                 "  <Ligand atom 4>  <X>  <Y>  <Z>\n" \
                 "  <Ligand atom 5>  <X>  <Y>  <Z>\n" \
                 "  <Ligand atom 6>  <X>  <Y>  <Z>\n" \
                 "  <optional>\n" \
                 "  ...\n"
    msg = Message(hp, text=msg_help_2, width="450")
    msg.config(font="Arial 10 italic")
    msg.pack(anchor=W)

    # References
    lbl = Label(hp, text="References:")
    lbl.pack(anchor=W)
    msg_help_3 = "1. J. A. Alonso, M. J. Martı´nez-Lope, M. T. Casais, M. T. Ferna´ndez-Dı´az\n" \
                 "   Inorg. Chem. 2000, 39, 917-923\n" \
                 "2. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson\n" \
                 "   Inorg. Chem. 1996, 35, 2100.\n" \
                 "3. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau\n" \
                 "   Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
    msg = Message(hp, text=msg_help_3, width="450")
    # msg.config(font=("Arial 10"))
    msg.pack(anchor=W)

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