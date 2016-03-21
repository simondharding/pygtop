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



if __name__ == "__main__":
    unittest.main()
