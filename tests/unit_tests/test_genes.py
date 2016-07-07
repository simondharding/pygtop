from unittest import TestCase
from pygtop.shared import Gene


class GeneTest(TestCase):

    def setUp(self):
        self.gene_json = {
         "targetId": 1,
         "species": "Human",
         "geneSymbol": "HTR1A",
         "geneName": "5-hydroxytryptamine receptor 1A",
         "officialGeneId": "5286",
         "genomicLocation": "5q11.2-q13",
         "aminoAcids": "422",
         "transmembraneDomains": "7",
         "poreLoops": "1",
         "refs": []
        }



class DatabaseLinkCreationTests(GeneTest):

    def test_can_create_gene(self):
        gene = Gene(self.gene_json)
        self.assertEqual(gene.json_data, self.gene_json)
        self.assertEqual(gene.target_id, 1)
        self.assertEqual(gene.species, "Human")
        self.assertEqual(gene.gene_symbol, "HTR1A")
        self.assertEqual(gene.gene_name, "5-hydroxytryptamine receptor 1A")
        self.assertEqual(gene.official_gene_id, "5286")
        self.assertEqual(gene.genomic_location, "5q11.2-q13")
        self.assertEqual(gene.amino_acids, 422)
        self.assertEqual(gene.transmembrane_domains, 7)
        self.assertEqual(gene.pore_loops, 1)
        self.assertEqual(str(gene), "<Human Gene (HTR1A)>")


    def test_can_parse_none_counts(self):
        self.gene_json["aminoAcids"] = None
        self.gene_json["transmembraneDomains"] = None
        self.gene_json["poreLoops"] = None
        gene = Gene(self.gene_json)
        self.assertEqual(gene.amino_acids, 0)
        self.assertEqual(gene.transmembrane_domains, 0)
        self.assertEqual(gene.pore_loops, 0)
