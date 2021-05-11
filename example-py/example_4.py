###################################################
# Example 4 for running the test on OctaDist PyPI #
###################################################

import os
import octadist as oc

dir_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(dir_path, "../example-input/")
file = input_folder + "Multiple-metals.xyz"

atom_full, coor_full = oc.io.extract_coord(file)

# If complex contains metal center more than one, you can specify the index metal
# whose octahedral structure will be computed.
# For example, this complex contains three metal atoms: Fe, Ru, and Rd.
# I add "2" as a second argument for choosing Ru as metal of interest.

atom, coord = oc.io.extract_octa(atom_full, coor_full, 2)

dist = oc.CalcDistortion(coord)
zeta = dist.zeta  # Zeta
delta = dist.delta  # Delta
sigma = dist.sigma  # Sigma
theta = dist.theta  # Theta

print("\nAll computed parameters")
print("-----------------------")
print("Zeta  =", zeta)
print("Delta =", delta)
print("Sigma =", sigma)
print("Theta =", theta)

# All computed parameters
# -----------------------
# Zeta  = 0.001616439510534251
# Delta = 3.5425830613072754e-08
# Sigma = 1.26579367508117
# Theta = 4.177042495798965
