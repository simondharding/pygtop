from unittest import TestCase
import pygtop

class InteractionPropertyTests(TestCase):

    def test_can_get_gtop_pdbs(self):
        target = pygtop.get_target_by_id(2)
        interaction = target.get_interaction_by_id(143)
        pdbs = interaction.gtop_pdbs()
        self.assertIn("4IAQ", pdbs)


    def test_can_get_external_pdbs(self):
        target = pygtop.get_target_by_id(2)
        interaction = target.get_interaction_by_id(143)
        pdbs = interaction.all_external_pdbs()
        self.assertIn("4IAQ", pdbs)


    def test_can_get_all_pdbs(self):
        target = pygtop.get_target_by_id(2)
        interaction = target.get_interaction_by_id(143)
        pdbs = interaction.all_pdbs()
        self.assertIn("4IAQ", pdbs)
