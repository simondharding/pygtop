import requests
import json
from .gtop import *
from .exceptions import *
from .shared import *

def get_ligand_by_id(ligand_id):
    json_data = get_json_from_gtop("ligands/%i" % ligand_id)
    if json_data:
        return Ligand(json_data)
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
        json_data = get_json_from_gtop("ligands/%i/%s" % (self.ligand_id, STRUCTURAL_PROPERTIES))
        self.iupac_name = json_data["iupacName"] if json_data else None
        self.smiles = json_data["smiles"] if json_data else None
        self.inchi = json_data["inchi"] if json_data else None
        self.inchi_key = json_data["inchiKey"] if json_data else None
        self.one_letter_sequence = json_data["oneLetterSeq"] if json_data else None
        self.three_letter_sequence = json_data["threeLetterSeq"] if json_data else None
        self.post_translational_modifications = json_data["postTranslationalModifications"] if json_data else None
        self.chemical_modifications = json_data["chemicalModifications"] if json_data else None


    def get_molecular_properties(self):
        json_data = get_json_from_gtop("ligands/%i/%s" % (self.ligand_id, MOLECULAR_PROPERTIES))
        self.hydrogen_bond_acceptors = json_data["hydrogenBondAcceptors"] if json_data else None
        self.hydrogen_bond_donors = json_data["hydrogenBondDonors"] if json_data else None
        self.rotatable_bonds = json_data["rotatableBonds"] if json_data else None
        self.topological_polar_surface_area = json_data["topologicalPolarSurfaceArea"] if json_data else None
        self.molecular_weight = json_data["molecularWeight"] if json_data else None
        self.log_p = json_data["logP"] if json_data else None
        self.lipinksi_rules_broken = json_data["lipinskisRuleOfFive"] if json_data else None


    def get_database_properties(self):
        json_data = get_json_from_gtop("ligands/%i/%s" % (self.ligand_id, DATABASE_PROPERTIES))
        self.database_links = [DatabaseLink(link) for link in json_data] if json_data else []


    def get_synonym_properties(self):
        json_data = get_json_from_gtop("ligands/%i/%s" % (self.ligand_id, SYNONYM_PROPERTIES))
        self.synonyms = [synonym["name"] for synonym in json_data] if json_data else []


    def get_comment_properties(self):
        json_data = get_json_from_gtop("ligands/%i/%s" % (self.ligand_id, COMMENT_PROPERTIES))
        self.general_comments = json_data["comments"] if json_data else ""
        self.bioactivity_comments = json_data["bioactivityComments"] if json_data else ""
        self.clinical_use_comments = json_data["clinicalUse"] if json_data else ""
        self.mechanism_of_action_comments = json_data["mechanismOfAction"] if json_data else ""
        self.absorption_and_distribution_comments = json_data["absorptionAndDistribution"] if json_data else ""
        self.metabolism_comments = json_data["metabolism"] if json_data else ""
        self.elimination_comments = json_data["elimination"] if json_data else ""
        self.population_pharmacokinetics_comments = json_data["populationPharmacokinetics"] if json_data else ""
        self.organ_function_impairments_comments = json_data["organFunctionImpairment"] if json_data else ""
        self.mutations_and_pathophysiology_comments = json_data["mutationsAndPathophysiology"] if json_data else ""


    def get_precursor_properties(self):
        json_data = get_json_from_gtop("ligands/%i/%s" % (self.ligand_id, PRECURSOR_PROPERTIES))
        self.precursors = [Precursor(p) for p in json_data] if json_data else []


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
