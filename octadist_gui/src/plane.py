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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from octadist_gui.src import echo_logs, linear, popup, projection


def proj_planes(self, aco, all_face):
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
        popup.err_no_calc(self)
        return 1
    elif len(aco) > 1:
        popup.err_many_files(self)
        return 1

    echo_logs(self, "Info: Display the selected 4 pairs of opposite planes (faces)")
    echo_logs(self, "      Scattering plot of all atoms")
    echo_logs(self, "      Draw surface for 4 pairs of reference and opposite planes")
    echo_logs(self, "")

    num, metal, ao, co = aco[0]
    # num = number of file, metal = metal center
    # ao = atomic labels, co = atomic coordinates

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
        ax.scatter(co[0][0], co[0][1], co[0][2], color='yellow', marker='o', s=100,
                   linewidths=1, edgecolors='black', label="Metal center")
        ax.text(co[0][0] + 0.1, co[0][1] + 0.1, co[0][2] + 0.1, ao[0], fontsize=9)

        for j in range(1, 7):
            ax.scatter(co[j][0], co[j][1], co[j][2], color='red', marker='o', s=50,
                       linewidths=1, edgecolors='black', label="Ligand atoms")
            ax.text(co[j][0] + 0.1, co[j][1] + 0.1, co[j][2] + 0.1, "{0},{1}".format(ao[j], j), fontsize=9)

        # Draw plane
        ax.add_collection3d(Poly3DCollection(ref_vertices_list[i], alpha=0.5, color=color_list_1[i]))
        ax.add_collection3d(Poly3DCollection(oppo_vertices_list[i], alpha=0.5, color=color_list_2[i]))

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


def twisting_faces(self, aco, all_face):
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
        popup.err_no_calc(self)
        return 1
    elif len(aco) > 1:
        popup.err_many_files(self)
        return 1

    echo_logs(self, "Info: Display the reference and projected atoms")
    echo_logs(self, "      Scattering plot of all projected atoms on the reference plane")
    echo_logs(self, "      Draw surface for 4 pairs of two twisting triangular faces")
    echo_logs(self, "")

    num, metal, ao, co = aco[0]
    # num = number of file, metal = metal center
    # ao = atomic labels, co = atomic coordinates

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
        a, b, c, d = linear.find_eq_of_plane(c_ref[i][0], c_ref[i][1], c_ref[i][2])
        m = projection.project_atom_onto_plane(co[0], a, b, c, d)
        ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
        ax.set_title("Projection plane {0}".format(i + 1), fontsize='10')

        # Projected metal center atom
        ax.scatter(m[0], m[1], m[2], color='orange', s=100, marker='o',
                   linewidths=1, edgecolors='black', label="Metal center")
        ax.text(m[0] + 0.1, m[1] + 0.1, m[2] + 0.1, "{0}'".format(ao[0]), fontsize=9)

        # Reference atoms
        pl = []
        for j in range(3):
            ax.scatter(c_ref[i][j][0], c_ref[i][j][1], c_ref[i][j][2], color='red', s=50, marker='o',
                       linewidths=1, edgecolors='black', label="Reference atom")
            ax.text(c_ref[i][j][0] + 0.1, c_ref[i][j][1] + 0.1, c_ref[i][j][2] + 0.1, "{0}".format(j + 1), fontsize=9)
            # Project ligand atom onto the reference face
            pl.append(projection.project_atom_onto_plane(c_oppo[i][j], a, b, c, d))

        # Projected opposite atoms
        for j in range(3):
            ax.scatter(pl[j][0], pl[j][1], pl[j][2], color='blue', s=50, marker='o',
                       linewidths=1, edgecolors='black', label="Projected ligand atom")
            ax.text(pl[j][0] + 0.1, pl[j][1] + 0.1, pl[j][2] + 0.1, "{0}'".format(j + 1), fontsize=9)

        # Draw plane
        x, y, z = zip(*pl)
        projected_oppo_vertices_list = [list(zip(x, y, z))]
        ax.add_collection3d(Poly3DCollection(ref_vertices_list[i], alpha=0.5, color="yellow"))
        ax.add_collection3d(Poly3DCollection(projected_oppo_vertices_list, alpha=0.5, color="blue"))

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
