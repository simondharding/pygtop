import unittest
import json
import sys
sys.path.append(".")
from pygtop.pdb import *
import xml.etree.ElementTree as ElementTree

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


if __name__ == "__main__":
    unittest.main()
