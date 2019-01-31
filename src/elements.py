"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np


def check_atom(x):
    """Convert atomic number to symbol, or symbol to atomic number: 1-109

    :param x: If x is atomic number, return symbol, and vice versa.
    :return: symbol or atomic number, depending on input x
    """

    atoms = ['blank',
             'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O',
             'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S',
             'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr',
             'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge',
             'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
             'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
             'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba',
             'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
             'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf',
             'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
             'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra',
             'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm',
             'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf',
             'Db', 'Sg', 'Bh', 'Hs', 'Mt']

    if isinstance(x, int):
        return atoms[x]
    else:
        for i in atoms:
            if x == i:
                return atoms.index(i)


def check_bond_cutoff(x):
    """Convert atom to bond cutoff

    :param x: atom
    :return:
    """

    if x == "H":
        x = 1
    elif x == "He":
        x = 2
    elif x == "Li":
        x = 3
    elif x == "Be":
        x = 4
    elif x == "B":
        x = 5
    elif x == "C":
        x = 6
    elif x == "N":
        x = 7
    elif x == "O":
        x = 8
    elif x == "F":
        x = 9
    elif x == "Ne":
        x = 10
    elif x == "Na":
        x = 11
    elif x == "Mg":
        x = 12
    elif x == "Al":
        x = 13
    elif x == "Si":
        x = 14
    elif x == "P":
        x = 15
    elif x == "S":
        x = 16
    elif x == "Cl":
        x = 17
    elif x == "Ar":
        x = 18
    elif x == "K":
        x = 19
    elif x == "Ca":
        x = 20
    elif x == "Sc":
        x = 21
    elif x == "Ti":
        x = 22
    elif x == "V":
        x = 23
    elif x == "Cr":
        x = 24
    elif x == "Mn":
        x = 25
    elif x == "Fe":
        x = 26
    elif x == "Co":
        x = 27
    elif x == "Ni":
        x = 28
    elif x == "Cu":
        x = 29
    elif x == "Zn":
        x = 30
    elif x == "Ga":
        x = 31
    elif x == "Ge":
        x = 32
    elif x == "As":
        x = 33
    elif x == "Se":
        x = 34
    elif x == "Br":
        x = 35
    elif x == "Kr":
        x = 36
    elif x == "Rb":
        x = 37
    elif x == "Sr":
        x = 38
    elif x == "Y":
        x = 39
    elif x == "Zr":
        x = 40
    elif x == "Nb":
        x = 41
    elif x == "Mo":
        x = 42
    elif x == "Tc":
        x = 43
    elif x == "Ru":
        x = 44
    elif x == "Rh":
        x = 45
    elif x == "Pd":
        x = 46
    elif x == "Age":
        x = 47
    elif x == "Cd":
        x = 48
    elif x == "In":
        x = 49
    elif x == "Sn":
        x = 50
    elif x == "Sb":
        x = 51
    elif x == "Te":
        x = 52
    elif x == "I":
        x = 53
    elif x == "Xe":
        x = 54
    elif x == "Cs":
        x = 55
    elif x == "Ba":
        x = 56
    elif x == "La":
        x = 57
    elif x == "Ce":
        x = 58
    elif x == "Pr":
        x = 59
    elif x == "Nd":
        x = 60
    elif x == "Pm":
        x = 61
    elif x == "Sm":
        x = 62
    elif x == "Eu":
        x = 63
    elif x == "Gd":
        x = 64
    elif x == "Tb":
        x = 65
    elif x == "Dy":
        x = 66
    elif x == "Ho":
        x = 67
    elif x == "Er":
        x = 68
    elif x == "Tm":
        x = 69
    elif x == "Yb":
        x = 70
    else:
        x = "X"

    return x


def check_radii(x):
    """Convert atomic number (index) to atom radii in Angstroms: 1-119
    Skip 0th index

    :param x: atomic number
    :return:
    """

    atom_radii = np.array([
        0,
        230, 930, 680, 350, 830, 680, 680, 680, 640,
        1120, 970, 1100, 1350, 1200, 750, 1020, 990,
        1570, 1330, 990, 1440, 1470, 1330, 1350, 1350,
        1340, 1330, 1500, 1520, 1450, 1220, 1170, 1210,
        1220, 1210, 1910, 1470, 1120, 1780, 1560, 1480,
        1470, 1350, 1400, 1450, 1500, 1590, 1690, 1630,
        1460, 1460, 1470, 1400, 1980, 1670, 1340, 1870,
        1830, 1820, 1810, 1800, 1800, 1990, 1790, 1760,
        1750, 1740, 1730, 1720, 1940, 1720, 1570, 1430,
        1370, 1350, 1370, 1320, 1500, 1500, 1700, 1550,
        1540, 1540, 1680, 1700, 2400, 2000, 1900, 1880,
        1790, 1610, 1580, 1550, 1530, 1510, 1500, 1500,
        1500, 1500, 1500, 1500, 1500, 1500, 1600, 1600,
        1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600,
        1600, 1600, 1600, 1600, 1600, 1600],
        dtype=np.float32) / 1000.0

    return atom_radii[x]


def check_color(x):
    """Convert atomic number to color: 1-109
    Ref: http://jmol.sourceforge.net/jscolors/

    Skip 0th index

    :param x: atomic number
    :return:
    """

    atom_color = np.array([
        'blank',
        '#FFFFFF', '#D9FFFF', '#CC80FF', '#C2FF00', '#FFB5B5',
        '#909090', '#3050F8', '#FF0D0D', '#90E050', '#B3E3F5',
        '#AB5CF2', '#8AFF00', '#BFA6A6', '#F0C8A0', '#FF8000',
        '#FFFF30', '#1FF01F', '#80D1E3', '#8F40D4', '#3DFF00',
        '#E6E6E6', '#BFC2C7', '#A6A6AB', '#8A99C7', '#9C7AC7',
        '#E06633', '#F090A0', '#50D050', '#C88033', '#7D80B0',
        '#C28F8F', '#668F8F', '#BD80E3', '#FFA100', '#A62929',
        '#5CB8D1', '#702EB0', '#00FF00', '#94FFFF', '#94E0E0',
        '#73C2C9', '#54B5B5', '#3B9E9E', '#248F8F', '#0A7D8C',
        '#006985', '#C0C0C0', '#FFD98F', '#A67573', '#668080',
        '#9E63B5', '#D47A00', '#940094', '#429EB0', '#57178F',
        '#00C900', '#70D4FF', '#FFFFC7', '#D9FFC7', '#C7FFC7',
        '#A3FFC7', '#8FFFC7', '#61FFC7', '#45FFC7', '#30FFC7',
        '#1FFFC7', '#00FF9C', '#00E675', '#00D452', '#00BF38',
        '#00AB24', '#4DC2FF', '#4DA6FF', '#2194D6', '#267DAB',
        '#266696', '#175487', '#D0D0E0', '#FFD123', '#B8B8D0',
        '#A6544D', '#575961', '#9E4FB5', '#AB5C00', '#754F45',
        '#428296', '#420066', '#007D00', '#70ABFA', '#00BAFF',
        '#00A1FF', '#008FFF', '#0080FF', '#006BFF', '#545CF2',
        '#785CE3', '#8A4FE3', '#A136D4', '#B31FD4', '#B31FBA',
        '#B30DA6', '#BD0D87', '#C70066', '#CC0059', '#D1004F',
        '#D90045', '#E00038', '#E6002E', '#EB0026'])

    return atom_color[x]
