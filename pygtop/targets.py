"""Contains target-specific objects and functions."""

from .exceptions import *
from .gtop import *

def get_target_by_id(target_id):
    json_data = get_json_from_gtop("targets/%i" % target_id)
    if json_data:
        return Target(json_data)
    else:
        raise NoSuchTargetError


class Target:

    def __init__(self, json_data):
        self.json_data = json_data

        self.target_id = json_data["targetId"]
        self.name = json_data["name"]
        self.abbreviation = json_data["abbreviation"]\
         if json_data["abbreviation"] else ""
        self.target_type = json_data["type"]
        self.systematic_name = json_data["systematicName"]\
         if json_data["systematicName"] else ""
        self.target_type = json_data["type"]
        self._family_ids = json_data["familyIds"]
        self._subunit_ids = json_data["subunitIds"]
        self._complex_ids = json_data["complexIds"]
