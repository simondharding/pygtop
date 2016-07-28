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
        self.assertEqual(link._accession, self.dblink2_json["accession"])
        self.assertEqual(link._database, self.dblink2_json["database"])
        self.assertEqual(link._url, self.dblink2_json["url"])
        self.assertEqual(link._species, self.dblink2_json["species"])
        self.assertEqual(str(link), "<Ensembl Gene link (ENSRNOG00000010254) for Rat>")


    def test_can_parse_none_species(self):
        link = DatabaseLink(self.dblink1_json)
        self.assertEqual(link._species, None)
        self.assertEqual(str(link), "<ChEMBL Ligand link (CHEMBL1742477)>")



class DatabaseLinkPropertyTests(DatabaseLinkTest):

    def test_database_link_properties(self):
        link = DatabaseLink(self.dblink2_json)
        self.assertIs(link.accession(), link._accession)
        self.assertIs(link.database(), link._database)
        self.assertIs(link.url(), link._url)
        self.assertIs(link.species(), link._species)
