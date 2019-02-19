"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import linear
import elements
import popup
import tkinter as tk


def file_lines(file):
    """Count line in file

    :param file: string - absolute path of file
    :return: number of line in file
    """
    with open(file) as f:
        for i, l in enumerate(f):
            pass

    return i + 1


def check_xyz_file(f):
    """Check if the input file is .xyz file format

    xyz file format
    ---------------

    <number of atom>
    comment
    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    ...
    <index 6> <X> <Y> <Z>

    ***The first atom must be a metal center.
    :param f: string - user input filename
    :return: if the file is .xyz format, return True
    """
    file = open(f, "r")

    first_line = file.readline()

    # Check if the first line is integer
    try:
        int(first_line)
    except ValueError:
        return True

    if file_lines(f) < 9:
        return False
    else:
        return True


def check_gaussian_file(f):
    """Check if the input file is Gaussian file format

    :param f: string - user input file
    :return: if file is Gaussian output file, return True
    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            return True

    return False


def check_nwchem_file(f):
    """Check if the input file is NWChem file format

    :param f: string - user input file
    :return: if file is NWChem output file, return True
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


def check_orca_file(f):
    """Check if the input file is ORCA file format

    :param f: string - user input file
    :return: if file is ORCA output file, return True
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            return True

    return False


def check_qchem_file(f):
    """Check if the input file is Q-Chem file format

    :param f: string - user input file
    :return: if file is Q-Chem output file, return True
    """

    qchem_file = open(f, "r")
    nline = qchem_file.readlines()

    for i in range(len(nline)):
        if "OPTIMIZATION CONVERGED" in nline[i]:
            return True

    return False


def get_coord_xyz(f):
    """Get coordinate from .xyz file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    atom_full = []

    for l in line:
        # read atom on 1st column and insert to array
        l_strip = l.strip()
        lst = l_strip.split(' ')[0]
        atom_full.append(lst)

    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> file.seek(0) <<
        2. use >> file = open(f, "r") <<
    """

    file = open(f, "r")
    coord_full = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    return atom_full, coord_full


def get_coord_gaussian(f):
    """Extract XYZ coordinate from Gaussian output file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    start = 0
    end = 0

    atom_full, coord_full = [], []

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

        atom_full.append(data1)
        coord_full.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    return atom_full, coord_full


def get_coord_nwchem(f):
    """Extract XYZ coordinate from NWChem output file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    start = 0
    end = 0

    atom_full, coord_full = [], []

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

        atom_full.append(dat1)
        coord_full.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    return atom_full, coord_full


def get_coord_orca(f):
    """Extract XYZ coordinate from ORCA output file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0

    atom_full, coord_full = [], []

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

        atom_full.append(dat1)
        coord_full.append([coord_x, coord_y, coord_z])

    orca_file.close()

    return atom_full, coord_full


def get_coord_qchem(f):
    """Extract XYZ coordinate from Q-Chem output file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0

    atom_full, coord_full = [], []

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

        atom_full.append(dat1)
        coord_full.append([coord_x, coord_y, coord_z])

    orca_file.close()

    return atom_full, coord_full


def get_coord(f):
    """Check file type, read data, extract atom and coord from input file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    # Atom no. 1   metal center
    #          2-7 ligand atoms
    #          3-n other atoms

    # Check file extension
    if f.endswith(".xyz"):
        if check_xyz_file(f):
            print("Info: Check file type: XYZ file")
            atom_full, coord_full = get_coord_xyz(f)
        else:
            print("Error: Invalid XYZ file format")
            print("Error: Could not read data in XYZ file %s" % f)

    elif f.endswith(".out") or f.endswith(".log"):
        if check_gaussian_file(f):
            print("Info: Check file type: Gaussian Output")
            atom_full, coord_full = get_coord_gaussian(f)
        elif check_nwchem_file(f):
            print("Info: Check file type: NWChem Output")
            atom_full, coord_full = get_coord_nwchem(f)
        elif check_orca_file(f):
            print("Info: Check file type: ORCA Output")
            atom_full, coord_full = get_coord_orca(f)
        elif check_qchem_file(f):
            print("Info: Check file type: Q-Chem Output")
            atom_full, coord_full = get_coord_qchem(f)
        else:
            print("Error: Could not read output file %s" % f)

    else:
        print("Error: Could not read file %s" % f)
        print("Error: File type is not supported by the current version of OctaDist")

    # Remove empty string in list
    atom_full = list(filter(None, atom_full))

    return atom_full, coord_full


def auto_search_octa(af, cf):
    """Auto-search octahedral structure, on request.

    :param af: list - atom_full
    :param cf: array - coord_full
    :return atom_octa: atom list of extracted octahedral structure
    :return coord_octa: coord list of extracted octahedral structure
    """
    # Determine transition metal/heavy atoms
    count = 0
    atom_metal = []
    coord_metal = []

    for i in range(len(af)):
        if elements.check_atom(af[i]) >= 21:
            atom_metal.append(af[i])
            coord_metal.append(cf[i])
            count += 1

    # Determine octahedral structure
    if count == 0:
        popup.no_trans_metal_warning()
        return 1

    elif count == 1:
        dist_list = []

        for i in range(len(af)):
            dist = linear.distance_between(coord_metal[0], cf[i])
            dist_list.append([af[i], cf[i], dist])

        # Sort out bond distance
        p = 0
        while p < len(dist_list):
            r = p
            q = p + 1
            while q < len(dist_list):
                if dist_list[r][2] > dist_list[q][2]:
                    r = q
                q += 1
            dist_list[p], dist_list[r] = dist_list[r], dist_list[p]
            p += 1

        # Get only first 7 atoms
        dist_list = dist_list[:7]

        # Collect atom and coordinates
        atom_octa, coord_octa, distance = zip(*dist_list)

    elif count > 1:
        print("")
        print("Info: The complex has more than one metal atom")
        print("")
        print("Info: Show transition metal/heavy atom candidates")
        print("")
        print("      Atom        X             Y             Z")
        print("      ----    ----------    ----------    ----------")

        for i in range(count):
            print("       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
                  .format(atom_metal[i], coord_metal[i][0], coord_metal[i][1], coord_metal[i][2]))
        print("")

        popup.too_many_metals_warning()

        return 1

    return atom_octa, coord_octa

