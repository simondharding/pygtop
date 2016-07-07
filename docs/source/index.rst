pyGtoP Documentation
====================

pyGtoP is a Python wrapper for the `IUPHAR/BPS Guide to PHARMACOLOGY
<http://www.guidetopharmacology.org>`_ API. It
provides a Python interface for access to the GtoP database.

Example
-------

  >>> import pygtop
  >>> my_drug = pygtop.get_ligand_by_id(5239)
  >>> my_drug.name()
  'paracetamol'
  >>> my_drug.ligand_type()
  'Synthetic organic'

See the :doc:`overview page <overview>` for more examples, or the :doc:`full
documentation <full_documentation>` for a full listing of features.

Table of Contents
-----------------

.. toctree ::

    installing
    about_gtop
    overview
    full_documentation
    changelog
