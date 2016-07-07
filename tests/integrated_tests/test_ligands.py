from unittest import TestCase
import pygtop
from pygtop.ligands import Ligand
from pygtop.interactions import Interaction
from pygtop.targets import Target
from pygtop.exceptions import NoSuchLigandError, NoSuchInteractionError

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



class LigandPropertyTests(TestCase):

    def test_can_get_interactions(self):
        ligand = pygtop.get_ligand_by_id(2)
        interactions = ligand.interactions()
        self.assertGreater(len(interactions), 3)
        for interaction in interactions:
            self.assertIsInstance(interaction, Interaction)


    def test_can_get_interaction_by_id(self):
        ligand = pygtop.get_ligand_by_id(2)
        interaction = ligand.get_interaction_by_id(2)
        self.assertIsInstance(interaction, Interaction)


    def test_cannot_get_incorrect_interaction(self):
        ligand = pygtop.get_ligand_by_id(2)
        with self.assertRaises(NoSuchInteractionError):
            interaction = ligand.get_interaction_by_id(1000000)


    def test_can_get_targets(self):
        ligand = pygtop.get_ligand_by_id(2)
        targets = ligand.targets()
        self.assertGreater(len(targets), 3)
        for target in targets:
            self.assertIsInstance(target, Target)


    def test_can_get_gtop_pdbs(self):
        ligand = pygtop.get_ligand_by_id(121)
        pdbs = ligand.gtop_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_pdbs_by_smiles(self):
        ligand = pygtop.get_ligand_by_id(121)
        pdbs = ligand.smiles_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_pdbs_by_inchi(self):
        ligand = pygtop.get_ligand_by_id(4701)
        pdbs = ligand.inchi_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_pdbs_by_name(self):
        ligand = pygtop.get_ligand_by_id(121)
        pdbs = ligand.name_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_pdbs_by_sequence(self):
        ligand = pygtop.get_ligand_by_id(683)
        pdbs = ligand.sequence_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_external_pdbs(self):
        ligand = pygtop.get_ligand_by_id(121)
        pdbs = ligand.all_external_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_all_pdbs(self):
        ligand = pygtop.get_ligand_by_id(121)
        pdbs = ligand.all_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)



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
