#!/usr/bin/env python3.6

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

import octadist.main

version = octadist.__version__
release = octadist.__release__


def run_cli():
    parser = argparse.ArgumentParser(
        usage="octadist INPUT_FILE [options]",
        description="Octahedral Distortion Calculator"
    )

    # Positional arguments
    parser.add_argument('structure_input',
                        metavar='INPUT_FILE',
                        type=str,
                        help='input structure in .xyz format'
                        )
    parser.add_argument('structure_output',
                        metavar='OUTPUT_FILE',
                        type=str,
                        help='output in .txt format'
                        )

    # Optional arguments
    parser.add_argument('-v', '--version',
                        action='version',
                        version=version
                        )
    parser.add_argument('-a', '--author',
                        action='help',
                        help='show this help page'
                        )
    parser.add_argument('-o', '--output',
                        action='store_true',
                        help='save results to '
                        )

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        sys.exit(1)


def run_gui():
    print(f"\nProgram Starts >>>")
    print(f"... OctaDist {version} {release} ...")

    app = octadist.main.OctaDist()
    app.start_app()

    # Delete icon after closing app
    if app.octadist_icon is not None:
        os.remove(app.octadist_icon)

    print(f"<<< Program Terminated")


def run():
    # check API
    if sys.argv[1:]:
        run_cli()
    else:
        run_gui()


if __name__ == '__main__':
    run()
