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

from octadist_gui.src import elements, popup


def count_line(file):
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

    """
    with open(file) as f:
        for i, l in enumerate(f):
            pass

    return i + 1


def get_coord(f):
    """
    Check file type, read data, extract atom and coord from an input file.

    Parameters
    ----------
    f : str
        User input filename.

    Returns
    -------
    a_full : array_like
        Full atomic labels of complex.
    c_full : ndarray_like
        Full atomic coordinates of complex.

    Notes
    -----
    The following is the file type that OctaDist supports:

    - ``XYZ``
    - ``Gaussian``
    - ``NWChem``
    - ``ORCA``
    - ``Q-Chem``

    """
    a_full = []
    c_full = []
    check = True

    # Check file extension
    if f.endswith(".xyz"):
        if check_xyz_file(f):
            a_full, c_full = get_coord_xyz(f)

        else:
            ftype = "XYZ"
            popup.err_invalid_ftype(ftype)
            check = False

    elif f.endswith(".out") or f.endswith(".log"):
        if check_gaussian_file(f):
            a_full, c_full = get_coord_gaussian(f)

        elif check_nwchem_file(f):
            a_full, c_full = get_coord_nwchem(f)

        elif check_orca_file(f):
            a_full, c_full = get_coord_orca(f)

        elif check_qchem_file(f):
            a_full, c_full = get_coord_qchem(f)

        else:
            check = False

    else:
        popup.err_wrong_format()
        check = False

    # return values
    if check:
        # Remove empty string in list
        a_full = list(filter(None, a_full))
        return a_full, c_full

    else:
        return a_full, c_full


def count_metal(a_full, c_full):
    """
    Count the number of metal center atom in complex.

    Parameters
    ----------
    a_full : list
        Full atomic labels of complex.
    c_full : list
        Full atomic coordinates of complex.

    Returns
    -------
    count : int
        The total number of metal center atom.
    a_metal : list
        Atomic labels of metal center atom.
    c_metal : list
        Atomic coordinates of metal center atom.

    """
    count = 0
    a_metal = []
    c_metal = []

    for i in range(len(a_full)):
        number = elements.check_atom(a_full[i])

        if 21 <= number <= 30 or \
                39 <= number <= 48 or \
                57 <= number <= 80 or \
                89 <= number <= 109:

            count += 1
            a_metal.append(a_full[i])
            c_metal.append(c_full[i])

    return count, a_metal, c_metal


def search_octa(a_full, c_full, c_metal, cutoff_metal_ligand=2.8):
    """
    Search the octahedral structure in complex.

    Parameters
    ----------
    a_full : list
        Full atomic labels of complex.
    c_full : list
        Full atomic coordinates of complex.
    c_metal : list
        Atomic coordinate of metal center.
    cutoff_metal_ligand : float, optional
        Cutoff distance for screening metal-ligand bond.
        Default value is 2.8.

    Returns
    -------
    a_octa : list
        Atomic labels of octahedral structure.
    c_octa : ndarray
        Atomic coordinates of octahedral structure.

    """
    dist_list = []
    for i in range(len(a_full)):
        dist = distance.euclidean(c_metal, c_full[i])
        if dist <= cutoff_metal_ligand:
            dist_list.append([a_full[i], c_full[i], dist])

    # sort list of tuples by distance in ascending order
    dist_list.sort(key=itemgetter(2))

    # Get only first 7 atoms
    dist_list = dist_list[:7]

    # Collect atom and coordinates
    a_octa, c_octa, dist = zip(*dist_list)

    # list --> array
    c_octa = np.asarray(c_octa, dtype=np.float64)

    return a_octa, c_octa


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
    a_full : list
        Full atomic labels of complex.
    c_full : ndarray
        Full atomic coordinates of complex.

    """
    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    a_full = []
    for l in line:
        # read atom on 1st column and insert to list
        l_strip = l.strip()
        lst = l_strip.split(' ')[0]
        a_full.append(lst)

    file = open(f, "r")
    c_full = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    c_full = np.asarray(c_full, dtype=np.float64)

    return a_full, c_full


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
    a_full : list
        Full atomic labels of complex.
    c_full : ndarray
        Full atomic coordinates of complex.

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

    start = 0
    end = 0
    a_full, c_full = [], []
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
        a_full.append(data1)
        c_full.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    c_full = np.asarray(c_full, dtype=np.float64)

    return a_full, c_full


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
    a_full : list
        Full atomic labels of complex.
    c_full : ndarray
        Full atomic coordinates of complex.

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

    start = 0
    end = 0
    a_full, c_full = [], []
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
        a_full.append(dat1)
        c_full.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    c_full = np.asarray(c_full, dtype=np.float64)

    return a_full, c_full


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
    a_full : list
        Full atomic labels of complex.
    c_full : ndarray
        Full atomic coordinates of complex.

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

    start = 0
    end = 0
    a_full, c_full = [], []
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
        a_full.append(dat1)
        c_full.append([coord_x, coord_y, coord_z])

    orca_file.close()

    c_full = np.asarray(c_full, dtype=np.float64)

    return a_full, c_full


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
    a_full : list
        Full atomic labels of complex.
    c_full : ndarray
        Full atomic coordinates of complex.

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
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0
    a_full, c_full = [], []
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
        a_full.append(dat1)
        c_full.append([coord_x, coord_y, coord_z])

    orca_file.close()

    c_full = np.asarray(c_full, dtype=np.float64)

    return a_full, c_full
