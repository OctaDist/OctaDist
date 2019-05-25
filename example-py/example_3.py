###################################################
# Example 3 for running the test on OctaDist PyPI #
###################################################

import octadist as oc

# You can also import your input file, like this:

file = r"../example-input/Multiple-metals.xyz"

# Then use coord.extract_file to extract all atomic symbols and coordinates,
# and then use coord.extract_octa for taking the octahedral structure.

atom_full, coord_full = oc.coord.extract_file(file)
atom, coord = oc.coord.extract_octa(atom_full, coord_full)

zeta = oc.calc.calc_zeta(coord)             # Zeta
delta = oc.calc.calc_delta(coord)           # Delta
sigma = oc.calc.calc_sigma(coord)           # Sigma
theta = oc.calc.calc_theta(coord)           # Theta

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
