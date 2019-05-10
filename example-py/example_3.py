###################################################
# Example 3 for running the test on OctaDist PyPI #
###################################################

from octadist import coord, calc

# You can also import your input file, like this:

file = r"../example-input/Multiple-metals.xyz"

# Then use coord.extract_file to extract all atomic symbols and coordinates,
# and then use coord.extract_octa for taking the octahedral structure.

atom_full, coor_full = coord.extract_file(file)
atom_octa, coor_octa = coord.extract_octa(atom_full, coor_full)

zeta, delta, sigma, theta = calc.calc_all(coor_octa)

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
