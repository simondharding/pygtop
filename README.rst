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

pyGtoP is written for Python 3, but should be compatible with Python 2.7. To
install for Python 2, use:

``$ pip install pygtop``

Requirements
~~~~~~~~~~~~

PyGtoP requires the Python library
`requests <http://docs.python-requests.org/>`_. This will be installed
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
     for Rat>, <GPCRDB link (Q9EP86) for Rat>, <PhosphoSitePlus link (Q9EP86) fo
     r Rat>, <Protein GI link (294661831) for Rat>, <RefSeq Nucleotide link (NM_
     022291) for Rat>, <RefSeq Protein link (NP_071627) for Rat>, <UniProtKB lin
     k (Q9EP86) for Rat>, <UniProtKB ID/Entry name link (NPFF1_RAT) for Rat>]

Changelog
---------

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
