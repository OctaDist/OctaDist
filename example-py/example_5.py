###################################################
# Example 5 for running the test on OctaDist PyPI #
###################################################

import octadist as oc

file = r"../example-input/Multiple-metals.xyz"

atom_full, coord_full = oc.coord.extract_file(file)

# Graphical display for octahedral complex
oc.draw.all_atom(atom_full, coord_full)
