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

__author__ = "R. Ketkaew, Y. Tantirungrotechai, D. J. Harding, P. Harding, and M. Marchivie"
__maintainer__ = "Rangsiman Ketkaew"
__copyright__ = "OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al."
__license__ = "GNU v3"
__credit__ = "OctaDist development team"
__email__ = "rangsiman1993@gmail.com"
__version__ = "2.5.2"
__revision__ = "2019.252"
__release__ = "May 2019"
__status__ = "stable"
__website__ = "https://octadist.github.io"
__github__ = "https://github.com/OctaDist/OctaDist"
__doc__ = "OctaDist: A tool for calculating distortion parameters in coordination complexes."
__manual__ = "https://octadist.github.io/manual.html"

__all__ = \
    ['calc_d_mean',
     'calc_zeta',
     'calc_delta',
     'calc_sigma',
     'calc_theta',
     'calc_all'
     ]

# Bring sub-modules and methods to top-level directory

from octadist_gui import src
from .src import __src__

from .src.calc import calc_d_mean
from .src.calc import calc_zeta
from .src.calc import calc_delta
from .src.calc import calc_sigma
from .src.calc import calc_theta
from .src.calc import calc_all

