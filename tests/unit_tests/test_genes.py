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



class GeneCreationTests(GeneTest):

    def test_can_create_gene(self):
        gene = Gene(self.gene_json)
        self.assertEqual(gene.json_data, self.gene_json)
        self.assertEqual(gene._target_id, 1)
        self.assertEqual(gene._species, "Human")
        self.assertEqual(gene._gene_symbol, "HTR1A")
        self.assertEqual(gene._gene_name, "5-hydroxytryptamine receptor 1A")
        self.assertEqual(gene._official_gene_id, "5286")
        self.assertEqual(gene._genomic_location, "5q11.2-q13")
        self.assertEqual(gene._amino_acids, 422)
        self.assertEqual(gene._transmembrane_domains, 7)
        self.assertEqual(gene._pore_loops, 1)
        self.assertEqual(str(gene), "<Human Gene (HTR1A)>")


    def test_can_parse_none_counts(self):
        self.gene_json["aminoAcids"] = None
        self.gene_json["transmembraneDomains"] = None
        self.gene_json["poreLoops"] = None
        gene = Gene(self.gene_json)
        self.assertEqual(gene._amino_acids, 0)
        self.assertEqual(gene._transmembrane_domains, 0)
        self.assertEqual(gene._pore_loops, 0)



class GenePropertyTests(GeneTest):

    def test_gene_properties(self):
        gene = Gene(self.gene_json)
        self.assertIs(gene.target_id(), gene._target_id)
        self.assertIs(gene.species(), gene._species)
        self.assertIs(gene.gene_symbol(), gene._gene_symbol)
        self.assertIs(gene.gene_name(), gene._gene_name)
        self.assertIs(gene.official_gene_id(), gene._official_gene_id)
        self.assertIs(gene.genomic_location(), gene._genomic_location)
        self.assertIs(gene.amino_acids(), gene._amino_acids)
        self.assertIs(gene.transmembrane_domains(), gene._transmembrane_domains)
        self.assertIs(gene.pore_loops(), gene._pore_loops)
