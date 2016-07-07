from unittest import TestCase
import pygtop

class AllLigandsTest(TestCase):

    def test_all_ligands(self):
        structure = False
        molecular = False
        synonyms = False
        comments = False
        database = False

        ligands = pygtop.get_all_ligands()
        for ligand in ligands:
            ligand_iupac = ligand.iupac_name()
            ligand_mass = ligand.molecular_weight()
            ligand_synonyms = ligand.synonyms()
            ligand_comments = ligand.general_comments()
            ligand_links = ligand.database_links()
            if ligand_iupac: structure = True
            if ligand_mass: molecular = True
            if ligand_synonyms: synonyms = True
            if ligand_comments: comments = True
            if ligand_links: database = True

        self.assertTrue(structure)
        self.assertTrue(molecular)
        self.assertTrue(synonyms)
        self.assertTrue(comments)
        self.assertTrue(database)
