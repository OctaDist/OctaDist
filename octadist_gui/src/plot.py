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

from octadist_gui.src import echo_logs, popup


def plot_zeta_sigma(self, zeta, sigma):
    """Relationship plot between Zeta and Sigma parameters

    :param self: master frame
    :param zeta: Zeta parameter
    :param sigma: Sigma parameter
    :type zeta: list
    :type sigma: list
    """
    if len(zeta) == 0:
        popup.err_no_calc(self)
        return 1

    echo_logs(self, "Info: Show relationship plot between ζ and Σ")
    echo_logs(self, "")

    ax = plt.subplot()
    for i in range(len(zeta)):
        ax.scatter(zeta, sigma, label='Complex {0}'.format(i + 1))
        ax.text(zeta[i] + 0.2, sigma[i] + 0.2, i + 1, fontsize=9)

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)

    plt.title("Relationship plot between $\zeta$ and $\Sigma$")
    plt.xlabel(r'$\zeta$')
    plt.ylabel(r'$\Sigma$')
    plt.show()


def plot_sigma_theta(self, sigma, theta):
    """Relationship plot between Sigma and Theta parameters

    :param self: master frame
    :param sigma: Sigma parameter
    :param theta: Theta parameter
    :type sigma: list
    :type theta: list
    """
    if len(sigma) == 0:
        popup.err_no_calc(self)
        return 1

    echo_logs(self, "Info: Show relationship plot between Σ and Θ")
    echo_logs(self, "")

    ax = plt.subplot()
    for i in range(len(sigma)):
        ax.scatter(sigma, theta, label='Complex {0}'.format(i + 1))
        ax.text(sigma[i] + 0.2, theta[i] + 0.2, i + 1, fontsize=9)

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)

    plt.title("Relationship plot between $\Sigma$ and $\Theta$")
    plt.xlabel(r'$\Sigma$')
    plt.ylabel(r'$\Theta$')
    plt.show()
