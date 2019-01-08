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
OctaDist version 1.1

Octahedral Distortion Analysis
Software website: www.github.com/rangsimanketkaew/octadist
Last modified: January 2018

This program, we use Python 3.7.2 and TkInter as GUI maker.
PyInstaller is used as executable compiler.
Written and tested on PyCharm 2018.3.3 (Community Edition) program

Author: Rangsiman Ketkaew
        Computational Chemistry Research Unit
        Department of Chemistry
        Faculty of Science and Technology
        Thammasat University, Pathum Thani, 12120 Thailand
Contact: rangsiman1993@gmail.com
         rangsiman_k@sci.tu.ac.th
Personal website: https://sites.google.com/site/rangsiman1993
"""

program_version = 1.1

import datetime
import numpy as np
import webbrowser
from math import *
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def clear_cache():
    """Clear cache and free variable"""
    print("Command: Clear cache")
    global filename, filedata, atom_list, coord_list
    filename = ""
    filedata = ""
    atom_list = 0
    coord_list = 0
    textBox_coord.delete(1.0, END)
    textBox_delta.delete(1.0, END)
    textBox_sigma.delete(1.0, END)
    textBox_theta.delete(1.0, END)
    clear_results()


def clear_results():
    global computed_delta, computed_sigma, computed_theta
    computed_delta = 0.0
    computed_sigma = 0.0
    computed_theta = 0.0


def quit_program():
    print("Command: Quit program")
    print("Bye bye ...")
    root.quit()
    master.quit()


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


def popup_nocalc_error():
    """Show error message when save file but no any parameters computed"""
    print("Error: No results")
    showinfo("Error", "No results. Click \"Compute parameters\" to calculate octahedral distortion parameters.")


def popup_wrong_format():
    """Show error message when opening file twice"""
    print("Error: Wrong input format")
    showinfo("Error", "Your input file format is not supported.")


def popup_program_help():
    """Open program help page
        - Usage
        - Input file format
        - References
    """
    print("Command: Show program help")
    hp = Tk()
    # hp.overrideredirect(1)
    hp.option_add("*Font", "Segoe-UI 10")
    hp.geometry("500x450+750+200")
    hp.title("Program Help")
    # frame1 = Frame(hp, highlightbackground="Black", highlightthickness=10, bd="20")
    # frame1.pack()
    # Usage
    lbl = Label(hp, text="Usage:")
    lbl.pack(anchor=W)
    msg_help_1 = "1. Browse file\n"\
                 "2. Compute parameters\n"\
                 "3. Check results\n"\
                 "4. File → Save as ..\n"
    msg = Message(hp, text=msg_help_1, width="450")
    # msg.config(font=("Segoe-UI 10"))
    msg.pack(anchor=W)
    # Input format
    lbl = Label(hp, text="Supported input file format:")
    lbl.pack(anchor=W)
    msg_help_2 = "  <Metal center 0>  <X>  <Y>  <Z>\n"\
                 "  <Ligand atom 1>  <X>  <Y>  <Z>\n"\
                 "  <Ligand atom 2>  <X>  <Y>  <Z>\n"\
                 "  <Ligand atom 3>  <X>  <Y>  <Z>\n"\
                 "  <Ligand atom 4>  <X>  <Y>  <Z>\n"\
                 "  <Ligand atom 5>  <X>  <Y>  <Z>\n"\
                 "  <Ligand atom 6>  <X>  <Y>  <Z>\n"\
                 "  <optional>\n"\
                 "  ...\n"
    msg = Message(hp, text=msg_help_2, width="450")
    msg.config(font="Segoe-UI 10 italic")
    msg.pack(anchor=W)
    # References
    lbl = Label(hp, text="References:")
    lbl.pack(anchor=W)
    msg_help_3 = "1. J. A. Alonso, M. J. Martı´nez-Lope, M. T. Casais, M. T. Ferna´ndez-Dı´az\n"\
                 "   Inorg. Chem. 2000, 39, 917-923\n"\
                 "2. J. K. McCusker, A. L. Rheingold, D. N. Hendrickson\n"\
                 "   Inorg. Chem. 1996, 35, 2100.\n"\
                 "3. M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau\n"\
                 "   Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.\n"
    msg = Message(hp, text=msg_help_3, width="450")
    # msg.config(font=("Segoe-UI 10"))
    msg.pack(anchor=W)
    hp.mainloop()


def popup_about():
    """Show author information"""
    print("Command: Show program information")
    text =  "OctaDist version {}\n"\
            "\n"\
            "Programming:\n"\
            "Rangsiman Ketkaew\n"\
            "Computational Chemistry Research Unit\n"\
            "Department of Chemistry\n"\
            "Faculty of Science and Technology\n"\
            "Thammasat University, Pathum Thani, 12120 Thailand\n"\
            "\n"\
            "Contact:\n"\
            "E-mail: rangsiman1993@gmail.com\n"\
            "Website: https://github.com/rangsimanketkaew/OctaDist"\
            .format(program_version)
    showinfo("About program", text)


def popup_license():
    """Show program info"""
    print("Command: Show program license information")
    text =  "OctaDist {} Copyright (C) 2019  Rangsiman Ketkaew\n"\
            "\n"\
            "This program is free software: you can redistribute it "\
            "and/or modify it under the terms of the GNU General Public "\
            "License as published by the Free Software Foundation, either "\
            "version 3 of the License, or (at your option) any later version.\n"\
            "\n"\
            "This program is distributed in the hope that it will be useful, "\
            "but WITHOUT ANY WARRANTY; without even the implied warranty "\
            "of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. "\
            "See the GNU General Public License for more details.\n"\
            "\n"\
            "You should have received a copy of the GNU General Public License "\
            "along with this program. If not, see <https://www.gnu.org/licenses/>."\
            .format(program_version)
    showinfo("License", text)


def callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def open_file():
    """Open file using Open Dialog
    Molecular coordinates must be cartesian coordinate format.
    File extensions supported are *.txt, *.xyz, and *.com
    """
    print("Command: Open input file")
    global filename, filedata
    # check if filename is empty
    if filename != "":
        clear_cache()
    """
    # check if filename is empty
    if filename != "":
        popup_open_error()
        return 1
    """
    # Open text file
    filename = filedialog.askopenfilename(  # initialdir="C:/Users/",
        title="Choose input file",
        filetypes=(("Text File", "*.txt"),
                   ("XYZ File", "*.xyz"),
                   ("Input File", "*.com"),
                   ("All Files", "*.*")))
    # Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(filename, 'r') as f:
            print("         Open file: " + filename)
            print("Command: Insert file data into coordinate box")
            textBox_coord.insert(INSERT, f.read())
            f.close()
        # with open(filename, 'r') as f:
        #    print(f.read())
        with open(filename, 'r') as f:
            filedata = f.read()
            get_coord()
            f.close()
    except:
        print("Warning: No file exists")


def save_file():
    """Save file using Save Dialog
    All results is saved into text file (*.txt)
    """
    print("Command: Save data to output file")
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    # check if parameters are computed
    if run_check == 0:
        popup_nocalc_error()
        return 1
    f = filedialog.asksaveasfile(mode='w',
                                 defaultextension=".txt",
                                 title="Save as",
                                 filetypes=(("Text File", "*.txt"),
                                            ("Output File", "*.out"),
                                            ("All Files", "*.*")))
    # asksaveasfile return `None` if dialog closed with "cancel".
    if f is None:
        print("Warning: Cancelled save file")
        return 0
    f.write("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew\n")
    f.write("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.\n")
    f.write("This is free software, and you are welcome to redistribute it under\n")
    f.write("certain conditions; see <https://www.gnu.org/licenses/> for details.\n\n")
    f.write("OctaDist {}: Octahedral Distortion Analysis\n".format(program_version))
    f.write("https://github.com/rangsimanketkaew/OctaDist\n\n")
    f.write("By Rangsiman Ketkaew, Computational Chemistry Research Unit\n")
    f.write("Department of Chemistry, Faculty of Science and Technology\n")
    f.write("Thammasat University, Pathum Thani, 12120 Thailand\n")
    f.write("E-mail: rangsiman1993@gmail.com\n\n")
    f.write("Output file\n")
    f.write("===========\n")
    f.write("Date: Saved on {}\n\n".format(datetime.datetime.now()))
    f.write("Input file: " + filename + "\n\n")
    f.write("Molecular specification of Octahedral structure\n")
    f.write("Atom list:\n")
    for item in atom_list:
        f.write("%s  " % item)
    f.write("\n\n")
    f.write("Coordinate list:\n")
    for item in coord_list:
        f.write("%s\n" % item)
    f.write("\n")
    f.write("Octahedral distortion parameters:\n")
    f.write(" - Delta = {0:5.10f}\n".format(computed_delta))
    f.write(" - Sigma = {0:5.10f} degree\n".format(computed_sigma))
    f.write(" - Theta = {0:5.10f} degree\n".format(computed_theta))
    f.write("\n")
    f.write("============ Output file ends here. ============\n\n")
    f.close()  # `()` was missing.
    print("Command: Data has been saved to ", f)


def get_coord():
    """get coordinate from text file.
    Molecular coordinates must be in XYZ (cartesian) format

    Input file Format
    ----------
                                                 4
        <index 0> <X> <Y> <Z>                2   |      6
        <index 1> <X> <Y> <Z>                 \  |    /
        <index 2> <X> <Y> <Z>                  \ |  /
        <index 3> <X> <Y> <Z>                    0
        <index 4> <X> <Y> <Z>                  / | \
        <index 5> <X> <Y> <Z>                //  |  \\
        <index 6> <X> <Y> <Z>               1    |   5
                                                 3
    """
    # check if input file is correct format
    # check_format()
    print("Command: Get XYZ coordinates")
    global atom_list
    global coord_list
    """This function is used to get coordinate from either file or text box.
    1. read coordinate from file
    2. read coordinate from text box
    """
    f = open(filename, "r")
    line = f.readlines()
    f.close()
    # line = textBox_coord.get('1.0', END).splitlines()
    atom_raw = []
    for l in line:
        # read only the 1st column, elements, and pass into array
        lst = l.split(' ')[0]
        atom_raw.append(lst)
    # remove multiple lines after the last element
    atom_list = atom_raw[0:7]
    print("Command: Show atom lists")
    print("        ", atom_list, "\n")
    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> f.seek(0) <<
        2. use >> f = open(filename, "r") <<
    """
    f = open(filename, "r")
    coord_raw = np.loadtxt(f, skiprows=0, usecols=[1, 2, 3])
    f.close()
    # get only coordinates of 1 central atom and 6 ligand atoms
    coord_list = coord_raw[0:7]
    print("Command: Show Coordinate lists")
    for i in range(7):
        print("        ", coord_list[i])
    print("")
    """Return both lists of atom_list and coord_list. 
    To use list, just grab a tuple, and use >> atom_list, coord_list = get_coord() <<
    """
    return atom_list, coord_list


def dist_btw(x, y):
    """Find distance between two point
    """
    return sqrt(sum([pow(x[i] - y[i], 2) for i in range(3)]))


def dist_avg(x):
    """Calculate mean M-X distance by averaging the distance between
    metal center and ligand atom, d_i

            ----------------------------------------
    d_i = \/ (x - x_0)^2 + (y - y_0)^2 + (z - z_0)^2

    where x_0, y_0, and z_0 are component vector of metal center
    """
    dist_sum = []
    for i in range(1, 7):
        results_sum = dist_btw(x[i], x[0])
        dist_sum.append(results_sum)
    return sum([dist_sum[i] for i in range(6)]) / 6


def calc_delta(x):
    """Calculate 1st octahedral distortion parameter, delta.

                                      2
                 1         / d_i - d \
    delta(d) =  --- * sum | -------- |
                 6        \    d    /

                where d_i is individual M-X distance and d is mean M-X distance.

    Ref: DOI: 10.1107/S0108768103026661  Acta Cryst. (2004). B60, 10-20
    """
    global computed_delta
    dist_indi = []
    print("Command: Calculate distance between atoms (in Ångström)")
    for i in range(1, 7):
        distant_indi = sqrt(sum([pow(x[i][j] - x[0][j], 2) for j in range(3)]))
        print("         Distance between metal center and ligand atom", i, "is {0:5.5f}".format(distant_indi))
        dist_indi.append(distant_indi)
    print("")
    print("         Total number of computed distance:", len(dist_indi))
    print("")
    for i in range(6):
        diff_dist = (dist_indi[i] - dist_avg(x)) / dist_avg(x)
        computed_delta = (pow(diff_dist, 2) / 6) + computed_delta
    return computed_delta


def normalize_vector(v):
    """Returns the unit vector of the vector v: normalizing
    """
    if np.linalg.norm(v) == 0:
        print("Error: norm of vector", v, "is 0. Thus function normalize_vector returns a wrong value.")
    return v / np.linalg.norm(v)


def angle_between(v0, v1, v2):
    """Compute the angle between vector <v1 - v0> and <v2 - v0>
    and returns the angle in degree.

                                / v1_x * v2_x + v1_y * v2_y + v1_z * v2_z  \
    angle (in radian) = arccos | ----------------------------------------- |
                               \               |v1| * |v2|                /

    Ex.
            >> angle_between((1, 0, 0), (0, 1, 0), (0, 0, 0))
            1.5707963267948966 (radian)
            90.0 (degree)
    """
    sub_v1 = v1 - v0
    sub_v2 = v2 - v0
    v1_u = normalize_vector(sub_v1)
    v2_u = normalize_vector(sub_v2)
    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))


def calc_sigma(v):
    """Calculate octahedral distortion parameter, Σ

          12
    Σ = sigma < 90 - angle_i >
         i=1

    For more details, please refer to following article.
    J. K. McCusker, A. L. Rheingold, D. N. Hendrickson, Inorg. Chem. 1996, 35, 2100.
    """
    global angle_sigma_list, computed_sigma
    ligand_atom_list = []
    angle_sigma_list = []
    print("Command: Calculate angle between ligand atoms (in degree)")
    print("         Three trans angle (three biggest angles) are excluded.")
    print("")
    print("                   Atom i\n"
          "                    ^\n"
          "                   /\n"
          "                  /\n"
          "                 /\n"
          "                /\n"
          "              Vertex -----> Atom j")
    print("")
    print("         Metal center atom is taken as vertex.")
    print("")
    # Calculate individual angle and add to list
    for i in range(1, 7):
        for j in range(i+1, 7):
            angle_sigma_indi = angle_between(v[0], v[i], v[j])
            angle_sigma_list.append(angle_sigma_indi)
            ligand_atom_list.append([i, j])
    # Show list of angle before sorted
    print("         List before sorted:")
    for i in range(len(angle_sigma_list)):
        print("         Angle between atom", ligand_atom_list[i][0], "and atom", ligand_atom_list[i][1],
                "is {0:5.5f}".format(angle_sigma_list[i]))
    print("")
    # Sort the angle from lowest to highest
    # Two loops is used to sort the distance from lowest to greatest numbers
    i = 0
    while i < len(angle_sigma_list):
        k = i
        j = i + 1
        while j < len(angle_sigma_list):
            if angle_sigma_list[k] > angle_sigma_list[j]:
                k = j
            j += 1
        angle_sigma_list[i], angle_sigma_list[k] = angle_sigma_list[k], angle_sigma_list[i]
        i += 1
    # Show angle list after sorted
    print("         List before sorted:")
    for i in range(len(angle_sigma_list)):
        print("         ", angle_sigma_list[i])
    print("")
    # Remove last three angles (last three rows)
    new_angle_sigma_list = angle_sigma_list[:len(angle_sigma_list)-3]
    # Show new plane list after unwanted plane excluded
    print("         List after sorted:")
    for i in range(len(new_angle_sigma_list)):
        print("         ", new_angle_sigma_list[i])
    print("")
    print("         Total number of angles before sorted:", len(angle_sigma_list))
    print("         Total number of angles after sorted :", len(new_angle_sigma_list))
    print("")
    # Calculate Sigma parameter
    for i in range(len(new_angle_sigma_list)):
        computed_sigma = abs(90.0 - new_angle_sigma_list[i]) + computed_sigma
    return computed_sigma


def find_plane(v):
    """Find plane of given octahedral complex
    v = XYZ coordinate of complex
    v[0] = metal center atom of complex
    v[i] = ligand atom of complex
    """
    global final_plane_list
    # list of vertex of triangle (face of octahedral)
    plane_list = []
    print("Command: Find the plane (AKA the face on octahedron). Given three atoms as vertices")
    print("")
    print("                   Atom i\n"
          "                   /  \\\n"
          "                  /    \\\n"
          "                 /      \\\n"
          "                /        \\\n"
          "              Atom j-----Atom k")
    print("")
    print("         Total number of the selected plane is 10")
    print("")
    # Find four possible faces --> This would result 10 plane
    for i in range(1, 4):
        for j in range(i+1, 5):
            for k in range(j+1, 6):
                find_plane_eq(v[i], v[j], v[k])
    # Find distance between metal center atom and its projected point on plane
    # and store the vertex of triangle (face/plane) and distance btw metal to plane into array
                m = project_atom_onto_plane(v[0], a, b, c, d)
                d_btw = dist_btw(m, v[0])
                plane_list.append(np.array([i, j, k, d_btw]))
    # Show plane list before sorted
    print("Command: Show the list of given three atoms and shortest distance from metal center to the plane")
    print("         Format of list:\n")
    print("         [<atom_i> <atom_j> <atom_k> <shortest_distance_from_metal_center_to_the_plane>]\n")
    print("         List before sorted:")
    for i in range(len(plane_list)):
        print("         ", plane_list[i])
    print("")
    # Use distance between metal center and its projected point to sort list (array)
    # Two loops is used to sort the distance from lowest to greatest numbers
    i = 0
    while i < len(plane_list):
        k = i
        j = i + 1
        while j < len(plane_list):
            if plane_list[k][3] > plane_list[j][3]:
                k = j
            j += 1
        plane_list[i], plane_list[k] = plane_list[k], plane_list[i]
        i += 1
    # Show plane list after sorted
    print("         List after sorted:")
    for i in range(len(plane_list)):
        print("         ", plane_list[i])
    print("")
    # Remove first six planes from list (first six rows)
    excluded_plane_list = plane_list[6:]
    # Show new plane list after unwanted plane excluded
    print("Command: Delete six planes that mostly closest to metal center atom")
    print("         List after unwanted plane deleted:")
    for i in range(len(excluded_plane_list)):
        print("         ", excluded_plane_list[i])
    print("")
    # Remove the 4th column of distance
    final_plane_list = np.delete(excluded_plane_list, 3, 1)
    # Show final plane list
    print("         Final list of the number of atoms for four selected plane:")
    for i in range(len(final_plane_list)):
        print("         ", final_plane_list[i].astype(int))
    print("")
    # Return string 2D array
    return final_plane_list.astype(int)


def convert_atom_to_point(v):
    """Find 4 correct plane of octahedral complex
    For example,

    list of atom                    list of XYZ coordinate of atom
     [[1 2 3]          [[[0.00 0.00 0.00]  [1.22 2.34 1.23]  [3.21 1.09 -0.43]
      [1 2 4]    --->   [[0.00 0.00 0.00]  [1.22 2.34 1.23]  [-0.56 2.65 0.45]
      [2 3 5]]          [[1.22 2.34 1.23]  [3.21 1.09 -0.43] [2.32 -0.54 -0.23]]
    """
    global coord_vertex_list
    coord_vertex_list = []
    f = find_plane(v)
    # Generate list of coordinate of selected point
    for i in range(len(f)):
        coord_vertex_list.append(np.array([v[f[i][0]], v[f[i][1]], v[f[i][2]]]))
    print("Command: Show coordinate list of three ligand atoms for four selected plane")
    conv_v = coord_vertex_list
    for i in range(len(conv_v)):
        print("         Plane", i + 1)
        for j in range(3):
            print("         ", conv_v[i][j])
    print("")
    return coord_vertex_list


def find_plane_eq(p1, p2, p3):
    """Find the equation of plane that defined by three points (ligand atoms)
    The general form of plane equation is Ax + By + Cz = D

    Input arguments are vertex of plane (triangle)
    """
    global a, b, c, d
    v1 = p3 - p1
    v2 = p2 - p1
    # find the vector orthogonal to the plane using cross product method
    norm_p = np.cross(v1, v2)
    a, b, c = norm_p
    d = np.dot(norm_p, p3)

    return a, b, c, d


def project_atom_onto_plane(v, a, b, c, d):
    """Find the orthogonal vector of point onto the given plane.
    If the equation of plane is Ax + By + Cz = D and the location of point is (L, M, N), 
    then the location in the plane that is closest to the point (P, Q, R) is

    (P, Q, R) = (L, M, N) + λ * (A, B, C)

    where λ = (D - ( A*L + B*M + C*N)) / (A^2 + B^2 + C^2)

    Input argument: v is vector
                    a, b, and c are A, B, and C
                    d is D
    """
    # Create array of coefficient of vector plane
    v_plane = np.array([a, b, c])
    lmbda = (d - (a*v[0] + b*v[1] + c*v[2])) / np.dot(v_plane, v_plane)
    # Return location of metal center atom projected on the plane
    return v + (lmbda * v_plane)


def calc_theta(v):
    """Calculate octahedral distortion parameter, Θ

          24
    Θ = sigma < 60 - angle_i >
         i=1

    where angle_i is angle between two plane defined by vector of
    metal center and ligand atoms.

    4 faces, 6 angles each, thus the total number of theta angle is 24 angles.

    For more details, please refer to following article.
    M. Marchivie, P. Guionneau, J. F. Letard, D. Chasseau,
    Acta Crystal-logr. Sect. B Struct. Sci. 2005, 61, 25.
    """
    global angle_theta_list, computed_theta
    global cv, m, l_1, l_2, a, b, c, d
    angle_theta_list = []
    q = 0
    cv = convert_atom_to_point(v)
    print("Command: Calculate the following items")
    print("         - The equation of plane given by three selected ligand atoms, Ax + By + Cz = D")
    print("           Use orthogonal projection to find the projection of all atoms on the given plane.")
    print("")
    print("                             Atom i\n"
          "                              / \\        \n"
          "                    Atom p --/---\\---- Atom r\n"
          "                         \  /     \\    /\n"
          "                          \\/       \\  /\n"
          "                          /\\ Metal  \\/\n"
          "                         /  \\       /\\\n"
          "                        /    \\     /  \\\n"
          "                       /      \\   /    \\\n"
          "                    Atom j --- \\-/ --- Atom k\n"  
          "                              Atom q")
    print("")
    print("           All atoms are on the same plane.")
    print("")
    print("         - Compute the angle between Metal and ligand atom [i, j, k, p, q, r] (in degree)")
    print("")
    print("         - Default settings:")
    print("           1. If the angle is greater than", angle_cutoff_for_theta_max, ", it will be set to 60.0")
    print("           2. If the angle is less than", angle_cutoff_for_theta_min, ", it will be set to 60.0")
    print("")
    print("         ------------------------------------")
    print("")
    for i in range(4):
        find_plane_eq(cv[i][0], cv[i][1], cv[i][2])
        print("         Orthogonal projection onto the plane", i+1)
        print("          The equation of plane: {1:5.5f}x + {2:5.5f}y + {3:5.5f}z = {4:5.5f}"\
              .format(i+1, a, b, c, d))
        m = project_atom_onto_plane(v[0], a, b, c, d)
        print("          The point of metal center atom on the given plane: "
              "({0:5.5f}, {1:5.5f}, {2:5.5f})".format(m[0], m[1], m[2]))
        print("")
        for j in range(1, 6):
            for k in range(2, 7):
                l_1 = project_atom_onto_plane(v[j], a, b, c, d)
                print("          The point of ligand atom {0} onto given plane: "
                      "({1:5.5f}, {2:5.5f}, {3:5.5f})".format(j, l_1[0], l_1[1], l_1[2]))
                l_2 = project_atom_onto_plane(v[k], a, b, c, d)
                print("          The point of ligand atom {0} onto given plane: "
                      "({1:5.5f}, {2:5.5f}, {3:5.5f})".format(k, l_2[0], l_2[1], l_2[2]))
                angle_theta_indi = angle_between(m, l_1, l_2)
                if angle_theta_indi > angle_cutoff_for_theta_max or angle_theta_indi <= angle_cutoff_for_theta_min:
                    angle_theta_indi = 60.0
                    angle_theta_list.append(angle_theta_indi)
                    q += 1
                else:
                    angle_theta_list.append(angle_theta_indi)
                print("          Angle between atom {0} and {1}: {2:5.5f}".format(j, k, angle_theta_indi))
        print("")
    # Sum up all individual theta angle
    for i in range(len(angle_theta_list)):
        computed_theta += abs(60.0 - angle_theta_list[i])
    print("         Total number of all angle     :", len(angle_theta_list))
    print("         Total number of unwanted angle:", q)
    print("         Total number of selected angle:", len(angle_theta_list) - q)
    print("")
    return computed_theta


def calc_all_param():
    """Calculate octahedral distortion parameters including
    Delta, Sigma, and Theta parameters
    """
    global filename, run_check, computed_delta, computed_sigma, computed_theta
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    run_check = 1
    clear_results()
    calc_delta(coord_list)
    calc_sigma(coord_list)
    calc_theta(coord_list)
    formatted_computed_delta = "{0:10.8f}".format(computed_delta)
    formatted_computed_sigma = "{0:10.8f}".format(computed_sigma)
    formatted_computed_theta = "{0:10.8f}".format(computed_theta)
    print("Command: Calculate octahedral distortion parameters")
    print("         Delta  <Δ> =", formatted_computed_delta)
    print("         Sigma  <Σ> =", formatted_computed_sigma, "degree")
    print("         Theta  <Θ> =", formatted_computed_theta, "degree")
    print("")
    textBox_delta.delete(1.0, END)
    textBox_delta.insert(INSERT, formatted_computed_delta)
    textBox_sigma.delete(1.0, END)
    textBox_sigma.insert(INSERT, formatted_computed_sigma)
    textBox_theta.delete(1.0, END)
    textBox_theta.insert(INSERT, formatted_computed_theta)


def draw_strc():
    """Display 3D structure of octahedral complex with label for each atoms
    """
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    get_coord()
    print("Command: Display octahedral structure")
    # Plot and configuration
    fig = plt.figure()
    ax = Axes3D(fig)
    cl = coord_list
    ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=200, linewidths=2, edgecolors='blue')
    ax.text(cl[0][0] + 0.1, cl[0][1] + 0.2, cl[0][2] + 0.2, atom_list[0], fontsize=12)
    for i in range(1, 7):
        ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=100, linewidths=2, edgecolors='blue')
        ax.text(cl[i][0] + 0.1, cl[i][1] + 0.2, cl[i][2] + 0.2, atom_list[i] + ",{0}".format(i), fontsize=12)
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Octahedral structure')
    ax.grid(True)
    # plt.axis('equal')
    plt.show()


def draw_plane():
    """Display the plane defined by three ligand atoms
    """
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    # check if the orthogonal projection is computed
    if run_check == 0:
        popup_nocalc_error()
        return 1
    print("Command: Display defined plane and orthogonal point")
    # Plot and configuration

    cl = coord_list
    vl = coord_vertex_list

    # This function is hard code. Waiting for improvement

    plane_1_x, plane_1_y, plane_1_z = [], [], []
    plane_2_x, plane_2_y, plane_2_z = [], [], []
    plane_3_x, plane_3_y, plane_3_z = [], [], []
    plane_4_x, plane_4_y, plane_4_z = [], [], []

    for j in range(3):
        plane_1_x.append(vl[0][j][0])
        plane_1_y.append(vl[0][j][1])
        plane_1_z.append(vl[0][j][2])
    for j in range(3):
        plane_2_x.append(vl[1][j][0])
        plane_2_y.append(vl[1][j][1])
        plane_2_z.append(vl[1][j][2])
    for j in range(3):
        plane_3_x.append(vl[2][j][0])
        plane_3_y.append(vl[2][j][1])
        plane_3_z.append(vl[2][j][2])
    for j in range(3):
        plane_4_x.append(vl[3][j][0])
        plane_4_y.append(vl[3][j][1])
        plane_4_z.append(vl[3][j][2])

    verts_1 = [list(zip(plane_1_x, plane_1_y, plane_1_z))]
    verts_2 = [list(zip(plane_2_x, plane_2_y, plane_2_z))]
    verts_3 = [list(zip(plane_3_x, plane_3_y, plane_3_z))]
    verts_4 = [list(zip(plane_4_x, plane_4_y, plane_4_z))]

    fig = plt.figure()

    # Plane 1
    ax = fig.add_subplot(2,2,1, projection='3d')
    ax.set_title('Plane 1')
    ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=100, linewidths=1, edgecolors='blue')
    ax.text(cl[0][0] + 0.1, cl[0][1] + 0.2, cl[0][2] + 0.2, atom_list[0], fontsize=9)
    for i in range(1, 7):
        ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=50, linewidths=1, edgecolors='blue')
        ax.text(cl[i][0] + 0.1, cl[i][1] + 0.2, cl[i][2] + 0.2, atom_list[i] + ",{0}".format(i), fontsize=9)
    ax.add_collection3d(Poly3DCollection(verts_1, alpha=0.5, color="red"))

    ax.set_xlabel(r'X', fontsize=10)
    ax.set_ylabel(r'Y', fontsize=10)
    ax.set_zlabel(r'Z', fontsize=10)
    ax.grid(True)

    # Plane 2
    ax = fig.add_subplot(2,2,2, projection='3d')
    ax.set_title('Plane 2')
    ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=100, linewidths=1, edgecolors='blue')
    ax.text(cl[0][0] + 0.1, cl[0][1] + 0.2, cl[0][2] + 0.2, atom_list[0], fontsize=9)
    for i in range(1, 7):
        ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=50, linewidths=1, edgecolors='blue')
        ax.text(cl[i][0] + 0.1, cl[i][1] + 0.2, cl[i][2] + 0.2, atom_list[i] + ",{0}".format(i), fontsize=9)
    ax.add_collection3d(Poly3DCollection(verts_2, alpha=0.5, color="blue"))

    ax.set_xlabel(r'X', fontsize=10)
    ax.set_ylabel(r'Y', fontsize=10)
    ax.set_zlabel(r'Z', fontsize=10)
    ax.grid(True)

    # Plane 3
    ax = fig.add_subplot(2,2,3, projection='3d')
    ax.set_title('Plane 3')
    ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=100, linewidths=1, edgecolors='blue')
    ax.text(cl[0][0] + 0.1, cl[0][1] + 0.2, cl[0][2] + 0.2, atom_list[0], fontsize=9)
    for i in range(1, 7):
        ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=50, linewidths=1, edgecolors='blue')
        ax.text(cl[i][0] + 0.1, cl[i][1] + 0.2, cl[i][2] + 0.2, atom_list[i] + ",{0}".format(i), fontsize=9)
    ax.add_collection3d(Poly3DCollection(verts_3, alpha=0.5, color="green"))

    ax.set_xlabel(r'X', fontsize=10)
    ax.set_ylabel(r'Y', fontsize=10)
    ax.set_zlabel(r'Z', fontsize=10)
    ax.grid(True)

    # Plane 4
    ax = fig.add_subplot(2,2,4, projection='3d')
    ax.set_title('Plane 4')
    ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='yellow', marker='o', s=100, linewidths=1, edgecolors='blue')
    ax.text(cl[0][0] + 0.1, cl[0][1] + 0.2, cl[0][2] + 0.2, atom_list[0], fontsize=9)
    for i in range(1, 7):
        ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='red', marker='o', s=50, linewidths=1, edgecolors='blue')
        ax.text(cl[i][0] + 0.1, cl[i][1] + 0.2, cl[i][2] + 0.2, atom_list[i] + ",{0}".format(i), fontsize=9)
    ax.add_collection3d(Poly3DCollection(verts_4, alpha=0.5, color="yellow"))

    ax.set_xlabel(r'X', fontsize=10)
    ax.set_ylabel(r'Y', fontsize=10)
    ax.set_zlabel(r'Z', fontsize=10)
    ax.grid(True)
    plt.axis('equal')

    plt.show()


def draw_projection():
    """Display the vector projection of all atoms onto the given plane
    """
    # global m, l
    # check if input file exist
    if filename == "":
        popup_nofile_error()
        return 1
    # check if the orthogonal projection is computed
    if run_check == 0:
        popup_nocalc_error()
        return 1
    print("Command: Display the orthogonal projection onto the given plane")
    # Plot and configuration
    fig = plt.figure()
    cl = coord_list

    # Figure configuration
    ax = fig.add_subplot(2, 2, 1, projection='3d')
    ax.set_title('Orthogonal projection onto the plane 1')
    # Metal center atom
    ax.scatter(cl[0][0], cl[0][1], cl[0][2], color='blue', marker='o', s=200, linewidths=2, edgecolors='blue')
    ax.text(cl[0][0] + 0.1, cl[0][1] + 0.2, cl[0][2] + 0.2, atom_list[0], fontsize=9)
    # Ligand atoms
    for i in range(1, 7):
        ax.scatter(cl[i][0], cl[i][1], cl[i][2], color='white', marker='o', s=100, linewidths=2, edgecolors='blue')
        ax.text(cl[i][0] + 0.1, cl[i][1] + 0.2, cl[i][2] + 0.2, atom_list[i] + ",{0}".format(i), fontsize=9)
    # Metal center atom projected onto the plane
    ax.scatter(m[0], m[1], m[2], color='skyblue', marker='o', s=200, linewidths=2, edgecolors='blue')
    ax.text(m[0] + 0.1, m[1] + 0.2, m[2] + 0.2, "Metal on the plane", fontsize=9)
    # Ligand atom projected onto the plane
    ax.scatter(l_1[0], l_1[1], l_1[2], color='orange', marker='o', s=200, linewidths=2, edgecolors='blue')
    ax.text(l_1[0] + 0.1, l_1[1] + 0.2, l_1[2] + 0.2, "Ligand atom on the plane", fontsize=9)

    ax.set_xlabel(r'X', fontsize=10)
    ax.set_ylabel(r'Y', fontsize=10)
    ax.set_zlabel(r'Z', fontsize=10)
    ax.grid(True)
    plt.axis('equal')

    plt.show()


##################################################
# Default value of global variables are set here #
##################################################
filename = ""
filedata = ""
run_check = 0
computed_delta = 0.0
computed_sigma = 0.0
computed_theta = 0.0
angle_cutoff_for_sigma = 150.0  # degree
angle_cutoff_for_theta_max = 60.0  # degree
angle_cutoff_for_theta_min = 1.0  # degree
##################################################

"""Start program. Create main window GUI using TkInter.
"""
root = Tk()
# Set font and text size as default setting.
FONT = "Segoe-UI 10"
root.option_add("*Font", FONT)
# Set program title
root.title("OctaDist")
# Failed to use iconbitmap
# root.iconbitmap(r'C:\Users\Nutt\PycharmProjects\OctaDist\icon-mol.ico')
# width x height + x_offset + y_offset
# master.geometry("350x610+400+100")
# Uncomment command below, user can resize window freely
# master.resizable(0,0)
# Cause pressing <Esc> to close the window.
# master.bind('<Escape>', quit)

# Configure frame
master = Frame(root, highlightbackground="Grey", highlightthickness=1, bd="5", width="2", height="2")
master.grid(padx=5, pady=5)

"""
Create menu bar
    File 
    |- New                        << clear_cache
    |- Open                       << open_file
    |- Save as ..                 << save_file
    |-------------
    |- Exit                       << quit_program
    Tools
    |- Draw octahedral structure  << draw_strc
    |- Draw projection plane      << draw_plane
    |- Draw orthogonal projection << draw_projection
    Help 
    |- Program help               << popup_program_help
    |- About program              << popup_about    
    |- License info               << popup_license
"""
menubar = Menu(master)
# add menu bar button
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
# sub-menu
filemenu.add_command(label="New", command=clear_cache)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save as ..", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit_program)
# add menu bar button
toolsmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tools", menu=toolsmenu)
# add sub-menu
toolsmenu.add_command(label="Draw octahedral structure", command=draw_strc)
toolsmenu.add_command(label="Draw projection plane", command=draw_plane)
toolsmenu.add_command(label="Draw orthogonal projection", command=draw_projection)
# add menu bar button
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
# add sub-menu
helpmenu.add_command(label="Program help", command=popup_program_help)
helpmenu.add_command(label="About program", command=popup_about)
helpmenu.add_command(label="License information", command=popup_license)
root.config(menu=menubar)

print("")
print("OctaDist  Copyright (C) 2019  Rangsiman Ketkaew")
print("This program comes with ABSOLUTELY NO WARRANTY; for details, go to Help/License.")
print("This is free software, and you are welcome to redistribute it under")
print("certain conditions; see <https://www.gnu.org/licenses/> for details.")
print("")
print("=========================================================================")
print("                              OctaDist {}".format(program_version))
print("")
print("                     Octahedral Distortion Analysis")
print("                     ------------------------------")
print("A Program for Determining The Structural Distortion of Octahedral Complex")
print("")
print("                          by Rangsiman Ketkaew")
print("                           January 8th, 2019")
print("              https://github.com/rangsimanketkaew/OctaDist")
print("=========================================================================")
print("")

# program details
msg_1 = Label(master, font=("Segoe-UI", 16, "bold"), text="Octahedral Distortion Analysis")
msg_1.config(fg="Blue")
msg_1.grid(pady="5", row=0, columnspan=4)
msg_2 = Label(master, text="Determine the structural distortion between two octahedral structures.")
msg_2.grid(pady="5", row=1, columnspan=4)
# button to browse input file
btn_open_file = Button(master, command=open_file, text="Browse file", )
btn_open_file.grid(pady="5", row=2, column=0)
# button to run
btn_run = Button(master, command=calc_all_param, text="Compute parameters")
# btn_run.config(font="Segoe 10")
btn_run.grid(sticky=W, pady="5", row=2, column=1, columnspan=2)
# button to clear cache
btn_open_file = Button(master, command=clear_cache, text="Clear cache", )
btn_open_file.grid(sticky=W, pady="5", row=2, column=3)
# coordinate label
lbl_1 = Label(master, text="Molecular specification")
lbl_1.grid(sticky=W, pady="5", row=3, columnspan=4)
# text box for showing cartesian coordinates
textBox_coord = Text(master, height="12", width="65", wrap="word")
textBox_coord.grid(pady="5", row=4, columnspan=4)
# Octahedral distortion parameters
lbl_2 = Label(master, text="Octahedral distortion parameters")
# lbl_2.config(font="Segoe 10 bold")
lbl_2.grid(row=6, column=1, columnspan=2)
# Delta
lbl_dist = Label(master, text="Δ  = ")
lbl_dist.grid(sticky=E, pady="5", row=7, column=1)
textBox_delta = Text(master, height="1", width="15", wrap="word")
textBox_delta.grid(row=7, column=2, sticky=W)
# Sigma
lbl_sigma = Label(master, text="Σ  = ")
lbl_sigma.grid(sticky=E, pady="5", row=8, column=1)
textBox_sigma = Text(master, height="1", width="15", wrap="word")
textBox_sigma.grid(sticky=W, row=8, column=2)
lbl_sigma_unit = Label(master, text="degree")
lbl_sigma_unit.grid(sticky=W, pady="5", row=8, column=3)
# Theta
lbl_theta = Label(master, text="Θ  = ")
lbl_theta.grid(sticky=E, pady="5", row=9, column=1)
textBox_theta = Text(master, height="1", width="15", wrap="word")
textBox_theta.grid(sticky=W, row=9, column=2)
lbl_theta_unit = Label(master, text="degree")
lbl_theta_unit.grid(sticky=W, pady="5", row=9, column=3)
# Link
lbl_link = Label(master, text=r"https://github.com/rangsimanketkaew/OctaDist", fg="blue", cursor="hand2")
lbl_link.grid(pady="5", row=10, columnspan=4)
lbl_link.bind("<Button-1>", callback)
# Display coordinate and vector projection
lbl_display = Label(master, text="Graphical Displays")
# lbl_display.config(font="Segoe 10 bold")
lbl_display.grid(row=6, column=0)
# button to draw structure
btn_draw_strc = Button(master, command=draw_strc, text="Octahedral structure")
btn_draw_strc.grid(pady="5", row=7, column=0)
# button to draw plane
btn_draw_plane = Button(master, command=draw_plane, text="Projection plane")
btn_draw_plane.grid(pady="5", row=8, column=0)
# button to draw vector projection
btn_draw_proj = Button(master, command=draw_projection, text="Orthogonal projection")
btn_draw_proj.grid(pady="5", row=9, column=0)

# activate the window
root.mainloop()

