from unittest import TestCase
import pygtop
from pygtop.targets import Target, TargetFamily
from pygtop.interactions import Interaction
from pygtop.ligands import Ligand
from pygtop.exceptions import NoSuchTargetError, NoSuchTargetFamilyError, NoSuchInteractionError

class TargetAccessTests(TestCase):

    def test_can_get_target_by_id(self):
        target = pygtop.get_target_by_id(1)
        self.assertIsInstance(target, Target)
        self.assertEqual(target.target_id(), 1)


    def test_cannot_get_target_by_incorrect_id(self):
        with self.assertRaises(NoSuchTargetError):
            pygtop.get_target_by_id(0)


    def test_can_get_target_by_name(self):
        target = pygtop.get_target_by_name("CCR5")
        self.assertIsInstance(target, Target)
        self.assertEqual(target.name(), "CCR5")


    def test_cannot_get_target_by_incorrect_name(self):
        with self.assertRaises(NoSuchTargetError):
            pygtop.get_target_by_name("fauxprot")


    def test_can_get_all_targets(self):
        targets = pygtop.get_all_targets()
        self.assertIsInstance(targets, list)
        self.assertIsInstance(targets[0], Target)
        self.assertGreater(len(targets), 2000)


    def test_can_get_target_family_by_id(self):
        target = pygtop.get_target_family_by_id(1)
        self.assertIsInstance(target, TargetFamily)
        self.assertEqual(target.family_id(), 1)


    def test_cannot_get_target_by_incorrect_id(self):
        with self.assertRaises(NoSuchTargetFamilyError):
            pygtop.get_target_family_by_id(0)


    def test_can_get_all_target_families(self):
        targets = pygtop.get_all_target_families()
        self.assertIsInstance(targets, list)
        self.assertIsInstance(targets[0], TargetFamily)
        self.assertGreater(len(targets), 20)



class TargetPropertyTests(TestCase):

    def test_can_get_interactions(self):
        target = pygtop.get_target_by_id(2)
        interactions = target.interactions()
        self.assertGreater(len(interactions), 3)
        for interaction in interactions:
            self.assertIsInstance(interaction, Interaction)


    def test_can_get_interaction_by_id(self):
        target = pygtop.get_target_by_id(2)
        interaction = target.get_interaction_by_id(107)
        self.assertIsInstance(interaction, Interaction)


    def test_cannot_get_incorrect_interaction(self):
        target = pygtop.get_target_by_id(2)
        with self.assertRaises(NoSuchInteractionError):
            interaction = target.get_interaction_by_id(1000000)


    def test_can_get_ligands(self):
        target = pygtop.get_target_by_id(2)
        ligands = target.ligands()
        self.assertGreater(len(ligands), 3)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)


    def test_can_get_gtop_pdbs(self):
        target = pygtop.get_target_by_id(2)
        pdbs = target.gtop_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_pdbs_by_uniprot(self):
        target = pygtop.get_target_by_id(2)
        pdbs = target.uniprot_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)


    def test_can_get_all_pdbs(self):
        target = pygtop.get_target_by_id(2)
        pdbs = target.all_pdbs()
        self.assertGreaterEqual(len(pdbs), 1)



class TargetSearchTests(TestCase):

    def test_can_get_gpcrs(self):
        gpcrs = pygtop.get_targets_by({"type": "gpcr"})
        self.assertIsInstance(gpcrs, list)
        self.assertIsInstance(gpcrs[0], Target)
        self.assertGreater(len(gpcrs), 400)
