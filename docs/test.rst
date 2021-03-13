====================
Example Calculations
====================

Supported File Format
---------------------

- **CIF file format**

File extension: ``.cif`` (https://en.wikipedia.org/wiki/Crystallographic_Information_File)

Crystallographic Information File (CIF). Example CIF is below:

::

    data_ADH041

    ###############
    ## ENTRY ##
    ###############

    _entry.id              ADH041

    ###############
    ## ATOM_SITE ##
    ###############                        
    loop_
    _atom_site.id
    _atom_site.label_atom_id                  
    _atom_site.label_comp_id                  
    _atom_site.label_asym_id                  
    _atom_site.auth_seq_id                   
    _atom_site.cartn_x                        
    _atom_site.cartn_y                        
    _atom_site.cartn_z                        
    _atom_site.occupancy                      
    _atom_site.B_iso_or_equiv                 
    _atom_site.label_entity_id
    _atom_site.label_seq_id
    1    O5*   G A   1       7.231  -2.196  -5.399  1.00 22.25   1 1         
    2    C5*   G A   1       6.950  -3.464  -4.723  1.00 15.86   1 1         
    3    C4*   G A   1       8.299  -4.018  -4.302  1.00 15.20   1 1         
    ...


- **XYZ file format**

File extension: ``.xyz`` (https://en.wikipedia.org/wiki/XYZ_file_format)

::

    <number of atoms>
    comment line
    <element 1>  <X> <Y> <Z>
    <element 2>  <X> <Y> <Z>
    <element 3>  <X> <Y> <Z>
    ...


- **Output of computational chemistry programs**

File extension: ``.out`` and ``.log``

1. `Gaussian <https://gaussian.com>`_
2. `NWChem <http://www.nwchem-sw.org/index.php/Main_Page>`_
3. `ORCA <https://orcaforum.kofo.mpg.de/app.php/portal>`_
4. `Q-Chem <https://www.q-chem.com>`_


Running the tests
-----------------

.. toctree::
   :maxdepth: 1

   docs-test/example-1.rst
   docs-test/example-2.rst
   docs-test/example-3.rst
   docs-test/example-4.rst
   docs-test/example-5.rst
   docs-test/example-6.rst

