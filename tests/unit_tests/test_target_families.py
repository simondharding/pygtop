from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.targets import TargetFamily, get_target_family_by_id
from pygtop.targets import get_all_target_families, Target
import pygtop.exceptions as exceptions

class TargetFamilyTest(TestCase):

    def setUp(self):
        self.family_json = {
         "familyId": 1,
         "name": "5-Hydroxytryptamine receptors",
         "targetIds": [1, 2, 5],
         "parentFamilyIds": [694],
         "subFamilyIds": [9]
        }

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



class TargetFamilyreationTests(TargetFamilyTest):

    def test_can_create_target_family(self):
        family = TargetFamily(self.family_json)
        self.assertEqual(family.json_data, self.family_json)
        self.assertEqual(family._family_id, 1)
        self.assertEqual(family._name, "5-Hydroxytryptamine receptors")
        self.assertEqual(family._target_ids, [1, 2, 5])
        self.assertEqual(family._parent_family_ids, [694])
        self.assertEqual(family._sub_family_ids, [9])


    def test_target_family_repr(self):
        family = TargetFamily(self.family_json)
        self.assertEqual(str(family), "<'5-Hydroxytryptamine receptors' TargetFamily>")



class TargetFamilyPropertyTests(TargetFamilyTest):

    def test_basic_property_methods(self):
        family = TargetFamily(self.family_json)
        self.assertIs(family._family_id, family.family_id())
        self.assertIs(family._name, family.name())
        self.assertIs(family._target_ids, family.target_ids())
        self.assertIs(family._parent_family_ids, family.parent_family_ids())
        self.assertIs(family._sub_family_ids, family.sub_family_ids())


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_targets(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        family = TargetFamily(self.family_json)
        targets = family.targets()
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), len(self.family_json["targetIds"]))
        for target in targets:
            self.assertIsInstance(target, Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_parent_families(self, mock_json_retriever):
        mock_json_retriever.return_value = self.family_json
        family = TargetFamily(self.family_json)
        parents = family.parent_families()
        self.assertIsInstance(parents, list)
        self.assertEqual(len(parents), len(self.family_json["parentFamilyIds"]))
        for parent in parents:
            self.assertIsInstance(parent, TargetFamily)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_sub_families(self, mock_json_retriever):
        mock_json_retriever.return_value = self.family_json
        family = TargetFamily(self.family_json)
        children = family.sub_families()
        self.assertIsInstance(children, list)
        self.assertEqual(len(children), len(self.family_json["subFamilyIds"]))
        for child in children:
            self.assertIsInstance(child, TargetFamily)



class TargetFamilyAccessTests(TargetFamilyTest):

    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_family_by_id(self, mock_json_retriever):
        mock_json_retriever.return_value = self.family_json
        target_family = get_target_family_by_id(1)
        self.assertIsInstance(target_family, TargetFamily)
        self.assertEqual(target_family.name(), self.family_json["name"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_family_id_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        with self.assertRaises(exceptions.NoSuchTargetFamilyError):
            target_family = get_target_family_by_id(1)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_family_id_must_be_int(self, mock_json_retriever):
        mock_json_retriever.return_value = self.family_json
        with self.assertRaises(TypeError):
            target_family = get_target_family_by_id("1")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_all_target_families(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.family_json, self.family_json]
        target_families = get_all_target_families()
        self.assertIsInstance(target_families, list)
        self.assertEqual(len(target_families), 2)
        self.assertIsInstance(target_families[0], TargetFamily)
        self.assertIsInstance(target_families[1], TargetFamily)
