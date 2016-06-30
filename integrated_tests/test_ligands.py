from unittest import TestCase
import pygtop
from pygtop.ligands import Ligand
from pygtop.exceptions import NoSuchLigandError

class LigandAccessTests(TestCase):

    def test_can_get_ligand_by_id(self):
        ligand = pygtop.get_ligand_by_id(1)
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.ligand_id(), 1)


    def test_cannot_get_ligand_by_incorrect_id(self):
        with self.assertRaises(NoSuchLigandError):
            pygtop.get_ligand_by_id(0)


    def test_can_get_ligand_by_name(self):
        ligand = pygtop.get_ligand_by_name("paracetamol")
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.name(), "paracetamol")


    def test_cannot_get_ligand_by_incorrect_name(self):
        with self.assertRaises(NoSuchLigandError):
            pygtop.get_ligand_by_name("paracetamoxyfrusebendroneomycin")


    def test_can_get_all_ligands(self):
        ligands = pygtop.get_all_ligands()
        self.assertIsInstance(ligands, list)
        self.assertIsInstance(ligands[0], Ligand)
        self.assertGreater(len(ligands), 5000)



class LigandSearchTests(TestCase):

    def test_can_get_peptides(self):
        peptides = pygtop.get_ligands_by({"type": "peptide"})
        self.assertIsInstance(peptides, list)
        self.assertIsInstance(peptides[0], Ligand)
        self.assertGreater(len(peptides), 100)


    def test_can_search_by_smiles(self):
        ligands = pygtop.get_ligands_by_smiles(
         "CC(CN(C)C)CN1c2ccccc2Sc2ccccc12",
         search_type="similarity",
         cutoff=0.3
        )
        self.assertIsInstance(ligands, list)
        self.assertIsInstance(ligands[0], Ligand)
        self.assertGreater(len(ligands), 1)
