"""
OctaDist  Copyright (C) 2019  Rangsiman Ketkaew

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import numpy as np


def check_atom(x):
    """Convert atomic number to atom

    :param x: atomic number
    :return: atom
    """

    if x == 1:
        x = "H"
    elif x == 2:
        x = "He"
    elif x == 3:
        x = "Li"
    elif x == 4:
        x = "Be"
    elif x == 5:
        x = "B"
    elif x == 6:
        x = "C"
    elif x == 7:
        x = "N"
    elif x == 8:
        x = "O"
    elif x == 9:
        x = "F"
    elif x == 10:
        x = "Ne"
    elif x == 11:
        x = "Na"
    elif x == 12:
        x = "Mg"
    elif x == 13:
        x = "Al"
    elif x == 14:
        x = "Si"
    elif x == 15:
        x = "P"
    elif x == 16:
        x = "S"
    elif x == 17:
        x = "Cl"
    elif x == 18:
        x = "Ar"
    elif x == 19:
        x = "K"
    elif x == 20:
        x = "Ca"
    elif x == 21:
        x = "Sc"
    elif x == 22:
        x = "Ti"
    elif x == 23:
        x = "V"
    elif x == 24:
        x = "Cr"
    elif x == 25:
        x = "Mn"
    elif x == 26:
        x = "Fe"
    elif x == 27:
        x = "Co"
    elif x == 28:
        x = "Ni"
    elif x == 29:
        x = "Cu"
    elif x == 30:
        x = "Zn"
    elif x == 31:
        x = "Ga"
    elif x == 32:
        x = "Ge"
    elif x == 33:
        x = "As"
    elif x == 34:
        x = "Se"
    elif x == 35:
        x = "Br"
    elif x == 36:
        x = "Kr"
    elif x == 37:
        x = "Rb"
    elif x == 38:
        x = "Sr"
    elif x == 39:
        x = "Y"
    elif x == 40:
        x = "Zr"
    elif x == 41:
        x = "Nb"
    elif x == 42:
        x = "Mo"
    elif x == 43:
        x = "Tc"
    elif x == 44:
        x = "Ru"
    elif x == 45:
        x = "Rh"
    elif x == 46:
        x = "Pd"
    elif x == 47:
        x = "Ag"
    elif x == 48:
        x = "Cd"
    elif x == 49:
        x = "In"
    elif x == 50:
        x = "Sn"
    elif x == 51:
        x = "Sb"
    elif x == 52:
        x = "Te"
    elif x == 53:
        x = "I"
    elif x == 54:
        x = "Xe"
    elif x == 55:
        x = "Cs"
    elif x == 56:
        x = "Ba"
    elif x == 57:
        x = "La"
    elif x == 58:
        x = "Ce"
    elif x == 59:
        x = "Pr"
    elif x == 60:
        x = "Nd"
    elif x == 61:
        x = "Pm"
    elif x == 62:
        x = "Sm"
    elif x == 63:
        x = "Eu"
    elif x == 64:
        x = "Gd"
    elif x == 65:
        x = "Tb"
    elif x == 66:
        x = "Dy"
    elif x == 67:
        x = "Ho"
    elif x == 68:
        x = "Er"
    elif x == 69:
        x = "Tm"
    elif x == 70:
        x = "Yb"
    else:
        x = "X"

    return x


def check_atomic_number(x):
    """Convert atom to atomic number

    :param x: atom
    :return: atomic number
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
        x = 79
    else:
        x = "X"

    return x


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
        x = 79
    else:
        x = "X"

    return x


def check_radii(x):
    """Convert atomic number (index) to atom radii in Angstroms
    Skip 0th index

    :param x: atomic number
    :return:
    """

    atom_radii = np.array([0, 230, 930, 680, 350, 830, 680, 680, 680, 640,
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
                           1600, 1600, 1600, 1600, 1600, 1600], dtype=np.float32) / 1000.0

    return atom_radii[x]


def check_color(x):
    """Convert atomic number to color   http://jmol.sourceforge.net/jscolors/
    Skip 0th index

    :param x: atomic number
    :return:
    """

    atom_color = [0, '#FFFFFF', '#D9FFFF', '#CC80FF', '#C2FF00', '#FFB5B5',
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
                  '#1FFFC7', '#00FF9C', '#00E675', '#00D452', '#00BF38']

    return atom_color[x]
