![Python version][py-ver-badge]
[![PyPI-Server][pypi-badge]][pypi-link]
![Python Wheel][py-wheel-badge]
![Code size][code-size]
![Repo size][repo-size]
![License][license]

[![Github Download All releases][dl-all-badge]][dl-all-link]
[![Github Download Latest version][dl-latest-badge]][dl-latest-link]
![Platform][platform]

[py-ver-badge]: https://img.shields.io/pypi/pyversions/octadist.svg
[py-wheel-badge]: https://img.shields.io/pypi/wheel/octadist.svg
[code-size]: https://img.shields.io/github/languages/code-size/OctaDist/OctaDist.svg
[repo-size]: https://img.shields.io/github/repo-size/OctaDist/OctaDist.svg
[dl-all-badge]: https://img.shields.io/github/downloads/OctaDist/octadist/total.svg
[dl-all-link]: https://github.com/OctaDist/OctaDist/releases
[dl-latest-badge]: https://img.shields.io/github/downloads/OctaDist/OctaDist/v.3.0.0/total.svg
[dl-latest-link]: https://github.com/OctaDist/OctaDist/releases/tag/v.3.0.0
[license]: https://img.shields.io/github/license/OctaDist/OctaDist
[platform]: https://img.shields.io/conda/pn/rangsiman/octadist

## OctaDist

Octahedral distortion calculator: A tool for calculating distortion parameters in coordination complexes.
https://octadist.github.io/

<p align="center">
   <img alt="molecule" src="https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/molecule.png" align=middle width="200pt" />
<p/>

## Standard abilities

OctaDist is computer software for inorganic chemistry and crystallography program.
OctaDist can be used for studying the structural distortion in coordination complexes.
With the abilities of OctaDist, you can:

- analyze the structure and conformation of coordination complexes.
- compute the octahedral distortion parameters.
- explore tilting distortion in perovskite and metal-organic framework.
- display 3D molecule for graphical analysis.
- implement OctaDist's module into your or other program.
- access the program core directly via an interactive scripting language.

## Documents

User manual : [https://octadist.github.io/manual.html][manual-link].

[manual-link]: https://octadist.github.io/manual.html

Reference manual :

| Version   |              Status               |                               Docs                                |
| --------- | :-------------------------------: | :---------------------------------------------------------------: |
| Stable    |  ![Doc-Latest-Badge][doc-latest]  |   [HTML][latest-html] / [PDF][latest-pdf] / [Epub][latest-epub]   |
| Dev Build | ![Doc-Nightly-Badge][doc-nightly] | [HTML][nightlyg-html] / [PDF][nightly-pdf] / [Epub][nightly-epub] |

[doc-latest]: https://img.shields.io/readthedocs/octadist/latest.svg
[latest-html]: https://octadist.readthedocs.io/en/latest/
[latest-pdf]: https://readthedocs.org/projects/octadist/downloads/pdf/latest/
[latest-epub]: https://readthedocs.org/projects/octadist/downloads/epub/latest/
[doc-nightly]: https://img.shields.io/readthedocs/octadist/nightly-build.svg
[nightlyg-html]: https://octadist.readthedocs.io/en/nightly-build/
[nightly-pdf]: https://readthedocs.org/projects/octadist/downloads/pdf/nightly-build/
[nightly-epub]: https://readthedocs.org/projects/octadist/downloads/epub/nightly-build/

## Download and Install

For Windows users, we strongly suggest a standalone executable:

[Click Here to Download OctaDist-2.6.1-Win-x86-64.exe][download-win-exe]

[download-win-exe]: https://github.com/OctaDist/OctaDist/releases/download/v.2.6.1/OctaDist-2.6.1-Win-x86-64.exe

For Linux or macOS users and already have Python 3 installed on the system,
the easiest way to install OctaDist is to use `pip`.

```sh
pip install octadist
```

or use `conda` for those who have Anaconda:

```sh
conda install -c rangsiman octadist
```

## Starting OctaDist

The following commands can be used to start OctaDist in different ways:

### Graphical User Interface (GUI)

To start GUI program:

```sh
octadist
```

Screenshots of program:

|  ![][ss_1]   |    ![][ss_2]    |           ![][ss_3]            |
| :----------: | :-------------: | :----------------------------: |
| OctaDist GUI | XYZ coordinates | Computed distortion parameters |

[ss_1]: https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Screenshots_OctaDist.png
[ss_2]: https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Screenshots_Example_Mol.png
[ss_3]: https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Screenshots_Computed.png

### Command Line Interface (CLI)

To start program command line:

```sh
octadist_cli
```

To calculate distortion parameters:

```sh
octadist_cli --inp EXAMPLE_INPUT.xyz
```

To calculate distortion parameters and show formatted output:

```sh
octadist_cli --inp EXAMPLE_INPUT.xyz --format
```

## Supporting input format

- CIF: `*.cif`
- XYZ: `*.xyz`
- Computational chemistry outputs: `*.out` and `*.log`
  - [Gaussian](http://gaussian.com/)
  - [NWChem](http://www.nwchem-sw.org)
  - [ORCA](https://orcaforum.kofo.mpg.de)
  - [Q-Chem](https://www.q-chem.com/)

## Running the tests: OctaDist as a package

#### Example 1: Explicitly define atomic label and coordinates

```python
import octadist as oc

# Prepare list of atomic coordinates of octahedral structure:

atom = ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']

coord = [
    [2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
    [1.885657000, 4.804777000, 6.183726000],
    [1.747515000, 6.960963000, 7.932784000],
    [4.094380000, 5.807257000, 7.588689000],
    [0.539005000, 4.482809000, 8.460004000],
    [2.812425000, 3.266553000, 8.131637000],
    [2.886404000, 5.392925000, 9.848966000],
]

dist = oc.CalcDistortion(coord)
zeta = dist.zeta             # 0.228072561
delta = dist.delta           # 0.000476251
sigma = dist.sigma           # 47.92652837
theta = dist.theta           # 122.6889727
```

#### Example 2: Load external Cartesian coordinates file

```python
import os
import octadist as oc

# You can also import your input file, like this:

file = "Multiple-metals.xyz"

# Then use coord.extract_file to extract all atomic symbols and coordinates,
# and then use coord.extract_octa for taking the octahedral structure.

atom_full, coord_full = oc.io.extract_coord(file)
atom, coord = oc.io.extract_octa(atom_full, coord_full)

dist = oc.CalcDistortion(coord)
zeta = dist.zeta              # 0.0030146365519487794
delta = dist.delta            # 1.3695007180404868e-07
sigma = dist.sigma            # 147.3168033970211
theta = dist.theta            # 520.6407679851042
```

#### Example 3: Display 3D structure of molecule

```python
import os
import octadist as oc

file = "Multiple-metals.xyz"

atom_full, coord_full = oc.io.extract_coord(file)

my_plot = oc.draw.DrawComplex_Matplotlib(atom=atom_full, coord=coord_full)
my_plot.add_atom()
my_plot.add_bond()
my_plot.add_legend()
my_plot.save_img()
my_plot.show_plot()

# Figure will be saved as Complex_saved_by_OctaDist.png by default.
```

<p align="center">
   <img alt="molecule" 
   src="https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Complex_saved_by_OctaDist.png" 
   align=middle width="350pt" />
<p/>

Other example scripts and octahedral complexes are available at [example-py][ex-py-link] and [example-input][ex-inp-link], respectively.

[ex-py-link]: https://github.com/OctaDist/OctaDist-PyPI/tree/master/example-py
[ex-inp-link]: https://github.com/OctaDist/OctaDist-PyPI/tree/master/example-input

## Development and Release

OctaDist is written entirely in Python 3 binding to Tkinter GUI toolkit.
It is cross-platform program which can work on multiple operating systems.
The stable version and development build of OctaDist are released at [here][release-link].
A standalone executable for graphical user interface (GUI) and
source code for command line interface (CLI) are available for as follows:

[release-link]: https://github.com/OctaDist/OctaDist/releases

| Platform       | Description                                                    |                     Status                     |
| -------------- | -------------------------------------------------------------- | :--------------------------------------------: |
| Windows        | [![windows][windows-2.6.1-badge]][windows-2.6.1-link]          | [![Travis-CI Test][travis-badge]][travis-link] |
| Linux          | [![latest-release][latest-release-badge]][latest-release-link] | [![Travis-CI Test][travis-badge]][travis-link] |
| macOS          | [![latest-release][latest-release-badge]][latest-release-link] | [![Travis-CI Test][travis-badge]][travis-link] |
| PyPI library   | [![PyPI-Server][pypi-badge]][pypi-link]                        | [![Travis-CI Test][travis-badge]][travis-link] |
| Anaconda cloud | [![Conda-Server][conda-badge]][conda-link]                     | [![Travis-CI Test][travis-badge]][travis-link] |
| Nightly build  | Development build                                              |  [![Travis-CI Test][dev-badge]][travis-link]   |

[windows-2.6.1-badge]: https://img.shields.io/badge/release-v.2.6.1-blue
[windows-2.6.1-link]: https://github.com/OctaDist/OctaDist/releases/tag/v.2.6.1
[latest-release-badge]: https://img.shields.io/github/release/octadist/octadist.svg
[latest-release-link]: https://github.com/OctaDist/OctaDist/releases/latest
[travis-badge]: https://img.shields.io/travis/OctaDist/OctaDist/master.svg
[travis-link]: https://travis-ci.org/OctaDist/OctaDist
[pypi-badge]: https://img.shields.io/pypi/v/octadist.svg
[pypi-link]: https://pypi.org/project/octadist/
[conda-badge]: https://anaconda.org/rangsiman/octadist/badges/version.svg
[conda-link]: https://anaconda.org/rangsiman/octadist
[dev-badge]: https://img.shields.io/travis/OctaDist/OctaDist/nightly-build.svg

**Branch:**

1. [master](https://github.com/OctaDist/OctaDist)
2. [nightly-build](https://github.com/OctaDist/OctaDist/tree/nightly-build)

## Git Clone

```sh
git clone https://github.com/OctaDist/OctaDist.git
git checkout nightly-build
git pull origin nightly-build
```

## Register for OctaDist

To get notified when we release new version of OctaDist, please register at https://cutt.ly/regis-octadist.

## OctaDist Forum

The users can post questions in our Google Groups: [OctaDist Forum](https://groups.google.com/g/octadist-forum)

## Citation

Please cite this project when you use OctaDist for scientific publication.

```
Ketkaew, R.; Tantirungrotechai, Y.; Harding, P.; Chastanet, G.; Guionneau, P.; Marchivie, M.; Harding, D. J.
OctaDist: A Tool for Calculating Distortion Parameters in Spin Crossover and Coordination Complexes.
Dalton Trans., 2021,50, 1086-1096. https://doi.org/10.1039/D0DT03988H
```

BibTeX

```
@article{Ketkaew2021,
  doi = {10.1039/d0dt03988h},
  url = {https://doi.org/10.1039/d0dt03988h},
  year = {2021},
  publisher = {Royal Society of Chemistry ({RSC})},
  volume = {50},
  number = {3},
  pages = {1086--1096},
  author = {Rangsiman Ketkaew and Yuthana Tantirungrotechai and Phimphaka Harding and Guillaume Chastanet and Philippe Guionneau and Mathieu Marchivie and David J. Harding},
  title = {OctaDist: a tool for calculating distortion parameters in spin crossover and coordination complexes},
  journal = {Dalton Transactions}
}
```

## Bug report

If you found issues in OctaDist, please report it to us at [here][submit-issues].

[submit-issues]: https://github.com/OctaDist/OctaDist/issues

## Project team

- [Rangsiman Ketkaew][rk-link] (Thammasat University, Thailand)
  - E-mail: rangsiman1993@gmail.com
- [Yuthana Tantirungrotechai][yt-link] (Thammasat University, Thailand)
  - E-mail: yt203y@gmail.com
- [Phimphaka Harding][ph-link] (Walailak University, Thailand)
  - E-mail: kphimpha@mail.wu.ac.th
- Guillaume Chastanet (University of Bordeaux, France)
  - E-mail: Guillaume.Chastanet@icmcb.cnrs.fr
- Philippe Guionneau (University of Bordeaux, France)
  - E-mail: Philippe.Guionneau@icmcb.cnrs.fr
- [Mathieu Marchivie][mm-link] (University of Bordeaux, France)
  - E-mail: mathieu.marchivie@icmcb.cnrs.fr
- [David J. Harding][dh-link] (Walailak University, Thailand)
  - E-mail: hdavid@mail.wu.ac.th

[rk-link]: https://rangsimanketkaew.github.io
[yt-link]: https://sites.google.com/site/compchem403/people/faculty/yuthana
[ph-link]: https://www.funtechwu.com/phimphaka-harding
[mm-link]: http://www.icmcb-bordeaux.cnrs.fr/spip.php?article562&lang=en
[dh-link]: https://www.funtechwu.com/david-j-harding
