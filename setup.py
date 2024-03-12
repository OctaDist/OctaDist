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

# Metadata file for distribution of OctaDist software on PyPI
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import setuptools

__version__ = "3.0.0"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

description = (
    "OctaDist: A tool for calculating distortion parameters in molecule."
)

setuptools.setup(
    name="octadist",
    version=__version__,
    author="Rangsiman Ketkaew et al.",
    author_email="rangsiman1993@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3) on top the license of Python.",
    url="https://octadist.github.io",
    download_url="https://github.com/OctaDist/OctaDist/releases",
    project_urls={
        "Documentation": "https://octadist.readthedocs.io/en/latest/",
        "Source": "https://github.com/OctaDist/OctaDist",
        "Tracker": "https://github.com/OctaDist/OctaDist/issues",
    },
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy", 
        "scipy", 
        "matplotlib", 
        "rmsd", 
        "pymatgen", 
        "plotly"
        ],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: AIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: SunOS/Solaris",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
    ],
    keywords=[
        "chemistry",
        "computational chemistry",
        "inorganic chemistry",
        "crystallography",
        "coordination complex",
        "spin-crossover",
        "octahedral distortion parameter",
        "structural analysis",
        "Molecular visualization",
    ],
    python_requires=">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, \
        !=3.6.*, !=3.10.*, !=3.11.*",
    entry_points={
        "console_scripts": [
            "octadist=octadist.octadist_gui:run_gui",
            "octadist_gui=octadist.octadist_gui:run_gui",
            "octadist_cli=octadist.octadist_cli:run_cli",
        ]
    },
)
