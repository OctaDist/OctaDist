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


class Plot:
    """
    Relationship plot between Zeta and Sigma parameters.

    Parameters
    ----------
    self.data1 : List
        List of data set 1.
    self.data2 = data2
        List of data set 2.
    self.name1 = name1
        Name of data set 1.
    self.name2 = name2
        Name of data set 2.

    """
    def __init__(self, data1, data2, name1="Var1", name2="Var2"):
        self.data1 = data1
        self.data2 = data2
        self.name1 = name1
        self.name2 = name2

        self.start_plot()
        self.config_plot()
        self.set_label()

    def start_plot(self):
        """
        Start plot.

        """
        self.ax = plt.subplot()

    def add_point(self):
        """


        Returns
        -------

        """
        for i in range(len(self.data1)):
            self.ax.scatter(self.data1, self.data2, label=f'Complex {i + 1}')

    def add_text(self):
        for i in range(len(self.data1)):
            self.ax.text(self.data1[i] + 0.2, self.data2[i] + 0.2, i + 1, fontsize=9)

    def add_legend(self):
        # Put a legend below current axis
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                       fancybox=True, shadow=True, ncol=5)

    def config_plot(self):
        # Shrink current axis's height by 10% on the bottom
        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    def set_label(self):
        plt.title(f"Relationship plot between {self.name1} and {self.name2}")
        plt.xlabel(f"{self.name1}")
        plt.ylabel(f"{self.name2}")

    def show_plot(self):
        plt.show()

