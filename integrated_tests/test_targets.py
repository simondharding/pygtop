from unittest import TestCase
import pygtop
from pygtop.targets import Target, TargetFamily
from pygtop.exceptions import NoSuchTargetError, NoSuchTargetFamilyError

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



class TargetSearchTests(TestCase):

    def test_can_get_gpcrs(self):
        gpcrs = pygtop.get_targets_by({"type": "gpcr"})
        self.assertIsInstance(gpcrs, list)
        self.assertIsInstance(gpcrs[0], Target)
        self.assertGreater(len(gpcrs), 400)
