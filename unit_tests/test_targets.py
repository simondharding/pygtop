from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.targets import Target, get_target_by_id, get_all_targets, get_targets_by
from pygtop.targets import get_target_by_name, TargetFamily
import pygtop.exceptions as exceptions
from pygtop.shared import DatabaseLink

class TargetTest(TestCase):

    def setUp(self):
        self.target_json = {
         "targetId": 1,
         "name": "5-HT<sub>1A</sub> receptor",
         "abbreviation": "5-HT",
         "systematicName": None,
         "type": "GPCR",
         "familyIds": [1],
         "subunitIds": [2, 3],
         "complexIds": [4]
        }



class TargetCreationTests(TargetTest):

    def test_can_create_target(self):
        target = Target(self.target_json)
        self.assertEqual(target.json_data, self.target_json)
        self.assertEqual(target._target_id, 1)
        self.assertEqual(target._name, "5-HT<sub>1A</sub> receptor")
        self.assertEqual(target._abbreviation, "5-HT")
        self.assertEqual(target._systematic_name, None)
        self.assertEqual(target._target_type, "GPCR")
        self.assertEqual(target._family_ids, [1])
        self.assertEqual(target._subunit_ids, [2, 3])
        self.assertEqual(target._complex_ids, [4])


    def test_target_repr(self):
        target = Target(self.target_json)
        self.assertEqual(str(target), "<Target 1 (5-HT<sub>1A</sub> receptor)>")



class TargetPropertyTests(TargetTest):

    def test_basic_property_methods(self):
        target = Target(self.target_json)
        self.assertIs(target._target_id, target.target_id())
        self.assertIs(target._name, target.name())
        self.assertIs(target._abbreviation, target.abbreviation())
        self.assertIs(target._systematic_name, target.systematic_name())
        self.assertIs(target._target_type, target.target_type())
        self.assertIs(target._family_ids, target.family_ids())
        self.assertIs(target._subunit_ids, target.subunit_ids())
        self.assertIs(target._complex_ids, target.complex_ids())


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_synonym_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = [
         {"name": "ADRBRL1", "refs": []},
         {"name": "5-HT1A", "refs": []}
        ]
        target = Target(self.target_json)

        self.assertEqual(target.synonyms(), ["ADRBRL1", "5-HT1A"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_synonym_properties_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)

        self.assertEqual(target.synonyms(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_database_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = [
         {
          "accession": "10576",
          "database": "ChEMBL Target",
          "url": "http://www.ebi.ac.uk/chembldb/index.php/target/inspect/10576",
          "species": "Rat"
         },
         {
          "accession": "11863",
          "database": "ChEMBL Target",
          "url": "http://www.ebi.ac.uk/chembldb/index.php/target/inspect/11863",
          "species": "Mouse"
         }
        ]
        target = Target(self.target_json)

        self.assertEqual(len(target.database_links()), 2)
        self.assertIsInstance(target.database_links()[0], DatabaseLink)
        self.assertIsInstance(target.database_links()[1], DatabaseLink)
        self.assertEqual(target.database_links()[0].accession, "10576")
        self.assertEqual(target.database_links()[1].accession, "11863")
        self.assertEqual(target.database_links()[0].species, "Rat")
        self.assertEqual(target.database_links()[1].species, "Mouse")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_database_properties_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)

        self.assertEqual(target.database_links(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_families(self, mock_json_retriever):
        mock_json_retriever.return_value = {
         "familyId": 1,
         "name": "5-Hydroxytryptamine receptors",
         "targetIds": [1, 2, 5],
         "parentFamilyIds": [694],
         "subFamilyIds": [9]
        }
        target = Target(self.target_json)
        families = target.families()
        self.assertIsInstance(families, list)
        self.assertEqual(len(families), len(self.target_json["familyIds"]))
        for family in families:
            self.assertIsInstance(family, TargetFamily)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_subunits(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        target = Target(self.target_json)
        subunits = target.subunits()
        self.assertIsInstance(subunits, list)
        self.assertEqual(len(subunits), len(self.target_json["subunitIds"]))
        for subunit in subunits:
            self.assertIsInstance(subunit, Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_complexes(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        target = Target(self.target_json)
        complexes = target.complexes()
        self.assertIsInstance(complexes, list)
        self.assertEqual(len(complexes), len(self.target_json["complexIds"]))
        for complex_ in complexes:
            self.assertIsInstance(complex_, Target)



class TargetAccessTests(TargetTest):

    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_by_id(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        target = get_target_by_id(1)
        self.assertIsInstance(target, Target)
        self.assertEqual(target.name(), self.target_json["name"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_id_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        with self.assertRaises(exceptions.NoSuchTargetError):
            target = get_target_by_id(1)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_id_must_be_int(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        with self.assertRaises(TypeError):
            target = get_target_by_id("1")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_all_targets(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json, self.target_json]
        targets = get_all_targets()
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), 2)
        self.assertIsInstance(targets[0], Target)
        self.assertIsInstance(targets[1], Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_by_query(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json, self.target_json]
        targets = get_targets_by({"type": "gpcr"})
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), 2)
        self.assertIsInstance(targets[0], Target)
        self.assertIsInstance(targets[1], Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_query_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        targets = get_targets_by({"type": "gcpr"})
        self.assertEqual(targets, [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_query_must_be_dict(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json, self.target_json]
        with self.assertRaises(TypeError):
            target = get_targets_by("astring")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_by_name(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json]
        target = get_target_by_name("actin")
        self.assertIsInstance(target, Target)
        self.assertEqual(target.target_id(), self.target_json["targetId"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_name_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        with self.assertRaises(exceptions.NoSuchTargetError):
            target = get_target_by_name("fauxprot")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_name_must_be_str(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json]
        with self.assertRaises(TypeError):
            target = get_target_by_name(1)

'''import unittest
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
        if target.abbreviation: self.assertIsInstance(target.abbreviation, string)
        if target.systematic_name: self.assertIsInstance(target.systematic_name, string)
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
        self.check_target_database_properties(target)
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



class TargetPdbs(unittest.TestCase):

    def test_target_can_get_gtop_pdbs(self):
        target = get_target_by_id(206)
        self.assertEqual(
         target.get_gtop_pdbs(),
         ["2JXA", "2JX9", "4DLQ"]
        )
        target = get_target_by_id(1)
        self.assertEqual(
         target.get_gtop_pdbs(),
         []
        )


    def test_species_target_can_get_gtop_pdbs(self):
        target = SpeciesTarget(206, "rat")
        self.assertEqual(
         target.get_gtop_pdbs(),
         ["4DLQ"]
        )
        target = SpeciesTarget(1, "human")
        self.assertEqual(
         target.get_gtop_pdbs(),
         []
        )


    def test_target_can_find_pdbs_by_uniprot(self):
        target = get_target_by_id(2)
        uniprot_pdbs = target.find_pdbs_by_uniprot_accession()
        self.assertIsInstance(uniprot_pdbs, list)
        self.assertGreaterEqual(len(uniprot_pdbs), 1)
        self.assertNotIn(":", "".join(uniprot_pdbs))


    def test_target_can_find_all_pdbs(self):
        target = get_target_by_id(2)
        pdbs = target.find_all_pdbs()
        self.assertIsInstance(pdbs, list)
        self.assertGreaterEqual(len(pdbs), 1)




if __name__ == "__main__":
    unittest.main()
'''
