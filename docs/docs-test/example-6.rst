=========
Example 6
=========

**Example 6 for running the test on OctaDist PyPI**

.. code-block:: python

    import octadist as oc

    file = r"../example-input/Multiple-metals.xyz"

    atom_full, coord_full = oc.molecule.extract_coord(file)

    # Display and automatically save image as .png file with user-specified name
    my_plot = oc.draw.DrawComplex(atom=atom_full, coord=coord_full)
    my_plot.add_atom()
    my_plot.add_bond()
    my_plot.add_legend()
    my_plot.save_img()
    my_plot.show_plot()

    # Output image, Complex_saved_by_OctaDist.png, is stored at ../images directory

.. figure:: Complex_saved_by_OctaDist.png
    :width: 400px
    :align: center
    :alt: structure to show

    Snapshot of structure saved by OctaDist.

