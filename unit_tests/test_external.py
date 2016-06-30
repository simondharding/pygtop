from unittest import TestCase
from pygtop.shared import DatabaseLink


class DatabaseLinkTest(TestCase):

    def setUp(self):
        self.dblink1_json = {
         "accession": "CHEMBL1742477",
         "database": "ChEMBL Ligand",
         "url": "http://www.ebi.ac.uk/chembldb/index.php/compound/inspect/CHEMBL1742477",
         "species": "None"
        }

        self.dblink2_json = {
         "accession": "ENSRNOG00000010254",
         "database": "Ensembl Gene",
         "url": "http://www.ensembl.org/Gene/Summary?g=ENSRNOG00000010254",
         "species": "Rat"
        }



class DatabaseLinkCreationTests(DatabaseLinkTest):

    def test_can_create_database_link(self):
        link = DatabaseLink(self.dblink2_json)
        self.assertEqual(link.json_data, self.dblink2_json)
        self.assertEqual(link.accession, self.dblink2_json["accession"])
        self.assertEqual(link.database, self.dblink2_json["database"])
        self.assertEqual(link.url, self.dblink2_json["url"])
        self.assertEqual(link.species, self.dblink2_json["species"])
        self.assertEqual(str(link), "<Ensembl Gene link (ENSRNOG00000010254) for Rat>")


    def test_can_parse_none_species(self):
        link = DatabaseLink(self.dblink1_json)
        self.assertEqual(link.species, None)
        self.assertEqual(str(link), "<ChEMBL Ligand link (CHEMBL1742477)>")
