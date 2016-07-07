from .exceptions import NoSuchLigandError, NoSuchTargetError, NoSuchInteractionError
from . import gtop
from .pdb import ask_about_molecupy

def get_interaction_by_id(self, interaction_id):
    if not isinstance(interaction_id, int):
        raise TypeError("interaction_id must be int, not '%s'" % str(interaction_id))
    for interaction in self.interactions():
        if interaction.interaction_id() == interaction_id:
            return interaction
    raise NoSuchInteractionError("%s has no interaction %i" % (str(self), interaction_id))


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
        self._affinity_low = affinity_values[0] if affinity_values else None
        self._affinity_high = affinity_values[-1] if affinity_values else None
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


    def ligand(self):
        """Returns the Ligand object for this interaction.

        :rtype: :py:class:`.Ligand`"""

        from .ligands import get_ligand_by_id
        try:
            return get_ligand_by_id(self._ligand_id)
        except NoSuchLigandError:
            return None


    def target_id(self):
        return self._target_id


    def target(self):
        """Returns the Target object for this interaction.

        :rtype: :py:class:`.Target`"""

        from .targets import get_target_by_id
        try:
            return get_target_by_id(self._target_id)
        except NoSuchTargetError:
            return None


    @ask_about_molecupy
    def gtop_pdbs(self):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this interaction.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        json_data = gtop.get_json_from_gtop("targets/%i/pdbStructure" % self._target_id)
        if json_data:
            return [
             pdb["pdbCode"] for pdb in json_data
              if pdb["species"].lower() == self._species.lower()
               and pdb["ligandId"] == self._ligand_id
                and pdb["pdbCode"]
            ]
        else:
            return []


    @ask_about_molecupy
    def all_external_pdbs(self):
        """Queries the RSCB PDB database for PDBs containing this interaction
        by all parameters.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        ligand_external_pdbs = self.ligand().all_external_pdbs()
        target_external_pdbs = self.target().uniprot_pdbs(species=self.species())
        return [code for code in ligand_external_pdbs if code in target_external_pdbs]


    @ask_about_molecupy
    def all_pdbs(self):
        """Get a list of PDB codes containing this interaction using all means
        available - annotated and external.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        ligand_pdbs = self.ligand().all_pdbs()
        target_pdbs = self.target().all_pdbs(species=self.species())
        return [code for code in ligand_pdbs if code in target_pdbs]


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
