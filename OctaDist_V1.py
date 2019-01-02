"""
Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

----------------------------------------------------------------------
Octahedral Distortion Analysis v.1

Software website: www.github.com/rangsimanketkaew/octadist

Last modified: January 2018

This program, we use Python 3.7.2 and TkInter as GUI maker.
PyInstaller is used as executable compiler.
Written and tested on PyCharm 2018.3.3 (Community Edition) program

Author: Rangsiman Ketkaew
        Department of Chemistry,
        Faculty of Science and Technology,
        Thammasat University, Pathum Thani, 12120 Thailand
Contact: rangsiman1993@gmail.com
Personal website: https://sites.google.com/site/rangsiman1993
"""

import numpy as np
from math import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


# global variables
filename = ""
filedata = ""


def openfile():
    """Open file using Open Dialog
    This function also includes condition that user can open only
    *.xyz and *.txt files. Molecular coordinates must be cartesian coordinate format.
    """
    print("Command: Open input file")
    global filename
    global filedata

    # check if filename is empty
    if filename != "":
        popup_open_error()
        return 1

    """Open text file"""
    filename = askopenfilename(  # initialdir="C:/Users/",
        title="Choose input file",
        filetypes=(("XYZ File", "*.xyz"),
                   ("Text File", "*.txt"),
                   ("All Files", "*.*")))

    # Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(filename, 'r') as f:
            print("Open file: " + filename)
            print("Coordinate file:")
            textBox_1.insert(INSERT, f.read())
        with open(filename, 'r') as f:
            print(f.read())
        with open(filename, 'r') as f:
            filedata = f.read()
    except:
        print("No file exists")


def savefile():
    donothing()


def check_xyz():
    """Check if the input file chosen by user is XYZ format
    The first word of file must be positive integer.
    """
    f = open(filename, "r")
    line = f.readlines()[0]
    firstword = line.split(' ')[0]
    print(firstword)
    print(type(firstword))
    print(firstword.isdigit())

    if firstword.isdigit() == True:
        print("ddd")
    else:
        popup_wrong_format()
        clear_cache()


def get_coord():
    """get coordinate from text file.
    Molecular coordinates must be in XYZ (cartesian) format

    XZY Format
    ----------
    <number of atoms>
    comment line
    <element> <X> <Y> <Z>
    ...

    """

    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1

    # check if input file is xyz format
    # check_xyz()

    print("Command: Get XYZ coordinates")

    global atom_list
    global coord_list
    f = open(filename, "r")
    # read lines with skips first two lines
    line = f.readlines()[2:]
    f.close()
    atom_raw = []

    for l in line:
        # read only the 1st column, elements, and pass into array
        lst = l.split(' ')[0]
        atom_raw.append(lst)
    # remove multiple lines after the last element
    atom_list = atom_raw[0:6]
    print("Command: Show atom lists")
    print(atom_list)

    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> f.seek(0) <<
        2. use >> f = open(filename, "r") <<
    """
    f = open(filename, "r")
    # read lines with skips first two lines
    coord_raw = np.loadtxt(f, skiprows=2, usecols=[1, 2, 3])
    f.close()
    # get only coordinates of 1 central atom and 6 ligand atoms
    coord_list = coord_raw[0:7]
    print("Command: Show Coordinate lists")
    print(coord_list)

    """Return both lists of atom_list and coord_list. 
    To use list, just grab a tuple, and use >> atom_list, coord_list = get_coord() <<
    """
    return atom_list, coord_list


def prog_help():
    print("Command: Show program help")
    """Open program help page
        - Usage
        - XYZ file format
        - References
    """
    hp = Tk()
    # hp.overrideredirect(1)
    hp.option_add("*Font", "Segoe-UI 10")
    hp.geometry("450x450+750+200")
    hp.title("Program Help")

    # frame1 = Frame(hp, highlightbackground="Black", highlightthickness=10, bd="20")
    # frame1.pack()

    # Usage
    lbl = Label(hp, text="Usage:")
    lbl.pack(anchor=W)

    msg_Help_1 = "1. Click Browse file.\n" \
                 "2. Browse to file that contains coordinates of octahedral structure.\n" \
                 "3. Click Ok.\n" \
                 "4. Click Run.\n" \
                 "5. Check results.\n" \
                 "6. Go to menu bar. \n" \
                 "7. Click File --> Save as ..\n"
    msg = Message(hp, text=msg_Help_1, width="450")
    # msg.config(font=("Segoe-UI 10"))
    msg.pack(anchor=W)

    # XYZ file format
    lbl = Label(hp, text="XYZ file format:")
    lbl.pack(anchor=W)

    msg_Help_2 = "  <number of atoms>\n" \
                 "  comment line\n" \
                 "  <element 1> <X> <Y> <Z>\n" \
                 "  <element 2> <X> <Y> <Z>\n" \
                 "  <element 3> <X> <Y> <Z>\n" \
                 "  ...\n"
    msg = Message(hp, text=msg_Help_2, width="450")
    msg.config(font="Segoe-UI 10 italic")
    msg.pack(anchor=W)

    # References
    lbl = Label(hp, text="References:")
    lbl.pack(anchor=W)

    msg_Help_3 = "1. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson, \n" \
                 "    Inorg. Chem. 1996, 35, 2100.\n" \
                 "2. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau, \n" \
                 "    Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
    msg = Message(hp, text=msg_Help_3, width="450")
    # msg.config(font=("Segoe-UI 10"))
    msg.pack(anchor=W)

    hp.mainloop()


def clear_cache():
    """Clear cache and free variable"""
    print("Command: Clear cache")
    global filename
    global filedata

    filename = ""
    filedata = ""
    textBox_1.delete(1.0, END)


def quit_msg():
    print("Command: Quit program")
    """Confirm quitting, ask yes and no before quit"""
    qw = Tk()
    qw.overrideredirect(1)
    qw.geometry("200x75+650+400")

    frame1 = Frame(qw, highlightbackground="Black", highlightthickness=1, bd="2")
    frame1.pack()

    lbl = Label(frame1, text="Are you sure you want to quit?", font="Segoe-UI 10")
    lbl.pack()

    yes_btn = Button(frame1, text="Yes", bg="blue", fg="yellow", command=quit, width=10)
    yes_btn.pack(padx=10, pady=10, side=LEFT)

    no_btn = Button(frame1, text="No", bg="blue", fg="yellow", command=qw.destroy, width=10)
    no_btn.pack(padx=10, pady=10, side=LEFT)

    qw.mainloop()


def popup_open_error():
    """Show error message when opening file twice"""
    print("Error: Open Error")
    showinfo("Error", "You already loaded input file. Please clear cache before loading a new file.")


def popup_nofile_error():
    """Show error message when opening file twice"""
    print("Error: No input file")
    showinfo("Error", "No input file. Click \"Browse file\" to load a new file.")


def popup_wrong_format():
    """Show error message when opening file twice"""
    print("Error: Not XYZ format")
    showinfo("Error", "Your input file is not XYZ format.")


def popup_author():
    """Show author information"""
    print("Command: Show author information")
    showinfo("Author", "Rangsiman Ketkaew (MSc in Chemistry)\n"
                       "Computational Chemistry Research Unit\n"
                       "Department of Chemistry\n"
                       "Faculty of Science and Technology\n"
                       "Thammasat University, Pathum Thani, 12120 Thailand\n"
                       "E-mail: rangsiman1993@gmail.com")


def popup_license():
    """Show program info"""
    print("Command: Show program license information")
    showinfo("License", "Octahedral distortion analysis v. 1 \n\n"
                        "This program is free software: you can redistribute it "
                        "and/or modify it under the terms of the GNU General Public "
                        "License as published by the Free Software Foundation, either "
                        "version 3 of the License, or (at your option) any later version.\n\n"
                        "This program is distributed in the hope that it will be useful, "
                        "but WITHOUT ANY WARRANTY; without even the implied warranty "
                        "of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. "
                        "See the GNU General Public License for more details.\n\n"
                        "You should have received a copy of the GNU General Public License "
                        "along with this program. If not, see <https://www.gnu.org/licenses/>.")


def dot_product(x, y):
    return sum([x[i] * y[i] for i in range(len(x))])


def norm(x):
    return sqrt(dot_product(x, x))


def normalize(x):
    return [x[i] / norm(x) for i in range(len(x))]


def project_onto_plane(x, n):
    d = dot_product(x, n) / norm(n)
    p = [d * normalize(n)[i] for i in range(len(n))]
    return [x[i] - p[i] for i in range(len(x))]


def vector_project():
    return 0


def distance_avg(x):
    """Calculate mean M-X distance
    """
    dist_sum = []

    for i in range(1, 7):
        results_sum = sqrt(pow(x[i][0] - x[0][0], 2) + pow(x[i][1] - x[0][1], 2) + pow(x[i][2] - x[0][2], 2))
        dist_sum.append(results_sum)

    dist_avg = sum(dist_sum) / 6

    return dist_avg


def octa_dist_distance(x):
    """Calculate 1st octahedral distortion parameter, delta(d).
    delta(d) = 1/6 * sum[ ((d_i - d)/d)**2 ],
                where d_i is individual M-X distance,
                and d is mean M-X distance.
    Ref: DOI: 10.1107/S0108768103026661   Acta Cryst. (2004). B60, 10-20
    """
    print("Command: Calculate octahedral distortion parameter: distance")
    global dist_sum, dist_results

    dist_indi = []
    dist_results = 0

    for i in range(1, 7):
        results_indi = sqrt(pow(x[i][0] - x[0][0], 2) + pow(x[i][1] - x[0][1], 2) + pow(x[i][2] - x[0][2], 2))
        dist_indi.append(results_indi)

    # There are two ways to calculate delta(d) parameter
    # 1st way
    for i in range(6):
        dist_results = (dist_indi[i] - distance_avg(x)) / (distance_avg(x) * 6) + dist_results
    # 2nd way
    # dist_results = sum([(dist_indi[i] - distance_avg(x)) / (distance_avg(x) * 6) for i in range(6)])

    return dist_results


def octa_dist_angle():
    print("Command: Calculate octahedral distortion parameter: angle")
    return 0


def octa_dist_dihedral():
    print("Command: Calculate octahedral distortion parameter: dihedral")
    return 0


def calc_para():
    """Calculate octahedral distortion parameters
    For more details in algorithm and method used in this function,
    please refer to following articles.
    1. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson,
       Inorg. Chem. 1996, 35, 2100.
    2. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau,
       Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.
    """
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    else:
        print("Command: Calculate octahedral distortion parameters")
        print("         - Distance parameter")
        print("         - Angle parameter")
        print("         - Dehedral parameter")

    print(octa_dist_distance(coord_list))
    textBox_distance.insert(INSERT, dist_results)

    textBox_angle.insert(INSERT, "0.0")

    textBox_dihedral.insert(INSERT, "0.0")

    # p = project_onto_plane([3, 4, 5], [1, 2, 3])
    # print(p)


def plot_vector():
    """Displaying 3D structure of octahedral complex using Matplotlib
    """
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    print("Command: Show scatter plot of coordinate")

    # Create point for metal center
    x_M = coord_list[0, 0]
    y_M = coord_list[0, 1]
    z_M = coord_list[0, 2]
    # Create points for ligand atoms
    x_lg = coord_list[1:, 0]
    y_lg = coord_list[1:, 1]
    z_lg = coord_list[1:, 2]

    # Plot and configuration
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_M, y_M, z_M, color='yellow', marker='o', s=200, linewidths=2, edgecolors='blue')
    ax.scatter(x_lg, y_lg, z_lg, color='red', marker='o', s=100, linewidths=2, edgecolors='blue')
    #ax.plot(x_M, y_M, z_M, color='b')

    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Octahedral structure')
    ax.grid(True)
    # plt.axis('equal')
    plt.show()


"""Start program. Create program UI using TkInter.
master/root is used as a master frame.
==============================================================
"""
# Create main window
master = Tk()
# Set font and text size as default setting.
FONT = "Segoe-UI 10"
master.option_add("*Font", FONT)
# Set program title
master.title("Octahedral Distortion Analysis")
# width x height + x_offset + y_offset
master.geometry("450x680+200+100")
# Uncomment command below, user can resize window freely
# master.resizable(0,0)
# Cause pressing <Esc> to close the window.
# master.bind('<Escape>', quit)

# Configure frame
root = Frame(master, highlightbackground="Grey", highlightthickness=1, bd="5", width="10", height="2")
root.pack(padx=5, pady=5)

"""
Create menu bar
    File 
    |- New          << clear_cache
    |- Open         << openfile
    |- Save as ..   << savefile
    |- Exit         << root.quit
    Help 
    |- Help         << prog_help
    |- Author       << popup_author    
    |- License      << popup_license
"""
menubar = Menu(master)

# add menu bar button
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
# sub-menu
filemenu.add_command(label="New", command=clear_cache)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_command(label="Save as ..", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

# add menu bar button
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
# add sub-menu
helpmenu.add_command(label="Help", command=prog_help)
helpmenu.add_command(label="Author", command=popup_author)
helpmenu.add_command(label="License", command=popup_license)

master.config(menu=menubar)

print("Octahedral Distortion Analysis  Copyright (C) 2019  Rangsiman Ketkaew")
print("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.")
print("This is free software, and you are welcome to redistribute it under")
print("certain conditions; see <https://www.gnu.org/licenses/> for details.")
print(" ")
print("------------------------------")
print("Octahedral Distortion Analysis")
print("------------------------------")

# program details
msg_1 = Label(root, font=("Segoe-UI", 16, "bold"),
              text="Octahedral Distortion Analysis")
msg_1.config(fg="Blue")
msg_1.pack(pady=5)
msg_2 = Label(root, wraplength=400, justify=CENTER,
              text="Computing the octahedral distortion parameters "
                   "for determining the structural difference between "
                   "two octahedral structures.", )
msg_2.pack(pady=5)

# button to browse input file
btn_openfile = Button(root, command=openfile, text="Browse file", )
btn_openfile.pack(anchor=W, pady="5")

# coordinate label
para_1 = Label(root, text="Molecular specification")
para_1.pack(anchor="w", pady=5)

# text box for showing cartesian coordinates
textBox_1 = Text(root, height="12", wrap="word")
textBox_1.pack(side="top", fill="both", pady="5")

# button to get coordinate from file
btn_getcoor = Button(root, text='Get coordinate', command=get_coord)
btn_getcoor.pack(pady="0")

# button to run
btn_run = Button(root, command=calc_para, text="Run")
btn_run.pack(pady="10")

# -----------------------------------------------------------

# Octahedral distortion parameters
para_0 = Label(root, text="Octahedral distortion parameters")
para_0.config(font="Sogoe 10 bold")
para_0.pack(anchor="w")

# Distance
para_1 = Label(root, text="D (in Ångström)")
para_1.pack(anchor="w", pady=5)
textBox_distance = Text(root, height="1", width=1, wrap="word")
textBox_distance.pack(side="top", fill="both")

# Angle
para_2 = Label(root, text="Σ (in degree)")
para_2.pack(anchor="w", pady=5)
textBox_angle = Text(root, height="1", width=1, wrap="word")
textBox_angle.pack(side="top", fill="both")

# Dehedral
para_3 = Label(root, text="Θ (in degree)")
para_3.pack(anchor="w", pady=5)
textBox_dihedral = Text(root, height="1", width=1, wrap="word")
textBox_dihedral.pack(side="top", fill="both")

# button to plot vector
btn_plot = Button(root, command=plot_vector, text="Plot")
btn_plot.pack(pady="10")

# activate the window
root.mainloop()

"""
with open(filename, 'r') as f:
        configfile.insert(INSERT, f.read())
"""
