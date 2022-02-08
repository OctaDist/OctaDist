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

# Use TkAgg as MPL backend
# Note that IPython service such as Google Colab does not support TkAgg
# try:
#     import tkinter
#     import matplotlib

#     matplotlib.use("TkAgg")
# except ImportError:
#     pass

__author__ = "R. Ketkaew, Y. Tantirungrotechai, P. Harding, G. Chastanet, P. Guionneau, M. Marchivie, D. J. Harding"
__author_full__ = (
    "Rangsiman Ketkaew, Yuthana Tantirungrotechai, Phimphaka Harding, Guillaume Chastanet, "
    "Philippe Guionneau, Mathieu Marchivie, David J. Harding"
)
__maintainer__ = "Rangsiman Ketkaew"
__copyright__ = "OctaDist  Copyright (C) 2019  Rangsiman Ketkaew et al."
__license__ = "GNU v3"
__credit__ = "OctaDist Development Team"
__email__ = "rangsiman1993@gmail.com"
__version__ = "3.0.0"
__revision__ = "2021.300"
__release__ = "2021"
__status__ = "stable"
__title__ = "Octahedral Distortion Calculator"
__description__ = "A tool for calculating distortion parameters in molecule."
__doc__ = "OctaDist documentation is available at https://octadist.readthedocs.io"
__help__ = "https://octadist.readthedocs.io"
__website__ = "https://octadist.github.io"
__github__ = "https://github.com/OctaDist/OctaDist"
__ref__ = "Dalton Trans., 2021,50, 1086-1096"
__doi__ = "https://doi.org/10.1039/D0DT03988H"

__all__ = [
    "calc",
    "draw",
    "elements",
    "linear",
    "io",
    "plane",
    "plot",
    "popup",
    "projection",
    "structure",
    "tools",
    "util",
    # -----------------------
    "CalcDistortion",
    "DrawComplex_Matplotlib",
    "DrawComplex_Plotly",
    "DrawProjection",
    "DrawTwistingPlane",
    "check_atom",
    "check_radii",
    "check_color",
    "angle_sign",
    "angle_btw_vectors",
    "angle_btw_planes",
    "triangle_area",
    "count_line",
    "extract_coord",
    "find_metal",
    "extract_octa",
    "is_cif",
    "is_xyz",
    "is_gaussian",
    "is_nwchem",
    "is_orca",
    "is_qchem",
    "get_coord_cif",
    "get_coord_xyz",
    "get_coord_gaussian",
    "get_coord_nwchem",
    "get_coord_orca",
    "get_coord_qchem",
    "find_eq_of_plane",
    "find_fit_plane",
    "Plot",
    "project_atom_onto_line",
    "project_atom_onto_plane",
    "DataComplex",
    "StructParam",
    "SurfaceArea",
    "CalcJahnTeller",
    "CalcRMSD",
    "find_bonds",
    "find_faces_octa",
]


# Bring sub-modules to top-level directory

from octadist import logo
from .logo import Icon_Base64

from octadist import src

from .src import __src__

from .src import calc
from .src import draw
from .src import elements
from .src import linear
from .src import io
from .src import plane
from .src import plot
from .src import popup
from .src import projection
from .src import structure
from .src import tools
from .src import util

# Bring function and method to top-level directory

from .src.calc import CalcDistortion

from .src.draw import DrawComplex_Matplotlib
from .src.draw import DrawComplex_Plotly
from .src.draw import DrawProjection
from .src.draw import DrawTwistingPlane

from .src.elements import number_to_symbol
from .src.elements import number_to_radii
from .src.elements import number_to_color

from .src.linear import angle_sign
from .src.linear import angle_btw_vectors
from .src.linear import angle_btw_planes
from .src.linear import triangle_area

from .src.io import count_line
from .src.io import extract_coord
from .src.io import find_metal
from .src.io import extract_octa
from .src.io import is_xyz
from .src.io import is_gaussian
from .src.io import is_nwchem
from .src.io import is_orca
from .src.io import is_qchem
from .src.io import get_coord_xyz
from .src.io import get_coord_gaussian
from .src.io import get_coord_nwchem
from .src.io import get_coord_orca
from .src.io import get_coord_qchem

from .src.plane import find_eq_of_plane
from .src.plane import find_fit_plane

from .src.plot import Plot

from .src.projection import project_atom_onto_line
from .src.projection import project_atom_onto_plane

from .src.structure import DataComplex
from .src.structure import StructParam
from .src.structure import SurfaceArea

from .src.tools import CalcJahnTeller
from .src.tools import CalcRMSD

from .src.util import find_bonds
from .src.util import find_faces_octa

