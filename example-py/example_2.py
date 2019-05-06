from octadist import coord, calc

#############
# Example 2 #
#############

# Open and read input file
file = r"../example-input/Multiple-metals.xyz"

# Extract atomic labels and coordinates of octahedral structure from metal complex
atom, coor = coord.extract_octa(file)

# Calculate all octahedral parameters
d_mean, zeta, delta, sigma, theta = calc.calc_all(atom, coor)

# Show all computed parameters
print("\nEx.2: All computed parameters")
print("-----------------------------")
print("Mean distance =", d_mean)
print("         Zeta =", zeta)
print("        Delta =", delta)
print("        Sigma =", sigma)
print("        Theta =", theta)

