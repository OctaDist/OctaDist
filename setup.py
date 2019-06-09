#!/usr/bin/env python

# Metadata file for distribution of OctaDist software on PyPI
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

import setuptools

__version__ = "2.5.3"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

description = "OctaDist: A tool for calculating distortion parameters in coordination complexes."

setuptools.setup(
    name="octadist",
    version=__version__,
    author="Rangsiman Ketkaew",
    author_email="rangsiman1993@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://octadist.github.io",
    download_url="https://github.com/OctaDist/OctaDist-PyPI/releases",
    project_urls={
        'Documentation': 'https://octadist-pypi.readthedocs.io/en/latest/',
        'Source': 'https://github.com/OctaDist/OctaDist-PyPI',
        'Tracker': 'https://github.com/OctaDist/OctaDist-PyPI/issues',
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'rmsd'
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
        'chemistry'
        'crystallography',
        'inorganic chemistry',
        'coordination complex'
        'octahedral distortion',
    ],
    python_requires='>=3',
)
