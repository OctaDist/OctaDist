#!/usr/bin/env python

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

import os

import octadist.main

version = octadist.__version__
release = octadist.__release__


def run_gui():
    """
    OctaDist graphical user interface (GUI).

    """
    print(">>> Program started")
    print(f">>> OctaDist {version} {release}")

    app = octadist.main.OctaDist()
    app.start_app()

    # Delete icon after closing app
    if app.octadist_icon is not None:
        os.remove(app.octadist_icon)

    print(">>> Program terminated")


if __name__ == "__main__":
    run_gui()

