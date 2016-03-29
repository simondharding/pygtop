from __future__ import division

class Interaction:

    def __init__(self, json_data):
        self.json_data = json_data

        self.interaction_id = json_data["interactionId"]
        self._target_id = json_data["targetId"]
        self._ligand_id = json_data["ligandId"]
        self.species = json_data["targetSpecies"]
        self.type = json_data["type"]
        self.action = json_data["action"]
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
