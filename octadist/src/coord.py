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

from operator import itemgetter

import numpy as np
from scipy.spatial import distance

from octadist.src import elements, popup


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
    >>> file = "/home/Jack/[Fe(1-bpp)2][BF4]2-HS.xyz"
    >>> line = count_line(file)

    >>> line
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
    Check file type, read data, extract atom and coord from an input file.

    Parameters
    ----------
    file : str
        User input filename.

    Returns
    -------
    atom : list
        Full atomic labels of complex.
    coord : ndarray
        Full atomic coordinates of complex.

    Notes
    -----
    The following is the file type that OctaDist supports:

    - ``XYZ``
    - ``Gaussian``
    - ``NWChem``
    - ``ORCA``
    - ``Q-Chem``

    Examples
    --------
    >>> file = "/home/Jack/[Fe(1-bpp)2][BF4]2-HS.xyz"
    >>> atom, coord = extract_coord(file)

    >>> atom
    ['Fe', 'N', 'N', 'N', 'N', 'N', 'N']

    >>> coord
    [[-1.95348286e+00,  4.51770478e+00,  1.47855811e+01],
     [-1.87618286e+00,  4.48070478e+00,  1.26484811e+01],
     [-3.90128286e+00,  5.27750478e+00,  1.40814811e+01],
     [-4.88286000e-03,  3.69060478e+00,  1.42392811e+01],
     [-2.18698286e+00,  4.34540478e+00,  1.69060811e+01],
     [-1.17538286e+00,  6.38340478e+00,  1.56457811e+01],
     [-2.75078286e+00,  2.50260478e+00,  1.51806811e+01]]

    """
    if file is None:
        raise TypeError("extract_coord needs one argument: input file")

    atom = []
    coord = np.array([])
    check = True

    # Check file extension
    if file.endswith(".xyz"):
        if check_xyz_file(file):
            atom, coord = get_coord_xyz(file)

        else:
            ftype = "XYZ"
            popup.err_invalid_ftype(ftype)
            check = False

    elif file.endswith(".out") or file.endswith(".log"):
        if check_gaussian_file(file):
            atom, coord = get_coord_gaussian(file)
        elif check_nwchem_file(file):
            atom, coord = get_coord_nwchem(file)
        elif check_orca_file(file):
            atom, coord = get_coord_orca(file)
        elif check_qchem_file(file):
            atom, coord = get_coord_qchem(file)
        else:
            check = False
    else:
        popup.err_wrong_format()
        check = False

    if check:
        # Remove empty string in list
        atom = list(filter(None, atom))
        return atom, coord
    else:
        return atom, coord


def count_metal(atom=None, coord=None):
    """
    Count the number of metal center atom in complex.

    Parameters
    ----------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.

    Returns
    -------
    count : int
        The total number of metal center atom.
    atom_metal : list
        Atomic labels of metal center atom.
    coord_metal : list
        Atomic coordinates of metal center atom.

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

    >>> count, atom_metal, coord_metal = count_metal(atom, coord)

    >>> count
    1

    >>> atom_metal
    ['Fe']

    >>> coord_metal
    [[-1.95348286  4.51770478 14.78558113]]

    """
    if atom is None or coord is None:
        raise TypeError("count_metal needs two arguments: atom, coord")

    count = 0
    atom_metal = []
    coord_metal = []

    for i in range(len(atom)):
        number = elements.check_atom(atom[i])

        if 21 <= number <= 30 or \
                39 <= number <= 48 or \
                57 <= number <= 80 or \
                89 <= number <= 109:

            count += 1
            atom_metal.append(atom[i])
            coord_metal.append(coord[i])

    coord_metal = np.asarray(coord_metal, dtype=np.float64)

    return count, atom_metal, coord_metal


def extract_octa(atom=None, coord=None, coord_metal=None, cutoff_metal_ligand=2.8):
    """
    Search the octahedral structure in complex and return atoms and coordinates.

    Parameters
    ----------
    atom : list
        Full atomic labels of complex.
    coord : array_like
        Full atomic coordinates of complex.
    coord_metal : array_like
        Atomic coordinate of metal center.
    cutoff_metal_ligand : float, optional
        Cutoff distance for screening metal-ligand bond.
        Default value is 2.8.

    Returns
    -------
    atom_octa : list
        Atomic labels of octahedral structure.
    coord_octa : ndarray
        Atomic coordinates of octahedral structure.

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

    >>> coord_metal
    [[-1.95348286  4.51770478 14.78558113]]

    >>> atom_octa, coord_octa = extract_octa(atom, coord, coord_metal)

    >>> atom_octa
    ['Fe', 'N', 'N', 'N', 'N', 'N', 'N']

    >>> coord_octa
    [[-1.95348286e+00,  4.51770478e+00,  1.47855811e+01],
     [-1.87618286e+00,  4.48070478e+00,  1.26484811e+01],
     [-3.90128286e+00,  5.27750478e+00,  1.40814811e+01],
     [-4.88286000e-03,  3.69060478e+00,  1.42392811e+01],
     [-2.18698286e+00,  4.34540478e+00,  1.69060811e+01],
     [-1.17538286e+00,  6.38340478e+00,  1.56457811e+01],
     [-2.75078286e+00,  2.50260478e+00,  1.51806811e+01]]

    """
    if atom is None or coord is None or coord_metal is None:
        raise TypeError("count_metal needs three arguments: atom, coord, coord_metal")

    dist_list = []
    for i in range(len(list(atom))):
        dist = distance.euclidean(coord_metal, coord[i])
        if dist <= cutoff_metal_ligand:
            dist_list.append([atom[i], coord[i], dist])

    # sort list of tuples by distance in ascending order
    dist_list.sort(key=itemgetter(2))

    # Keep only first 7 atoms
    dist_list = dist_list[:7]
    atom_octa, coord_octa, dist = zip(*dist_list)

    atom_octa = list(atom_octa)
    coord_octa = np.asarray(coord_octa, dtype=np.float64)

    return atom_octa, coord_octa


def check_xyz_file(f):
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

    Notes
    -----
    XYZ file format is like following:

    >>> 
    <number of atom>
    comment
    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    ...
    <index 6> <X> <Y> <Z>

    Examples
    --------
    >>> example.xyz 
    7
    Comment: From Excel file
    Fe  6.251705    9.063211    5.914842
    N   8.15961     9.066456    5.463087
    N   6.749414    10.457551   7.179682
    N   5.709997    10.492955   4.658257
    N   4.350474    9.106286    6.356091
    O   5.789096    7.796326    4.611355
    O   6.686381    7.763872    7.209699

    >>> check_xyz_file(example.xyz)
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
    coord : ndarray
        Full atomic coordinates of complex.

    """
    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    atom = []
    for l in line:
        # read atom on 1st column and insert to list
        l_strip = l.strip()
        lst = l_strip.split(' ')[0]
        atom.append(lst)

    file = open(f, "r")
    coord = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def check_gaussian_file(f):
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

    Examples
    --------
    >>> gaussian.log
                                Standard orientation:
    ---------------------------------------------------------------------
    Center     Atomic      Atomic             Coordinates (Angstroms)
    Number     Number       Type             X           Y           Z
    ---------------------------------------------------------------------
         1         26           0        0.000163    1.364285   -0.000039
         2          8           0        0.684192    0.084335   -1.192008
         3          8           0       -0.683180    0.083251    1.191173
         4          7           0        1.639959    1.353157    1.006941
         5          7           0       -0.563377    2.891083    1.435925
    ...

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
    coord : ndarray
        Full atomic coordinates of complex.

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

    for line in nline[start + 5: end]:
        data = line.split()
        data1 = int(data[1])
        coord_x = float(data[3])
        coord_y = float(data[4])
        coord_z = float(data[5])
        data1 = elements.check_atom(data1)
        atom.append(data1)
        coord.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def check_nwchem_file(f):
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

    Examples
    --------
    >>> nwchem.out
      ----------------------
      Optimization converged
      ----------------------
    ...
    ...
     No.       Tag          Charge          X              Y              Z
    ---- ---------------- ---------- -------------- -------------- --------------
       1 Ru(Fragment=1)      44.0000    -3.04059115    -0.08558108    -0.07699482
       2 C(Fragment=1)        6.0000    -1.62704660     2.40971357     0.63980357
       3 C(Fragment=1)        6.0000    -0.61467778     0.59634595     1.68841986
       4 C(Fragment=1)        6.0000     0.31519183     1.41684566     2.30745116
       5 C(Fragment=1)        6.0000     0.28773462     2.80126911     2.08006241
    ...

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
    coord : ndarray
        Full atomic coordinates of complex.

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
        dat1 = elements.check_atom(dat1)
        atom.append(dat1)
        coord.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    coord = np.asarray(coord, dtype=np.float64)

    return atom, coord


def check_orca_file(f):
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

    Examples
    --------
    >>> orca.out
    ---------------------------------
    CARTESIAN COORDINATES (ANGSTROEM)
    ---------------------------------
      C      0.009657    0.000000    0.005576
      C      0.009657   -0.000000    1.394424
      C      1.212436   -0.000000    2.088849
      C      2.415214    0.000000    1.394425
      C      2.415214   -0.000000    0.005575
    ...

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
    coord : ndarray
        Full atomic coordinates of complex.

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

    for line in nline[start + 2:end]:
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


def check_qchem_file(f):
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

    Examples
    --------
    >>> qchem.out
    ******************************
    **  OPTIMIZATION CONVERGED  **
    ******************************
                               Coordinates (Angstroms)
        ATOM                X               Y               Z
         1  C         0.2681746845   -0.8206222796   -0.3704019386
         2  C        -1.1809302341   -0.5901746612   -0.6772716414
         3  H        -1.6636318262   -1.5373167851   -0.9496501352
         4  H        -1.2829834971    0.0829227646   -1.5389938241
         5  C        -1.9678565203    0.0191922768    0.5346693165
    ...

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
    coord : ndarray
        Full atomic coordinates of complex.

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

    for line in nline[start + 5:end]:
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
