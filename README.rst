pyGtoP
======

pyGtoP is a Python wrapper for the `IUPHAR/BPS Guide to PHARMACOLOGY
<http://www.guidetopharmacology.org>`_ API. It
provides a Python interface for access to the GtoP database.


Installing
----------

pip
~~~

pyGtoP can be installed using pip:

``$ pip3 install pygtop``

pyGtoP is written for Python 3, and as of version 0.1.0 is incompatible with
Python 2. Versions 0.4.1 and earlier will continue to support Python 2.


Requirements
~~~~~~~~~~~~

PyGtoP requires the Python librares
`requests <http://docs.python-requests.org/>`_ and
`molecuPy <http://molecupy.readthedocs.io>`_. These will be installed
automatically if pyGtoP is installed with pip.

Otherwise pyGtoP has no external dependencies, and is pure Python.


Overview
--------

Ligands
~~~~~~~
The simplest way to create a ligand is via its GtoP ID:

    >>> import pygtop
    >>> my_drug = pygtop.get_ligand_by_id(5239)
    >>> my_drug.name
    'paracetamol'
    >>> my_drug.ligand_type
    'Synthetic organic'

Properties other than the most basic ones must be requested separately, as they
require their own HTTP request:

    >>> my_drug.request_molecular_properties()
    >>> my_drug.rotatable_bonds
    2
    >>> my_drug.molecular_weight
    151.0633286
    >>> my_drug.request_structural_properties()
    >>> my_drug.smiles
    'CC(=O)Nc1ccc(cc1)O'

Ligands can also be accessed by name, or at random:

    >>> pygtop.get_ligand_by_name('caffeine')
    <'caffeine' Ligand (Natural product)>
    >>> pygtop.get_random_ligand()
    <'3,5-dihydroxybenzoic acid' Ligand (Synthetic organic)>
    >>> pygtop.get_random_ligand(ligand_type='antibody')
    <'blinatumomab' Ligand (Antibody)>

You can get a list of ligands by either requesting all ligands, or providing a
query:

    >>> all_ligands = pygtop.get_all_ligands()
    >>> len(all_ligands) # There are 8,328 ligands as of March 2016
    8328
    >>> all_ligands[0]
    <'10,10-difluoro TXA<sub>2</sub>' Ligand (Synthetic organic)>
    >>> query = {"type": "Approved", "molWeightGt": 50, "molWeightLt": 200}
    >>> ligands = pygtop.get_ligands_by(query) # Get approved ligands between 50 and 200 Da
    >>> len(ligands)
    104


Targets
~~~~~~~
The API for targets works in much the same way as for ligands:

    >>> import pygtop
    >>> my_target = pygtop.get_target_by_id(297)
    >>> my_target.name
    'motilin receptor'
    >>> my_target.target_type
    'GPCR'

    >>> pygtop.get_target_by_name('CYP3A4')
    <'CYP3A4' Target (Enzyme)>
    >>> pygtop.get_random_ligand()
    <'OAT6' Target (Transporter)>
    >>> pygtop.get_random_target(target_type='NHR')
    <'Glucocorticoid receptor' Target (NHR)>

    >>> all_targets = pygtop.get_all_targets()
    >>> len(all_targets) # There are 2,859 ligands as of March 2016
    2859
    >>> all_targets[-1]
    <'Kynurenine 3-monooxygenase' Target (Enzyme)>
    >>> query = {"type": "NHR"}
    >>> targets = pygtop.get_targets_by(query) # Get all NHR targets
    >>> len(targets)
    49

As with the ligands, certain properties must be explicitly requested before
they can be accessed:

    >>> my_target.request_database_properties()
    >>> my_target.database_links[0]
    <ChEMBL Target link (11061) for Human>

There is a class representing target families, which are arranged hierarchically:

    >>> my_target.get_families()
    [<'Motilin receptor' TargetFamily>]
    >>> my_target.get_families()[0].get_parent_families()
    [<'G protein-coupled receptors' TargetFamily>]
    >>> len(my_target.get_families()[0].get_parent_families()[0].get_subfamilies())
    69


Because so many properties of targets are specific to species variants, there is
also a class representing targets of a particular species:

    >>> rat_variant = pygtop.SpeciesTarget(300, "rat")
    <rat NPFF1 receptor>
    >>> rat_variant.target_id
    300
    >>> rat_variant.target
    <'NPFF1 receptor' Target (GPCR)>
    >>> rat_variant.species
    'rat'

When additional properties of these species variants are requested, only those
pertaining to that species will be obtained:

    >>> rat_variant.request_database_properties()
    >>> rat_variant.database_links
    [<Ensembl Gene link (ENSRNOG00000000559) for Rat>, <Entrez Gene link (64107)
    for Rat>, <GPCRDB link (Q9EP86) for Rat>, <PhosphoSitePlus link (Q9EP86) for
    Rat>, <Protein GI link (294661831) for Rat>, <RefSeq Nucleotide link (NM_022
    291) for Rat>, <RefSeq Protein link (NP_071627) for Rat>, <UniProtKB link (Q
    9EP86) for Rat>, <UniProtKB ID/Entry name link (NPFF1_RAT) for Rat>]

Interactions
~~~~~~~~~~~~

The interactions of a ligand can be accessed as follows:

    >>> import pygtop
    >>> ligand = pygtop.get_ligand_by_id(5239)
    >>> ligand.get_interactions()
    [<Interaction (5239 --> Human 1375)>, <Interaction (5239 --> Human 1376)>]

Alternatively you can request the interacting targets instead:

    >>> ligand.get_targets()
    [<'COX-1' Target (Enzyme)>, <'COX-2' Target (Enzyme)>]
    >>> ligand.get_species_targets()
    [<human COX-1>, <human COX-2>]

Targets can access interactions in much the same way:

    >>> target = pygtop.get_target_by_id(50)
    >>> target.get_interactions()
    [<Interaction (681 --> Human 50)>, <Interaction (682 --> Human 50)>, <Intera
    ction (683 --> Human 50)>, <Interaction (684 --> Human 50)>, <Interaction (6
    95 --> Mouse 50)>, <Interaction (695 --> Rat 50)>, <Interaction (696 --> Rat
     50)>, <Interaction (697 --> Mouse 50)>, <Interaction (697 --> Rat 50)>, <In
    teraction (3768 --> Human 50)>, <Interaction (700 --> Human 50)>, <Interacti
    on (701 --> Mouse 50)>, <Interaction (701 --> Rat 50)>, <Interaction (705 --o
    > Mouse 50)>, <Interaction (705 --> Rat 50)>, <Interaction (706 --> Human 50
    )>]
    >>> species_target = pygtop.SpeciesTarget(50, "rat")
    >>> species_target.get_interactions()
    [<Interaction (695 --> Rat 50)>, <Interaction (696 --> Rat 50)>, <Interactio
    n (697 --> Rat 50)>, <Interaction (701 --> Rat 50)>, <Interaction (705 --> R
    at 50)>]
    >>> target.get_ligands()
    [<'&alpha;-CGRP' Ligand (Peptide)>, <'&beta;-CGRP' Ligand (Peptide)>, <'adre
    nomedullin' Ligand (Peptide)>, <'adrenomedullin 2/intermedin' Ligand (Peptid
    e)>, <'&alpha;-CGRP' Ligand (Peptide)>, <'&alpha;-CGRP' Ligand (Peptide)>, <
    '&beta;-CGRP' Ligand (Peptide)>, <'adrenomedullin' Ligand (Peptide)>, <'adre
    nomedullin' Ligand (Peptide)>, <'[<sup>125</sup>I]AM (rat)' Ligand (Peptide)
    >, <'&alpha;-CGRP-(8-37) (human)' Ligand (Peptide)>, <'&alpha;-CGRP-(8-37) (
    rat)' Ligand (Peptide)>, <'&alpha;-CGRP-(8-37) (rat)' Ligand (Peptide)>, <'A
    M-(20-50) (rat)' Ligand (Peptide)>, <'AM-(20-50) (rat)' Ligand (Peptide)>, <
    'AM-(22-52) (human)' Ligand (Peptide)>]
    >>> species_target.get_ligands()
    [<'&alpha;-CGRP' Ligand (Peptide)>, <'&beta;-CGRP' Ligand (Peptide)>, <'adre
    nomedullin' Ligand (Peptide)>, <'&alpha;-CGRP-(8-37) (rat)' Ligand (Peptide)
    >, <'AM-(20-50) (rat)' Ligand (Peptide)>]

The interaction objects themselves have methods for returning the relevant
ligand or target object:

    >>> interaction = ligand.get_interactions()[0]
    >>> interaction.get_ligand()
    <'paracetamol' Ligand (Synthetic organic)>
    >>> interaction.get_target()
    <'COX-1' Target (Enzyme)>
    >>> interaction.get_species_target()
    <human COX-1>

The interactions between a ligand and target, if any, can be obtained using:

    >>> ligand = pygtop.get_ligand_by_id(1)
    >>> target = pygtop.get_target_by_id(1)
    >>> pygtop.get_interactions_between(ligand, target)
    [<Interaction (1 --> Human 1)>]

Structural Data
~~~~~~~~~~~~~~~

The Guide to PHARMACOLOGY has PDB codes annotated on some ligands and targets.
These can be accessed as follows:

    >>> ligand = pygtop.get_ligand_by_id(149)
    >>> ligand.get_gtop_pdbs()
    ['4IB4']
    >>> target = pygtop.get_target_by_id(595)
    >>> target.get_gtop_pdbs()
    ['1NYX']

In addition, ligands and targets can query the `RSCB PDB Web Services
<http:/www.rcsb.org/pdb/software/rest.do>`_ to find other PDB codes
(SpeciesTargets will only return PDBs relevant to that species):

    >>> ligand.find_pdbs_by_smiles()
    ['4IAR', '4IB4', '4NC3']
    >>> target.find_pdbs_by_uniprot_accession()
    ['1FM6', '1FM9', '1I7I', '1K74', '1KNU', '1NYX', '1PRG', '1RDT', '1WM0', '1Z
    EO', '1ZGY', '2ATH', '2F4B', '2FVJ', '2G0G', '2G0H', '2GTK', '2HFP', '2HWQ',
    '2HWR', '2I4J', '2I4P', '2I4Z', '2OM9', '2P4Y', '2POB', '2PRG', '2Q59', '2Q5
    9', '2Q5P', '2Q5S', '2Q61', '2Q6R', '2Q6S', '2Q8S', '2QMV', '2VSR', '2VST',
    '2VV0', '2VV1', '2VV1', '2VV2', '2VV3', '2VV4', '2VV4', '2XKW', '2YFE', '2ZK
    0', '2ZK1', '2ZK2', '2ZK3', '2ZK4', '2ZK5', '2ZK6', '2ZNO', '2ZVT', '3ADS',
    '3ADT', '3ADU', '3ADV', '3ADW', '3ADX', '3AN3', '3AN4', '3B0Q', '3B0R', '3B1
    M', '3B3K', '3BC5', '3CDP', '3CDS', '3CS8', '3CWD', '3D6D', '3DZU', '3DZY',
    '3E00', '3ET0', '3ET3', '3FEJ', '3FUR', '3G9E', '3GBK', '3H0A', '3HO0', '3HO
    D', '3IA6', '3K8S', '3KMG', '3LMP', '3NOA', '3OSI', '3OSW', '3PBA', '3PO9',
    '3PRG', '3QT0', '3R5N', '3R8A', '3R8I', '3S9S', '3SZ1', '3T03', '3TY0', '3U9
    Q', '3V9T', '3V9V', '3V9Y', '3VJH', '3VJI', '3VN2', '3VSO', '3VSP', '3WJ4',
    '3WJ5', '3WMH', '3X1H', '3X1I', '4A4V', '4A4W', '4CI5', '4E4K', '4E4Q', '4EM
    9', '4EMA', '4F9M', '4FGY', '4HEE', '4JAZ', '4JL4', '4L96', '4L98', '4O8F',
    '4OJ4', '4PRG', '4PVU', '4PWL', '4R06', '4R2U', '4R6S', '4XLD', '4XTA', '4XU
    M', '4Y29', '4YT1']

See the full documentation for a list of all the ways to search for PDB codes.

pyGtoP can now also use the `molecuPy <http://molecupy.readthedocs.io>`_ library
to return PDBs as PDB objects. To do this, simply provide ``molecupy=True`` to
any of the PDB requesting methods:

    >>> ligand.find_pdbs_by_smiles(molecupy=True)
    [<Pdb (4IAR)>, <Pdb (4IB4)>, <Pdb (4NC3)>]

See the molecuPy documentation for a full accounting of the functionality this
offers.



Changelog
---------

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
