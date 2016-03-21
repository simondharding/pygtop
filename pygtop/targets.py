"""Contains target-specific objects and functions."""

from .exceptions import *
from .gtop import *

def get_target_by_id(target_id):
    json_data = get_json_from_gtop("targets/%i" % target_id)
    if json_data:
        return Target(json_data)
    else:
        raise NoSuchTargetError


def get_family_by_id(family_id):
    json_data = get_json_from_gtop("targets/families/%i" % family_id)
    if json_data:
        return TargetFamily(json_data)
    else:
        raise NoSuchFamilyError


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


    def __repr__(self):
        return "<'%s' Target (%s)>" % (self.name, self.target_type)


    def get_subunits(self):
        return [get_target_by_id(i) for i in self._subunit_ids]


    def get_complexes(self):
        return [get_target_by_id(i) for i in self._complex_ids]


    def get_families(self):
        return [get_family_by_id(i) for i in self._family_ids]



class TargetFamily:

    def __init__(self, json_data):
        self.json_data = json_data

        self.family_id = json_data["familyId"]
        self.name = json_data["name"]
        self._target_ids = json_data["targetIds"]
        self._parent_family_ids = json_data["parentFamilyIds"]
        self._sub_family_ids = json_data["subFamilyIds"]


    def __repr__(self):
        return "<'%s' TargetFamily>" % self.name


    def get_targets(self):
        return [get_target_by_id(i) for i in self._target_ids]


    def get_parent_families(self):
        return [get_family_by_id(i) for i in self._parent_family_ids]


    def get_subfamilies(self):
        return [get_family_by_id(i) for i in self._sub_family_ids]
