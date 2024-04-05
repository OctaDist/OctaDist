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

from operator import itemgetter

import numpy as np
import pymatgen
from scipy.spatial import distance

from octadist.src import elements, popup


def is_cif(f):
    """
    Check if the input file is .cif file format.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    bool : bool
        If file is CIF file, return True.

    See Also
    --------
    get_coord_cif :
        Find atomic coordinates of molecule from CIF file.

    Notes
    -----
    More details about CIF file format are provided at https://en.wikipedia.org/wiki/Crystallographic_Information_File.

    Examples
    --------
    >>> # example.cif
    >>> # example
    >>> # _audit_creation_date              2012-10-26T21:09:50-0400
    >>> # _audit_creation_method            fapswitch 2.2
    >>> # _symmetry_space_group_name_H-M    P1
    >>> # _symmetry_Int_Tables_number       1
    >>> # _space_group_crystal_system       triclinic
    >>> # _cell_length_a                    16.012374
    >>> # _cell_length_b                    14.740457
    >>> # _cell_length_c                    19.436146
    >>> # _cell_angle_alpha                 89.939227
    >>> # _cell_angle_beta                  90.110039
    >>> # _cell_angle_gamma                 90.015104
    >>> # _cell_volume                      4587.49671393
    >>> #
    >>> # loop_
    >>> # _atom_site_label
    >>> # _atom_site_type_symbol
    >>> # _atom_type_description
    >>> # _atom_site_fract_x
    >>> # _atom_site_fract_y
    >>> # _atom_site_fract_z
    >>> # _atom_type_partial_charge
    >>> # C1    C     C_R   0.340882 0.499989 0.500098 0.541130
    >>> # C2    C     C_R   0.528123 0.048033 0.558069 0.232589
    >>> # C3    C     C_R   0.499931 0.902862 0.500001 -0.063750
    >>> # C4    C     C_R   0.500061 0.097137 0.500001 -0.063745
    >>> # C5    C     C_1   0.499958 0.802655 0.499991 0.266033
    >>> # ...
    >>> is_cif("example.cif")
    True

    """
    cif_file = open(f, "r")
    nline = cif_file.readlines()

    for i in range(len(nline)):
        if "loop_" in nline[i]:
            return True

    return False


def get_coord_cif(f):
    """
    Get coordinate from .cif file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Examples
    --------
    >>> file = "example.cif"
    >>> atom, coord = get_coord_cif(file)
    >>> atom
    ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    >>> coord
    array([[18.268051, 11.28912 ,  2.565804],
           [19.823874, 10.436314,  1.381569],
           [19.074466,  9.706294,  3.743576],
           [17.364238, 10.733354,  0.657318],
           [16.149538, 11.306661,  2.913619],
           [18.599941, 12.116308,  4.528988],
           [18.364987, 13.407634,  2.249608]])

    """
    import warnings

    warnings.filterwarnings("ignore")

    # works only with pymatgen <= v2021.3.3
    structure = pymatgen.Structure.from_file(f)
    atom = list(map(lambda x: elements.number_to_symbol(x), structure.atomic_numbers))
    coord = structure.cart_coords

    return atom, coord


def is_xyz(f):
    """
    Check if the input file is .xyz file format.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    bool : bool
        If file is XYZ file, return True.

    See Also
    --------
    get_coord_xyz :
        Find atomic coordinates of molecule from XYZ file.

    Examples
    --------
    >>> # example.xyz
    >>> # 20
    >>> # Comment: From Excel file
    >>> # Fe  6.251705    9.063211    5.914842
    >>> # N   8.15961     9.066456    5.463087
    >>> # N   6.749414    10.457551   7.179682
    >>> # N   5.709997    10.492955   4.658257
    >>> # N   4.350474    9.106286    6.356091
    >>> # O   5.789096    7.796326    4.611355
    >>> # O   6.686381    7.763872    7.209699
    >>> # ...
    >>> is_xyz("example.xyz")
    True

    """
    file = open(f, "r")

    first_line = file.readline()

    # Check if the first line is integer
    try:
        int(first_line)
    except ValueError:
        return False

    if count_line(f) < 9:
        return False
    else:
        return True


def get_coord_xyz(f):
    """
    Get coordinate from .xyz file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Examples
    --------
    >>> file = "Fe-distorted-complex.xyz"
    >>> atom, coord = get_coord_xyz(file)
    >>> atom
    ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    >>> coord
    array([[18.268051, 11.28912 ,  2.565804],
           [19.823874, 10.436314,  1.381569],
           [19.074466,  9.706294,  3.743576],
           [17.364238, 10.733354,  0.657318],
           [16.149538, 11.306661,  2.913619],
           [18.599941, 12.116308,  4.528988],
           [18.364987, 13.407634,  2.249608]])

    """
    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    atom = []
    for l in line:
        # read atom on 1st column and insert to list
        l_strip = l.strip()
        lst = l_strip.split(" ")[0]
        atom.append(lst)

    file = open(f, "r")
    coord = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def is_gaussian(f):
    """
    Check if the input file is Gaussian file format.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    bool : bool
        If file is Gaussian output file, return True.

    See Also
    --------
    get_coord_gaussian :
        Find atomic coordinates of molecule from Gaussian file.

    Examples
    --------
    >>> # gaussian.log
    >>> #                             Standard orientation:
    >>> # ---------------------------------------------------------------------
    >>> # Center     Atomic      Atomic             Coordinates (Angstroms)
    >>> # Number     Number       Type             X           Y           Z
    >>> # ---------------------------------------------------------------------
    >>> #      1         26           0        0.000163    1.364285   -0.000039
    >>> #      2          8           0        0.684192    0.084335   -1.192008
    >>> #      3          8           0       -0.683180    0.083251    1.191173
    >>> #      4          7           0        1.639959    1.353157    1.006941
    >>> #      5          7           0       -0.563377    2.891083    1.435925
    >>> # ...
    >>> is_gaussian("gaussian.log")
    True

    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            return True

    return False


def get_coord_gaussian(f):
    """
    Extract XYZ coordinate from Gaussian output file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Examples
    --------
    >>> file = "Gaussian-Fe-distorted-complex.out"
    >>> atom, coord = get_coord_gaussian(file)
    >>> atom
    ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    >>> coord
    array([[18.268051, 11.28912 ,  2.565804],
           [19.823874, 10.436314,  1.381569],
           [19.074466,  9.706294,  3.743576],
           [17.364238, 10.733354,  0.657318],
           [16.149538, 11.306661,  2.913619],
           [18.599941, 12.116308,  4.528988],
           [18.364987, 13.407634,  2.249608]])

    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    start = 0
    end = 0
    atom, coord = [], []
    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            start = i

    for i in range(start + 5, len(nline)):
        if "---" in nline[i]:
            end = i
            break

    for line in nline[start + 5 : end]:
        data = line.split()
        data1 = int(data[1])
        coord_x = float(data[3])
        coord_y = float(data[4])
        coord_z = float(data[5])
        data1 = elements.number_to_symbol(data1)
        atom.append(data1)
        coord.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def is_nwchem(f):
    """
    Check if the input file is NWChem file format.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    bool : bool
        If file is NWChem output file, return True.

    See Also
    --------
    get_coord_nwchem :
        Find atomic coordinates of molecule from NWChem file.

    Examples
    --------
    >>> # nwchem.out
    >>> #   ----------------------
    >>> #   Optimization converged
    >>> #   ----------------------
    >>> # ...
    >>> # ...
    >>> #  No.       Tag          Charge          X              Y              Z
    >>> # ---- ---------------- ---------- -------------- -------------- --------------
    >>> #    1 Ru(Fragment=1)      44.0000    -3.04059115    -0.08558108    -0.07699482
    >>> #    2 C(Fragment=1)        6.0000    -1.62704660     2.40971357     0.63980357
    >>> #    3 C(Fragment=1)        6.0000    -0.61467778     0.59634595     1.68841986
    >>> #    4 C(Fragment=1)        6.0000     0.31519183     1.41684566     2.30745116
    >>> #    5 C(Fragment=1)        6.0000     0.28773462     2.80126911     2.08006241
    >>> # ...
    >>> is_nwchem("nwchem.out")
    True

    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            if not int(nline[i].split()[4]):
                return False

    for j in range(len(nline)):
        if "Optimization converged" in nline[j]:
            return True

    return False


def get_coord_nwchem(f):
    """
    Extract XYZ coordinate from NWChem output file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Examples
    --------
    >>> file = "NWChem-Fe-distorted-complex.out"
    >>> atom, coord = get_coord_nwchem(file)
    >>> atom
    ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    >>> coord
    array([[18.268051, 11.28912 ,  2.565804],
           [19.823874, 10.436314,  1.381569],
           [19.074466,  9.706294,  3.743576],
           [17.364238, 10.733354,  0.657318],
           [16.149538, 11.306661,  2.913619],
           [18.599941, 12.116308,  4.528988],
           [18.364987, 13.407634,  2.249608]])

    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    start = 0
    end = 0
    atom, coord = [], []
    for i in range(len(nline)):
        if "Optimization converged" in nline[i]:
            start = i

    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            end = int(nline[i].split()[4])

    start = start + 18
    end = start + end
    # The 1st line of coordinate is at 18 lines next to 'Optimization converged'
    for line in nline[start:end]:
        dat = line.split()
        dat1 = int(float(dat[2]))
        coord_x = float(dat[3])
        coord_y = float(dat[4])
        coord_z = float(dat[5])
        dat1 = elements.number_to_symbol(dat1)
        atom.append(dat1)
        coord.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def is_orca(f):
    """
    Check if the input file is ORCA file format.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    bool : bool
        If file is ORCA output file, return True.

    See Also
    --------
    get_coord_orca :
        Find atomic coordinates of molecule from ORCA file.

    Examples
    --------
    >>> # orca.out
    >>> # ---------------------------------
    >>> # CARTESIAN COORDINATES (ANGSTROEM)
    >>> # ---------------------------------
    >>> #   C      0.009657    0.000000    0.005576
    >>> #   C      0.009657   -0.000000    1.394424
    >>> #   C      1.212436   -0.000000    2.088849
    >>> #   C      2.415214    0.000000    1.394425
    >>> #   C      2.415214   -0.000000    0.005575
    >>> # ...
    >>> is_orca("orca.out")
    True

    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()
    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            return True

    return False


def get_coord_orca(f):
    """
    Extract XYZ coordinate from ORCA output file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Examples
    --------
    >>> file = "ORCA-Fe-distorted-complex.out"
    >>> atom, coord = get_coord_orca(file)
    >>> atom
    ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    >>> coord
    array([[18.268051, 11.28912 ,  2.565804],
           [19.823874, 10.436314,  1.381569],
           [19.074466,  9.706294,  3.743576],
           [17.364238, 10.733354,  0.657318],
           [16.149538, 11.306661,  2.913619],
           [18.599941, 12.116308,  4.528988],
           [18.364987, 13.407634,  2.249608]])

    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0
    atom, coord = [], []
    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            start = i

    for i in range(start + 2, len(nline)):
        if "---" in nline[i]:
            end = i - 1
            break

    for line in nline[start + 2 : end]:
        dat = line.split()
        dat1 = dat[0]
        coord_x = float(dat[1])
        coord_y = float(dat[2])
        coord_z = float(dat[3])
        atom.append(dat1)
        coord.append([coord_x, coord_y, coord_z])

    orca_file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def is_qchem(f):
    """
    Check if the input file is Q-Chem file format.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    bool : bool
        If file is Q-Chem output file, return True.

    See Also
    --------
    get_coord_qchem :
        Find atomic coordinates of molecule from Q-Chem file.

    Examples
    --------
    >>> # qchem.out
    >>> # ******************************
    >>> # **  OPTIMIZATION CONVERGED  **
    >>> # ******************************
    >>> #                            Coordinates (Angstroms)
    >>> #     ATOM                X               Y               Z
    >>> #      1  C         0.2681746845   -0.8206222796   -0.3704019386
    >>> #      2  C        -1.1809302341   -0.5901746612   -0.6772716414
    >>> #      3  H        -1.6636318262   -1.5373167851   -0.9496501352
    >>> #      4  H        -1.2829834971    0.0829227646   -1.5389938241
    >>> #      5  C        -1.9678565203    0.0191922768    0.5346693165
    >>> # ...
    >>> is_qchem("qchem.out")
    True

    """
    qchem_file = open(f, "r")
    nline = qchem_file.readlines()

    for i in range(len(nline)):
        if "OPTIMIZATION CONVERGED" in nline[i]:
            return True

    return False


def get_coord_qchem(f):
    """
    Extract XYZ coordinate from Q-Chem output file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Examples
    --------
    >>> file = "Qchem-Fe-distorted-complex.out"
    >>> atom, coord = get_coord_qchem(file)
    >>> atom
    ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    >>> coord
    array([[18.268051, 11.28912 ,  2.565804],
           [19.823874, 10.436314,  1.381569],
           [19.074466,  9.706294,  3.743576],
           [17.364238, 10.733354,  0.657318],
           [16.149538, 11.306661,  2.913619],
           [18.599941, 12.116308,  4.528988],
           [18.364987, 13.407634,  2.249608]])

    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0
    atom, coord = [], []
    for i in range(len(nline)):
        if "OPTIMIZATION CONVERGED" in nline[i]:
            start = i

    for i in range(start + 5, len(nline)):
        if "Z-matrix Print:" in nline[i]:
            end = i - 1
            break

    for line in nline[start + 5 : end]:
        dat = line.split()
        dat1 = dat[1]
        coord_x = float(dat[2])
        coord_y = float(dat[3])
        coord_z = float(dat[4])
        atom.append(dat1)
        coord.append([coord_x, coord_y, coord_z])

    orca_file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def count_line(file=None):
    """
    Count lines in an input file.

    Parameters
    ----------
    file : str
        Absolute or full path of input file.

    Returns
    -------
    i + 1 : int
        Number of line in file.

    Examples
    --------
    >>> file = "[Fe(1-bpp)2][BF4]2-HS.xyz"
    >>> count_line(file)
    27

    """
    if file is None:
        raise TypeError("count_line needs one argument: input file")

    with open(file) as f:
        for i, l in enumerate(f):
            pass

    return i + 1


def extract_coord(file=None):
    """
    Check file type, read data, extract atomic symbols and cartesian coordinate from
    a structure input file provided by the user. This function can efficiently manupulate I/O process.
    File types currently supported are listed in notes below. Other file formats can also be implemented
    easily within this module.

    Parameters
    ----------
    file : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    See Also
    --------
    octadist.main.OctaDist.open_file :
        Open file dialog and to browse input file.
    octadist.main.OctaDist.search_coord :
        Search octahedral structure in complex.

    Notes
    -----
    The following are file types supported by the current virsion of OctaDist:

    - ``CIF``
    - ``XYZ``
    - ``Gaussian``
    - ``NWChem``
    - ``ORCA``
    - ``Q-Chem``

    Examples
    --------
    >>> file = "[Fe(1-bpp)2][BF4]2-HS.xyz"
    >>> atom, coord = extract_coord(file)
    >>> atom
    ['Fe', 'N', 'N', 'N', 'N', 'N', 'N', 'C', 'C']
    >>> coord
    array([[-1.95348286e+00,  4.51770478e+00,  1.47855811e+01],
           [-1.87618286e+00,  4.48070478e+00,  1.26484811e+01],
           [-2.18698286e+00,  4.34540478e+00,  1.69060811e+01],
           [-4.88286000e-03,  3.69060478e+00,  1.42392811e+01],
           [-1.17538286e+00,  6.38340478e+00,  1.56457811e+01],
           [-2.75078286e+00,  2.50260478e+00,  1.51806811e+01],
           [-3.90128286e+00,  5.27750478e+00,  1.40814811e+01],
           [-6.14953418e+00,  8.30666180e+00,  2.91361978e+01],
           [-8.59995241e+00,  7.11630815e+00,  4.52898814e+01]])

    """
    if file is None:
        raise TypeError("extract_coord needs one argument: input file")

    atom = []
    coord = np.array([])
    is_ftype_correct = True
    is_format_correct = True
    is_coord_correct = True

    # Check file extension
    # --- CIF ---
    if file.endswith(".cif"):
        if is_cif(file):
            atom, coord = get_coord_cif(file)
        else:
            is_ftype_correct = False
            is_coord_correct = False
    # --- XYZ ---
    elif file.endswith(".xyz"):
        if is_xyz(file):
            atom, coord = get_coord_xyz(file)
        else:
            is_ftype_correct = False
            is_coord_correct = False
    # --- Other formats ---
    elif file.endswith(".out") or file.endswith(".log"):
        # Gaussian
        if is_gaussian(file):
            atom, coord = get_coord_gaussian(file)
        # NWChem
        elif is_nwchem(file):
            atom, coord = get_coord_nwchem(file)
        # ORCA
        elif is_orca(file):
            atom, coord = get_coord_orca(file)
        # Q-Chem
        elif is_qchem(file):
            atom, coord = get_coord_qchem(file)
        else:
            is_coord_correct = False
    else:
        is_format_correct = False
        is_coord_correct = False

    if not is_ftype_correct:
        popup.err_invalid_ftype()

    if not is_format_correct:
        popup.err_wrong_format()

    if is_coord_correct:
        # if atom and coord are correct, remove empty string in list
        atom = list(filter(None, atom))
        return atom, coord
    else:
        # return empty atom and coord
        return atom, coord


def find_metal(atom=None, coord=None):
    """
    Count the number of metal center atom in complex.

    Parameters
    ----------
    atom : list or None
        Full atomic labels of complex.
        Default is None.
    coord : array_like or None
        Full atomic coordinates of complex.
        Default is None.

    Returns
    -------
    atom_metal : list
        Atomic labels of metal center atom.
    coord_metal : array_like
        Atomic coordinates of metal center atom.
    index_metal : list
        Indices of metal atoms found.

    See Also
    --------
    octadist.src.elements.check_atom :
        Convert atomic number to atomic symbol and vice versa.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'N', 'N', 'N']
    >>> coord = [[-1.95348286e+00,  4.51770478e+00,  1.47855811e+01],
                 [-1.87618286e+00,  4.48070478e+00,  1.26484811e+01],
                 [-3.90128286e+00,  5.27750478e+00,  1.40814811e+01],
                 [-4.88286000e-03,  3.69060478e+00,  1.42392811e+01],
                 [-2.18698286e+00,  4.34540478e+00,  1.69060811e+01],
                 [-1.17538286e+00,  6.38340478e+00,  1.56457811e+01],
                 [-2.75078286e+00,  2.50260478e+00,  1.51806811e+01]]
    >>> atom_metal, coord_metal = find_metal(atom, coord)
    >>> atom_metal
    ['Fe']
    >>> coord_metal
    array([[-1.95348286,  4.51770478, 14.7855811 ]])

    """
    if atom is None or coord is None:
        raise TypeError("find_metal needs two arguments: atom, coord")

    atom_metal = []
    coord_metal = []
    index_metal = []

    for i in range(len(atom)):
        number = elements.number_to_symbol(atom[i])
        if (
            21 <= number <= 30
            or 39 <= number <= 48
            or 57 <= number <= 80
            or 89 <= number <= 109
        ):
            atom_metal.append(atom[i])
            coord_metal.append(coord[i])
            index_metal.append(i)

    coord_metal = np.asarray(coord_metal, dtype=np.float64)

    return atom_metal, coord_metal, index_metal


def extract_octa(atom, coord, ref_index=0, cutoff_ref_ligand=2.8):
    """
    Search the octahedral structure in complex and return atoms and coordinates.

    Parameters
    ----------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.
    ref_index : int
        Index of the reference to be used as the center atom for neighbor atoms
        in octahedral structure of the complex. Python-based index.
        Default is 0.
    cutoff_ref_ligand : float, optional
        Cutoff distance for screening bond distance between reference and ligand atoms.
        Default is 2.8.

    Returns
    -------
    atom_octa : list
        Atomic labels of octahedral structure.
    coord_octa : array_like
        Atomic coordinates of octahedral structure.

    See Also
    --------
    find_metal :
        Find metals in complex.
    octadist.main.OctaDist.search_coord :
        Search octahedral structure in complex.

    Examples
    --------
    >>> atom = ['Fe', 'N', 'N', 'N', 'N', 'N', 'N', 'C', 'C']
    >>> coord = [[-1.95348286e+00,  4.51770478e+00,  1.47855811e+01],
                 [-1.87618286e+00,  4.48070478e+00,  1.26484811e+01],
                 [-3.90128286e+00,  5.27750478e+00,  1.40814811e+01],
                 [-4.88286000e-03,  3.69060478e+00,  1.42392811e+01],
                 [-2.18698286e+00,  4.34540478e+00,  1.69060811e+01],
                 [-1.17538286e+00,  6.38340478e+00,  1.56457811e+01],
                 [-2.75078286e+00,  2.50260478e+00,  1.51806811e+01],
                 [-6.14953418e+00,  8.30666180e+00,  2.91361978e+01],
                 [-8.59995241e+00,  7.11630815e+00,  4.52898814e+01]]
    >>> atom_octa, coord_octa = extract_octa(atom, coord)
    >>> atom_octa
    ['Fe', 'N', 'N', 'N', 'N', 'N', 'N']
    >>> coord_octa
    array([[-1.95348286e+00,  4.51770478e+00,  1.47855811e+01],
           [-1.87618286e+00,  4.48070478e+00,  1.26484811e+01],
           [-2.18698286e+00,  4.34540478e+00,  1.69060811e+01],
           [-4.88286000e-03,  3.69060478e+00,  1.42392811e+01],
           [-1.17538286e+00,  6.38340478e+00,  1.56457811e+01],
           [-2.75078286e+00,  2.50260478e+00,  1.51806811e+01],
           [-3.90128286e+00,  5.27750478e+00,  1.40814811e+01]])

    """
    if ref_index < 0:
        raise ValueError(
            "index of the reference center atom must be equal or greater than zero"
        )
    elif ref_index + 1 > len(atom):
        raise ValueError(
            "index of the reference center atom is greater than the total number of atoms in the complex."
        )

    dist_list = []
    for i in range(len(list(atom))):
        dist = distance.euclidean(coord[ref_index], coord[i])
        if dist <= cutoff_ref_ligand:
            dist_list.append([atom[i], coord[i], dist])

    # sort list of tuples by distance in ascending order
    dist_list.sort(key=itemgetter(2))

    # Keep only first 7 atoms
    dist_list = dist_list[:7]
    atom_octa, coord_octa, dist = zip(*dist_list)
    atom_octa = list(atom_octa)
    coord_octa = np.asarray(coord_octa, dtype=np.float64)

    return atom_octa, coord_octa
