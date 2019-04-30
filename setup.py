#!/usr/bin/env python

# Metadata file for distribution of OctaDist software on PyPI
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import setuptools
from octadist import main

__version__ = main.program_version

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

description = "Octahedral distortion calculator for coordination complexes"

setuptools.setup(
    name="octadist",
    version=__version__,
    author="Rangsiman Ketkaew",
    author_email="rangsiman1993@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://octadist.github.io",
    download_url="https://github.com/OctaDist/OctaDist/releases",
    project_urls={
        'Documentation': 'https://octadist.github.io/manual.html',
        'Source': 'https://github.com/OctaDist/OctaDist',
        'Tracker': 'https://github.com/OctaDist/OctaDist/issues',
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
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
        'octahedral distortion',
        'crystallography',
        'chemistry'
    ],
    python_requires='>=3',
)
