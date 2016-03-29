from __future__ import division
from .exceptions import NoSuchLigandError, NoSuchTargetError

class Interaction:

    def __init__(self, json_data):
        self.json_data = json_data

        self.interaction_id = json_data["interactionId"]
        self._target_id = json_data["targetId"]
        self._ligand_id = json_data["ligandId"]
        self.species = json_data["targetSpecies"]
        self.type = json_data["type"]
        self.action = json_data["action"]
        if json_data["affinity"] == "-":
            self.affinity_range = ()
            self.affinity_value = None
            self.affinity_type = None
        else:
            self.affinity_range = tuple(
             [float(val) for val in json_data["affinity"].split(" &ndash; ")]
            ) if "&" in json_data["affinity"] else (float(json_data["affinity"]),)
            self.affinity_value = self.affinity_range[0] if len(self.affinity_range
             ) == 1 else sum(self.affinity_range) / len(self.affinity_range)
            self.affinity_type = json_data["affinityType"]
        self.is_voltage_dependent = json_data["voltageDependent"]
        self.voltage = float(json_data["voltage"]
         ) if json_data["voltage"] != "-" else None
        self.ligand_primary_target = json_data["primaryTarget"]
        self.references = [
         "(%i) %s" % (ref["year"], ref["articleTitle"]) for ref in json_data["refs"]
        ]


    def get_ligand(self):
        from .ligands import get_ligand_by_id
        try:
            return get_ligand_by_id(self._ligand_id)
        except NoSuchLigandError:
            return None


    def get_target(self):
        from .targets import get_target_by_id
        try:
            return get_target_by_id(self._target_id)
        except NoSuchTargetError:
            return None


    def get_species_target(self):
        from .targets import SpeciesTarget
        try:
            return SpeciesTarget(self._target_id, self.species)
        except NoSuchTargetError:
            return None
