from unittest import TestCase
import xml.etree.ElementTree as ElementTree
import unittest.mock
from unittest.mock import patch
from pygtop.pdb import query_rcsb

class SimpleQueryTest(TestCase):

    def setUp(self):
        self.mock_response = unittest.mock.Mock()
        self.mock_response.text = '''<?xml version='1.0' standalone='no' ?>
<smilesQueryResult smiles="NC(=O)C1=CC=CC=C1" search_type="4">
<ligandInfo>
<ligand structureId="2XG3" chemicalID="UNU" type="non-polymer" molecularWeight="121.137">
  <chemicalName>BENZAMIDE</chemicalName>
  <formula>C7 H7 N O</formula>
  <InChIKey>KXDAEFPNCMNJSK-UHFFFAOYSA-N</InChIKey>
  <InChI>InChI=1S/C7H7NO/c8-7(9)6-4-2-1-3-5-6/h1-5H,(H2,8,9)</InChI>
  <smiles>c1ccc(cc1)C(=O)N</smiles>
</ligand>
<ligand structureId="3A1I" chemicalID="UNU" type="non-polymer" molecularWeight="121.137">
  <chemicalName>BENZAMIDE</chemicalName>
  <formula>C7 H7 N O</formula>
  <InChIKey>KXDAEFPNCMNJSK-UHFFFAOYSA-N</InChIKey>
  <InChI>InChI=1S/C7H7NO/c8-7(9)6-4-2-1-3-5-6/h1-5H,(H2,8,9)</InChI>
  <smiles>c1ccc(cc1)C(=O)N</smiles>
</ligand>
</ligandInfo>
</smilesQueryResult>'''
        self.mock_response.status_code = 200
        self.mock_response.headers = {"Content-Type": "xml"}


    @patch("requests.get")
    def test_can_produce_xml(self, mock_get):
        mock_get.return_value = self.mock_response
        result = query_rcsb("smilesQuery", {
         "smiles": "NC(=O)C1=CC=CC=C1",
         "search_type": "exact"
        })
        self.assertIsInstance(result, ElementTree.Element)


    @patch("requests.get")
    def test_can_produce_none_from_invalid_search(self, mock_get):
        self.mock_response.headers["Content-Type"] = "html"
        mock_get.return_value = self.mock_response
        result = query_rcsb("smilesQuery", {
         "smiles": "NC(=O)C1=CC=CC=C1",
         "search_type": "exact"
        })
        self.assertIs(result, None)


'''import unittest
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
    unittest.main()'''
