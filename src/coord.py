"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np
import elements


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


def check_txt_file(f):
    """Check if the input file
    text file format
    ----------------

    <index 0> <X> <Y> <Z>
    <index 1> <X> <Y> <Z>
    ...
    <index 6> <X> <Y> <Z>

    ***The first atom must be metal center.

    :param f: string - user filename
    :return: if file is a .txt fie format, return True
    """
    with open(f) as f_1:
        line = f_1.readline()

    if len(line.split()) != 4:
        return False
    elif file_lines(f) < 7:
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


def get_coord_txt(f):
    """Get coordinate from .txt file

    :param f: string - user input file
    :return atom_full: list - full atom list of user's complex
    :return coord_full: array - full coordinates of all atoms of complex
    """
    file = open(f, "r")
    line = file.readlines()
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
    coord_full = np.loadtxt(file, skiprows=0, usecols=[1, 2, 3])
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

    elif f.endswith(".txt"):
        if check_txt_file(f):
            print("Info: Check file type: TXT file")
            atom_full, coord_full = get_coord_txt(f)
        else:
            print("Error: Invalid TXT file format")
            print("Error: Could not read data in TXT file %s" % f)

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
        print("Error: File type is not supported in current version of OctaDist")

    # Remove empty string in list
    atom_full = list(filter(None, atom_full))

    return atom_full, coord_full


def cut_coord(fal, fcl):
    """Get only first 7 atoms (octahedron)

    :param fal: list - atom_full
    :param fcl: array - coord_full
    :return atom_list: list - atom in octahedral structure
    :return coord_list: array - coordinates of atom in octahedral structure
    """
    # If complex has atoms > 7, print all atoms and coordinates.
    if len(fcl) > 7:
        show_all_atoms(fal, fcl)

    atom_list = np.asarray(fal[0:7])
    coord_list = np.asarray(fcl[0:7])

    # Print 7 atoms and their coordinates
    show_octahedron_atoms(atom_list, coord_list)

    return atom_list, coord_list


def show_all_atoms(fal, fcl):
    """Show atomic symbol and coordinates of all atoms

    :param fal: list - atom_full
    :param fcl: array - coord_full
    :return:
    """
    print("Info: Show Cartesian coordinates of all %s atoms\n" % len(fcl))
    print("      Atom        X              Y             Z")
    print("      ----    ----------    ----------    ----------")

    for i in range(len(fcl)):
        print("       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
              .format(fal[i], fcl[i][0], fcl[i][1], fcl[i][2]))

    print("")


def show_octahedron_atoms(al, cl):
    """Show selected atoms of octahedral structure

    :param al: list - atom_list
    :param cl: array - coord_list
    :return:
    """
    print("Info: Show Cartesian coordinates of selected 7 atoms\n")
    print("      Atom        X              Y             Z")
    print("      ----    ----------    ----------    ----------")

    for i in range(len(cl)):
        print("       {0:>2}   {1:12.8f}  {2:12.8f}  {3:12.8f}"
              .format(al[i], cl[i][0], cl[i][1], cl[i][2]))

    print("")
