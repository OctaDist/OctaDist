###################################################
# Example 5 for running the test on OctaDist PyPI #
###################################################

from octadist import coord, draw

file = r"../example-input/Multiple-metals.xyz"

# Graphical display for octahedral complex

atom_full, coor_full = coord.extract_file(file)
draw.all_atom(atom_full, coor_full)

# Display and automatically save image as .png file with user-specified name

draw.all_atom(atom_full, coor_full, "complex_octadist")

# Output image, complex_octadist.png, is stored at ../images directory
