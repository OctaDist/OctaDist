"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import elements


def file_len(fname):
    """Count line in file

    :param fname: string
    :return: number of line in file
    """
    with open(fname) as f:
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
    :param f: string - filename
    :return: int - 1 if the file is .xyz format
    """
    file = open(f, 'r')

    first_line = file.readline()

    try:
        int(first_line)
    except ValueError:
        return 0

    if file_len(f) >= 9:
        return 1
    else:
        return 0


def get_coord_from_xyz(f):
    """Get coordinate from .xyz file

    :param f: string - input file
    :return: atom_list and full_coord_list
    """
    print("Command: Get Cartesian coordinates")

    file = open(f, "r")
    # read file from 3rd line
    line = file.readlines()[2:]
    file.close()

    full_atom_list = []

    for l in line:
        # read atom on 1st column and insert to array
        lst = l.split(' ')[0]
        full_atom_list.append(lst)

    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> file.seek(0) <<
        2. use >> file = open(f, "r") <<
    """

    file = open(f, "r")
    full_coord_list = np.loadtxt(file, skiprows=2, usecols=[1, 2, 3])
    file.close()

    return full_atom_list, full_coord_list


def check_txt_file(f):
    """Check if the input file
    text file format
    ----------------

    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    ...
    <index 6> <X> <Y> <Z>

    ***The first atom must be metal center.

    :param f: string - filename
    :return: int 1 if file is a .txt fie format
    """

    if file_len(f) < 7:
        return 0
    else:
        return 1


def get_coord_from_txt(f):
    """Get coordinate from .txt file

    :param f: string - file
    :return: full_atom_list and full_coord_list
    """
    print("Command: Get Cartesian coordinates")

    file = open(f, "r")
    line = file.readlines()
    file.close()

    full_atom_list = []

    for l in line:
        # read atom on 1st column and insert to array
        lst = l.split(' ')[0]
        full_atom_list.append(lst)

    """Read file again for getting XYZ coordinate
        We have two ways to do this, 
        1. use >> file.seek(0) <<
        2. use >> file = open(f, "r") <<
    """

    file = open(f, "r")
    full_coord_list = np.loadtxt(file, skiprows=0, usecols=[1, 2, 3])
    file.close()

    return full_atom_list, full_coord_list


def check_gaussian_file(f):
    """Check if the input file is Gaussian file format

    :param f: string - input file
    :return: int - 1 if file is Gaussian output file, return 0 if not.
    """
    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            return 1

    return 0


def get_coord_from_gaussian(f):
    """Extract XYZ coordinate from Gaussian output file

    :param f: string - input file
    :return: full_atom_list and full_coord_list
    """
    print("Command: Get Cartesian coordinates")

    gaussian_file = open(f, "r")
    nline = gaussian_file.readlines()

    start = 0
    end = 0

    full_atom_list, full_coord_list = [], []

    for i in range(len(nline)):
        if "Standard orientation:" in nline[i]:
            start = i

    for i in range(start + 5, len(nline)):
        if "---" in nline[i]:
            end = i
            break

    for line in nline[start + 5: end]:
        dat = line.split()
        dat1 = int(dat[1])
        coord_x = float(dat[3])
        coord_y = float(dat[4])
        coord_z = float(dat[5])

        dat1 = elements.check_atom(dat1)

        full_atom_list.append(dat1)
        full_coord_list.append([coord_x, coord_y, coord_z])

    gaussian_file.close()

    return full_atom_list, full_coord_list


def check_nwchem_file(f):
    """Check if the input file is NWChem file format

    :param f: string - input file
    :return: int - 1 if file is NWChem output file, return 0 if not.
    """
    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    for i in range(len(nline)):
        if "No. of atoms" in nline[i]:
            if not int(nline[i].split()[4]):
                return 0

    for j in range(len(nline)):
        if "Optimization converged" in nline[j]:
            return 1

    return 0


def get_coord_from_nwchem(f):
    """Extract XYZ coordinate from NWChem output file

    :param f: string - input file
    :return: full_atom_list and full_coord_list
    """
    print("Command: Get Cartesian coordinates")

    nwchem_file = open(f, "r")
    nline = nwchem_file.readlines()

    start = 0
    end = 0

    full_atom_list, full_coord_list = [], []

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

        full_atom_list.append(dat1)
        full_coord_list.append([coord_x, coord_y, coord_z])

    nwchem_file.close()

    return full_atom_list, full_coord_list


def check_orca_file(f):
    """Check if the input file is ORCA file format

    :param f: string - input file
    :return: int - 1 if file is ORCA output file, return 0 if not.
    """
    orca_file = open(f, "r")
    nline = orca_file.readlines()

    for i in range(len(nline)):
        if "CARTESIAN COORDINATES (ANGSTROEM)" in nline[i]:
            return 1

    return 0


def get_coord_from_orca(f):
    """Extract XYZ coordinate from ORCA output file

    :param f: string - input file
    :return: full_atom_list and full_coord_list
    """
    print("Command: Get Cartesian coordinates")

    orca_file = open(f, "r")
    nline = orca_file.readlines()

    start = 0
    end = 0

    full_atom_list, full_coord_list = [], []

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

        full_atom_list.append(dat1)
        full_coord_list.append([coord_x, coord_y, coord_z])

    orca_file.close()

    return full_atom_list, full_coord_list


def get_coord(f):
    """Check file type, read data, extract atom and coord from input file

    :param f: string - input file
    :return: insert atom and coord read from input file into text box
    """
    # Check file extension
    if f.endswith(".xyz"):
        if check_xyz_file(f) == 1:
            print("         File type: XYZ file\n")
            full_atom_list, full_coord_list = get_coord_from_xyz(f)
        else:
            print("Error: Invalid XYZ file format")
            print("       Could not read data in XYZ file %s" % f)
    elif f.endswith(".txt"):
        if check_txt_file(f) == 1:
            print("         File type: TXT file")
            print("")
            full_atom_list, full_coord_list = get_coord_from_txt(f)
        else:
            print("Error: Invalid TXT file format")
            print("       Could not read data in TXT file %s" % f)
    elif f.endswith(".out") or f.endswith(".log"):
        if check_gaussian_file(f) == 1:
            print("         File type: Gaussian Output\n")
            full_atom_list, full_coord_list = get_coord_from_gaussian(f)
        elif check_nwchem_file(f) == 1:
            print("         File type: NWChem Output\n")
            full_atom_list, full_coord_list = get_coord_from_nwchem(f)
        elif check_orca_file(f) == 1:
            print("         File type: ORCA Output\n")
            full_atom_list, full_coord_list = get_coord_from_orca(f)
        else:
            print("Error: Could not read output file %s" % f)
    else:
        print("Error: Could not read file %s" % f)
        print("Error: File type is not supported in OctaDist")

    # Sort the atoms order:
    # Atom no. 1   metal center
    #          2-7 ligand atoms
    #          3-n other atoms

    return full_atom_list, full_coord_list


def cut_coord(full_atom_list, full_coord_list):
    """

    :param full_atom_list:
    :param full_coord_list:
    :return:
    """
    if len(full_coord_list) > 7:
        print("Command: Show Cartesian coordinates of all %s atoms" % len(full_coord_list))

        for i in range(len(full_coord_list)):
            print("          {0:>2}   ({1:12.8f}, {2:12.8f}, {3:12.8f})"
                  .format(full_atom_list[i], full_coord_list[i][0], full_coord_list[i][1],
                          full_coord_list[i][2]))
        print("")

    # Get only first 7 atoms (octahedron)
    atom_list = np.asarray(full_atom_list[0:7])
    coord_list = np.asarray(full_coord_list[0:7])

    # if atom_list:
    print("Command: Show Cartesian coordinates of selected 7 atoms")

    for i in range(len(coord_list)):
        print("          {0:>2}   ({1:12.8f}, {2:12.8f}, {3:12.8f})"
              .format(atom_list[i], coord_list[i][0], coord_list[i][1], coord_list[i][2]))
    print("")

    return atom_list, coord_list

