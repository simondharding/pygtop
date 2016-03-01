import requests
import json
from .gtop_constants import *
from .exceptions import *

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
