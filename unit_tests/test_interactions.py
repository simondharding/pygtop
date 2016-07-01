from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.interactions import Interaction
import pygtop.exceptions as exceptions

class InteractionTest(TestCase):

    def setUp(self):
        self.interaction_json = {
         "interactionId": 79397,
         "targetId": 1,
         "ligandAsTargetId": 0,
         "targetSpecies": "Human",
         "primaryTarget": False,
         "targetBindingSite": "",
         "ligandId": 7191,
         "ligandContext": "",
         "endogenous": False,
         "type": "Agonist",
         "action": "Agonist",
         "actionComment": "",
         "selectivity": "None",
         "concentrationRange": "-",
         "affinity": "7.2",
         "affinityType": "pKi",
         "originalAffinity": "6x10<sup>-8</sup>",
         "originalAffinityType": "Ki",
         "originalAffinityRelation": "",
         "assayDescription": "",
         "assayConditions": "",
         "useDependent": False,
         "voltageDependent": False,
         "voltage": "-",
         "physiologicalVoltage": False,
         "conciseView": False,
         "dataPoints": [],
         "refs": []
        }



class InteractionCreationTests(InteractionTest):

    def test_can_create_interaction(self):
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction.json_data, self.interaction_json)
        self.assertEqual(interaction._interaction_id, 79397)
        self.assertEqual(interaction._ligand_id, 7191)
        self.assertEqual(interaction._target_id, 1)
        self.assertEqual(interaction._species, "Human")
        self.assertEqual(interaction._primary_target, False)
        self.assertEqual(interaction._endogenous, False)
        self.assertEqual(interaction._interaction_type, "Agonist")
        self.assertEqual(interaction._action, "Agonist")
        self.assertEqual(interaction._affinity_low, 7.2)
        self.assertEqual(interaction._affinity_high, 7.2)
        self.assertEqual(interaction._affinity_type, "pKi")


    def test_can_process_affinity_range(self):
        self.interaction_json["affinity"] = "9.4 &ndash; 10.3"
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction._affinity_low, 9.4)
        self.assertEqual(interaction._affinity_high, 10.3)


    def test_can_process_affinity_range_with_median(self):
        self.interaction_json["affinity"] = "7.7 &ndash; 9.0 (median: 8.6)"
        interaction = Interaction(self.interaction_json)
        self.assertEqual(interaction._affinity_low, 7.7)
        self.assertEqual(interaction._affinity_high, 9.0)


    def test_interaction_repr(self):
        interaction = Interaction(self.interaction_json)
        self.assertEqual(str(interaction), "<Interaction (7191 --> Human 1)>")



class InteractionPropertyTests(InteractionTest):

    def test_basic_property_methods(self):
        interaction = Interaction(self.interaction_json)
        self.assertIs(interaction._interaction_id, interaction.interaction_id())
        self.assertIs(interaction._ligand_id, interaction.ligand_id())
        self.assertIs(interaction._target_id, interaction.target_id())
        self.assertIs(interaction._species, interaction.species())
        self.assertIs(interaction._primary_target, interaction.primary_target())
        self.assertIs(interaction._endogenous, interaction.endogenous())
        self.assertIs(interaction._interaction_type, interaction.interaction_type())
        self.assertIs(interaction._action, interaction.action())
        self.assertIs(interaction._affinity_low, interaction.affinity_low())
        self.assertIs(interaction._affinity_high, interaction.affinity_high())
        self.assertIs(interaction._affinity_type, interaction.affinity_type())


'''import unittest
import json
import sys
sys.path.append(".")
import pygtop
from pygtop.interactions import *
from pygtop.ligands import *
from pygtop.targets import *
from pygtop.gtop import *
from pygtop.exceptions import *

string = str

class InteractionTest(unittest.TestCase):

    def check_interaction_properties(self, interaction):
        str(interaction)
        self.assertIsInstance(interaction, Interaction)
        self.assertIsInstance(interaction.interaction_id, int)
        self.assertIsInstance(interaction._ligand_id, int)
        self.assertIsInstance(interaction._target_id, int)
        self.assertIsInstance(interaction.species, string)
        if interaction.affinity_value: self.assertIsInstance(
         interaction.affinity_range, tuple
        )
        for val in interaction.affinity_range:
            self.assertIsInstance(val, float)
        if interaction.affinity_value:
            self.assertIsInstance(interaction.affinity_value, float)
        if interaction.affinity_value:
            self.assertIsInstance(interaction.affinity_type, string)
        self.assertIsInstance(interaction.type, string)
        self.assertIsInstance(interaction.action, string)
        self.assertIsInstance(interaction.ligand_primary_target, bool)
        self.assertIsInstance(interaction.is_voltage_dependent, bool)
        if interaction.voltage_value:
            self.assertIsInstance(interaction.voltage_value, float)
        else:
            self.assertEqual(interaction.voltage_value, None)
        self.assertIsInstance(interaction.references, list)
        for ref in interaction.references:
            self.assertIsInstance(ref, string)
            self.assertEqual(ref[0], "(")


    def test_can_make_interaction(self):
        interaction_json = get_json_from_gtop("/targets/485/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)
        interaction_json = get_json_from_gtop("/targets/64/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)
        interaction_json = get_json_from_gtop("/targets/381/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)


    def test_interaction_can_get_ligand(self):
        interaction_json = get_json_from_gtop("/targets/1/interactions")[0]
        interaction = Interaction(interaction_json)
        ligand = interaction.get_ligand()
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.name, "frovatriptan")

        interaction._ligand_id = 0
        self.assertEqual(None, interaction.get_ligand())


    def test_interaction_can_get_target(self):
        interaction_json = get_json_from_gtop("/targets/1/interactions")[0]
        interaction = Interaction(interaction_json)
        target = interaction.get_target()
        self.assertIsInstance(target, Target)
        self.assertEqual(target.name, "5-HT<sub>1A</sub> receptor")

        species_target = interaction.get_species_target()
        self.assertIsInstance(species_target, SpeciesTarget)
        self.assertEqual(species_target.target.name, "5-HT<sub>1A</sub> receptor")

        interaction._target_id = 0
        self.assertEqual(None, interaction.get_target())


    def test_ligand_can_get_interactions(self):
        ligand = get_ligand_by_id(1)
        interactions = ligand.get_interactions()
        self.assertGreater(len(interactions), 0)
        for interaction in interactions:
            self.check_interaction_properties(interaction)
            self.assertEqual(interaction._ligand_id, ligand.ligand_id)


    def test_ligand_can_get_specific_interaction(self):
        ligand = get_ligand_by_id(1)
        interaction = ligand.get_interaction_by_id(1)
        self.assertEqual(interaction.interaction_id, 1)
        self.assertRaises(
         NoSuchInteractionError,
         lambda: ligand.get_interaction_by_id(2)
        )


    def test_ligand_can_get_targets(self):
        ligand = get_ligand_by_id(1)
        targets = ligand.get_targets()
        self.assertGreater(len(targets), 0)
        for target in targets:
            self.assertIsInstance(target, Target)


    def test_ligand_can_get_species_targets(self):
        ligand = get_ligand_by_id(1)
        targets = ligand.get_species_targets()
        self.assertGreater(len(targets), 0)
        for target in targets:
            self.assertIsInstance(target, SpeciesTarget)


    def test_target_can_get_interactions(self):
        target = get_target_by_id(1)
        interactions = target.get_interactions()
        self.assertGreater(len(interactions), 0)
        for interaction in interactions:
            self.check_interaction_properties(interaction)
            self.assertEqual(interaction._target_id, target.target_id)


    def test_target_can_get_specific_interaction(self):
        target = get_target_by_id(1)
        interaction = target.get_interaction_by_id(1)
        self.assertEqual(interaction.interaction_id, 1)
        self.assertRaises(
         NoSuchInteractionError,
         lambda: target.get_interaction_by_id(0)
        )


    def test_species_target_can_get_interactions(self):
        target = SpeciesTarget(1, "human")
        interactions = target.get_interactions()
        self.assertGreater(len(interactions), 0)
        for interaction in interactions:
            self.check_interaction_properties(interaction)
            self.assertEqual(interaction._target_id, target.target_id)
            self.assertEqual(interaction.species.lower(), target.species.lower())


    def test_target_can_get_ligands(self):
        target = get_target_by_id(1)
        ligands = target.get_ligands()
        self.assertGreater(len(ligands), 0)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)


    def test_interactions_between(self):
        ligand = get_ligand_by_id(1)
        target = get_target_by_id(1)
        mutual = get_interactions_between(ligand, target)
        self.assertEqual(len(mutual), 1)



class InteractionPdbs(unittest.TestCase):

    def test_interaction_can_get_gtop_pdbs(self):
        interaction = get_target_by_id(2).get_interaction_by_id(143)
        self.assertEqual(
         interaction.get_gtop_pdbs(),
         ["4IAQ"]
        )
        interaction = get_target_by_id(2).get_interaction_by_id(79398)
        self.assertEqual(
         interaction.get_gtop_pdbs(),
         []
        )


    def test_interaction_can_find_all_external_pdbs(self):
        interaction = get_target_by_id(2).get_interaction_by_id(143)
        external_pdbs = interaction.find_all_external_pdbs()
        self.assertIsInstance(external_pdbs, list)
        self.assertGreaterEqual(len(external_pdbs), 1)


    def test_interaction_can_find_all_pdbs(self):
        interaction = get_target_by_id(2).get_interaction_by_id(143)
        pdbs = interaction.find_all_pdbs()
        self.assertIsInstance(pdbs, list)
        self.assertGreaterEqual(len(pdbs), 1)






if __name__ == "__main__":
    unittest.main()'''
