###################################################
# Example 5 for running the test on OctaDist PyPI #
###################################################

import octadist as oc

file = r"../example-input/Multiple-metals.xyz"

atom_full, coord_full = oc.molecule.extract_coord(file)

# Graphical display for octahedral complex
my_plot = oc.draw.DrawComplex(atom=atom_full, coord=coord_full)
my_plot.add_atom()
my_plot.add_bond()
my_plot.add_legend()
my_plot.show_plot()
