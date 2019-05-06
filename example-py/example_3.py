from octadist import coord, calc

#############
# Example 3 #
#############

# Open and read input file
file = r"../example-input/Multiple-metals.xyz"

# If complex contains metal center more than one, you can specify the index of metal of interest.
# For example, this complex contains three metal atoms: Fe, Ru, and Rd. I add second argument "2"
# for computing the parameter for Ru metal center atom.
atom, coor = coord.extract_octa(file, 2)

# Calculate all octahedral parameters
d_mean, zeta, delta, sigma, theta = calc.calc_all(atom, coor)

# Show all computed parameters
print("\nEx.3: All computed parameters")
print("-----------------------------")
print("Mean distance =", d_mean)
print("         Zeta =", zeta)
print("        Delta =", delta)
print("        Sigma =", sigma)
print("        Theta =", theta)

