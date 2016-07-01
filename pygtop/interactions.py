class Interaction:

    def __init__(self, json_data):
        self.json_data = json_data

        self._interaction_id = json_data["interactionId"]
        self._ligand_id = json_data["ligandId"]
        self._target_id = json_data["targetId"]
        self._species = json_data["targetSpecies"]
        self._primary_target = json_data["primaryTarget"]
        self._endogenous = json_data["endogenous"]
        self._interaction_type = json_data["type"]
        self._action = json_data["action"]
        affinity_values = "".join(
         [char for char in json_data["affinity"] if char in "0123456789. "]
        ).split()
        affinity_values = tuple(sorted([float(val) for val in affinity_values]))
        self._affinity_low = affinity_values[0]
        self._affinity_high = affinity_values[-1]
        self._affinity_type = json_data["affinityType"]


    def __repr__(self):
        return "<Interaction (%i --> %s %i)>" % (
         self._ligand_id,
         self._species,
         self._target_id
        )


    def interaction_id(self):
        return self._interaction_id


    def ligand_id(self):
        return self._ligand_id


    def target_id(self):
        return self._target_id


    def species(self):
        return self._species


    def primary_target(self):
        return self._primary_target


    def endogenous(self):
        return self._endogenous


    def interaction_type(self):
        return self._interaction_type


    def action(self):
        return self._action


    def affinity_low(self):
        return self._affinity_low


    def affinity_high(self):
        return self._affinity_high


    def affinity_type(self):
        return self._affinity_type

'''from __future__ import division
from .gtop import *
from . import pdb
from .exceptions import NoSuchLigandError, NoSuchTargetError, NoSuchInteractionError

def get_interactions_between(ligand, target):
    """Returns a list of the interactions, if any, between a ligand and target.

    :param Ligand ligand: The interacting ligand.
    :param Target target: The interacting target (can be species-specific).
    :returns: list of :py:class:`Interaction` objects."""

    ligand_interactions = ligand.get_interactions()
    ligand_interaction_ids = [i._ligand_id for i in ligand_interactions]
    target_interactions = target.get_interactions()
    mutual_interactions = []
    for interaction in target_interactions:
        if interaction._ligand_id in ligand_interaction_ids:
            mutual_interactions.append(interaction)
    return mutual_interactions


def get_interaction_by_id(self, interaction_id):
    for interaction in self.get_interactions():
        if interaction.interaction_id == interaction_id:
            return interaction
    raise NoSuchInteractionError("%s has no interaction %i" % (str(self), interaction_id))



class Interaction:
    """A Guide to PHARMACOLOGY interaction object.

    .. py:attribute:: interaction_id:

        The interaction's GtoP ID.

    .. py:attribute:: species:

        The species in which the interaction occurs.

    .. py:attribute:: type:

        The type of interaction.

    .. py:attribute:: action:

        The interaction's action.

    .. py:attribute:: affinity_range:

        A tuple containing the ranges of affinity for this interaction.

    .. py:attribute:: affinity_value:

        A single value for the interaction's affinity (a mean if the range has multiple values).

    .. py:attribute:: affinity_type:

        The type of affinity the above values represent (IC\ :sub:`50`\  etc.).

    .. py:attribute:: is_voltage_dependent:

        Returns True if the interactions is dependent on a certain voltage.

    .. py:attribute:: voltage_range:

        A tuple containing the ranges of voltage for this interaction.

    .. py:attribute:: voltage_value:

        The voltage for voltage dependent interactions, None for other interactions.

    .. py:attribute:: ligand_primary_target:

        Returns True if the interaction represents a ligand interacting with its primary target.

    .. py:attribute:: references:

        A list of academic paper titles as strings which constitute the references for this interaction.
    """





    def get_ligand(self):
        """Returns the Ligand object for this interaction.

        :rtype: :py:class:`.Ligand`"""

        from .ligands import get_ligand_by_id
        try:
            return get_ligand_by_id(self._ligand_id)
        except NoSuchLigandError:
            return None


    def get_target(self):
        """Returns the Target object for this interaction.

        :rtype: :py:class:`.Target`"""

        from .targets import get_target_by_id
        try:
            return get_target_by_id(self._target_id)
        except NoSuchTargetError:
            return None


    @pdb.ask_about_molecupy
    def get_gtop_pdbs(self):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this interaction.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        json_data = get_json_from_gtop("targets/%i/pdbStructure" % self._target_id)
        if json_data:
            return [
             pdb["pdbCode"] for pdb in json_data
              if pdb["species"].lower() == self.species.lower()
               and pdb["ligandId"] == self._ligand_id
                and pdb["pdbCode"]
            ]
        else:
            return []


    @pdb.ask_about_molecupy
    def find_all_external_pdbs(self):
        """Queries the RSCB PDB database for PDBs containing this interaction
        by all parameters.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        ligand_external_pdbs = self.get_ligand().find_all_external_pdbs()
        target_external_pdbs = self.get_species_target().find_pdbs_by_uniprot_accession()
        return [code for code in ligand_external_pdbs if code in target_external_pdbs]


    @pdb.ask_about_molecupy
    def find_all_pdbs(self):
        """Get a list of PDB codes containing this interaction using all means
        available - annotated and external.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        ligand_pdbs = self.get_ligand().find_all_pdbs()
        target_pdbs = self.get_species_target().find_all_pdbs()
        return [code for code in ligand_pdbs if code in target_pdbs]


def value_string_to_tuple_value(s):
    if s == "-":
        return ((), None)
    else:
        if "median" in s:
            s = s.split()[0]
        range_ = tuple([float(val) for val in s.split(" &ndash; ")]
         ) if "&" in s else (float(s),)
        value = range_[0] if len(range_) == 1 else (sum(range_) / len(range_))
        return range_, value'''
