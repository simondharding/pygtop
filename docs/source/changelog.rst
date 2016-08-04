Changelog
---------

Release 2.0.1
~~~~~~~~~~~~~

`4 August 2016`

* pyGtoP not compatible for molecuPy 1.0.0 and higher.

* DatabaseLink and Gene objects now have method properties.


Release 2.0.0
~~~~~~~~~~~~~

`9 July 2016`

* Most properties now accessible as methods.

    * Affects ligands, targets and interactions.
    * This removes the need to request these properties separately.

* Gene object added.

* Added ability to strip HTML from certain string outputs, such as name.

* Added extra safeguards to GtoP web services requester to make more stable.

* Changed handling of affinity values in Interactions.

    * Now provides a low and a high value as numbers.
    * String range accessible via the original JSON object.

* This release is backwards-incompatible with the 1.x releases.


Release 1.0.1
~~~~~~~~~~~~~

`19 May 2016`

* Version number fix.


Release 1.0.0
~~~~~~~~~~~~~

`18 May 2016`

* `molecuPy <http://molecupy.readthedocs.io>`_ integration

    * PDB retrieval can now be by 4-char string, or molecuPy PDB object.
    * Ligands now have methods for locating themselves in a PDB file.

As molecuPy is a Python 3 package, this is the first version of pyGtoP to be
incompatible with Python 2, hence the new major version number.


Release 0.4.0
~~~~~~~~~~~~~

`22 April 2016`

* PDB functionality

  * Access GtoP PDB annotations for ligands, targets and interactions
  * Query RSCB PDB web services for PDBs of ligands, targets and interactions

* Can now search for ligands by SMILES string

Release 0.3.1
~~~~~~~~~~~~~

`31 March 2016`

* Bug fixes:

  * Interactions with median affinity values no longer throw errors
  * Interactions with string voltages no longer throw errors

Release 0.3.0
~~~~~~~~~~~~~

`30 March 2016`

* Interaction functionality

  * Interaction objects now available, which can link to ligands and targets
  * Ligands can get their interactions, and by extension their targets
  * Targets can get their interactions, and by extension their ligands

* Other features

  * Python 2 json strings no longer throw errors if they contain special characters
  * All species names now lowercase, regardless of how they are stored in the database

Release 0.2.0
~~~~~~~~~~~~~

`23 March 2016`

* Target functionality

  * Single target access (by ID, name, or at random)
  * Multiple target access (all, or by providing a query)
  * Target family manipulation
  * Target species-variant handling

* New Ligand features

  * Ligands now have methods for returning other ligands instead of lists of ligand IDs

Release 0.1.1
~~~~~~~~~~~~~

`16 March 2016`

* Added Python 2 compatibility

* Bug fixes:

  * Ligand string repr no longer throws attribute error

Release 0.1.0
~~~~~~~~~~~~~

`15 March 2016`

* Ligand functionality

  * Single ligand access (by ID, name, or at random)
  * Multiple ligand access (all, or by providing a query)
