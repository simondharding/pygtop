from unittest import TestCase
import unittest.mock
from unittest.mock import patch
from pygtop.targets import Target, get_target_by_id, get_all_targets, get_targets_by
from pygtop.targets import get_target_by_name, TargetFamily
from pygtop.interactions import Interaction
from pygtop.ligands import Ligand
import pygtop.exceptions as exceptions
from pygtop.shared import DatabaseLink, Gene

class TargetTest(TestCase):

    def setUp(self):
        self.target_json = {
         "targetId": 1,
         "name": "5-HT<sub>1A</sub> receptor",
         "abbreviation": "5-HT",
         "systematicName": None,
         "type": "GPCR",
         "familyIds": [1],
         "subunitIds": [2, 3],
         "complexIds": [4]
        }

        self.database_json = [
         {
          "accession": "10576",
          "database": "ChEMBL Target",
          "url": "http://www.ebi.ac.uk/chembldb/index.php/target/inspect/10576",
          "species": "Rat"
         },
         {
          "accession": "11863",
          "database": "ChEMBL Target",
          "url": "http://www.ebi.ac.uk/chembldb/index.php/target/inspect/11863",
          "species": "Mouse"
         }
        ]

        self.gene_json = [
         {
          "targetId": 380,
          "species": "Human",
          "geneSymbol": "KCNMA1",
          "geneName": "potassium calcium-activated channel subfamily M alpha 1",
          "officialGeneId": "6284",
          "genomicLocation": "10q22.3",
          "aminoAcids": "1182",
          "transmembraneDomains": "6",
          "poreLoops": "1",
          "refs": []
         },
         {
          "targetId": 380,
          "species": "Mouse",
          "geneSymbol": "Kcnma1",
          "geneName": "potassium large conductance calcium-activated channel",
          "officialGeneId": "MGI:99923",
          "genomicLocation": "14 A3",
          "aminoAcids": "1236",
          "transmembraneDomains": "6",
          "poreLoops": "1",
          "refs": []
         },
         {
          "targetId": 380,
          "species": "Rat",
          "geneSymbol": "Kcnma2",
          "geneName": "potassium calcium-activated channel subfamily M alpha 1",
          "officialGeneId": "620715",
          "genomicLocation": "15p16",
          "aminoAcids": "1243",
          "transmembraneDomains": "6",
          "poreLoops": "1",
          "refs": []
         }
        ]

        self.interaction_json = {
         "interactionId": 79397,
         "targetId": 1,
         "ligandAsTargetId": 0,
         "targetSpecies": "Human",
         "primaryTarget": False,
         "targetBindingSite": "",
         "ligandId": 7191,
         "ligandContext": "",
         "endogenous": False,
         "type": "Agonist",
         "action": "Agonist",
         "actionComment": "",
         "selectivity": "None",
         "concentrationRange": "-",
         "affinity": "7.2",
         "affinityType": "pKi",
         "originalAffinity": "6x10<sup>-8</sup>",
         "originalAffinityType": "Ki",
         "originalAffinityRelation": "",
         "assayDescription": "",
         "assayConditions": "",
         "useDependent": False,
         "voltageDependent": False,
         "voltage": "-",
         "physiologicalVoltage": False,
         "conciseView": False,
         "dataPoints": [],
         "refs": []
        }

        self.ligand_json = {
         "ligandId": 1,
         "name": "flesinoxan",
         "abbreviation": "flexo",
         "inn": "flesinoxan",
         "type": "Synthetic organic",
         "species": None,
         "radioactive": False,
         "labelled": True,
         "approved": True,
         "withdrawn": False,
         "approvalSource": "FDA (1997)",
         "subunitIds": [2, 3],
         "complexIds": [5],
         "prodrugIds": [7],
         "activeDrugIds": [9, 10]
        }


        self.pdb_json = [
         {
          "targetId" : 2,
          "ligandId" : 121,
          "endogenous" : False,
          "pdbCode" : "4IAQ",
          "description" : "Crystal structure of the chimeric protein of 5-HT1B-BRIL in complex with dihydroergotamine",
          "resolution" : 2.8,
          "species" : "Human",
          "refs" : []
         }, {
          "targetId" : 2,
          "ligandId" : 149,
          "endogenous" : False,
          "pdbCode" : "4IAR",
          "description" : "Crystal structure of the chimeric protein of 5-HT1B-BRIL in complex with ergotamine",
          "resolution" : 2.7,
          "species" : "Rat",
          "refs" : []
         }
        ]



class TargetCreationTests(TargetTest):

    def test_can_create_target(self):
        target = Target(self.target_json)
        self.assertEqual(target.json_data, self.target_json)
        self.assertEqual(target._target_id, 1)
        self.assertEqual(target._name, "5-HT<sub>1A</sub> receptor")
        self.assertEqual(target._abbreviation, "5-HT")
        self.assertEqual(target._systematic_name, None)
        self.assertEqual(target._target_type, "GPCR")
        self.assertEqual(target._family_ids, [1])
        self.assertEqual(target._subunit_ids, [2, 3])
        self.assertEqual(target._complex_ids, [4])


    def test_target_repr(self):
        target = Target(self.target_json)
        self.assertEqual(str(target), "<Target 1 (5-HT<sub>1A</sub> receptor)>")



class TargetPropertyTests(TargetTest):

    def test_basic_property_methods(self):
        target = Target(self.target_json)
        self.assertIs(target._target_id, target.target_id())
        self.assertIs(target._name, target.name())
        self.assertIs(target._abbreviation, target.abbreviation())
        self.assertIs(target._systematic_name, target.systematic_name())
        self.assertIs(target._target_type, target.target_type())
        self.assertIs(target._family_ids, target.family_ids())
        self.assertIs(target._subunit_ids, target.subunit_ids())
        self.assertIs(target._complex_ids, target.complex_ids())


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_synonym_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = [
         {"name": "ADRBRL1", "refs": []},
         {"name": "5-HT1A", "refs": []}
        ]
        target = Target(self.target_json)

        self.assertEqual(target.synonyms(), ["ADRBRL1", "5-HT1A"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_synonym_properties_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)

        self.assertEqual(target.synonyms(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_database_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = self.database_json
        target = Target(self.target_json)

        self.assertEqual(len(target.database_links()), 2)
        self.assertIsInstance(target.database_links()[0], DatabaseLink)
        self.assertIsInstance(target.database_links()[1], DatabaseLink)
        self.assertEqual(target.database_links()[0].accession(), "10576")
        self.assertEqual(target.database_links()[1].accession(), "11863")
        self.assertEqual(target.database_links()[0].species(), "Rat")
        self.assertEqual(target.database_links()[1].species(), "Mouse")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_database_properties_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)

        self.assertEqual(target.database_links(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_species_database_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = self.database_json
        target = Target(self.target_json)

        links = target.database_links(species="mouse")
        self.assertEqual(len(links), 1)
        self.assertIsInstance(links[0], DatabaseLink)
        self.assertEqual(links[0].accession(), "11863")
        self.assertEqual(links[0].species(), "Mouse")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_gene_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = self.gene_json
        target = Target(self.target_json)

        self.assertEqual(len(target.genes()), 3)
        self.assertIsInstance(target.genes()[0], Gene)
        self.assertIsInstance(target.genes()[1], Gene)
        self.assertIsInstance(target.genes()[2], Gene)
        self.assertEqual(target.genes()[0].gene_symbol(), "KCNMA1")
        self.assertEqual(target.genes()[1].gene_symbol(), "Kcnma1")
        self.assertEqual(target.genes()[2].gene_symbol(), "Kcnma2")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_gene_properties_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)

        self.assertEqual(target.genes(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_species_gene_properties(self, mock_json_retriever):
        mock_json_retriever.return_value = self.gene_json
        target = Target(self.target_json)

        genes = target.genes(species="mouse")
        self.assertEqual(len(genes), 1)
        self.assertIsInstance(genes[0], Gene)
        self.assertEqual(genes[0].gene_symbol(), "Kcnma1")
        self.assertEqual(genes[0].species(), "Mouse")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_families(self, mock_json_retriever):
        mock_json_retriever.return_value = {
         "familyId": 1,
         "name": "5-Hydroxytryptamine receptors",
         "targetIds": [1, 2, 5],
         "parentFamilyIds": [694],
         "subFamilyIds": [9]
        }
        target = Target(self.target_json)
        families = target.families()
        self.assertIsInstance(families, list)
        self.assertEqual(len(families), len(self.target_json["familyIds"]))
        for family in families:
            self.assertIsInstance(family, TargetFamily)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_subunits(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        target = Target(self.target_json)
        subunits = target.subunits()
        self.assertIsInstance(subunits, list)
        self.assertEqual(len(subunits), len(self.target_json["subunitIds"]))
        for subunit in subunits:
            self.assertIsInstance(subunit, Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_complexes(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        target = Target(self.target_json)
        complexes = target.complexes()
        self.assertIsInstance(complexes, list)
        self.assertEqual(len(complexes), len(self.target_json["complexIds"]))
        for complex_ in complexes:
            self.assertIsInstance(complex_, Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_interactions(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.interaction_json, self.interaction_json]
        target = Target(self.target_json)
        interactions = target.interactions()
        self.assertIsInstance(interactions, list)
        self.assertEqual(len(interactions), 2)
        for interaction in interactions:
            self.assertIsInstance(interaction, Interaction)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_interactions_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)
        self.assertEqual(target.interactions(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_interaction_by_id(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.interaction_json, self.interaction_json]
        target = Target(self.target_json)
        interaction = target.get_interaction_by_id(self.interaction_json["interactionId"])
        self.assertIsInstance(interaction, Interaction)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_cannot_get_interaction_by_invalid_id(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)
        with self.assertRaises(exceptions.NoSuchInteractionError):
            interaction = target.get_interaction_by_id(0)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_interaction_id_id_must_be_int(self, mock_json_retriever):
        mock_json_retriever.return_value =[self.interaction_json, self.interaction_json]
        target = Target(self.target_json)
        with self.assertRaises(TypeError):
            target.get_interaction_by_id("1")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_ligands(self, mock_json_retriever):
        mock_json_retriever.side_effect = [
         [self.interaction_json, self.interaction_json], self.ligand_json, self.ligand_json
        ]
        target = Target(self.target_json)
        ligands = target.ligands()
        self.assertIsInstance(ligands, list)
        self.assertEqual(len(ligands), 2)
        for ligand in ligands:
            self.assertIsInstance(ligand, Ligand)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_gtop_pdbs(self, mock_json_retriever):
        mock_json_retriever.return_value = self.pdb_json
        target = Target(self.target_json)
        pdbs = target.gtop_pdbs()
        self.assertEqual(pdbs, ["4IAQ", "4IAR"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_gtop_pdbs_when_no_json(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        target = Target(self.target_json)
        self.assertEqual(target.gtop_pdbs(), [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_gtop_pdbs_by_species(self, mock_json_retriever):
        mock_json_retriever.return_value = self.pdb_json
        target = Target(self.target_json)
        pdbs = target.gtop_pdbs(species="rat")
        self.assertEqual(pdbs, ["4IAR"])


    @patch("pygtop.gtop.get_json_from_gtop")
    @patch("pygtop.pdb.query_rcsb_advanced")
    def test_can_get_uniprot_pdbs(self, mock_xml_retriever, mock_json_retriever):
        mock_json_retriever.return_value = [
         {"accession": "10576", "database": "UniProtKB", "species": "Human", "url":"http"}
        ]
        mock_xml_retriever.return_value = ["2XG3", "3A1I"]
        target = Target(self.target_json)
        pdbs = target.uniprot_pdbs()
        self.assertEqual(pdbs, ["2XG3", "3A1I"])


    @patch("pygtop.gtop.get_json_from_gtop")
    @patch("pygtop.pdb.query_rcsb_advanced")
    def test_can_get_uniprot_pdbs_when_no_results(self, mock_xml_retriever, mock_json_retriever):
        mock_json_retriever.return_value = [
         {"accession": "10576", "database": "UniProtKB", "species": "Human", "url":"http"}
        ]
        mock_xml_retriever.return_value = None
        target = Target(self.target_json)
        pdbs = target.uniprot_pdbs()
        self.assertEqual(pdbs, [])


    @patch("pygtop.gtop.get_json_from_gtop")
    @patch("pygtop.pdb.query_rcsb_advanced")
    def test_can_get_uniprot_pdbs_by_species(self, mock_xml_retriever, mock_json_retriever):
        mock_json_retriever.return_value = [
         {"accession": "10576", "database": "UniProtKB", "species": "Human", "url":"http"},
         {"accession": "10576", "database": "UniProtKB", "species": "Rat", "url":"http"}
        ]
        mock_xml_retriever.side_effect = [["2XG3", "3A1I"], ["1xxx"]]
        target = Target(self.target_json)
        pdbs = target.uniprot_pdbs(species="rat")
        self.assertEqual(pdbs, ["2XG3", "3A1I"])


    @patch("pygtop.gtop.get_json_from_gtop")
    @patch("pygtop.pdb.query_rcsb_advanced")
    def test_can_get_all_pdbs(self, mock_xml_retriever, mock_json_retriever):
        mock_json_retriever.side_effect = [
         self.pdb_json,
         [{"accession": "10576", "database": "UniProtKB", "species": "Human", "url":"http"}]
        ]
        mock_xml_retriever.return_value = ["2XG3", "3A1I"]
        target = Target(self.target_json)
        pdbs = target.all_pdbs()
        self.assertEqual(len(pdbs), 4)
        for code in ["4IAQ", "4IAR", "2XG3", "3A1I"]:
            self.assertIn(code, pdbs)



class TargetAccessTests(TargetTest):

    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_by_id(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        target = get_target_by_id(1)
        self.assertIsInstance(target, Target)
        self.assertEqual(target.name(), self.target_json["name"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_id_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        with self.assertRaises(exceptions.NoSuchTargetError):
            target = get_target_by_id(1)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_id_must_be_int(self, mock_json_retriever):
        mock_json_retriever.return_value = self.target_json
        with self.assertRaises(TypeError):
            target = get_target_by_id("1")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_all_targets(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json, self.target_json]
        targets = get_all_targets()
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), 2)
        self.assertIsInstance(targets[0], Target)
        self.assertIsInstance(targets[1], Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_by_query(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json, self.target_json]
        targets = get_targets_by({"type": "gpcr"})
        self.assertIsInstance(targets, list)
        self.assertEqual(len(targets), 2)
        self.assertIsInstance(targets[0], Target)
        self.assertIsInstance(targets[1], Target)


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_query_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        targets = get_targets_by({"type": "gcpr"})
        self.assertEqual(targets, [])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_query_must_be_dict(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json, self.target_json]
        with self.assertRaises(TypeError):
            target = get_targets_by("astring")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_can_get_target_by_name(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json]
        target = get_target_by_name("actin")
        self.assertIsInstance(target, Target)
        self.assertEqual(target.target_id(), self.target_json["targetId"])


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_invalid_target_name_error(self, mock_json_retriever):
        mock_json_retriever.return_value = None
        with self.assertRaises(exceptions.NoSuchTargetError):
            target = get_target_by_name("fauxprot")


    @patch("pygtop.gtop.get_json_from_gtop")
    def test_target_name_must_be_str(self, mock_json_retriever):
        mock_json_retriever.return_value = [self.target_json]
        with self.assertRaises(TypeError):
            target = get_target_by_name(1)
