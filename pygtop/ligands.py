import requests
import json
from .gtop_constants import *
from .exceptions import *
from .shared import *

def get_ligand_by_id(ligand_id):
    response = requests.get("%sligands/%i" % (ROOT_URL, ligand_id))
    if response.status_code == 200:
        json_data = response.text
        return Ligand(json.loads(json_data))
    else:
        raise NoSuchLigandError


class Ligand:

    def __init__(self, json_data):
        self.json_data = json_data

        self.ligand_id = json_data["ligandId"]
        self.name = json_data["name"]
        self.abbreviation = json_data["abbreviation"]
        self.inn = json_data["inn"]
        self.type = json_data["type"]
        self.type = json_data["type"]
        self.species = json_data["species"]
        self.radioactive = json_data["radioactive"]
        self.labelled = json_data["labelled"]
        self.approved = json_data["approved"]
        self.withdrawn = json_data["withdrawn"]
        self.approval_source = json_data["approvalSource"]
        self.subunit_ids = json_data["subunitIds"]
        self.complex_ids = json_data["complexIds"]
        self.prodrug_ids = json_data["prodrugIds"]
        self.active_drug_ids = json_data["activeDrugIds"]


    def __getattr__(self, key):
        error_message = self._get_missing_attribute_error_message(key)
        if error_message:
            raise PropertyNotRequestedYetError(error_message)
        else:
            raise AttributeError("Ligand object has no attribute '%s'" % key)


    def __repr__(self):
        return "<'%s' Ligand (%s)>" % (self.name, self.type)



    def get_structural_properties(self):
        response = requests.get("%sligands/%i/%s" % (ROOT_URL, self.ligand_id, STRUCTURAL_PROPERTIES))
        json_data = json.loads(response.text)
        self.iupac_name = json_data["iupacName"]
        self.smiles = json_data["smiles"]
        self.inchi = json_data["inchi"]
        self.inchi_key = json_data["inchiKey"]
        self.one_letter_sequence = json_data["oneLetterSeq"]
        self.three_letter_sequence = json_data["threeLetterSeq"]
        self.post_translational_modifications = json_data["postTranslationalModifications"]
        self.chemical_modifications = json_data["chemicalModifications"]


    def get_molecular_properties(self):
        response = requests.get("%sligands/%i/%s" % (ROOT_URL, self.ligand_id, MOLECULAR_PROPERTIES))
        json_data = json.loads(response.text)
        self.hydrogen_bond_acceptors = json_data["hydrogenBondAcceptors"]
        self.hydrogen_bond_donors = json_data["hydrogenBondDonors"]
        self.rotatable_bonds = json_data["rotatableBonds"]
        self.topological_polar_surface_area = json_data["topologicalPolarSurfaceArea"]
        self.molecular_weight = json_data["molecularWeight"]
        self.log_p = json_data["logP"]
        self.lipinksi_rules_broken = json_data["lipinskisRuleOfFive"]


    def get_database_properties(self):
        response = requests.get("%sligands/%i/%s" % (ROOT_URL, self.ligand_id, DATABASE_PROPERTIES))
        json_data = json.loads(response.text)
        self.database_links = [DatabaseLink(link) for link in json_data]


    def _get_missing_attribute_error_message(self, attribute):
        message = "'%s' is a %s property - you need to request this seperately with my %s() method"
        values = []

        if attribute in self._structural_properties:
            values = ["structural", "get_structural_properties"]
        elif attribute in self._molecular_properties:
            values = ["molecular", "get_molecular_properties"]
        elif attribute in self._database_properties:
            values = ["database", "get_database_properties"]
        elif attribute in self._synonym_properties:
            values = ["synonym", "get_synonym_properties"]
        elif attribute in self._comment_properties:
            values = ["comment", "get_common_properties"]
        elif attribute in self._precursor_properties:
            values = ["precursor", "get_precursor_properties"]

        if values:
            values = [attribute] + values
            print(message % tuple(values))
            return (message % tuple(values))
        else:
            return None


    _structural_properties = [
     "iupac_name",
     "smiles",
     "inchi",
     "inchi_key",
     "one_letter_sequence",
     "three_letter_sequence",
     "post_translational_modifications",
     "chemical_modifications"
    ]

    _molecular_properties = [
     "hydrogen_bond_acceptors",
     "hydrogen_bond_donors",
     "rotatable_bonds",
     "topological_polar_surface_area",
     "molecular_weight",
     "log_p",
     "lipinksi_rules_broken"
    ]

    _database_properties = [
     "database_links"
    ]

    _synonym_properties = [
     "synonyms"
    ]

    _comment_properties = [
     "general_comments",
     "bioactivity_comments",
     "clinical_use_comments",
     "mechanism_of_action_comments",
     "absorption_and_distribution_comments",
     "metabolism_comments",
     "elimination_comments",
     "population_pharmacokinetics_comments",
     "organ_function_impairments_comments",
     "mutations_and_pathophysiology_comments"
    ]

    _precursor_properties = [
     "precursors"
    ]
