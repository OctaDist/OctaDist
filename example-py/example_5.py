###################################################
# Example 5 for running the test on OctaDist PyPI #
###################################################

import os
import octadist as oc

dir_path = os.path.dirname(os.path.realpath(__file__))
input_folder = os.path.join(dir_path, "../example-input/")
file = input_folder + "Multiple-metals.xyz"

atom_full, coord_full = oc.io.extract_coord(file)

# Graphical display for octahedral complex
my_plot = oc.draw.DrawComplex_Matplotlib(atom=atom_full, coord=coord_full)
my_plot.add_atom()
my_plot.add_bond()
my_plot.add_legend()
my_plot.show_plot()
