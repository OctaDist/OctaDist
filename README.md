![Python version][Py-ver-badge]
[![PyPI-Server][PyPI-badge]][PyPI-link]
![Python Wheel][Py-wheel-badge]
![Code size][Code-size]
![Repo size][Repo-size]

[![Github Download All releases][DL-all-badge]][DL-all-link]
[![Github Download Latest version][DL-latest-badge]][DL-latest-link]

[Py-ver-badge]: https://img.shields.io/pypi/pyversions/octadist.svg
[Py-wheel-badge]: https://img.shields.io/pypi/wheel/octadist.svg
[Code-size]: https://img.shields.io/github/languages/code-size/OctaDist/OctaDist.svg
[Repo-size]: https://img.shields.io/github/repo-size/OctaDist/OctaDist.svg
[DL-all-badge]: https://img.shields.io/github/downloads/OctaDist/octadist/total.svg
[DL-all-link]: https://github.com/OctaDist/OctaDist/releases
[DL-latest-badge]: https://img.shields.io/github/downloads/OctaDist/OctaDist/v.2.6.1/total.svg
[DL-latest-link]: https://github.com/OctaDist/OctaDist/releases/tag/v.2.6.1


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
- display 3D molecule and other graphical analysis.
- upgrade your and other program with OctaDist abilities.
- deal with the code directly via an interactive scripting code.


## Development and Release

OctaDist is written entirely in Python 3 binding to Tkinter GUI toolkit. 
It is cross-platform program which can work on multiple operating systems. 
The stable version and development build of OctaDist are released at [here][release-link].
A standalone executable for graphical user interface (GUI) and 
source code for command line interface (CLI) are available for as follows:

[release-link]: https://github.com/OctaDist/OctaDist/releases

| Platform  | Description | Status |
|-----------|-------------|:------:|
| Windows   | Standalone executable | [![Travis-CI Test][Travis-badge]][Travis-link] |
| Linux     | Support for GUI and CLI | [![Travis-CI Test][Travis-badge]][Travis-link] |
| macOS     | Support for GUI and CLI | [![Travis-CI Test][Travis-badge]][Travis-link] |
| PyPI library   | [![PyPI-Server][PyPI-badge]][PyPI-link]| [![Travis-CI Test][Travis-badge]][Travis-link] |
| Anaconda cloud | [![Conda-Server][Conda-badge]][Conda-link]| [![Travis-CI Test][Travis-badge]][Travis-link] |
| Nightly build | Development build | [![Travis-CI Test][Dev-badge]][Travis-link] |

[Travis-badge]: https://img.shields.io/travis/OctaDist/OctaDist/master.svg
[Travis-link]: https://travis-ci.org/OctaDist/OctaDist
[PyPI-badge]: https://img.shields.io/pypi/v/octadist.svg
[PyPI-link]: https://pypi.org/project/octadist/
[Conda-badge]: https://anaconda.org/rangsiman/octadist/badges/version.svg
[Conda-link]: https://anaconda.org/rangsiman/octadist
[Dev-badge]: https://img.shields.io/travis/OctaDist/OctaDist/nightly-build.svg

**Branch:**

1. Master stable: https://github.com/OctaDist/OctaDist/tree/master
2. Nightly dev: https://github.com/OctaDist/OctaDist/tree/nightly-build

## Git Clone

```sh
git clone https://github.com/OctaDist/OctaDist.git
git checkout nightly-build
git pull origin nightly-build
```

## Documents

User manual : [https://octadist.github.io/manual.html][manual-link].

[manual-link]: https://octadist.github.io/manual.html

Reference manual : 

| Version  | Status      | Docs   |
|----------|:-----------:|:------:|
|Stable    | ![Doc-Latest-Badge][Doc-Latest]   | [HTML][Latest-HTML] / [PDF][Latest-PDF] / [Epub][Latest-Epub]  |
|Dev Build | ![Doc-Nightly-Badge][Doc-Nightly] | [HTML][NightlyG-HTML] / [PDF][Nightly-PDF] / [Epub][Nightly-Epub]  |

[Doc-Latest]: https://img.shields.io/readthedocs/octadist/latest.svg
[Latest-HTML]: https://octadist.readthedocs.io/en/latest/
[Latest-PDF]: https://readthedocs.org/projects/octadist/downloads/pdf/latest/
[Latest-Epub]: https://readthedocs.org/projects/octadist/downloads/epub/latest/

[Doc-Nightly]: https://img.shields.io/readthedocs/octadist/nightly-build.svg
[NightlyG-HTML]: https://octadist.readthedocs.io/en/nightly-build/
[Nightly-PDF]: https://readthedocs.org/projects/octadist/downloads/pdf/nightly-build/
[Nightly-Epub]: https://readthedocs.org/projects/octadist/downloads/epub/nightly-build/


## Download and Install

If you use Windows, we strongly suggest you download a standalone executable:

[Click Here to Download OctaDist-2.6.1-Win-x86-64.exe][download-win-exe]

[download-win-exe]: https://github.com/OctaDist/OctaDist/releases/download/v.2.6.1/OctaDist-2.6.1-Win-x86-64.exe


If you use Linux or macOS and already have Python 3 installed on the system, 
the easiest way to install OctaDist is to use `pip`.

```sh
pip install octadist
```

or use `conda` for those who have Anaconda:

```sh
conda install -c rangsiman octadist
```

## Starting OctaDist

### Graphical User Interface (GUI)

To start GUI program:

```sh
octadist
```

Download a standalone executable to your system.

|![][Screenshots_1] | ![][Screenshots_2] | ![][Screenshots_3]|
|:-----------------:|:------------------:|:-----------------:|
| OctaDist GUI      | XYZ coordinates    | Computed distortion parameters|

[Screenshots_1]: https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Screenshots_OctaDist.png
[Screenshots_2]: https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Screenshots_Example_Mol.png
[Screenshots_3]: https://raw.githubusercontent.com/OctaDist/OctaDist/master/images/Screenshots_Computed.png

### Command Line Interface (CLI)

To start program command line (with help):

```sh
octadist_cli
```

To compute parameters:

```sh
octadist_cli -i INPUT.xyz
```

## Running the tests

#### Example 1: OctaDist as a package

```python
import octadist as oc

# Prepare list of atomic coordinates of octahedral structure:

atom = ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']

coord = [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
         [1.885657000, 4.804777000, 6.183726000],
         [1.747515000, 6.960963000, 7.932784000],
         [4.094380000, 5.807257000, 7.588689000],
         [0.539005000, 4.482809000, 8.460004000],
         [2.812425000, 3.266553000, 8.131637000],
         [2.886404000, 5.392925000, 9.848966000]]

dist = oc.CalcDistortion(coord)
zeta = dist.zeta             # 0.228072561
delta = dist.delta           # 0.000476251
sigma = dist.sigma           # 47.92652837
theta = dist.theta           # 122.6889727
```

#### Example 2: Display 3D structure of molecule

```python
import octadist as oc

file = r"../example-input/Multiple-metals.xyz"

atom_full, coord_full = oc.molecule.extract_coord(file)

my_plot = oc.draw.DrawComplex(atom=atom_full, coord=coord_full)
my_plot.add_atom()
my_plot.add_bond()
my_plot.add_legend()
my_plot.save_img()
my_plot.show_plot()

# Figure will be saved as Complex_saved_by_OctaDist.png by default.
```

<p align="center">
   <img alt="molecule" 
   src="https://raw.githubusercontent.com/OctaDist/OctaDist/master/example-py/Complex_saved_by_OctaDist.png" 
   align=middle width="350pt" />
<p/>


Other example scripts and octahedral complexes are available at 
[example-py](https://github.com/OctaDist/OctaDist-PyPI/tree/master/example-py) and 
[example-input](https://github.com/OctaDist/OctaDist-PyPI/tree/master/example-input).


## Citation

Please cite this project when you use OctaDist for scientific publication.

```
OctaDist - A tool for calculating distortion parameters in coordination complexes.
https://octadist.github.io
```


## Bug report

If you found issues in OctaDist, please report it to us at [here][submit-issues].

[submit-issues]: https://github.com/OctaDist/OctaDist/issues


## Project team

- [Rangsiman Ketkaew](https://sites.google.com/site/rangsiman1993) (Thammasat University, Thailand) <br/>
  - E-mail: rangsiman1993@gmail.com <br/>
- [Yuthana Tantirungrotechai](https://sites.google.com/site/compchem403/people/faculty/yuthana) (Thammasat University, Thailand)
  - E-mail: yt203y@gmail.com
- [David J. Harding](https://www.funtechwu.com/david-j-harding) (Walailak University, Thailand)
  - E-mail: hdavid@mail.wu.ac.th
- [Phimphaka Harding](https://www.funtechwu.com/phimphaka-harding) (Walailak University, Thailand)
  - E-mail: kphimpha@mail.wu.ac.th
- [Mathieu Marchivie](http://www.icmcb-bordeaux.cnrs.fr/spip.php?article562&lang=fr) (University of Bordeaux, France)
  - E-mail: mathieu.marchivie@icmcb.cnrs.fr
