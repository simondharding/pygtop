import unittest
import json
import sys
sys.path.append(".")
import pygtop
from pygtop.targets import *
from pygtop.exceptions import *

string = str

class TargetTest(unittest.TestCase):

    def check_target_basic_properties(self, target):
        str(target)
        self.assertIsInstance(target, Target)
        self.assertIsInstance(target.name, string)
        self.assertIsInstance(target.abbreviation, string)
        self.assertIsInstance(target.systematic_name, string)
        self.assertIsInstance(target.target_type, string)
        self.assertIsInstance(target._family_ids, list)
        if target._family_ids: self.assertIsInstance(target._family_ids[0], int)
        self.assertIsInstance(target._subunit_ids, list)
        if target._subunit_ids: self.assertIsInstance(target._subunit_ids[0], int)
        self.assertIsInstance(target._complex_ids, list)
        if target._complex_ids: self.assertIsInstance(target._complex_ids[0], int)


    def check_family_basic_properties(self, family):
        str(family)
        self.assertIsInstance(family, TargetFamily)
        self.assertIsInstance(family.name, string)
        self.assertIsInstance(family._target_ids, list)
        if family._target_ids: self.assertIsInstance(family._target_ids[0], int)
        self.assertIsInstance(family._parent_family_ids, list)
        if family._parent_family_ids: self.assertIsInstance(family._parent_family_ids[0], int)
        self.assertIsInstance(family._sub_family_ids, list)
        if family._sub_family_ids: self.assertIsInstance(family._sub_family_ids[0], int)



class SingleTargets(TargetTest):

    def test_can_make_target(self):
        test_json = {
         "targetId": 1,
         "name": "5-HT<sub>1A</sub> receptor",
         "abbreviation": None,
         "systematicName": None,
         "type": "GPCR",
         "familyIds": [
          1
         ],
         "subunitIds": [],
         "complexIds": []
        }
        target = Target(test_json)
        self.check_target_basic_properties(target)


    def test_can_get_target_by_id(self):
        target = get_target_by_id(100)
        self.check_target_basic_properties(target)


    def test_invalid_target_id(self):
        self.assertRaises(NoSuchTargetError, lambda: get_target_by_id(0))


    def test_can_get_subunits(self):
        target = get_target_by_id(44)
        self.check_target_basic_properties(target)
        subunits = target.get_subunits()
        self.assertGreater(len(subunits), 0)
        for subunit in subunits:
            self.assertIsInstance(subunit, Target)


    def test_can_get_complexes(self):
        target = get_target_by_id(51)
        self.check_target_basic_properties(target)
        complexes = target.get_complexes()
        self.assertGreater(len(complexes), 0)
        for complex in complexes:
            self.assertIsInstance(complex, Target)


    def test_can_get_families(self):
        target = get_target_by_id(1)
        self.check_target_basic_properties(target)
        families = target.get_families()
        self.assertGreater(len(families), 0)
        for family in families:
            self.assertIsInstance(family, TargetFamily)



class Families(TargetTest):

    def test_can_make_target(self):
        test_json = {
         "familyId": 120,
         "name": "Chloride channels",
         "targetIds": [],
         "parentFamilyIds": [
          861
         ],
         "subFamilyIds": [
          128,
          129,
          130,
          131,
          132
         ]
        }
        family = TargetFamily(test_json)
        self.check_family_basic_properties(family)


    def test_can_get_family_by_id(self):
        family = get_family_by_id(120)
        self.check_family_basic_properties(family)


    def test_invalid_target_id(self):
        self.assertRaises(NoSuchFamilyError, lambda: get_family_by_id(0))


    def test_can_get_targets(self):
        family = get_family_by_id(840)
        self.check_family_basic_properties(family)
        targets = family.get_targets()
        self.assertGreater(len(targets), 0)
        for target in targets:
            self.assertIsInstance(target, Target)


    def test_can_get_sub_families(self):
        family = get_family_by_id(283)
        self.check_family_basic_properties(family)
        sub_families = family.get_subfamilies()
        self.assertGreater(len(sub_families), 0)
        for family in sub_families:
            self.assertIsInstance(family, TargetFamily)


    def test_can_get_parent_families(self):
        family = get_family_by_id(283)
        self.check_family_basic_properties(family)
        parent_families = family.get_parent_families()
        self.assertGreater(len(parent_families), 0)
        for family in parent_families:
            self.assertIsInstance(family, TargetFamily)



if __name__ == "__main__":
    unittest.main()
