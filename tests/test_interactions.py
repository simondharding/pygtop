import unittest
import json
import sys
sys.path.append(".")
import pygtop
from pygtop.interactions import *
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
        self.assertIsInstance(interaction.affinity_range, tuple)
        for val in interaction.affinity_range:
            self.assertIsInstance(val, float)
        self.assertIsInstance(interaction.affinity_value, float)
        self.assertIsInstance(interaction.affinity_type, str)
        self.assertIsInstance(interaction.type, str)
        self.assertIsInstance(interaction.action, str)
        self.assertIsInstance(interaction.ligand_primary_target, bool)
        self.assertIsInstance(interaction.is_voltage_dependent, bool)
        if interaction.is_voltage_dependent:
            self.assertIsInstance(interaction.voltage, float)
        else:
            self.assertEqual(interaction.voltage, None)


    def test_can_make_interaction(self):
        interaction_json = get_json_from_gtop("/targets/485/interactions")[0]
        interaction = Interaction(interaction_json)
        self.check_interaction_properties(interaction)


if __name__ == "__main__":
    unittest.main()
