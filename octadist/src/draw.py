# OctaDist  Copyright (C) 2019-2024  Rangsiman Ketkaew et al.
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

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import plotly.graph_objects as go

from octadist.src import elements, plane, projection, util


class DrawComplex_Matplotlib:
    """
    Display 3D structure of octahedral complex with label for each atoms using Matplotlib.

    Parameters
    ----------
    atom : list
        Atomic symbols of octahedral structure.
        Default is None.
    coord : list or array_like or tuple or bool
        Atomic coordinates of octahedral structure.
        Default is None.
    cutoff_global : int or float
        Global cutoff for screening bonds.
        Default is 2.0.
    cutoff_hydrogen : int or float
        Cutoff for screening hydrogen bonds.
        Default is 1.2.

    See Also
    --------
    draw.DrawComplex_Plotly :
        Use Plotly engine to draw a complex.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> test = DrawComplex_Matplotlib(atom=atom, coord=coord)
    >>> test.add_atom()
    >>> test.add_bond()
    >>> test.add_legend()
    >>> test.show_plot()

    """

    def __init__(self, atom=None, coord=None, cutoff_global=2.0, cutoff_hydrogen=1.2):
        self.atom = atom
        self.coord = coord
        self.cutoff_global = cutoff_global
        self.cutoff_hydrogen = cutoff_hydrogen

        if self.atom is None:
            raise TypeError("atom is not specified")
        if self.coord is None:
            raise TypeError("coord is not specified")

        self.title_name = "Display Complex"
        self.title_size = "12"
        self.label_size = "10"
        self.show_title = True
        self.show_axis = True
        self.show_grid = True

        self.atoms_pair = []
        self.bond_list = None

        self.start_plot()
        self.plot_title()

    def start_plot(self):
        """
        Introduce figure to plot.

        """
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        # ax = fig.add_subplot(111, projection='3d')

    def plot_title(self, title="Full complex", font_size="12"):
        """
        Add plot title at top position.

        Parameters
        ----------
        title : str
            Top title of the plot.
            Default is "Full complex".
        fontsize : int or float or str
            Font size of title.
            Default is "12".

        """
        self.st = self.fig.suptitle(title, fontsize=font_size)

    def add_atom(self):
        """
        Add all atoms to show in figure.

        """
        for i in range(len(self.coord)):
            # Determine atomic number
            n = elements.number_to_symbol(self.atom[i])
            self.ax.scatter(
                self.coord[i][0],
                self.coord[i][1],
                self.coord[i][2],
                marker="o",
                linewidths=0.5,
                edgecolors="black",
                color=elements.number_to_color(n),
                label=f"{self.atom[i]}",
                s=elements.number_to_radii(n) * 300,
            )

    def add_symbol(self):
        """
        Add symbol of atoms to show in figure.

        """
        for j in range(len(self.atom)):
            self.ax.text(
                self.coord[j][0] + 0.1,
                self.coord[j][1] + 0.1,
                self.coord[j][2] + 0.1,
                f"{self.atom[j]},{j}",
                fontsize=9,
            )

    def add_bond(self):
        """
        Calculate bond distance, screen bond, and add them to show in figure.

        See Also
        --------
        octadist.src.util.find_bonds :
            Find atomic bonds.

        """
        _, self.bond_list = util.find_bonds(
            self.atom, self.coord, self.cutoff_global, self.cutoff_hydrogen
        )

        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            self.atoms_pair.append(atoms)

        for i in range(len(self.atoms_pair)):
            merge = list(zip(self.atoms_pair[i][0], self.atoms_pair[i][1]))
            x, y, z = merge
            self.ax.plot(x, y, z, "-", color="black", linewidth=2)

    def add_face(self, coord):
        """
        Find the faces of octahedral structure and add those faces to show in figure.

        See Also
        --------
        octadist.src.util.find_faces_octa :
            Find all faces of octahedron.

        """
        _, c_ref, _, _ = util.find_faces_octa(coord)

        # Added faces
        color_list = [
            "red",
            "blue",
            "green",
            "yellow",
            "violet",
            "cyan",
            "brown",
            "grey",
        ]

        for i in range(8):
            # Create array of vertices for 8 faces
            get_vertices = c_ref[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]
            self.ax.add_collection3d(
                Poly3DCollection(vertices, alpha=0.5, color=color_list[i])
            )

    def add_legend(self):
        """
        Add atoms legend to show in figure.

        References
        ----------
        1. Remove duplicate labels in legend.
            Ref: https://stackoverflow.com/a/26550501/6596684.

        2. Fix size of point in legend.
            Ref: https://stackoverflow.com/a/24707567/6596684.

        """
        # remove duplicate labels
        handles, labels = self.ax.get_legend_handles_labels()
        handle_list, label_list = [], []

        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        leg = plt.legend(
            handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12
        )

        # fix size of point in legend
        for i in range(len(leg.legend_handles)):
            leg.legend_handles[i]._sizes = [90]

    def config_plot(self, show_title=True, show_axis=True, show_grid=True, **kwargs):
        """
        Setting configuration for figure.

        Parameters
        ----------
        show_title : bool
            If True, show title of figure.
            If False, not show title of figure.
        show_axis : bool
            If True, show axis of figure.
            If False, not show axis of figure.
        show_grid : bool
            If True, show grid of figure.
            If False, not show grid of figure.
        kwargs : dict, optional
            title_name : title name of figure.
            title_size : text size of title.
            label_size : text size of axis labels.

        """
        title_name_user = kwargs.get("title_name")
        self.title_size = kwargs.get("title_size")
        self.label_size = kwargs.get("label_size")
        self.show_title = show_title
        self.show_axis = show_axis
        self.show_grid = show_grid

        if title_name_user is not None:
            self.ax.set_title(title_name_user)

        if self.title_size is not None:
            if title_name_user is None:
                title_name_user = self.title_name
            self.ax.set_title(title_name_user, fontsize=self.title_size)

        if self.label_size is not None:
            self.ax.set_xlabel(r"X", fontsize=self.label_size)
            self.ax.set_ylabel(r"Y", fontsize=self.label_size)
            self.ax.set_zlabel(r"Z", fontsize=self.label_size)

        if not self.show_title:
            self.ax.set_title("")
        if not self.show_axis:
            plt.axis("off")
        if not self.show_grid:
            self.ax.grid(False)

    @staticmethod
    def save_img(save="Complex_saved_by_OctaDist", file="png"):
        """
        Save figure as an image.

        Parameters
        ----------
        save : str
            Name of image file.
            Default is "Complex_saved_by_OctaDist".
        file : str
            Image type.
            Default is "png".

        """
        plt.savefig(f"{save}.{file}")

    @staticmethod
    def show_plot():
        """
        Show plot.

        """
        plt.show()


class DrawComplex_Plotly:
    """
    Display 3D structure of octahedral complex in web browser using Plotly.

    Parameters
    ----------
    atom : list
        Atomic symbols of octahedral structure.
        Default is None.
    coord : list or array_like or tuple or bool
        Atomic coordinates of octahedral structure.
        Default is None.
    cutoff_global : int or float
        Global cutoff for screening bonds.
        Default is 2.0.
    cutoff_hydrogen : int or float
        Cutoff for screening hydrogen bonds.
        Default is 1.2.

    See Also
    --------
    draw.DrawComplex_Matplotlib :
        Use Matplotlib engine to draw a complex.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> test = DrawComplex_Plotly(atom=atom, coord=coord)
    >>> test.add_atom()
    >>> test.add_bond()
    >>> test.show_plot()

    """

    def __init__(self, atom=None, coord=None, cutoff_global=2.0, cutoff_hydrogen=1.2):
        self.atom = atom
        self.coord = coord
        self.cutoff_global = cutoff_global
        self.cutoff_hydrogen = cutoff_hydrogen

        if self.atom is None:
            raise TypeError("atom is not specified")
        if self.coord is None:
            raise TypeError("coord is not specified")

        # Make sure that coord is a NumPy array
        self.coord = np.asarray(self.coord, dtype=np.float32)

        self.title_name = "Display Complex"
        self.title_size = "12"
        self.label_size = "10"
        self.show_title = True
        self.show_axis = True
        self.show_grid = True

        self.atoms_pair = []
        self.bond_list = None

        self.start_plot()
        self.plot_title()

    def start_plot(self):
        """
        Introduce figure to plot.

        """
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        # ax = fig.add_subplot(111, projection='3d')

    def plot_title(self, title="Full complex", font_size="12"):
        """
        Add plot title at top position.

        Parameters
        ----------
        title : str
            Top title of the plot.
            Default is "Full complex".
        fontsize : int or float or str
            Font size of title.
            Default is "12".

        """
        self.st = self.fig.suptitle(title, fontsize=font_size)

    def add_atom(self):
        """
        Add all atoms to show in figure.

        """
        n = [elements.number_to_symbol(i) for i in self.atom]
        s = [elements.number_to_radii(i) * 100 for i in n]
        c = [elements.number_to_color(i) for i in n]

        marker_data = go.Scatter3d(
            x=self.coord[:, 0],
            y=self.coord[:, 1],
            z=self.coord[:, 2],
            marker=dict(
                size=s,
                color=c,
                colorscale="Viridis",
                opacity=0.9,
                line=dict(width=10, color="rgb(0,0,0)"),
                # linewidths=0.5,
                # edgecolors="black",
            ),
            mode="markers",
            name="atoms",
        )
        self.fig = go.Figure(data=[marker_data])
        plotly_warning = "Generated by DrawComplex_Plotly in OctaDist"
        self.fig.update_layout(
            title=self.title_name + " : " + plotly_warning,
            scene=dict(
                xaxis=dict(
                    range=[
                        np.min(self.coord[:, 0]) - 0.5,
                        np.max(self.coord[:, 0]) + 0.5,
                    ]
                ),
                yaxis=dict(
                    range=[
                        np.min(self.coord[:, 1]) - 0.5,
                        np.max(self.coord[:, 1]) + 0.5,
                    ]
                ),
                zaxis=dict(
                    range=[
                        np.min(self.coord[:, 2]) - 0.5,
                        np.max(self.coord[:, 2]) + 0.5,
                    ]
                ),
            ),
            #   autosize=True,
            # width=500, height=500,
            # margin=dict(l=65, r=50, b=65, t=90),
        )

    def add_bond(self):
        """
        Calculate bond distance, screen bond, and add them to show in figure.

        See Also
        --------
        octadist.src.util.find_bonds :
            Find atomic bonds.

        """
        _, self.bond_list = util.find_bonds(
            self.atom, self.coord, self.cutoff_global, self.cutoff_hydrogen
        )

        for i in range(len(self.bond_list)):
            get_atoms = self.bond_list[i]
            x, y, z = zip(*get_atoms)
            atoms = list(zip(x, y, z))
            self.atoms_pair.append(atoms)

        for i in range(len(self.atoms_pair)):
            merge = list(zip(self.atoms_pair[i][0], self.atoms_pair[i][1]))
            x, y, z = merge
            line = go.Scatter3d(
                x=x,
                y=y,
                z=z,
                line=dict(
                    width=20,
                    color="black",
                ),
                opacity=0.7,
                mode="lines",
                name="bond-" + str(i + 1),
            )
            self.fig.add_trace(line)

    # def add_legend(self):
    #     """
    #     Add atoms legend to show in figure.

    #     References
    #     ----------
    #     1. Remove duplicate labels in legend.
    #         Ref: https://stackoverflow.com/a/26550501/6596684.

    #     2. Fix size of point in legend.
    #         Ref: https://stackoverflow.com/a/24707567/6596684.

    #     """
    #     # remove duplicate labels
    #     handles, labels = self.ax.get_legend_handles_labels()
    #     handle_list, label_list = [], []

    #     for handle, label in zip(handles, labels):
    #         if label not in label_list:
    #             handle_list.append(handle)
    #             label_list.append(label)
    #     leg = plt.legend(
    #         handle_list, label_list, loc="lower left", scatterpoints=1, fontsize=12
    #     )

    #     # fix size of point in legend
    #     for i in range(len(leg.legend_handles)):
    #         leg.legend_handles[i]._sizes = [90]

    def save_img(self, save="Complex_saved_by_OctaDist", file="png"):
        """
        Save figure as an image. Note that psutil and plotly-orca are needed for saving Plotly plot as image.

        Parameters
        ----------
        save : str
            Name of image file.
            Default is "Complex_saved_by_OctaDist".
        file : str
            Image type.
            Default is "png".

        """
        self.fig.write_image(f"{save}.{file}")

    def show_plot(self):
        """
        Show plot.

        """
        self.fig.show()


class DrawProjection:
    """
    Display the selected 4 faces of octahedral complex.

    Parameters
    ----------
    atom : list
        Atomic symbols of octahedral structure.
        Default is None.
    coord : list or array_like or tuple
        Atomic coordinates of octahedral structure.
        Default is None.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> test = DrawProjection(atom=atom, coord=coord)
    >>> test.add_atom()
    >>> test.add_symbol()
    >>> test.add_plane()
    >>> test.show_plot()

    """

    def __init__(self, atom=None, coord=None):
        self.atom = atom
        self.coord = coord

        if self.atom is None:
            raise TypeError("atom is not specified")
        if self.coord is None:
            raise TypeError("coord is not specified")

        self.sub_plot = []

        self.start_plot()
        self.plot_title()
        self.shift_plot()

    def start_plot(self):
        """
        Introduce figure to plot.

        """
        self.fig = plt.figure()

        for i in range(4):
            ax = self.fig.add_subplot(2, 2, int(i + 1), projection="3d")
            ax.set_title(f"Pair {i + 1}")
            self.sub_plot.append(ax)

    def plot_title(self, title="4 pairs of opposite planes", font_size="x-large"):
        """
        Add plot title at top position.

        Parameters
        ----------
        title : str
            Top title of the plot.
            Default is "Full complex".
        fontsize : int or float or str
            Font size of title.
            Default is "x-large".

        """
        # self.st = self.fig.suptitle(, fontsize="")
        self.st = self.fig.suptitle(title, fontsize=font_size)

    def shift_plot(self):
        """
        Shift subplots down.
        Default is 0.25.

        """
        self.fig.subplots_adjust(top=0.25)
        self.st.set_y(1.0)

    def add_atom(self):
        """
        Add all atoms to show in figure.

        """
        for i in range(4):
            ax = self.sub_plot[i]
            # Metal
            ax.scatter(
                self.coord[0][0],
                self.coord[0][1],
                self.coord[0][2],
                color="yellow",
                marker="o",
                s=100,
                linewidths=1,
                edgecolors="black",
                label="Metal center",
            )

            # Ligand
            for j in range(1, 7):
                ax.scatter(
                    self.coord[j][0],
                    self.coord[j][1],
                    self.coord[j][2],
                    color="red",
                    marker="o",
                    s=50,
                    linewidths=1,
                    edgecolors="black",
                    label="Ligand atoms",
                )

    def add_symbol(self):
        """
        Add all atoms to show in figure.

        """
        for i in range(4):
            ax = self.sub_plot[i]
            # Metal
            ax.text(
                self.coord[0][0] + 0.1,
                self.coord[0][1] + 0.1,
                self.coord[0][2] + 0.1,
                self.atom[0],
                fontsize=9,
            )

            # Ligand
            for j in range(1, 7):
                ax.text(
                    self.coord[j][0] + 0.1,
                    self.coord[j][1] + 0.1,
                    self.coord[j][2] + 0.1,
                    f"{self.atom[j]},{j}",
                    fontsize=9,
                )

    def add_plane(self):
        """
        Add the projection planes to show in figure.

        See Also
        --------
        octadist.src.util.find_faces_octa :
            Find all faces of octahedron.

        """
        _, c_ref, _, c_oppo = util.find_faces_octa(self.coord)

        color_1 = ["red", "blue", "orange", "magenta"]
        color_2 = ["green", "yellow", "cyan", "brown"]

        for i in range(4):
            ax = self.sub_plot[i]

            # reference face
            get_vertices = c_ref[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices_ref = [list(zip(x, y, z))]

            # opposite face
            x, y, z = zip(*c_oppo[i])
            vertices_oppo = [list(zip(x, y, z))]

            ax.add_collection3d(
                Poly3DCollection(vertices_ref, alpha=0.5, color=color_1[i])
            )
            ax.add_collection3d(
                Poly3DCollection(vertices_oppo, alpha=0.5, color=color_2[i])
            )

    @staticmethod
    def save_img(save="Complex_saved_by_OctaDist", file="png"):
        """
        Save figure as an image.

        Parameters
        ----------
        save : str
            Name of image file.
            Default is "Complex_saved_by_OctaDist".
        file : file
            Image type.
            Default is "png".

        """
        plt.savefig(f"{save}.{file}")

    @staticmethod
    def show_plot():
        """
        Show plot.

        """
        plt.tight_layout()
        plt.show()


class DrawTwistingPlane:
    """
    Display twisting triangular faces and vector projection.

    Parameters
    ----------
    atom : list
        Atomic symbols of octahedral structure.
        Default is None.
    coord : list or array or tuple
        Atomic coordinates of octahedral structure.
        Default is None.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'O', 'O', 'O']
    >>> coord = [[2.298354000, 5.161785000, 7.971898000],
                 [1.885657000, 4.804777000, 6.183726000],
                 [1.747515000, 6.960963000, 7.932784000],
                 [4.094380000, 5.807257000, 7.588689000],
                 [0.539005000, 4.482809000, 8.460004000],
                 [2.812425000, 3.266553000, 8.131637000],
                 [2.886404000, 5.392925000, 9.848966000]]
    >>> test = DrawTwistingPlane(atom=atom, coord=coord)
    >>> test.add_plane()
    >>> test.add_symbol()
    >>> test.add_bond()
    >>> test.show_plot()

    """

    def __init__(self, atom=None, coord=None, symbol_fontsize=15):
        self.atom = atom
        self.coord = coord
        self.symbol_fontsize = symbol_fontsize

        if self.atom is None:
            raise TypeError("atom is not specified")
        if self.coord is None:
            raise TypeError("coord is not specified")

        _, self.c_ref, _, self.c_oppo = util.find_faces_octa(self.coord)

        self.all_ax = []
        self.all_m = []
        self.all_proj_ligs = []

        self.start_plot()
        self.plot_title()
        self.shift_plot()
        self.create_subplots()

    def start_plot(self):
        """
        Introduce figure to plot.

        """
        self.fig = plt.figure()

    def plot_title(
        self, title="Projected twisting triangular faces", font_size="x-large"
    ):
        """
        Add plot title at top position.

        Parameters
        ----------
        title : str
            Top title of the plot.
            Default is "Projected twisting triangular faces".
        fontsize : int or float or str
            Font size of title.
            Default is "x-large".

        """
        self.st = self.fig.suptitle(title, fontsize=font_size)

    def shift_plot(self):
        """
        Shift subplots down.
        Default is 0.25.

        """
        self.fig.subplots_adjust(top=0.25)
        self.st.set_y(1.0)

    def create_subplots(self):
        """
        Create subplots.

        """
        for i in range(4):
            ax = self.fig.add_subplot(2, 2, int(i + 1), projection="3d")
            ax.set_title(f"Projection plane {i + 1}", fontsize="10")

            self.all_ax.append(ax)

    def add_plane(self):
        """
        Add the projection planes to show in figure.

        See Also
        --------
        octadist.src.plane.find_eq_of_plane :
            Find the equation of the plane.
        octadist.src.projection.project_atom_onto_plane :
            Orthogonal projection of point onto the plane.

        """
        for i in range(4):
            a, b, c, d = plane.find_eq_of_plane(
                self.c_ref[i][0], self.c_ref[i][1], self.c_ref[i][2]
            )
            m = projection.project_atom_onto_plane(self.coord[0], a, b, c, d)
            self.all_m.append(m)

            ax = self.all_ax[i]

            # Projected metal center atom
            ax.scatter(
                m[0],
                m[1],
                m[2],
                color="orange",
                s=100,
                marker="o",
                linewidths=1,
                edgecolors="black",
                label="Metal center",
            )

            # Reference atoms
            all_proj_lig = []
            for j in range(3):
                ax.scatter(
                    self.c_ref[i][j][0],
                    self.c_ref[i][j][1],
                    self.c_ref[i][j][2],
                    color="red",
                    s=50,
                    marker="o",
                    linewidths=1,
                    edgecolors="black",
                    label="Reference atom",
                )

                # Project ligand atom onto the reference face
                proj_lig = projection.project_atom_onto_plane(
                    self.c_oppo[i][j], a, b, c, d
                )
                all_proj_lig.append(proj_lig)

                # Projected opposite atoms
                ax.scatter(
                    proj_lig[0],
                    proj_lig[1],
                    proj_lig[2],
                    color="blue",
                    s=50,
                    marker="o",
                    linewidths=1,
                    edgecolors="black",
                    label="Projected ligand atom",
                )

            self.all_proj_ligs.append(all_proj_lig)

            # Draw plane
            get_vertices = self.c_ref[i].tolist()
            x, y, z = zip(*get_vertices)
            vertices = [list(zip(x, y, z))]

            x, y, z = zip(*self.all_proj_ligs[i])
            projected_oppo_vertices_list = [list(zip(x, y, z))]
            ax.add_collection3d(Poly3DCollection(vertices, alpha=0.5, color="yellow"))
            ax.add_collection3d(
                Poly3DCollection(projected_oppo_vertices_list, alpha=0.5, color="blue")
            )

            # Adjust tick spacing
            ax.set_xticks(ax.get_xticks()[::1])
            ax.set_yticks(ax.get_yticks()[::1])
            ax.set_zticks(ax.get_zticks()[::1])

    def add_symbol(self):
        """
        Add all atoms to show in figure.

        """
        for i in range(4):
            ax = self.all_ax[i]
            ax.text(
                self.all_m[i][0] + 0.2,
                self.all_m[i][1] + 0.2,
                self.all_m[i][2] + 0.2,
                f"{self.atom[0]}'",
                fontsize=self.symbol_fontsize,
            )

            for j in range(3):
                ax.text(
                    self.c_ref[i][j][0] + 0.2,
                    self.c_ref[i][j][1] + 0.2,
                    self.c_ref[i][j][2] + 0.2,
                    f"{j + 1}",
                    fontsize=self.symbol_fontsize,
                )

                ax.text(
                    self.all_proj_ligs[i][j][0] + 0.2,
                    self.all_proj_ligs[i][j][1] + 0.2,
                    self.all_proj_ligs[i][j][2] + 0.2,
                    f"{j + 1}'",
                    fontsize=self.symbol_fontsize,
                )

    def add_bond(self):
        """
        Calculate bond distance, screen bond, and add them to show in figure.

        """
        for i in range(4):
            for j in range(3):
                merge = list(zip(self.all_m[i].tolist(), self.c_ref[i][j].tolist()))
                x, y, z = merge
                self.all_ax[i].plot(x, y, z, "-", color="black")

                merge = list(
                    zip(self.all_m[i].tolist(), self.all_proj_ligs[i][j].tolist())
                )
                x, y, z = merge
                self.all_ax[i].plot(x, y, z, "->", color="black")

    @staticmethod
    def save_img(save="Complex_saved_by_OctaDist", file="png"):
        """
        Save figure as an image.

        Parameters
        ----------
        save : str
            Name of image file.
            Default is "Complex_saved_by_OctaDist".
        file : str
            Image type.
            Default is "png".

        """
        plt.savefig(f"{save}.{file}")

    @staticmethod
    def show_plot():
        """
        Show plot.

        """
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
        plt.tight_layout()
        plt.show()
