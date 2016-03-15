"""Contains ligand-specific objects and functions."""

import requests
import json
import random
from .gtop import *
from .exceptions import *
from .shared import *

def get_ligand_by_id(ligand_id):
    """Returns a Ligand object of the ligand with the given ID.

    :param int ligand_id: The GtoP IDof the Ligand desired.
    :rtype: :py:class:`Ligand`
    :raises: :class:`.NoSuchLigandError`: if no such ligand exists in the database"""

    json_data = get_json_from_gtop("ligands/%i" % ligand_id)
    if json_data:
        return Ligand(json_data)
    else:
        raise NoSuchLigandError


def get_random_ligand(ligand_type=None):
    """Returns a random ligand, with the option to specify the ligand type.
    This can take a few seconds as it must first request *all* ligands.

    :param str ligand_type: If not None, the function will pick a ligand from\
     this category only.

    :rtype: :py:class:`Ligand`
    :raises: :class:`.NoSuchTypeError`: if a ligand type is supplied which doesn't exist
    """

    if ligand_type:
        json_data = get_json_from_gtop("ligands?type=%s" % ligand_type.lower())
        if not json_data:
            raise NoSuchTypeError("There are no ligands of type %s" % ligand_type)
    else:
        json_data = get_json_from_gtop("ligands")
    return Ligand(random.choice(json_data))


def get_all_ligands():
    """Returns a list of all ligands in the Guide to PHARMACOLOGY database. This
    can take a few seconds.

    :returns: list of :py:class:`Ligand` objects"""

    json_data = get_json_from_gtop("ligands")
    return [Ligand(l) for l in json_data]


def get_ligands_by(criteria):
    """Get all ligands which specify the criteria dictionary.

    :param dict criteria: A dictionary of `field=value` pairs. See the\
     `GtoP web services page <http://www.guidetopharmacology.org/\
     webServices.jsp#ligands>`_ for key/value pairs which can be supplied.
    :returns: list of :py:class:`Ligand` objects."""

    search_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    json_data = get_json_from_gtop("ligands?%s" % search_string)
    if json_data:
        return [Ligand(l) for l in json_data]
    else:
        return []


def get_ligand_by_name(name):
    """Returns the ligand which matches the name given. Will raise a
    NoSuchLigandError if no ligand by that ID exists.

    :param str name: The name of the ligand to search for. Note that synonyms \
    will not be searched.
    :rtype: :py:class:`Ligand`
    :raises:  :class:`.NoSuchLigandError`: if no such ligand exists in the database."""

    ligands = get_ligands_by({"name": name})
    if ligands:
        return ligands[0]
    else:
        raise NoSuchLigandError



class Ligand:
    """A Guide to PHARMACOLOGY ligand object.

    .. py:attribute:: ligand_id (int):

        The ligand's GtoP ID.

    .. py:attribute:: abbreviation:

        The ligand's SMILES string.

    .. py:attribute:: inn:

        The ligand's INN name.

    .. py:attribute:: ligand_type:

        The ligand type.

    .. py:attribute:: species:

        The ligand's GtoP ID.

    .. py:attribute:: radioactive:

        Is the ligand radioactive?

    .. py:attribute:: labelled:

        Is the ligand labelled?.

    .. py:attribute:: approved:

        Has the ligand been approved?

    .. py:attribute:: withdrawn:

        Has the drug been withdrawn?

    .. py:attribute:: approval_source:

        The regulatory body which approved the drug.

    .. py:attribute:: subunit_ids:

        GtoP IDs of subunits.

    .. py:attribute:: complex_ids:

        GtoP IDs of complexes the ligand forms.

    .. py:attribute:: prodrug_ids:

        GtoP IDs of prodrugs.

    .. py:attribute:: active_drug_ids:

        GtoP IDs of active equivalents.
    """

    def __init__(self, json_data):
        self.json_data = json_data

        self.ligand_id = json_data["ligandId"]
        self.name = json_data["name"]
        self.abbreviation = json_data["abbreviation"] if json_data["abbreviation"] else ""
        self.inn = json_data["inn"]
        self.ligand_type = json_data["type"]
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


    def request_structural_properties(self):
        """Give ligand object structural properties:

        .. py:attribute:: iupac_name:

            The ligand's full IUPAC name.

        .. py:attribute:: smiles:

            The ligand's SMILES string.

        .. py:attribute:: inchi:

            The ligand's InChI string.

        .. py:attribute:: inchi_key:

            The ligand's InChI key.

        .. py:attribute:: one_letter_sequence:

            If relevant, the single-code Amino Acid sequence.

        .. py:attribute:: three_letter_sequence:

            If relevant, the three-char-code Amino Acid sequence.

        .. py:attribute:: post_translational_modifications:

            Post-translational modifications, if any.

        .. py:attribute:: chemical_modifications:

            Chemical modifications, if any."""

        json_data = get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, STRUCTURAL_PROPERTIES))
        self.iupac_name = json_data["iupacName"] if json_data else None
        self.smiles = json_data["smiles"] if json_data else None
        self.inchi = json_data["inchi"] if json_data else None
        self.inchi_key = json_data["inchiKey"] if json_data else None
        self.one_letter_sequence = json_data["oneLetterSeq"] if json_data else None
        self.three_letter_sequence = json_data["threeLetterSeq"] if json_data else None
        self.post_translational_modifications = json_data[
         "postTranslationalModifications"] if json_data else None
        self.chemical_modifications = json_data[
         "chemicalModifications"] if json_data else None


    def request_molecular_properties(self):
        """Give ligand object molecular properties:

        .. py:attribute:: hydrogen_bond_acceptors:

            Number of H-bond acceptor atoms.

        .. py:attribute:: hydrogen_bond_donors:

            Number of H-bond donor atoms.

        .. py:attribute:: rotatable_bonds:

            Number of rotatable bonds in the ligand.

        .. py:attribute:: topological_polar_surface_area:

            polar surface area, in Angstroms.

        .. py:attribute:: molecular_weight:

            Ligand's mass.

        .. py:attribute:: log_p:

            Log of partition coefficient - a measure fo solubility.

        .. py:attribute:: lipinksi_rules_broken:

            Number of Lipinski's rules the ligand breaks (a measure of druglikeness)."""

        json_data = get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, MOLECULAR_PROPERTIES))
        self.hydrogen_bond_acceptors = json_data[
         "hydrogenBondAcceptors"] if json_data else None
        self.hydrogen_bond_donors = json_data["hydrogenBondDonors"] if json_data else None
        self.rotatable_bonds = json_data["rotatableBonds"] if json_data else None
        self.topological_polar_surface_area = json_data[
         "topologicalPolarSurfaceArea"] if json_data else None
        self.molecular_weight = json_data["molecularWeight"] if json_data else None
        self.log_p = json_data["logP"] if json_data else None
        self.lipinksi_rules_broken = json_data[
         "lipinskisRuleOfFive"] if json_data else None


    def request_database_properties(self):
        """Give ligand object database properties:

        .. py:attribute:: database_links:

            A list of  :class:`.DatabaseLink`: objects."""

        json_data = get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, DATABASE_PROPERTIES))
        self.database_links = [
         DatabaseLink(link) for link in json_data] if json_data else []


    def request_synonym_properties(self):
        """Give ligand object synonym properties:

        .. py:attribute:: synonyms:

            A list of synonym strings."""

        json_data = get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, SYNONYM_PROPERTIES))
        self.synonyms = [
         synonym["name"] for synonym in json_data] if json_data else []


    def request_comment_properties(self):
        """Give ligand object comment properties:

        .. py:attribute:: general_comments:

            General comments.

        .. py:attribute:: bioactivity_comments:

            Bioactivity comments.

        .. py:attribute:: clinical_use_comments:

            Clinical use comments.

        .. py:attribute:: mechanism_of_action_comments:

            Mechanism comments.

        .. py:attribute:: absorption_and_distribution_comments:

            Absorption and distribution comments.

        .. py:attribute:: metabolism_comments:

            Metabolism comments.

        .. py:attribute:: elimination_comments:

            Elimination comments.

        .. py:attribute:: population_pharmacokinetics_comments:

            Population kinetics comments.

        .. py:attribute:: organ_function_impairments_comments:

            Organ funciton impairment comments."""

        json_data = get_json_from_gtop(
         "ligands/%i/%s" % (self.ligand_id, COMMENT_PROPERTIES))
        self.general_comments = json_data[
         "comments"] if json_data else ""
        self.bioactivity_comments = json_data[
         "bioactivityComments"] if json_data else ""
        self.clinical_use_comments = json_data[
         "clinicalUse"] if json_data else ""
        self.mechanism_of_action_comments = json_data[
         "mechanismOfAction"] if json_data else ""
        self.absorption_and_distribution_comments = json_data[
         "absorptionAndDistribution"] if json_data else ""
        self.metabolism_comments = json_data["metabolism"] if json_data else ""
        self.elimination_comments = json_data["elimination"] if json_data else ""
        self.population_pharmacokinetics_comments = json_data[
         "populationPharmacokinetics"] if json_data else ""
        self.organ_function_impairments_comments = json_data[
         "organFunctionImpairment"] if json_data else ""
        self.mutations_and_pathophysiology_comments = json_data[
         "mutationsAndPathophysiology"] if json_data else ""


    def request_precursor_properties(self):
        """Give ligand object precursor properties:

        .. py:attribute:: precursors:

            A list of  :class:`.Precursor`: objects"""

        json_data = get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, PRECURSOR_PROPERTIES))
        self.precursors = [Precursor(p) for p in json_data] if json_data else []


    def request_all_properties(self):
        """Give ligand object all ancilliary properties."""

        self.request_structural_properties()
        self.request_molecular_properties()
        self.request_database_properties()
        self.request_synonym_properties()
        self.request_comment_properties()
        self.request_precursor_properties()


    def _get_missing_attribute_error_message(self, attribute):
        message = "'%s' is a %s property - you need to request this seperately \
        with my %s() method"
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
