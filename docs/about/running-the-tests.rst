=================
Running the Tests
=================

Example running the OctaDist.


**Example 1 for running the test on OctaDist PyPI:**

.. code-block:: python

    from octadist import calc
    
    # The first atom must be metal center atom of octahedral structure.
    # If not, please see example_2.py for how to handle this issue.
    
    atom = ['Fe', 'O', 'O', 'N', 'N', 'N', 'N']
    
    coor = [[2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
            [1.885657000, 4.804777000, 6.183726000],
            [1.747515000, 6.960963000, 7.932784000],
            [4.094380000, 5.807257000, 7.588689000],
            [0.539005000, 4.482809000, 8.460004000],
            [2.812425000, 3.266553000, 8.131637000],
            [2.886404000, 5.392925000, 9.848966000]]
    
    zeta, delta, sigma, theta = calc.calc_all(coor)
    
    print("\nAll computed parameters")
    print("-----------------------")
    print("Zeta  =", zeta)
    print("Delta =", delta)
    print("Sigma =", sigma)
    print("Theta =", theta)
    
    # All computed parameters
    # -----------------------
    # Zeta  = 0.22807256171728651
    # Delta = 0.0004762517834704151
    # Sigma = 47.926528379270124
    # Theta = 122.688972774546
    
**Example 2 for running the test on OctaDist PyPI:**
    
.. code-block:: python
    
    from octadist import calc, coord
    
    atom = ['O', 'O', 'Fe', 'N', 'N', 'N', 'N']
    
    coor = [[1.885657000, 4.804777000, 6.183726000],
            [1.747515000, 6.960963000, 7.932784000],
            [2.298354000, 5.161785000, 7.971898000],  # <- Metal atom
            [4.094380000, 5.807257000, 7.588689000],
            [0.539005000, 4.482809000, 8.460004000],
            [2.812425000, 3.266553000, 8.131637000],
            [2.886404000, 5.392925000, 9.848966000]]
    
    # What if the first atom in atomic symbol and coordinates lists are not metal atom,
    # you can also use coord.extract_octa to rearrange the sequence of atom in list.
    
    atom_octa, coor_octa = coord.extract_octa(atom, coor)
    
    zeta, delta, sigma, theta = calc.calc_all(coor_octa)
    
    print("\nAll computed parameters")
    print("-----------------------")
    print("Zeta  =", zeta)
    print("Delta =", delta)
    print("Sigma =", sigma)
    print("Theta =", theta)
    
    # All computed parameters
    # -----------------------
    # Zeta  = 0.22807256171728651
    # Delta = 0.0004762517834704151
    # Sigma = 47.926528379270124
    # Theta = 122.688972774546
    
    
**Example 3 for running the test on OctaDist PyPI:**

.. code-block:: python
        
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
    
    
**Example 4 for running the test on OctaDist PyPI:**

.. code-block:: python
    
    from octadist import coord, calc
    
    file = r"../example-input/Multiple-metals.xyz"
    
    atom_full, coor_full = coord.extract_file(file)
    
    # If complex contains metal center more than one, you can specify the index metal
    # whose octahedral structure will be computed.
    # For example, this complex contains three metal atoms: Fe, Ru, and Rd.
    # I add "2" as a second argument for choosing Ru as metal of interest.
    
    atom_octa, coor_octa = coord.extract_octa(atom_full, coor_full, 2)
    
    zeta, delta, sigma, theta = calc.calc_all(coor_octa)
    
    print("\nAll computed parameters")
    print("-----------------------")
    print("Zeta  =", zeta)
    print("Delta =", delta)
    print("Sigma =", sigma)
    print("Theta =", theta)
    
    # All computed parameters
    # -----------------------
    # Zeta  = 0.001616439510534251
    # Delta = 3.5425830613072754e-08
    # Sigma = 1.26579367508117
    # Theta = 4.177042495798965
    

**Example 5 for running the test on OctaDist PyPI:**
    
.. code-block:: python
    
    from octadist import coord, draw
    
    file = r"../example-input/Multiple-metals.xyz"
    
    # Graphical display for octahedral complex
    
    atom_full, coor_full = coord.extract_file(file)
    draw.all_atom(atom_full, coor_full)
    
    # Display and automatically save image as .png file with user-specified name
    
    draw.all_atom(atom_full, coor_full, "complex_octadist")
    
    # Output image, complex_octadist.png, is stored at ../images directory
    
    
    
    
