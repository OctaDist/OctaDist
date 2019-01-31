"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import plane
import proj
import elements
import tools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def draw_full_complex(fal, fcl):
    """Display 3D structure of octahedral complex with label for each atoms

    :param fal: list - full_atom_list
    :param fcl: array - full_coord_list
    :return:
    """

    print("Info: Display scattering plot of all atoms")

    fig = plt.figure()
    ax = Axes3D(fig)

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n),
                   label="{}".format(fal[i]),
                   s=elements.check_radii(n) * 300)

        # if fal[i] != "H":
        #     ax.text(fcl[i][0] + 0.1, fcl[i][1] + 0.1, fcl[i][2] + 0.1,
        #             "{0}".format(fal[i]), fontsize=10)
        #     ax.text(fcl[i][0], fcl[i][1], fcl[i][2], "{0}".format(fal[i]),
        #             fontsize=5, ha="center", va="center", style="normal")

    # Calculate distance
    bond_list = tools.calc_bond_distance(fal, fcl)

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


def draw_full_complex_and_faces(fal, fcl, pcl):
    """Display 3D structure of octahedral complex with label for each atoms

    :param fal: list - full_atom_list
    :param fcl: array - full_coord_list
    :param pcl: array - coordinate of atom in selected plane list
    :return:
    """

    print("Info: Display scattering plot of all atoms")
    print("      Draw surface for all 8 faces of selected octahedron")

    fig = plt.figure()
    ax = Axes3D(fig)
    vertices_list = []

    # Create array of vertices for 8 faces
    for i in range(8):
        get_vertices = pcl[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        vertices_list.append(vertices)

    # The following is for showing only 4 faces whose the minimum Theta value
    # for i in range(4):
    #     get_vertices = ref_pcl[i].tolist()
    #     x, y, z = zip(*get_vertices)
    #     vertices = [list(zip(x, y, z))]
    #     vertices_list.append(vertices)

    # Plot all atoms
    for i in range(len(fcl)):
        # Determine atomic number
        n = elements.check_atom(fal[i])
        ax.scatter(fcl[i][0], fcl[i][1], fcl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n),
                   label="{}".format(fal[i]),
                   s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow",
                  "violet", "cyan", "brown", "grey"]

    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i],
                                             alpha=0.5,
                                             color=color_list[i]))

    # Calculate distance
    bond_list = tools.calc_bond_distance(fal, fcl)

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


def draw_octahedron(al, cl):
    """Display 3D structure of octahedral complex

    :param al: list - atom_list
    :param cl: array - coord_list
    :return:
    """

    print("Info: Display scattering plot of truncated octahedral structure")
    print("      Draw surface for all 8 faces of selected octahedron")

    fig = plt.figure()
    ax = Axes3D(fig)

    # Plot atoms
    for i in range(len(cl)):
        # Determine atomic number
        n = elements.check_atom(al[i])
        ax.scatter(cl[i][0], cl[i][1], cl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n),
                   label="{}".format(al[i]),
                   s=elements.check_radii(n) * 300)

    # Draw line
    for i in range(1, len(cl)):
        merge = list(zip(cl[0], cl[i]))
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


def draw_octahedron_and_faces(al, cl, pcl):
    """Display 3D structure of octahedral complex with 8 faces

    :param al: list - atom_list
    :param cl: array - coord_list
    :param pcl: array - coordinate of atom of 8 faces list
    :return:
    """

    print("Info: Display scattering plot of truncated octahedral structure")
    print("      Draw surface for all 8 faces of selected oatahedral")

    fig = plt.figure()
    ax = Axes3D(fig)
    vertices_list = []

    # Create array of vertices for 8 faces
    for i in range(8):
        get_vertices = pcl[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        vertices_list.append(vertices)

    # Plot atoms
    for i in range(len(cl)):
        # Determine atomic number
        n = elements.check_atom(al[i])
        ax.scatter(cl[i][0], cl[i][1], cl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n),
                   label="{}".format(al[i]),
                   s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow",
                  "violet", "cyan", "brown", "grey"]

    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i],
                                             alpha=0.5,
                                             color=color_list[i]))

    # Draw line
    for i in range(1, len(cl)):
        merge = list(zip(cl[0], cl[i]))
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


def draw_octahedron_and_opt_faces(al, cl, ref_pcl):
    """Display 3D structure of octahedral complex with 8 faces

    :param al: list - atom_list
    :param cl: array - coord_list
    :param ref_pcl: array - coordinate of atom in selected optimal 4 faces
    :return:
    """

    print("Info: Display scattering plot of truncated octahedral structure")
    print("      Draw surface for all 8 faces of selected oatahedral")

    # Plot and configuration
    fig = plt.figure()
    ax = Axes3D(fig)
    vertices_list = []

    # The following is for showing only 4 faces whose the minimum Theta value
    for i in range(4):
        get_vertices = ref_pcl[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        vertices_list.append(vertices)

    # Plot atoms
    for i in range(len(cl)):
        # Determine atomic number
        n = elements.check_atom(al[i])
        ax.scatter(cl[i][0], cl[i][1], cl[i][2],
                   marker='o', linewidths=0.5, edgecolors='black',
                   color=elements.check_color(n),
                   label="{}".format(al[i]),
                   s=elements.check_radii(n) * 300)

    # Draw plane
    color_list = ["red", "blue", "green", "yellow"]

    for i in range(len(vertices_list)):
        ax.add_collection3d(Poly3DCollection(vertices_list[i],
                                             alpha=0.5,
                                             color=color_list[i]))

    # Draw line
    for i in range(1, len(cl)):
        merge = list(zip(cl[0], cl[i]))
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
    ax.set_title('Octahedral structure with optimal 4 faces', fontsize="12")
    ax.grid(True)

    # plt.axis('equal')
    # plt.axis('off')
    plt.show()


def draw_projection_planes(al, cl, vl, ovl):
    """Display the selected 4 faces of octahedral complex

    :param al: atom_list
    :param cl: coord_list
    :param vl: ref_pcl
    :param ovl: oppo_pcl
    :return:
    """

    print("Info: Display the selected 4 pairs of opposite faces")
    print("      Scattering plot of all atoms")
    print("      Draw surface for 4 pairs of reference and opposite faces")

    # reference face
    ref_vertices_list = []

    for i in range(4):
        get_vertices = vl[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        ref_vertices_list.append(vertices)

    # opposite face
    oppo_vertices_list = []

    for i in range(4):
        x, y, z = zip(*ovl[i])
        vertices = [list(zip(x, y, z))]
        oppo_vertices_list.append(vertices)

    fig = plt.figure()
    st = fig.suptitle("4 pairs of opposite faces", fontsize="x-large")

    # Display four planes
    color_list_1 = ["red", "blue", "orange", "magenta"]
    color_list_2 = ["green", "yellow", "cyan", "brown"]

    for i in range(4):
        ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
        ax.set_title("Plane {}".format(i + 1))
        ax.scatter(cl[0][0], cl[0][1], cl[0][2],
                   color='yellow', marker='o', s=100,
                   linewidths=1, edgecolors='black', label="Metal center")
        ax.text(cl[0][0] + 0.1, cl[0][1] + 0.1, cl[0][2] + 0.1,
                al[0], fontsize=9)

        for j in range(1, 7):
            ax.scatter(cl[j][0], cl[j][1], cl[j][2],
                       color='red', marker='o', s=50,
                       linewidths=1, edgecolors='black', label="Ligand atoms")
            ax.text(cl[j][0] + 0.1, cl[j][1] + 0.1, cl[j][2] + 0.1,
                    "{0},{1}".format(al[j], j), fontsize=9)

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


def draw_twisting_faces(al, cl, vl, ovl):
    """Display twisting triangular faces and vector projection

    :param al: list - atom_list
    :param cl: array - coord_list
    :param vl: ref_pcl - reference plane list
    :param ovl: oppo_pcl - opposite plane list
    :return:
    """

    print("Info: Display the reference and projected atoms")
    print("      Scattering plot of all projected atoms on the reference plane")
    print("      Draw surface for 4 pairs of two twisting triangular faces")

    ref_vertices_list = []

    for i in range(4):
        get_vertices = vl[i].tolist()
        x, y, z = zip(*get_vertices)
        vertices = [list(zip(x, y, z))]
        ref_vertices_list.append(vertices)

    fig = plt.figure()
    st = fig.suptitle("Projected twisting triangular faces", fontsize="x-large")

    for i in range(4):
        a, b, c, d = plane.find_eq_of_plane(vl[i][0], vl[i][1], vl[i][2])
        m = proj.project_atom_onto_plane(cl[0], a, b, c, d)

        ax = fig.add_subplot(2, 2, int(i + 1), projection='3d')
        ax.set_title("Projection plane {0}".format(i + 1), fontsize='10')

        # Projected metal center atom
        ax.scatter(m[0], m[1], m[2],
                   color='orange', s=100, marker='o',
                   linewidths=1, edgecolors='black',
                   label="Metal center")
        ax.text(m[0] + 0.1, m[1] + 0.1, m[2] + 0.1,
                "{0}'".format(al[0]), fontsize=9)

        # Reference atoms
        pl = []

        for j in range(3):
            ax.scatter(vl[i][j][0], vl[i][j][1], vl[i][j][2],
                       color='red', s=50, marker='o',
                       linewidths=1, edgecolors='black',
                       label="Reference atom")
            ax.text(vl[i][j][0] + 0.1, vl[i][j][1] + 0.1, vl[i][j][2] + 0.1,
                    "{0}".format(j + 1), fontsize=9)
            # Project ligand atom onto the reference face
            pl.append(proj.project_atom_onto_plane(ovl[i][j], a, b, c, d))

        # Projected opposite atoms
        for j in range(3):
            ax.scatter(pl[j][0], pl[j][1], pl[j][2],
                       color='blue', s=50, marker='o',
                       linewidths=1, edgecolors='black',
                       label="Projected ligand atom")
            ax.text(pl[j][0] + 0.1, pl[j][1] + 0.1, pl[j][2] + 0.1,
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
            merge = list(zip(m.tolist(), vl[i][j].tolist()))
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


def show_plot_angles(s, t):
    """Plot graph between Sigma and Theta parameters for multiple files

    :param s: array - computed Sigma parameter
    :param t: array - computed Theta parameter
    :return:
    """

    print("Info: Show relationship plot between Σ and Θ\n")

    ax = plt.subplot()

    for i in range(len(s)):
        ax.scatter(s, t, label='Complex %i' % int(i + 1))
        ax.text(s[i] + 0.2, t[i] + 0.2, i + 1, fontsize=9)

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
              fancybox=True, shadow=True, ncol=5)

    plt.title("Relationship plot between $\Sigma$ and $\Theta$")
    plt.xlabel(r'$\Sigma$')
    plt.ylabel(r'$\Theta$')
    plt.show()
