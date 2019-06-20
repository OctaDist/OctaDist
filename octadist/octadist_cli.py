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

import argparse
import os
import sys

import octadist
from octadist.__main__ import version, run_gui
from octadist.src.molecule import (
    is_xyz, get_coord_xyz, extract_octa
)


def check_file(file):
    """
    Check if input file is exist or not.

    Parameters
    ----------
    file : str
        Input file name.

    Returns
    -------
    file : str
        Input file name.

    """
    exist = os.path.isfile(file)

    if exist:
        return file
    else:
        print(f"File not found: {file}")
        sys.exit(1)


def find_coord(file):
    """
    Find atomic symbols and atomic coordinates of structure.

    Parameters
    ----------
    file : str
        Input file name.

    Returns
    -------
    atom : list
        Atomic symbols.
    coord : list
        Atomic coordinates.

    """
    if file.endswith(".xyz"):
        if is_xyz(file):
            atom, coord = get_coord_xyz(file)
        else:
            print(f"File type of input file is not supported: {file}")
            sys.exit(1)
    else:
        print(f"File type of input file is not supported: {file}")
        sys.exit(1)

    atom = list(filter(None, atom))

    return atom, coord


def find_octa(atom, coord):
    """
    Find atomic symbols and atomic coordinates of structure.

    Parameters
    ----------
    atom : list
        Atomic symbols of structure.
    coord : list
        Atomic coordinates of structure.

    Returns
    -------
    atom : list
        Atomic symbols of octahedral structure.
    coord : ndarray
        Atomic coordinates of octahedral structure.

    """
    atom, coord = extract_octa(atom, coord)

    return atom, coord


def calc_param(coord):
    """
    Calculate octahedral distortion parameters.

    Parameters
    ----------
    coord : array_like
        Atomic coordinates of octahedral structure.

    Returns
    -------
    computed : dict
        Computed parameters.

    """
    dist = octadist.CalcDistortion(coord)
    zeta = dist.zeta  # Zeta
    delta = dist.delta  # Delta
    sigma = dist.sigma  # Sigma
    theta = dist.theta  # Theta

    computed = {'zeta': zeta,
                'delta': delta,
                'sigma': sigma,
                'theta': theta
                }

    return computed


def run_cli():
    """
    OctaDist command-line interface (CLI).
    This function has been implemented by entry points function
    in setuptools package.

    """
    description = """\
Octahedral Distortion Calculator: 
A tool for computing octahedral distortion parameters in coordination complex.
For more details, please visit https://github.com/OctaDist/OctaDist.
"""

    epilog = f"Rangsiman Ketkaew\tUpdated on {octadist.__release__}\tE-mail: {octadist.__email__}"

    parser = argparse.ArgumentParser(
        prog="octadist_cli",
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )

    # info
    parser.add_argument('-v', '--version',
                        action='version',
                        version=version
                        )
    parser.add_argument('-a', '--author',
                        action='store_true',
                        help='show authors'
                        )
    parser.add_argument('--info',
                        action='store_true',
                        help='show program info'
                        )
    parser.add_argument('-g', '--gui',
                        action='store_true',
                        help='launch OctaDist GUI (this option is the same as \'octadist\' command'
                        )

    # input/output
    parser.add_argument('-i', '--inp',
                        action='store',
                        type=str,
                        metavar='INPUT',
                        help='input structure in .xyz format'
                        )
    parser.add_argument('-o', '--out',
                        action='store',
                        type=str,
                        metavar='OUTPUT',
                        help='save results to text file, '
                             'please specify name of OUTPUT file without \'.txt\' extension'
                        )

    # result
    parser.add_argument('--par',
                        type=str,
                        nargs='+',
                        choices=['zeta', 'delta', 'sigma', 'theta'],
                        metavar='PARAMETER',
                        help='select which the parameter (zeta, delta, sigma, theta) to show'
                        )
    parser.add_argument('--show',
                        type=str,
                        nargs='+',
                        choices=['atom', 'coord'],
                        metavar='MOL',
                        help='show atomic symbol (atom) and atomic coordinate (coord) of '
                             'octahedral structure'
                        )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.author:
        print(octadist.__author_full__)
        sys.exit(1)

    if args.info:
        print("\nOctaDist Program info")
        print("=====================")
        print(f"- Name\t\t=\t{octadist.__title__}")
        print(f"- Author\t=\t{octadist.__author__}")
        print(f"- Version\t=\t{octadist.__version__}")
        print(f"- Revision\t=\t{octadist.__revision__}")
        print(f"- Release\t=\t{octadist.__release__}")
        print(f"- Description\t=\t{octadist.__description__}")
        print(f"- E-mail\t=\t{octadist.__email__}")
        print(f"- Document\t=\t{octadist.__doc__}")
        print(f"- Website\t=\t{octadist.__website__}")
        sys.exit(1)

    # in case GUI is requested
    if args.gui:
        run_gui()
        sys.exit(1)

    atom_coord = {}
    computed = {}
    token = False

    # find coordinates of structure
    if args.inp:
        # check if file is correct
        file = check_file(args.inp)

        atom, coord = find_coord(file)
        atom, coord = find_octa(atom, coord)

        atom_coord = {'atom': atom,
                      'coord': coord
                      }

        computed = calc_param(coord)

        token = True
    else:
        print("No input file specified")

    # print computed parameters
    if not args.par and token:
        for key in ['zeta', 'delta', 'sigma', 'theta']:
            print(computed[key])
    else:
        for key in args.par:
            print(computed[key])

    # print atom and coord
    if args.show and token:
        for key in args.show:
            print(atom_coord[key])

    # save result
    if args.out and token:
        with open(args.out + '.txt', 'w') as f:
            f.write("Octahedral distortion parameters\n")
            f.write("--------------------------------\n")
            f.write(f"File: {args.inp}\n")
            f.write(f"Zeta   = {computed['zeta']}\n")
            f.write(f"Delta  = {computed['delta']}\n")
            f.write(f"Sigma  = {computed['sigma']}\n")
            f.write(f"Theta  = {computed['theta']}\n")
            f.write(f"\nComputed by OctaDist {version}\n")
            f.close()
        print(f"Output file has been saved to {f}")


if __name__ == '__main__':
    run_cli()
