pyGtoP Documentation
====================

pyGtoP is a Python wrapper for the `IUPHAR/BPS Guide to PHARMACOLOGY
<http://www.guidetopharmacology.org>`_ API. It
provides a Python interface for access to the GtoP database.

About the Guide to PHARMACOLOGY
-------------------------------

The Guide to PHARMACOLOGY (GtoP), originally a collaboration between The British
Pharmacological Society (BPS) and the International Union of Basic and Clinical
Pharmacology (IUPHAR), acts as a “one-stop shop” portal to pharmacological
information. One of its main aims is to provide a searchable database with
quantitative information on drug targets and the prescription medicines and
experimental drugs that act on them.

For more information, see `the website itself
<http://www.guidetopharmacology.org/about.jsp>`_. Information on the GtoP web
services which pyGtoP accesses can be found `here
<http://www.guidetopharmacology.org/webServices.jsp>`_.


Installing
----------

pyGtoP can be installed using pip:

``$ pip install pygtop``

Note that pyGtoP is a Python 3 package. If your system has Python 2 installed,
you may need to specify the Python 3 form of pip using:

``$ pip3 install pygtop``


Overview
--------

Ligands
~~~~~~~
The simplest way to create a ligand is via its GtoP ID:

    >>> import pygtop
    >>> my_drug = pygtop.get_ligand_by_id(5239)
    >>> my_drug.name
    'paracetamol'
    >>> my_drug.type
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
    >>> len(all_ligands) # There are 8,328 ligands as of April 2016
    8328
    >>> all_ligands[0]
    <'10,10-difluoro TXA<sub>2</sub>' Ligand (Synthetic organic)>
    >>> query = {"type": "Approved", "molWeightGt": 50, "molWeightLt": 200}
    >>> ligands = pygtop.get_ligands_by(query) # Get approved ligands between 50 and 200 Da
    >>> len(ligands)
    104

Full documentation
----------------


Ligands (ligands.py)
~~~~~~~~~~~~~~~~~~~~

.. automodule:: pygtop.ligands
    :members:

GtoP Interface (gtop.py)
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pygtop.gtop
    :members:

Shared objects (shared.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pygtop.shared
    :members:

Exceptions (exceptions.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pygtop.exceptions
    :members:

Changelog
---------

Release 0.1.0
~~~~~~~~~~~~~

* Ligand functionality

  * Single ligand access (by ID, name, or at random)
  * Multiple ligand access (all, or by providing a query)
