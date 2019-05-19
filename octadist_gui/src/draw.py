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

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from octadist_gui.src import elements, popup, tools, plane, projection


def all_atom(self, acf):
    """
    Display 3D structure of octahedral complex with label for each atoms.

    Parameters
    ----------
    acf : list
        Atomic labels and coordinates of full complex.

    Returns
    -------
    None

    """
    if len(acf) == 0:
        popup.err_no_file()
        return 1
    elif len(acf) > 1:
        popup.err_many_files()
        return 1

    fal, fcl = acf[0]

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0],
                   fcl[i][1],
                   fcl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}"
                   .format(fal[i]), s=elements.check_radii(n) * 300)

    # Calculate distance
    bond_list = tools.find_bonds(self, fal, fcl)
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
    leg = plt.legend(handle_list, label_list,
                     loc="lower left", scatterpoints=1, fontsize=12)
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

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def all_atom_and_face(self, acf, all_face):
    """
    Display 3D structure of octahedral complex with label for each atoms.

    Parameters
    ----------
    acf : list
        Atomic labels and coordinates of full complex.
    all_face : list
        Atomic labels and coordinates of 8 faces.

    Returns
    -------
    None

    """
    if len(acf) == 0:
        popup.err_no_file()
        return 1
    elif len(acf) > 1:
        popup.err_many_files()
        return 1
    if len(all_face) == 0:
        popup.err_no_calc()
        return 1

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
        ax.scatter(fcl[i][0],
                   fcl[i][1],
                   fcl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}"
                   .format(fal[i]), s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow",
                  "violet", "cyan", "brown", "grey"]
    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i],
                                             alpha=0.5,
                                             color=color_list[i]))

    # Calculate distance
    bond_list = tools.find_bonds(self, fal, fcl)
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
    leg = plt.legend(handle_list, label_list,
                     loc="lower left", scatterpoints=1, fontsize=12)
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


def octa(aco):
    """
    Display 3D structure of octahedral complex.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.

    Returns
    -------
    None

    """
    if len(aco) == 0:
        popup.err_no_calc()
        return 1
    elif len(aco) > 1:
        popup.err_many_files()
        return 1

    num, metal, ao, co = aco[0]
    # num = number of file, metal = metal center
    # ao = atomic labels, co = atomic coordinates

    fig = plt.figure()
    ax = Axes3D(fig)

    # Plot atoms
    for i in range(len(co)):
        # Determine atomic number
        n = elements.check_atom(ao[i])
        ax.scatter(co[i][0],
                   co[i][1],
                   co[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}"
                   .format(ao[i]), s=elements.check_radii(n) * 300)

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
    leg = plt.legend(handle_list, label_list,
                     loc="lower left", scatterpoints=1, fontsize=12)
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


def octa_and_face(aco, all_face):
    """
    Display 3D structure of octahedral complex with 8 faces.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.
    all_face : list
        Atomic labels and coordinates of 8 faces.

    Returns
    -------
    None

    """
    if len(aco) == 0:
        popup.err_no_calc()
        return 1
    elif len(aco) > 1:
        popup.err_many_files()
        return 1

    _, _, ao, co = aco[0]

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
        ax.scatter(co[i][0],
                   co[i][1],
                   co[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n), label="{}"
                   .format(ao[i]), s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow",
                  "violet", "cyan", "brown", "grey"]
    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i],
                                             alpha=0.5,
                                             color=color_list[i]))

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
    leg = plt.legend(handle_list, label_list,
                     loc="lower left", scatterpoints=1, fontsize=12)
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


def proj_planes(aco, all_face):
    """
    Display the selected 4 faces of octahedral complex.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.
    all_face : list
        Atomic labels and coordinates of 8 faces.

    Returns
    -------
    None

    """
    if len(aco) == 0:
        popup.err_no_calc()
        return 1
    elif len(aco) > 1:
        popup.err_many_files()
        return 1

    _, _, ao, co = aco[0]

    face_data = all_face[0]
    a_ref, c_ref, a_oppo, c_oppo = face_data

    # reference face
    ref_vertices_list = []
    for i in range(4):
        get_vertices = c_ref[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        ref_vertices_list.append(vertices)

    # opposite face
    oppo_vertices_list = []
    for i in range(4):
        x, y, z = zip(*c_oppo[i])
        vertices = [list(zip(x, y, z))]
        oppo_vertices_list.append(vertices)

    fig = plt.figure()
    st = fig.suptitle("4 pairs of opposite planes", fontsize="x-large")

    # Display four planes
    color_list_1 = ["red", "blue", "orange", "magenta"]
    color_list_2 = ["green", "yellow", "cyan", "brown"]

    for i in range(4):
        ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
        ax.set_title("Pair {}".format(i + 1))
        ax.scatter(co[0][0],
                   co[0][1],
                   co[0][2],
                   color='yellow', marker='o', s=100, linewidths=1,
                   edgecolors='black', label="Metal center")

        ax.text(co[0][0] + 0.1,
                co[0][1] + 0.1,
                co[0][2] + 0.1,
                ao[0], fontsize=9)

        for j in range(1, 7):
            ax.scatter(co[j][0],
                       co[j][1],
                       co[j][2],
                       color='red', marker='o', s=50, linewidths=1,
                       edgecolors='black', label="Ligand atoms")

            ax.text(co[j][0] + 0.1,
                    co[j][1] + 0.1,
                    co[j][2] + 0.1,
                    "{0},{1}".format(ao[j], j), fontsize=9)

        # Draw plane
        ax.add_collection3d(Poly3DCollection(ref_vertices_list[i],
                                             alpha=0.5,
                                             color=color_list_1[i]))

        ax.add_collection3d(Poly3DCollection(oppo_vertices_list[i],
                                             alpha=0.5,
                                             color=color_list_2[i]))

        # Set axis
        ax.set_xlabel(r'X', fontsize=10)
        ax.set_ylabel(r'Y', fontsize=10)
        ax.set_zlabel(r'Z', fontsize=10)
        ax.grid(True)

    # Shift subplots down
    st.set_y(1.0)
    fig.subplots_adjust(top=0.25)

    # plt.axis('equal')
    plt.tight_layout()
    plt.show()


def twisting_faces(aco, all_face):
    """
    Display twisting triangular faces and vector projection.

    Parameters
    ----------
    aco : list
        Atomic labels and coordinates of octahedral structure.
    all_face : list
        Atomic labels and coordinates of 8 faces.

    Returns
    -------
    None

    """
    if len(aco) == 0:
        popup.err_no_calc()
        return 1
    elif len(aco) > 1:
        popup.err_many_files()
        return 1

    _, _, ao, co = aco[0]

    face_data = all_face[0]
    a_ref, c_ref, a_oppo, c_oppo = face_data

    ref_vertices_list = []
    for i in range(4):
        get_vertices = c_ref[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        ref_vertices_list.append(vertices)

    fig = plt.figure()
    st = fig.suptitle("Projected twisting triangular faces", fontsize="x-large")

    for i in range(4):
        a, b, c, d = plane.find_eq_of_plane(c_ref[i][0], c_ref[i][1], c_ref[i][2])
        m = projection.project_atom_onto_plane(co[0], a, b, c, d)
        ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
        ax.set_title("Projection plane {0}".format(i + 1), fontsize='10')

        # Projected metal center atom
        ax.scatter(m[0],
                   m[1],
                   m[2],
                   color='orange', s=100, marker='o', linewidths=1,
                   edgecolors='black', label="Metal center")

        ax.text(m[0] + 0.1,
                m[1] + 0.1,
                m[2] + 0.1,
                "{0}'".format(ao[0]), fontsize=9)

        # Reference atoms
        pl = []
        for j in range(3):
            ax.scatter(c_ref[i][j][0],
                       c_ref[i][j][1],
                       c_ref[i][j][2],
                       color='red', s=50, marker='o', linewidths=1,
                       edgecolors='black', label="Reference atom")

            ax.text(c_ref[i][j][0] + 0.1,
                    c_ref[i][j][1] + 0.1,
                    c_ref[i][j][2] + 0.1,
                    "{0}".format(j + 1), fontsize=9)

            # Project ligand atom onto the reference face
            pl.append(projection.project_atom_onto_plane(c_oppo[i][j], a, b, c, d))

        # Projected opposite atoms
        for j in range(3):
            ax.scatter(pl[j][0],
                       pl[j][1],
                       pl[j][2],
                       color='blue', s=50, marker='o', linewidths=1,
                       edgecolors='black', label="Projected ligand atom")

            ax.text(pl[j][0] + 0.1,
                    pl[j][1] + 0.1,
                    pl[j][2] + 0.1,
                    "{0}'".format(j + 1), fontsize=9)

        # Draw plane
        x, y, z = zip(*pl)
        projected_oppo_vertices_list = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(ref_vertices_list[i],
                                             alpha=0.5,
                                             color="yellow"))
        ax.add_collection3d(Poly3DCollection(projected_oppo_vertices_list,
                                             alpha=0.5,
                                             color="blue"))

        # Draw line
        for j in range(3):
            merge = list(zip(m.tolist(), c_ref[i][j].tolist()))
            x, y, z = merge
            ax.plot(x, y, z, 'k-', color="black")

        for j in range(3):
            merge = list(zip(m.tolist(), pl[j].tolist()))
            x, y, z = merge
            ax.plot(x, y, z, 'k->', color="black")

        # Set axis
        ax.set_xlabel(r'X', fontsize=10)
        ax.set_ylabel(r'Y', fontsize=10)
        ax.set_zlabel(r'Z', fontsize=10)
        ax.grid(True)

    # Shift subplots down
    st.set_y(1.0)
    fig.subplots_adjust(top=0.25)

    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
    # plt.axis('equal')
    plt.tight_layout()
    plt.show()
