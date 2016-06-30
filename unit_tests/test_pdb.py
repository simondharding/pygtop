import unittest
import json
import sys
sys.path.append(".")
from pygtop.pdb import *
import xml.etree.ElementTree as ElementTree
from molecupy.pdb import Pdb

class GetXml(unittest.TestCase):

    def test_can_get_xml(self):
        xml = query_rcsb("smilesQuery", {
         "smiles": "NC(=O)C1=CC=CC=C1",
         "search_type": "exact"
        })
        self.assertIsInstance(xml, ElementTree.Element)


    def test_incorrect_query_returns_none(self):
        xml = query_rcsb("smileyQuery", {
         "smiles": "NC(=O)C1=CC=CC=C1",
         "search_type": "exact"
        })
        self.assertEqual(xml, None)
        xml = query_rcsb("smilesQuery", {
         "smiley": "NC(=O)C1=CC=CC=C1",
         "search_type": "exact"
        })
        self.assertEqual(xml, None)
        xml = query_rcsb("smilesQuery", {"smiles": "NC(=O)C1=CC=CC=C1"})
        self.assertEqual(xml, None)
        xml = query_rcsb("smilesQuery", {})
        self.assertEqual(xml, None)


    def test_can_get_xml_advanced_search(self):
        results = query_rcsb_advanced("ChemCompDescriptorQuery", {
         "descriptor": "InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H",
         "descriptorType": "InChI"
        })
        self.assertIsInstance(results, list)



class MolecupyDecoratorTests(unittest.TestCase):

    def setUp(self):
        self.return_pdb = lambda: ["1LOL"]


    def test_decorator_not_normally_noticable(self):
        decorated_return_pdb = ask_about_molecupy(self.return_pdb)
        self.assertEqual(decorated_return_pdb()[0], "1LOL")


    def test_decorator_can_return_molecupy_object(self):
        decorated_return_pdb = ask_about_molecupy(self.return_pdb)
        self.assertIsInstance(decorated_return_pdb(as_molecupy=True)[0], Pdb)


if __name__ == "__main__":
    unittest.main()
