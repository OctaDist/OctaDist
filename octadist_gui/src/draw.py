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

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import octadist_gui.src.popup
import octadist_gui.src.tools
from octadist_gui import main
from octadist_gui.src import elements


# import tkinter as tk
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.figure import Figure


def all_atom(self, acf):
    """Display 3D structure of octahedral complex with label for each atoms

    :param self: master frame
    :param acf: atomic labels and coordinates of full complex
    :type acf: list
    """
    if len(acf) == 0:
        octadist_gui.src.popup.err_no_file(self)
        return 1
    elif len(acf) > 1:
        octadist_gui.src.popup.err_many_files(self)
        return 1

    fal, fcl = acf[0]

    main.print_stdout(self, "Info: Display scattering plot of all atoms")
    main.print_stdout(self, "")

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2], marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}".format(fal[i]), s=elements.check_radii(n) * 300)

    # Calculate distance
    bond_list = octadist_gui.src.tools.find_bonds(self, fal, fcl)
    atoms_pair = []
    for i in range(len(bond_list)):
        get_atoms = bond_list[i]
        x, y, z = zip(*get_atoms)
        atoms = list(zip(x, y, z))
        atoms_pair.append(atoms)

    # Draw line
    for i in range(len(atoms_pair)):
        merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
        x, y, z = merge
        ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    # Set legend
    # Remove duplicate labels in legend.
    # Ref.https://stackoverflow.com/a/26550501/6596684
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    leg = plt.legend(handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12)
    # Fixed size of point in legend
    # Ref. https://stackoverflow.com/a/24707567/6596684
    for i in range(len(leg.legendHandles)):
        leg.legendHandles[i]._sizes = [90]

    # Set axis
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Full complex', fontsize="12")
    ax.grid(True)

    ###############

    # root = tk.Toplevel(self.master)
    # root.wm_title("All atom")
    #
    # # fig = Figure(figsize=(5, 4), dpi=1000)
    #
    # canvas = FigureCanvasTkAgg(fig, root)  # A tk.DrawingArea.
    # canvas.draw()
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    #
    # toolbar = NavigationToolbar2Tk(canvas, root)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    ###############

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def all_atom_and_face(self, acf, all_face):
    """Display 3D structure of octahedral complex with label for each atoms

    :param self: master frame
    :param acf: atomic labels and coordinates of full complex
    :param all_face: atomic labels and coordinates of 8 faces
    :type acf: list
    :type all_face: list
    """
    if len(acf) == 0:
        octadist_gui.src.popup.err_no_file(self)
        return 1
    elif len(acf) > 1:
        octadist_gui.src.popup.err_many_files(self)
        return 1
    if len(all_face) == 0:
        octadist_gui.src.popup.err_no_calc(self)
        return 1

    main.print_stdout(self, "Info: Display scattering plot of all atoms")
    main.print_stdout(self, "      Draw surface for all 8 faces of selected octahedral structure")
    main.print_stdout(self, "")

    fal, fcl = acf[0]
    face_data = all_face[0]
    a_ref, c_ref, a_oppo, c_oppo = face_data

    fig = plt.figure()
    ax = Axes3D(fig)
    vertices_list = []
    # Create array of vertices for 8 faces
    for i in range(8):
        get_vertices = c_ref[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        vertices_list.append(vertices)

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2], marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}".format(fal[i]), s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow",
                  "violet", "cyan", "brown", "grey"]
    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i], alpha=0.5, color=color_list[i]))

    # Calculate distance
    bond_list = octadist_gui.src.tools.find_bonds(self, fal, fcl)
    atoms_pair = []
    for i in range(len(bond_list)):
        get_atoms = bond_list[i]
        x, y, z = zip(*get_atoms)
        atoms = list(zip(x, y, z))
        atoms_pair.append(atoms)

    # Draw line
    for i in range(len(atoms_pair)):
        merge = list(zip(atoms_pair[i][0], atoms_pair[i][1]))
        x, y, z = merge
        ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    # Set legend
    # Remove duplicate labels in legend.
    # Ref.https://stackoverflow.com/a/26550501/6596684
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    leg = plt.legend(handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12)
    # Fixed size of point in legend
    # Ref. https://stackoverflow.com/a/24707567/6596684
    for i in range(len(leg.legendHandles)):
        leg.legendHandles[i]._sizes = [90]

    # Set axis
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Full complex with faces of octahedron', fontsize="12")
    ax.grid(True)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def octa(self, aco):
    """Display 3D structure of octahedral complex

    :param self: master frame
    :param aco: atomic labels and coordinates of octahedral structure
    :type aco: list
    """
    if len(aco) == 0:
        octadist_gui.src.popup.err_no_calc(self)
        return 1
    elif len(aco) > 1:
        octadist_gui.src.popup.err_many_files(self)
        return 1

    main.print_stdout(self, "Info: Display scattering plot of truncated octahedral structure")
    main.print_stdout(self, "      Draw surface for all 8 faces of selected octahedral structure")
    main.print_stdout(self, "")

    num, metal, ao, co = aco[0]
    # num = number of file, metal = metal center
    # ao = atomic labels, co = atomic coordinates

    fig = plt.figure()
    ax = Axes3D(fig)

    # Plot atoms
    for i in range(len(co)):
        # Determine atomic number
        n = elements.check_atom(ao[i])
        ax.scatter(co[i][0], co[i][1], co[i][2], marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}".format(ao[i]), s=elements.check_radii(n) * 300)

    # Draw line
    for i in range(1, len(co)):
        merge = list(zip(co[0], co[i]))
        x, y, z = merge
        ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    # Set legend
    # Remove duplicate labels in legend.
    # Ref.https://stackoverflow.com/a/26550501/6596684
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    leg = plt.legend(handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12)
    # Fixed size of point in legend
    # Ref. https://stackoverflow.com/a/24707567/6596684
    for i in range(len(leg.legendHandles)):
        leg.legendHandles[i]._sizes = [90]

    # Set axis
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Octahedral structure', fontsize="12")
    ax.grid(True)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def octa_and_face(self, aco, all_face):
    """Display 3D structure of octahedral complex with 8 faces

    :param self: master frame
    :param aco: atomic labels and coordinates of octahedral structure
    :param all_face: atomic labels and coordinates of 8 faces
    :type aco: list
    :type all_face: list
    """
    if len(aco) == 0:
        octadist_gui.src.popup.err_no_calc(self)
        return 1
    elif len(aco) > 1:
        octadist_gui.src.popup.err_many_files(self)
        return 1

    main.print_stdout(self, "Info: Display scattering plot of truncated octahedral structure")
    main.print_stdout(self, "      Draw surface for all 8 faces of selected octahedral structure")
    main.print_stdout(self, "")

    num, metal, ao, co = aco[0]
    # num = number of file, metal = metal center
    # ao = atomic labels, co = atomic coordinates

    face_data = all_face[0]
    a_ref, c_ref, a_oppo, c_oppo = face_data

    fig = plt.figure()
    ax = Axes3D(fig)
    vertices_list = []
    # Create array of vertices for 8 faces
    for i in range(8):
        get_vertices = c_ref[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        vertices_list.append(vertices)

    # Plot atoms
    for i in range(len(co)):
        # Determine atomic number
        n = elements.check_atom(ao[i])
        ax.scatter(co[i][0], co[i][1], co[i][2], marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}".format(ao[i]), s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow",
                  "violet", "cyan", "brown", "grey"]
    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i], alpha=0.5, color=color_list[i]))

    # Draw line
    for i in range(1, len(co)):
        merge = list(zip(co[0], co[i]))
        x, y, z = merge
        ax.plot(x, y, z, 'k-', color="black", linewidth=2)

    # Set legend
    # Remove duplicate labels in legend.
    # Ref.https://stackoverflow.com/a/26550501/6596684
    handles, labels = ax.get_legend_handles_labels()
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            handle_list.append(handle)
            label_list.append(label)
    leg = plt.legend(handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12)
    # Fixed size of point in legend
    # Ref. https://stackoverflow.com/a/24707567/6596684
    for i in range(len(leg.legendHandles)):
        leg.legendHandles[i]._sizes = [90]

    # Set axis
    ax.set_xlabel(r'X', fontsize=15)
    ax.set_ylabel(r'Y', fontsize=15)
    ax.set_zlabel(r'Z', fontsize=15)
    ax.set_title('Octahedral structure with faces', fontsize="12")
    ax.grid(True)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()
