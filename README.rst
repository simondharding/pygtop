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

pyGtoP is written for Python 3, and as of version 1.0.0 is incompatible with
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
    >>> my_drug.name()
    'paracetamol'
    >>> my_drug.ligand_type()
    'Synthetic organic'

Unlike previous versions of pyGtoP, all ligand (and target and interaction)
properties can be accessed without requesting them separately:

    >>> my_drug.rotatable_bonds()
    2
    >>> my_drug.molecular_weight()
    151.0633286
    >>> my_drug.smiles()
    'CC(=O)Nc1ccc(cc1)O'

Some properties, such as name and synonyms, contain HTML entities. To get these
without these often unceccessary additions, the ``strip_html`` argument can be
used:

    >>> my_drug = pygtop.get_ligand_by_id(2424)
    >>> my_drug.name()
    '&Delta;<sup>9</sup>-tetrahydrocannabinol'
    >>> my_drug.name(strip_html=True)
    'Δ9-tetrahydrocannabinol'
    >>> my_drug.synonyms()
    ['Abbott 40566', 'delta9-THC', '&Delta;<sup>9</sup>-THC', 'Marinol&reg;', 't
    etrahydrocannabinol']
    >>> my_drug.synonyms(strip_html=True)
    ['Abbott 40566', 'delta9-THC', 'Δ9-THC', 'Marinol®', 'tetrahydrocannabinol']


Ligands can also be accessed by name:

    >>> pygtop.get_ligand_by_name('caffeine')
    <Ligand 407 (caffeine)>

You can get a list of ligands by either requesting all ligands, or providing a
query:

    >>> all_ligands = pygtop.get_all_ligands()
    >>> len(all_ligands) # There are 8,400 ligands as of July 2016
    8400
    >>> all_ligands[0]
    <'10,10-difluoro TXA<sub>2</sub>' Ligand (Synthetic organic)>
    >>> query = {"type": "Approved", "molWeightGt": 50, "molWeightLt": 200}
    >>> ligands = pygtop.get_ligands_by(query) # Get approved ligands between 50 and 200 Da
    >>> len(ligands)
    106


Targets
~~~~~~~
The API for targets works in much the same way as for ligands:

    >>> import pygtop
    >>> my_target = pygtop.get_target_by_id(297)
    >>> my_target.name()
    'motilin receptor'
    >>> my_target.target_type()
    'GPCR'
    >>> pygtop.get_target_by_name('CYP3A4')
    <Target 1337 (CYP3A4)>

    >>> all_targets = pygtop.get_all_targets()
    >>> len(all_targets) # There are 2,866 ligands as of July 2016
    2866
    >>> all_targets[-1]
    <Target 2893 (Branched chain amino acid transaminase 2)>
    >>> query = {"type": "NHR"}
    >>> targets = pygtop.get_targets_by(query) # Get all NHR targets
    >>> len(targets)
    49

There is a class representing target families, which are arranged hierarchically:

    >>> my_target.families()
    [<'Motilin receptor' TargetFamily>]
    >>> my_target.families()[0].parent_families()
    [<'G protein-coupled receptors' TargetFamily>]
    >>> len(my_target.families()[0].parent_families()[0].sub_families())
    69


Because so many properties of targets are specific to species variants, many
properties have a ``species`` argument for only returning relevant results:

    >>> my_target = pygtop.get_target_by_id(300)
    >>> my_target.database_links()
    [<ChEMBL Target link (102733) for Human>, <Ensembl Gene link (ENSMUSG0000002
    0090) for Mouse>, <Ensembl Gene link (ENSRNOG00000000559) for Rat>, <Ensembl
     Gene link (ENSG00000148734) for Human>, <Entrez Gene link (237362) for Mous
    e>, <Entrez Gene link (64106) for Human>, <Entrez Gene link (64107) for Rat>
    , <GPCRDB link (Q9EP86) for Rat>, <GPCRDB link (Q9GZQ6) for Human>, <HomoloG
    ene link (23348) for Human>, <Human Protein Reference Database link (12120)
    for Human>, <OMIM link (607448) for Human>, <PharmGKB Gene link (PA134934991
    ) for Human>, <PhosphoSitePlus link (Q9GZQ6) for Human>, <PhosphoSitePlus li
    nk (Q9EP86) for Rat>, <PhosphoSitePlus link (E9Q468) for Mouse>, <Protein GI
     link (11545887) for Human>, <Protein GI link (294661833) for Mouse>, <Prote
    in GI link (294661831) for Rat>, <Protein Ontology (PRO) link (PRO:000001620
    ) for Human>, <RefSeq Nucleotide link (NM_022291) for Rat>, <RefSeq Nucleoti
    de link (NM_022146) for Human>, <RefSeq Nucleotide link (NM_001177511) for M
    ouse>, <RefSeq Protein link (NP_071627) for Rat>, <RefSeq Protein link (NP_0
    71429) for Human>, <RefSeq Protein link (NP_001170982) for Mouse>, <UniGene
    Hs. link (302026) for Human>, <UniProtKB link (Q9GZQ6) for Human>, <UniProtK
    B link (Q9EP86) for Rat>, <UniProtKB ID/Entry name link (NPFF1_HUMAN) for Hu
    man>, <UniProtKB ID/Entry name link (NPFF1_RAT) for Rat>]
    >>> my_target.database_links(species="rat")
    [<Ensembl Gene link (ENSRNOG00000000559) for Rat>, <Entrez Gene link (64107)
     for Rat>, <GPCRDB link (Q9EP86) for Rat>, <PhosphoSitePlus link (Q9EP86) fo
    r Rat>, <Protein GI link (294661831) for Rat>, <RefSeq Nucleotide link (NM_0
    22291) for Rat>, <RefSeq Protein link (NP_071627) for Rat>, <UniProtKB link
    (Q9EP86) for Rat>, <UniProtKB ID/Entry name link (NPFF1_RAT) for Rat>]


Interactions
~~~~~~~~~~~~

The interactions of a ligand can be accessed as follows:

    >>> import pygtop
    >>> ligand = pygtop.get_ligand_by_id(5239)
    >>> ligand.interactions()
    [<Interaction (5239 --> Human 1375)>, <Interaction (5239 --> Human 1376)>]

Alternatively you can request the interacting targets instead:

    >>> ligand.targets()
    [<Target 1375 (COX-1 )>, <Target 1376 (COX-2 )>]

Targets can access interactions in much the same way:

    >>> target = pygtop.get_target_by_id(50)
    >>> target.interactions()
    [<Interaction (681 --> Human 50)>, <Interaction (682 --> Human 50)>, <Intera
    ction (683 --> Human 50)>, <Interaction (684 --> Human 50)>, <Interaction (6
    95 --> Mouse 50)>, <Interaction (695 --> Rat 50)>, <Interaction (696 --> Rat
     50)>, <Interaction (697 --> Mouse 50)>, <Interaction (697 --> Rat 50)>, <In
    teraction (3768 --> Human 50)>, <Interaction (700 --> Human 50)>, <Interacti
    on (701 --> Mouse 50)>, <Interaction (701 --> Rat 50)>, <Interaction (705 --o
    > Mouse 50)>, <Interaction (705 --> Rat 50)>, <Interaction (706 --> Human 50
    )>]
    >>> target.interactions(species="rat")
    [<Interaction (695 --> Rat 50)>, <Interaction (696 --> Rat 50)>, <Interactio
    n (697 --> Rat 50)>, <Interaction (701 --> Rat 50)>, <Interaction (705 --> R
    at 50)>]
    >>> target.ligands()
    [<Ligand 681 (&alpha;-CGRP)>, <Ligand 682 (&beta;-CGRP)>, <Ligand 683 (adren
    omedullin)>, <Ligand 684 (adrenomedullin 2/intermedin)>, <Ligand 695 (&alpha
    ;-CGRP)>, <Ligand 695 (&alpha;-CGRP)>, <Ligand 696 (&beta;-CGRP)>, <Ligand 6
    97 (adrenomedullin)>, <Ligand 697 (adrenomedullin)>, <Ligand 3768 ([<sup>125
    </sup>I]AM (rat))>, <Ligand 700 (&alpha;-CGRP-(8-37) (human))>, <Ligand 701
    (&alpha;-CGRP-(8-37) (rat))>, <Ligand 701 (&alpha;-CGRP-(8-37) (rat))>, <Lig
    and 705 (AM-(20-50) (rat))>, <Ligand 705 (AM-(20-50) (rat))>, <Ligand 706 (A
    M-(22-52) (human))>]
    >>> target.ligands(species="rat")
    [<Ligand 695 (&alpha;-CGRP)>, <Ligand 696 (&beta;-CGRP)>, <Ligand 697 (adren
    omedullin)>, <Ligand 701 (&alpha;-CGRP-(8-37) (rat))>, <Ligand 705 (AM-(20-5
    0) (rat))>]

The interaction objects themselves have methods for returning the relevant
ligand or target object:

    >>> interaction = ligand.interactions()[0]
    >>> interaction.ligand()
    <Ligand 5239 (paracetamol)>
    >>> interaction.target()
    <Target 1375 (COX-1 )>


Structural Data
~~~~~~~~~~~~~~~

The Guide to PHARMACOLOGY has PDB codes annotated on some ligands and targets.
These can be accessed as follows:

    >>> ligand = pygtop.get_ligand_by_id(149)
    >>> ligand.gtop_pdbs()
    ['4IB4']
    >>> target = pygtop.get_target_by_id(595)
    >>> target.gtop_pdbs()
    ['1NYX']

In addition, ligands and targets can query the `RSCB PDB Web Services
<http:/www.rcsb.org/pdb/software/rest.do>`_ to find other PDB codes:

    >>> ligand.smiles_pdbs()
    ['4IAR', '4IB4', '4NC3']
    >>> target.uniprot_pdbs()
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

    >>> ligand.smiles_pdbs(molecupy=True)
    [<Pdb (4IAR)>, <Pdb (4IB4)>, <Pdb (4NC3)>]

See the molecuPy documentation for a full accounting of the functionality this
offers.




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
