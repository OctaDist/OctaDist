###################################################
# Example 6 for running the test on OctaDist PyPI #
###################################################

import octadist as oc

file = r"../example-input/Multiple-metals.xyz"

atom_full, coord_full = oc.coord.extract_file(file)

# Display and automatically save image as .png file with user-specified name
oc.draw.all_atom(atom_full, coord_full, "complex_octadist")

# Output image, complex_octadist.png, is stored at ../images directory
