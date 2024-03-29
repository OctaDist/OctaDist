###################################################
# Example 3 for running the test on OctaDist PyPI #
###################################################

import os
import octadist as oc

# You can also import your input file, like this:

dir_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(dir_path, "../example-input/")
file = input_folder + "Multiple-metals.xyz"

# Then use coord.extract_file to extract all atomic symbols and coordinates,
# and then use coord.extract_octa for taking the octahedral structure.

atom_full, coord_full = oc.io.extract_coord(file)
atom, coord = oc.io.extract_octa(atom_full, coord_full)

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
# Zeta  = 0.0030146365519487794
# Delta = 1.3695007180404868e-07
# Sigma = 147.3168033970211
# Theta = 520.6407679851042
