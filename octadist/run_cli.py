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
from octadist.src.molecule import *
from octadist.__main__ import version, run_gui


def check_file(file):
    exist = os.path.isfile(file)

    if exist:
        return file
    else:
        print(f"File not found: {file}")
        sys.exit(1)


def extract_coord(file):
    atom = []
    coord = np.array([])

    if file.endswith(".xyz"):
        if is_xyz(file):
            atom, coord = get_coord_xyz(file)
        else:
            print(f"File type of input file is not supported: {file}")
            sys.exit(1)

    elif file.endswith(".out") or file.endswith(".log"):
        if is_gaussian(file):
            atom, coord = get_coord_gaussian(file)
        elif is_nwchem(file):
            atom, coord = get_coord_nwchem(file)
        elif is_orca(file):
            atom, coord = get_coord_orca(file)
        elif is_qchem(file):
            atom, coord = get_coord_qchem(file)
        else:
            print(f"Could not extract atomic coordinate: {file}")
    else:
        print(f"Could not read file: {file}")
        sys.exit(1)

    atom = list(filter(None, atom))

    return atom, coord


def calc_param(coord):
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


def run():
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
                        help='input structure in .xyz or .out or .log formats'
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
                        default='all',
                        choices=['zeta', 'delta', 'sigma', 'theta', 'all'],
                        metavar='PARAMETER',
                        help='select which parameter to show (default is %(default)s)'
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

    if args.gui:
        run_gui()
        sys.exit(1)

    token = False

    if args.inp:
        # check if file is correct
        file = check_file(args.inp)

        # extract atomic coordinate
        atom, coord = extract_coord(file)

        computed = calc_param(coord)

        if args.par and 'all' in args.par:
            for key in computed.keys():
                print(computed[key])
        else:
            for key in args.par:
                print(computed[key])

        token = True
    else:
        print("No input file specified")

    if args.out and token:
        with open(args.out + '.txt', 'w') as f:
            f.write("Octahedral distortion parameters\n")
            f.write("--------------------------------\n")
            f.write(f"File: {args.inp}\n")
            f.write(f"Zeta   = {computed['zeta']}\n")
            f.write(f"Delta  = {computed['zeta']}\n")
            f.write(f"Sigma  = {computed['zeta']}\n")
            f.write(f"Theta  = {computed['zeta']}\n")
            f.write(f"\nComputed by OctaDist {version}\n")
            f.close()


if __name__ == '__main__':
    run()
