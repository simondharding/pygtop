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


    def check_target_database_properties(self, target):
        self.assertIsInstance(target.database_links, list)
        for link in target.database_links:
            self.assertIsInstance(link, pygtop.DatabaseLink)
            if link.accession: self.assertIsInstance(link.accession, string)
            if link.database: self.assertIsInstance(link.database, string)
            if link.url: self.assertIsInstance(link.url, string)
            if link.species: self.assertIsInstance(link.species, string)


    def check_target_synonym_properties(self, target):
        self.assertIsInstance(target.synonyms, list)
        for synonym in target.synonyms:
            self.assertIsInstance(synonym, string)
            self.assertGreater(len(synonym), 0)


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


    def test_database_properties(self):
        target = get_target_by_id(1)
        target.request_database_properties()
        self.check_target_database_properties(target)


    def test_synonym_properties(self):
        target = get_target_by_id(1)
        target.request_synonym_properties()
        self.check_target_synonym_properties(target)


    def test_all_properties(self):
        target = get_target_by_id(1)
        target.request_all_properties()
        self.check_target_database_properties(target)targets/485/interactions
        self.check_target_synonym_properties(target)


    def test_invalid_attribute_access(self):
        target = get_target_by_id(1)
        self.assertRaises(PropertyNotRequestedYetError, lambda: target.database_links)
        self.assertRaises(AttributeError, lambda: target.xxx)
        target.request_database_properties()
        self.assertIsInstance(target.database_links, list)
        self.assertRaises(AttributeError, lambda: target.xxx)


    def test_species_specific(self):
        ppt = SpeciesTarget(1, "human")
        str(ppt)
        self.assertIsInstance(ppt, SpeciesTarget)
        self.assertIsInstance(ppt.target, Target)
        self.assertEqual(1, ppt.target.target_id)


    def test_species_invalid_id(self):
        self.assertRaises(NoSuchTargetError, lambda: SpeciesTarget(0, "human"))


    def test_species_database_links(self):
        ppt = SpeciesTarget(1, "human")
        self.assertRaises(PropertyNotRequestedYetError, lambda: ppt.database_links)
        ppt.request_database_properties()
        self.assertIsInstance(ppt.database_links, list)
        for link in ppt.database_links:
            self.assertIsInstance(link, DatabaseLink)
            self.assertEqual(link.species.lower(), "human")



class MultiTargets(TargetTest):

    def test_can_get_all_targets(self):
        targets = get_all_targets()
        self.assertIsInstance(targets, list)
        self.assertGreater(len(targets), 2000)
        for target in targets:
            self.assertIsInstance(target, Target)


    def test_can_get_random_target(self):
        target = pygtop.get_random_target()
        self.assertIsInstance(target, Target)
        target = pygtop.get_random_target(target_type="GPCR")
        self.assertIsInstance(target, Target)
        self.assertEqual(target.target_type.lower(), "gpcr")
        self.assertRaises(
         NoSuchTypeError,
         lambda: pygtop.get_random_target(target_type="xxx")
        )


    def test_can_get_target_by_name(self):
        target = pygtop.get_target_by_name("ccr5")
        self.assertIsInstance(target, Target)
        self.assertRaises(
         NoSuchTargetError,
         lambda: pygtop.get_target_by_name("made up target")
        )


    def test_can_search_targets(self):
        criteria = {
         "type": "VGIC",
        }
        targets = pygtop.get_targets_by(criteria)
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), 145)



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


    def test_can_get_parent_families(self):
        family = get_family_by_id(283)
        self.check_family_basic_properties(family)
        parent_families = family.get_parent_families()
        self.assertGreater(len(parent_families), 0)
        for family in parent_families:
            self.assertIsInstance(family, TargetFamily)



class MultiFamilies(TargetTest):

    def test_can_get_all_families(self):
        families = get_all_families()
        self.assertIsInstance(families, list)
        self.assertGreater(len(families), 100)
        for family in families:
            self.assertIsInstance(family, TargetFamily)


    def test_can_get_random_family(self):
        family = pygtop.get_random_family()
        self.assertIsInstance(family, TargetFamily)



if __name__ == "__main__":
    unittest.main()
