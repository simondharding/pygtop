import unittest
import json
import sys
sys.path.append(".")
import pygtop
from pygtop.ligands import *
from pygtop.exceptions import *

string = str if sys.version_info == 3 else unicode

class LigandTest(unittest.TestCase):

    def check_ligand_basic_properties(self, ligand):
        self.assertIsInstance(ligand, Ligand)
        self.assertIsInstance(ligand.name, string)
        self.assertIsInstance(ligand.abbreviation, string)
        self.assertIsInstance(ligand.inn, string)
        if ligand.species: self.assertIsInstance(ligand.species, string)
        self.assertIsInstance(ligand.ligand_type, string)
        self.assertIsInstance(ligand.radioactive, bool)
        self.assertIsInstance(ligand.labelled, bool)
        self.assertIsInstance(ligand.approved, bool)
        self.assertIsInstance(ligand.withdrawn, bool)
        self.assertIsInstance(ligand.approval_source, string)
        self.assertIsInstance(ligand.subunit_ids, list)
        if ligand.subunit_ids: self.assertIsInstance(ligand.subunit_ids[0], int)
        self.assertIsInstance(ligand.complex_ids, list)
        if ligand.complex_ids: self.assertIsInstance(ligand.complex_ids[0], int)
        self.assertIsInstance(ligand.prodrug_ids, list)
        if ligand.prodrug_ids: self.assertIsInstance(ligand.prodrug_ids[0], int)
        self.assertIsInstance(ligand.active_drug_ids, list)
        if ligand.active_drug_ids: self.assertIsInstance(ligand.active_drug_ids[0], int)


    def check_ligand_structural_properties(self, ligand):
        if ligand.iupac_name:
            self.assertIsInstance(ligand.iupac_name, string)
        if ligand.smiles:
            self.assertIsInstance(ligand.smiles, string)
        if ligand.inchi:
            self.assertIsInstance(ligand.inchi, string)
        if ligand.inchi_key:
            self.assertIsInstance(ligand.inchi_key, string)
        if ligand.one_letter_sequence:
            self.assertIsInstance(ligand.one_letter_sequence, string)
        if ligand.three_letter_sequence:
            self.assertIsInstance(ligand.three_letter_sequence, string)
        if ligand.post_translational_modifications:
            self.assertIsInstance(ligand.post_translational_modifications, string)
        if ligand.chemical_modifications:
            self.assertIsInstance(ligand.chemical_modifications, string)


    def check_ligand_molecular_properties(self, ligand):
        if ligand.hydrogen_bond_acceptors:
            self.assertIsInstance(ligand.hydrogen_bond_acceptors, int)
        if ligand.hydrogen_bond_donors:
            self.assertIsInstance(ligand.hydrogen_bond_donors, int)
        if ligand.rotatable_bonds:
            self.assertIsInstance(ligand.rotatable_bonds, int)
        if ligand.topological_polar_surface_area:
            self.assertIsInstance(ligand.topological_polar_surface_area, float)
        if ligand.molecular_weight:
            self.assertIsInstance(ligand.molecular_weight, float)
        if ligand.log_p:
            self.assertIsInstance(ligand.log_p, float)
        if ligand.lipinksi_rules_broken:
            self.assertIsInstance(ligand.lipinksi_rules_broken, int)


    def check_ligand_database_properties(self, ligand):
        self.assertIsInstance(ligand.database_links, list)
        for link in ligand.database_links:
            self.assertIsInstance(link, pygtop.DatabaseLink)
            if link.accession: self.assertIsInstance(link.accession, string)
            if link.database: self.assertIsInstance(link.database, string)
            if link.url: self.assertIsInstance(link.url, string)
            if link.species: self.assertIsInstance(link.species, string)


    def check_ligand_synonym_properties(self, ligand):
        self.assertIsInstance(ligand.synonyms, list)
        for synonym in ligand.synonyms:
            self.assertIsInstance(synonym, string)
            self.assertGreater(len(synonym), 0)


    def check_ligand_comment_properties(self, ligand):
        self.assertIsInstance(ligand.general_comments, string)
        self.assertIsInstance(ligand.bioactivity_comments, string)
        self.assertIsInstance(ligand.clinical_use_comments, string)
        self.assertIsInstance(ligand.mechanism_of_action_comments, string)
        self.assertIsInstance(ligand.absorption_and_distribution_comments, string)
        self.assertIsInstance(ligand.metabolism_comments, string)
        self.assertIsInstance(ligand.elimination_comments, string)
        self.assertIsInstance(ligand.population_pharmacokinetics_comments, string)
        self.assertIsInstance(ligand.organ_function_impairments_comments, string)
        self.assertIsInstance(ligand.mutations_and_pathophysiology_comments, string)


    def check_ligand_precursor_properties(self, ligand):
        self.assertIsInstance(ligand.precursors, list)
        for precursor in ligand.precursors:
            self.assertIsInstance(precursor, pygtop.Precursor)
            self.assertIsInstance(precursor.precursor_id, int)
            self.assertIsInstance(precursor.gene_symbol, string)
            self.assertIsInstance(precursor.gene_name, string)
            self.assertIsInstance(precursor.official_gene_id, string)
            self.assertIsInstance(precursor.protein_name, string)
            self.assertIsInstance(precursor.species, string)
            self.assertIsInstance(precursor.synonyms, list)
            for synonym in precursor.synonyms:
                self.assertIsInstance(synonym, string)
                self.assertGreater(len(synonym), 0)



class SingleLigands(LigandTest):

    def test_can_get_single_ligand(self):
        ligand = get_ligand_by_id(1)
        self.assertIsInstance(ligand, Ligand)
        if sys.version_info[0] == 2:
            self.assertRegexpMatches(ligand.__repr__(), r'<.+>')
        else:
            self.assertRegex(ligand.__repr__(), r'<.+>')


    def test_invalid_ligand_exception(self):
        self.assertRaises(NoSuchLigandError, lambda: get_ligand_by_id(0))


    def test_basic_ligand_properties(self):
        ligand = get_ligand_by_id(4890)
        self.check_ligand_basic_properties(ligand)


    def test_structural_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_structural_properties()
        self.check_ligand_structural_properties(ligand)


    def test_invalid_attribute_access(self):
        ligand = get_ligand_by_id(4890)
        self.assertRaises(PropertyNotRequestedYetError, lambda: ligand.smiles)
        self.assertRaises(AttributeError, lambda: ligand.xxx)
        ligand.request_structural_properties()
        self.assertIsInstance(ligand.smiles, string)
        self.assertRaises(AttributeError, lambda: ligand.xxx)


    def test_structural_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_structural_properties()
        self.check_ligand_structural_properties(ligand)


    def test_molecular_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_molecular_properties()
        self.check_ligand_molecular_properties(ligand)


    def test_database_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_database_properties()
        self.check_ligand_database_properties(ligand)


    def test_comment_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_comment_properties()
        self.check_ligand_comment_properties(ligand)


    def test_precursor_properties(self):
        ligand = get_ligand_by_id(4890)
        ligand.request_precursor_properties()
        self.check_ligand_precursor_properties(ligand)



class MultiLigands(LigandTest):

    def test_can_get_all_ligands(self):
        ligands = get_all_ligands()
        self.assertIsInstance(ligands, list)
        self.assertGreater(len(ligands), 5000)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)


    def test_can_get_ligand_by_name(self):
        ligand = pygtop.get_ligand_by_name("APIGENIN")
        self.assertIsInstance(ligand, Ligand)
        self.assertRaises(
         NoSuchLigandError,
         lambda: pygtop.get_ligand_by_name("paracetamoxyfrusebendroneomycin")
        )


    def test_can_search_ligands(self):
        criteria = {
         "type": "Approved",
         "molWeightGt": 50,
         "molWeightLt": 200
        }
        ligands = pygtop.get_ligands_by(criteria)
        self.assertIsInstance(ligands, list)
        self.assertEqual(len(ligands), 104)


    def test_can_get_random_ligand(self):
        ligand = pygtop.get_random_ligand()
        self.assertIsInstance(ligand, Ligand)
        ligand = pygtop.get_random_ligand(ligand_type="peptide")
        self.assertIsInstance(ligand, Ligand)
        self.assertEqual(ligand.ligand_type.lower(), "peptide")
        self.assertRaises(
         NoSuchTypeError,
         lambda: pygtop.get_random_ligand(ligand_type="xxx")
        )





if __name__ == "__main__":
    unittest.main()
