import unittest
import sys
sys.path.append(".")
sys.path.append("..")
import pygtop
import pygtop.exceptions


class LigandAccess(unittest.TestCase):
    """This is the test for version 0.1.

    In this version, the user can access a ligand by ID, and access most of the
    properties accessible from the API. They cannot currently access interaction,
     PDB, rank order, complex, subunit or image information.

    They can also use the API ligand searcher for basic attributes, but not
    SMILES queries. This is extended to allow for getting a ligand by name."""


    def test_can_get_single_ligand(self):
        # The user gets a ligand by ID
        ligand = pygtop.get_ligand_by_id(1)

        # The user decides to get the structural information for the ligand
        ligand.get_structural_properties()

        # The user tries to access molecular properties
        self.assertRaises(pygtop.PropertyNotRequestedYetError, lambda: ligand.rotatable_bonds)

        # The user decides to get molecular properties for the ligand
        ligand.get_molecular_properties()

        # The user decides to get database properties for the ligand
        ligand.get_database_properties()

        # The user decides to get synonym properties for the ligand
        ligand.get_synonym_properties()

        # The user decides to get comment properties for the ligand
        ligand.get_comment_properties()

        # The user decides to get precursor properties for the ligand
        ligand.get_precursor_properties()

        # The user gets a random ligand
        pygtop.get_random_ligand()

        # The user decides to get a random peptide ligand
        pygtop.get_random_ligand(ligand_type="peptide")



    def test_can_get_all_ligands(self):

        # The user gets all ligands
        ligands = pygtop.get_all_ligands()
        self.assertIsInstance(ligands, list)
        self.assertGreater(len(ligands), 5000)
        for ligand in ligands:
            self.assertIsInstance(ligand, pygtop.Ligand)

        # The user searches for specific ligands
        criteria = {
         "type": "Approved",
         "molWeightGt": 50,
         "molWeightLt": 200
        }
        ligands = pygtop.get_ligands_by(criteria)

        # The user looks for a ligand with a certain name
        ligand = pygtop.get_ligand_by_name("APIGENIN")

        # The user looks for a ligand with a name that does not exist
        ligand = pygtop.get_ligand_by_name("paracetamoxyfrusebendroneomycin")
        self.assertEqual(ligand, None)


if __name__ == "__main__":
    unittest.main()
