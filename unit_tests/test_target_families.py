from unittest import TestCase
from pygtop.targets import TargetFamily


class TargetFamilyTest(TestCase):

    def setUp(self):
        self.family_json = {
         "familyId": 1,
         "name": "5-Hydroxytryptamine receptors",
         "targetIds": [1, 2, 5],
         "parentFamilyIds": [694],
         "subFamilyIds": [9]
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
