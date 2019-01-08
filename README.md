# OctaDist
Octahedral Distortion Analysis: determining the structural distortion of octahedral complex. <br/>
This program was written in Python 3.7.2 and tested on PyCharm 2018.3.2 (Community Edition). <br/>

## Background
### Octahedral Distortion Parameters
Octahedral structure is composed of 7 atoms: one metal center atom and six ligand atoms. It has eqight faces, 6 vertices, and 12 edges.
The structural distortion generally occurs in octahedral complex. Previous publications have determined the octahedral distortion using structural parameters: ![](https://latex.codecogs.com/svg.Latex?%5CDelta), ![](https://latex.codecogs.com/svg.Latex?%5CSigma), and ![](https://latex.codecogs.com/svg.Latex?%5CTheta), given by following equations

- ![](https://latex.codecogs.com/svg.Latex?%5CDelta%20%3D%20%5Cfrac%7B1%7D%7B6%7D%20%5Csum_%7Bi%20%3D%201%7D%5E%7B6%7D%20%28%5Cfrac%7Bd_%7Bi%7D%20-%20d%7D%7Bd%7D%29%5E2)

- ![](https://latex.codecogs.com/svg.Latex?%5CSigma%20%3D%20%5Csum_%7Bi%20%3D%201%7D%5E%7B12%7D%20%5Cabs%20%5Cleft%20%7C%2090%20-%20%5Cphi_%7Bi%7D%20%7C)

- ![](https://latex.codecogs.com/svg.Latex?%5CTheta%20%3D%20%5Csum_%7Bi%20%3D%201%7D%5E%7B24%7D%20%5Cabs%20%5Cleft%20%7C%2060%20-%20%5Ctheta_%7Bi%7D%20%7C) 

2D structure of octahedral Fe complex |  3D structure of octahedral Fe complex  | Projection of ligand atoms onto the twisting plane
:-------------------------:|:-------------------------:|:-------------------------:
![](complex-2.jpg)         |  ![](complex-3.jpg)       |  ![](complex-1.jpg)

### Methods
#### Orthogonal projection
Calculation of the ![](https://latex.codecogs.com/svg.Latex?%5CDelta) and ![](https://latex.codecogs.com/svg.Latex?%5CSigma) parameters are straightforward, but the ![](https://latex.codecogs.com/svg.Latex?%5CTheta) is tricky becuase the ![](https://latex.codecogs.com/svg.Latex?%5Ctheta) angle depends on how the two twisting planes are defined. Given three ligand atoms, we can find the plane for orthogonal projection of other ligan atoms onto the plane. The location of the ligand atoms on the given plane are called a projected point. Then, we compute the angle between the vector of a projected point of two atoms (ray 1 and ray 2), which a projected metal center is taken as vertex. 

<p align="center">
   <img alt="Angle" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Two_rays_and_one_vertex.png/440px-Two_rays_and_one_vertex.png" align=middle width="200pt" /> 
<p/>

## Usage
### Linux OS
For Linux user, use `python3 -V` to check python version.
1. Download program source code from [this page](https://github.com/rangsimanketkaew/OctaDist)
2. Change file permission: `chmod +x OctaDist_V*.py`
3. Execute program: `python OctaDist_V*.py`

### Windows OS
1. Download program executable from [this page](https://github.com/rangsimanketkaew/OctaDist/releases)
2. Right click and select `Run as administrator`
3. Click `Yes`

## Screenshots
<p align="left">
   <img alt="Capture_Window" src="Capture_Window.jpg" align=middle width="300pt" />
   <img alt="Capture_CMD" src="Capture_CMD.jpg" align=middle width="500pt"/>
<p/>

## Author
Rangsiman ketkaew <br/>
Computational Chemistry Research Unit <br/>
Department of Chemistry, Faculty of Science and Technology <br/>
Thammasat University, Pathum Thani, 12120 Thailand <br/>
E-mail: [rangsiman1993@gmail.com](rangsiman1993@gmail.com)
Website: [https://sites.google.com/site/rangsiman1993](https://sites.google.com/site/rangsiman1993)
