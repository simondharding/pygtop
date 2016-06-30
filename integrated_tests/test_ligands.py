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
