"""Contains target-specific objects and functions."""

from .exceptions import *
from .gtop import *
from .shared import *
import random


def get_target_by_id(target_id):
    json_data = get_json_from_gtop("targets/%i" % target_id)
    if json_data:
        return Target(json_data)
    else:
        raise NoSuchTargetError


def get_random_target(target_type=None):
    if target_type:
        json_data = get_json_from_gtop("targets?type=%s" % target_type.lower())
        if not json_data:
            raise NoSuchTypeError("There are no targets of type %s" % target_type)
    else:
        json_data = get_json_from_gtop("targets")
    return Target(random.choice(json_data))


def get_all_targets():
    json_data = get_json_from_gtop("targets")
    return [Target(t) for t in json_data]


def get_targets_by(criteria):
    search_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    json_data = get_json_from_gtop("targets?%s" % search_string)
    if json_data:
        return [Target(t) for t in json_data]
    else:
        return []


def get_target_by_name(name):
    targets = get_targets_by({"name": name})
    if targets:
        return targets[0]
    else:
        raise NoSuchTargetError


def get_family_by_id(family_id):
    json_data = get_json_from_gtop("targets/families/%i" % family_id)
    if json_data:
        return TargetFamily(json_data)
    else:
        raise NoSuchFamilyError


def get_all_families():
    json_data = get_json_from_gtop("targets/families")
    return [TargetFamily(f) for f in json_data]


def get_random_family():
    json_data = get_json_from_gtop("targets/families")
    return TargetFamily(random.choice(json_data))


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


    def __getattr__(self, key):
        error_message = self._get_missing_attribute_error_message(key)
        if error_message:
            raise PropertyNotRequestedYetError(error_message)
        else:
            raise AttributeError("Target object has no attribute '%s'" % key)


    def __repr__(self):
        return "<'%s' Target (%s)>" % (self.name, self.target_type)


    def get_subunits(self):
        return [get_target_by_id(i) for i in self._subunit_ids]


    def get_complexes(self):
        return [get_target_by_id(i) for i in self._complex_ids]


    def get_families(self):
        return [get_family_by_id(i) for i in self._family_ids]


    def request_database_properties(self):
        """Give target object database properties:

        .. py:attribute:: database_links:

            A list of  :class:`.DatabaseLink`: objects."""

        json_data = get_json_from_gtop("targets/%i/%s" % (
         self.target_id, DATABASE_PROPERTIES))
        self.database_links = [
         DatabaseLink(link) for link in json_data] if json_data else []


    def request_synonym_properties(self):
        """Give target object synonym properties:

        .. py:attribute:: synonyms:

            A list of synonym strings."""

        json_data = get_json_from_gtop("ligands/%i/%s" % (
         self.target_id, SYNONYM_PROPERTIES))
        self.synonyms = [
         synonym["name"] for synonym in json_data] if json_data else []


    def _get_missing_attribute_error_message(self, attribute):
        message = "'%s' is a %s property - you need to request this seperately with my %s() method"
        values = []

        if attribute in self._database_properties:
            values = ["database", "request_database_properties"]
        elif attribute in self._synonym_properties:
            values = ["synonym", "request_synonym_properties"]

        if values:
            values = [attribute] + values
            return (message % tuple(values))
        else:
            return None


    _database_properties = [
     "database_links"
    ]

    _synonym_properties = [
     "synonyms"
    ]



class SpeciesTarget(Target):

    def __init__(self, target_id, species):
        self.target_id = target_id
        self.target = get_target_by_id(target_id)
        self.species = species


    def __repr__(self):
        return "<%s %s>" % (self.species, self.target.name)


    def request_database_properties(self):
        Target.request_database_properties(self)
        self.database_links = [
         link for link in self.database_links
          if link.species.lower() == self.species.lower()
        ]




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
