import unittest
import sys
sys.path.append(".")
sys.path.append("..")
import pygtop
import pygtop.exceptions


class LigandAccess(unittest.TestCase):
    """This is the test for version 0.1.

    In this version, the user can access a ligand by ID, and access most of the
    properties accessible from the API. They cannot currently access interaction,
     PDB, rank order, complex, subunit or image information.

    They can also use the API ligand searcher for basic attributes, but not
    SMILES queries. This is extended to allow for getting a ligand by name."""

    def check_ligand_basic_properties(self, ligand):
        self.assertIsInstance(ligand, pygtop.Ligand)
        self.assertIsInstance(ligand.name, str)
        self.assertIsInstance(ligand.abbreviation, str)
        self.assertIsInstance(ligand.inn, str)
        if ligand.species: self.assertIsInstance(ligand.species, str)
        self.assertIsInstance(ligand.type, str)
        self.assertIsInstance(ligand.radioactive, bool)
        self.assertIsInstance(ligand.labelled, bool)
        self.assertIsInstance(ligand.approved, bool)
        self.assertIsInstance(ligand.withdrawn, bool)
        self.assertIsInstance(ligand.approval_source, str)
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
            self.assertIsInstance(ligand.iupac_name, str)
        if ligand.smiles:
            self.assertIsInstance(ligand.smiles, str)
        if ligand.inchi:
            self.assertIsInstance(ligand.inchi, str)
        if ligand.inchi_key:
            self.assertIsInstance(ligand.inchi_key, str)
        if ligand.one_letter_sequence:
            self.assertIsInstance(ligand.one_letter_sequence, str)
        if ligand.three_letter_sequence:
            self.assertIsInstance(ligand.three_letter_sequence, str)
        if ligand.post_translational_modifications:
            self.assertIsInstance(ligand.post_translational_modifications, str)
        if ligand.chemical_modifications:
            self.assertIsInstance(ligand.chemical_modifications, str)


    def check_ligand_molecular_properties(self, ligand):
        self.assertIsInstance(ligand.hydrogen_bond_acceptors, int)
        self.assertIsInstance(ligand.hydrogen_bond_donors, int)
        self.assertIsInstance(ligand.rotatable_bonds, int)
        self.assertIsInstance(ligand.topological_polar_surface_area, float)
        self.assertIsInstance(ligand.molecular_weight, float)
        self.assertIsInstance(ligand.log_p, float)
        self.assertIsInstance(ligand.lipinksi_rules_broken, int)


    def check_ligand_database_properties(self, ligand):
        self.assertIsInstance(ligand.database_links, list)
        for link in ligand.database_links:
            self.assertIsInstance(link, pygtop.DatabaseLink)
            if link.accession: self.assertIsInstance(link.accession, str)
            if link.database: self.assertIsInstance(link.database, str)
            if link.url: self.assertIsInstance(link.url, str)
            if link.species: self.assertIsInstance(link.species, str)


    def check_ligand_synonym_properties(self, ligand):
        self.assertIsInstance(ligand.synonyms, list)
        for synonym in ligand.synonyms:
            self.assertIsInstance(synonym, str)
            self.assertGreater(len(synonym), 0)


    def check_ligand_comment_properties(self, ligand):
        self.assertIsInstance(ligand.general_comments, str)
        self.assertIsInstance(ligand.bioactivity_comments, str)
        self.assertIsInstance(ligand.clinical_use_comments, str)
        self.assertIsInstance(ligand.mechanism_of_action_comments, str)
        self.assertIsInstance(ligand.absorption_and_distribution_comments, str)
        self.assertIsInstance(ligand.metabolism_comments, str)
        self.assertIsInstance(ligand.elimination_comments, str)
        self.assertIsInstance(ligand.population_pharmacokinetics_comments, str)
        self.assertIsInstance(ligand.organ_function_impairments_comments, str)
        self.assertIsInstance(ligand.mutations_and_pathophysiology_comments, str)


    def check_ligand_precursor_properties(self, ligand):
        self.assertIsInstance(ligand.precursors, list)
        for precursor in ligand.precursors:
            self.assertIsInstance(precursor, pygtop.Precursor)
            self.assertIsInstance(precursor.precursor_id, int)
            self.assertIsInstance(precursor.gene_symbol, str)
            self.assertIsInstance(precursor.gene_name)
            self.assertIsInstance(precursor.official_gene_id, str)
            self.assertIsInstance(precursor.protein_name, str)
            self.assertIsInstance(precursor.species, str)
            self.assertIsInstance(precursor.synonyms, list)
            for synonym in precursor.synonyms:
                self.assertIsInstance(synonym, str)
                self.assertGreater(len(synonym), 0)


    def check_ligand_complete(self, ligand):
        self.check_ligand_basic_properties(ligand)
        ligand.get_all_properties()
        self.check_ligand_structural_properties(ligand)
        self.check_ligand_molecular_properties(ligand)
        self.check_ligand_database_properties(ligand)
        self.check_ligand_synonym_properties(ligand)
        self.check_ligand_comment_properties(ligand)
        self.check_ligand_precursor_properties(ligand)


    def test_can_get_single_ligand(self):
        # The user gets a ligand by ID
        ligand = pygtop.get_ligand_by_id(1)

        # The user checks its basic properties
        self.check_ligand_basic_properties(ligand)

        # The user tries to get a ligand with a false ID
        self.assertRaises(
         pygtop.exceptions.NoSuchLigandError,
         pygtop.get_ligand_by_id,
         10000000
        )

        # The user decides to get the structural information for the ligand
        ligand.get_structural_properties()
        self.check_ligand_structural_properties(ligand)

        # The user tries to access molecular properties
        self.assertRaises(pygtop.PropertyNotRequestedYetError, lambda: ligand.rotatable_bonds)

        # The user decides to get molecular properties for the ligand
        ligand.get_molecular_properties()
        self.check_ligand_molecular_properties(ligand)

        # The user decides to get database properties for the ligand
        ligand.get_database_properties()
        self.check_ligand_database_properties(ligand)

        # The user decides to get synonym properties for the ligand
        ligand.get_synonym_properties()
        self.check_ligand_synonym_properties(ligand)

        # The user decides to get comment properties for the ligand
        ligand.get_comment_properties()
        self.check_ligand_comment_properties(ligand)

        # The user decides to get precursor properties for the ligand
        ligand.get_precursor_properties()
        self.check_ligand_precursor_properties(ligand)

        # The user gets a random ligand
        pygtop.get_random_ligand()
        self.check_ligand_complete(ligand)

        # The user decides to get a random peptide ligand
        pygtop.get_random_ligand(ligand_type="peptide")
        self.check_ligand_complete(ligand)



    def test_can_get_all_ligands(self):

        # The user gets all ligands
        ligands = pygtop.get_all_ligands()
        self.assertIsInstance(ligands, list)
        self.assertGreater(len(ligands), 5000)
        for ligand in ligands:
            self.assertIsInstance(ligand, pygtop.Ligand)

        # The user searches for specific ligands
        criteria = {
         "type": "Approved",
         "molWeightGt": 50,
         "molWeightLt": 200
        }
        ligands = pygtop.get_ligands_by(criteria)
        self.assertIsInstance(ligands, list)
        self.assertEqual(len(ligands), 104)
        for ligand in ligands:
            self.assertIsInstance(ligand, pygtop.Ligand)

        # The user looks for a ligand with a certain name
        ligand = pygtop.get_ligand_by_name("APIGENIN")
        self.assertIsInstance(ligand, pygtop.Ligand)
        self.check_ligand_complete(ligand)

        # The user looks for a ligand with a name that does not exist
        ligand = pygtop.get_ligand_by_name("paracetamoxyfrusebendroneomycin")
        self.assertEqual(ligand, None)


if __name__ == "__main__":
    unittest.main()
