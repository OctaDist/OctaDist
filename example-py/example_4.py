###################################################
# Example 4 for running the test on OctaDist PyPI #
###################################################

import os
import octadist as oc

dir_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(dir_path, "../example-input/")
file = input_folder + "Multiple-metals.xyz"

atom_full, coor_full = oc.io.extract_coord(file)

# If a complex contains more than one metal atoms, you can specify the index of metal
# whose octahedral structure will be computed.
# For example, a test complex contains three metal atoms: Fe, Ru, and Rd.
# You can  specify the index of the reference atom with ref_index keyword (Python-index-based, start from 0).
# So for Ru, I set it to 8 (because Ru is the 9th atom of the complex).

atom, coord = oc.io.extract_octa(atom_full, coor_full, ref_index=8)

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
