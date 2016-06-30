"""Contains ligand-specific objects and functions."""

from . import gtop
from .exceptions import NoSuchLigandError
from .shared import DatabaseLink

def get_ligand_by_id(ligand_id):
    """Returns a Ligand object of the ligand with the given ID.

    :param int ligand_id: The GtoP ID of the Ligand desired.
    :rtype: :py:class:`Ligand`
    :raises: :class:`.NoSuchLigandError` if no such ligand exists in the database"""

    if not isinstance(ligand_id, int):
        raise TypeError("ligand_id must be int, not '%s'" % str(ligand_id))
    json_data = gtop.get_json_from_gtop("ligands/%i" % ligand_id)
    if json_data:
        return Ligand(json_data)
    else:
        raise NoSuchLigandError("There is no ligand with ID %i" % ligand_id)


def get_all_ligands():
    """Returns a list of all ligands in the Guide to PHARMACOLOGY database. This
    can take a few seconds.

    :returns: list of :py:class:`Ligand` objects"""

    json_data = gtop.get_json_from_gtop("ligands")
    return [Ligand(l) for l in json_data]


def get_ligands_by(criteria):
    """Get all ligands which specify the criteria dictionary.

    :param dict criteria: A dictionary of `field=value` pairs. See the\
     `GtoP ligand web services page <http://www.guidetopharmacology.org/\
     webServices.jsp#ligands>`_ for key/value pairs which can be supplied.
    :returns: list of :py:class:`Ligand` objects."""

    if not isinstance(criteria, dict):
        raise TypeError("criteria must be dict, not '%s'" % str(criteria))

    search_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    json_data = gtop.get_json_from_gtop("ligands?%s" % search_string)
    if json_data:
        return [Ligand(l) for l in json_data]
    else:
        return []


def get_ligand_by_name(name):
    """Returns the ligand which matches the name given.

    :param str name: The name of the ligand to search for. Note that synonyms \
    will not be searched.
    :rtype: :py:class:`Ligand`
    :raises:  :class:`.NoSuchLigandError` if no such ligand exists in the database."""

    if not isinstance(name, str):
        raise TypeError("name must be str, not '%s'" % str(name))
    ligands = get_ligands_by({"name": name})
    if ligands:
        return ligands[0]
    else:
        raise NoSuchLigandError("There is no ligand with name %s" % name)



def get_ligands_by_smiles(smiles, search_type="exact", cutoff=0.8):
    """Search for ligands by SMILES string.

    :param str smiles: The SMILES string to search with.
    :param str search_type: The type of search. Viable options are ``"exact"``, \
    ``"substructure"`` or ``"similarity"``.
    :param float cutoff: If performing a similarity search, this is the cutoff \
    used for similarity. The default is 0.8 and the maximum is 1.
    :returns: list of :py:class:`Ligand` objects."""

    if not isinstance(smiles, str):
        raise TypeError("smiles must be str, not '%s'" % str(smiles))
    if not isinstance(search_type, str):
        raise TypeError("search_type must be str, not '%s'" % str(search_type))
    if search_type not in ["exact", "substructure", "similarity"]:
        raise ValueError("'%s' is not a valud search type" % search_type)
    if not isinstance(cutoff, int) and not isinstance(cutoff, float):
        raise TypeError("cutoff must be numeric, not '%s'" % str(cutoff))
    if not 0 <= cutoff <= 1:
        raise ValueError("cutoff must be between 0 and 1, not %s" % (str(cutoff)))

    query = "ligands/%s/smiles?smiles=%s%s" % (
     search_type,
     smiles,
     "similarityGt=%f" % cutoff if search_type == "similarity" else ""
    )
    json_data = gtop.get_json_from_gtop(query)
    if json_data:
        return [Ligand(l) for l in json_data]
    else:
        return []



class Ligand:

    def __init__(self, json_data):
        self.json_data = json_data
        self._ligand_id = json_data["ligandId"]
        self._name = json_data["name"]
        self._abbreviation = json_data["abbreviation"] if json_data["abbreviation"] else None
        self._inn = json_data["inn"]
        self._ligand_type = json_data["type"]
        self._species = json_data["species"]
        self._radioactive = json_data["radioactive"]
        self._labelled = json_data["labelled"]
        self._approved = json_data["approved"]
        self._withdrawn = json_data["withdrawn"]
        self._approval_source = json_data["approvalSource"]
        self._subunit_ids = json_data["subunitIds"]
        self._complex_ids = json_data["complexIds"]
        self._prodrug_ids = json_data["prodrugIds"]
        self._active_drug_ids = json_data["activeDrugIds"]


    def __repr__(self):
        return "<Ligand %i (%s)>" % (self._ligand_id, self._name)


    def ligand_id(self):
        return self._ligand_id


    def name(self):
        return self._name


    def abbreviation(self):
        return self._abbreviation


    def inn(self):
        return self._inn


    def ligand_type(self):
        return self._ligand_type


    def species(self):
        return self._species


    def radioactive(self):
        return self._radioactive


    def labelled(self):
        return self._labelled


    def approved(self):
        return self._approved


    def withdrawn(self):
        return self._withdrawn


    def approval_source(self):
        return self._approval_source


    def subunit_ids(self):
        return self._subunit_ids


    def subunits(self):
        return [get_ligand_by_id(id_) for id_ in self._subunit_ids]


    def complex_ids(self):
        return self._complex_ids


    def complexes(self):
        return [get_ligand_by_id(id_) for id_ in self._complex_ids]


    def prodrug_ids(self):
        return self._prodrug_ids


    def prodrugs(self):
        return [get_ligand_by_id(id_) for id_ in self._prodrug_ids]


    def active_drug_ids(self):
        return self._active_drug_ids


    def active_drugs(self):
        return [get_ligand_by_id(id_) for id_ in self._active_drug_ids]


    def iupac_name(self):
        return self._get_structure_json().get("iupacName")


    def smiles(self):
        return self._get_structure_json().get("smiles")


    def inchi(self):
        return self._get_structure_json().get("inchi")


    def inchi_key(self):
        return self._get_structure_json().get("inchiKey")


    def one_letter_sequence(self):
        return self._get_structure_json().get("oneLetterSeq")


    def three_letter_sequence(self):
        return self._get_structure_json().get("threeLetterSeq")


    def post_translational_modifications(self):
        return self._get_structure_json().get("postTranslationalModifications")


    def chemical_modifications(self):
        return self._get_structure_json().get("chemicalModifications")


    def hydrogen_bond_acceptors(self):
        return self._get_molecular_json().get("hydrogenBondAcceptors")


    def hydrogen_bond_donors(self):
        return self._get_molecular_json().get("hydrogenBondDonors")


    def rotatable_bonds(self):
        return self._get_molecular_json().get("rotatableBonds")


    def topological_polar_surface_area(self):
        return self._get_molecular_json().get("topologicalPolarSurfaceArea")


    def molecular_weight(self):
        return self._get_molecular_json().get("molecularWeight")


    def log_p(self):
        return self._get_molecular_json().get("logP")


    def lipinski_rules_broken(self):
        return self._get_molecular_json().get("lipinskisRuleOfFive")


    def synonyms(self):
        return [synonym["name"] for synonym in self._get_synonym_json()]


    def general_comments(self):
        return self._get_comments_json().get("comments")


    def bioactivity_comments(self):
        return self._get_molecular_json().get("bioactivityComments")


    def clinical_use_comments(self):
        return self._get_molecular_json().get("clinicalUse")


    def mechanism_of_action_comments(self):
        return self._get_molecular_json().get("mechanismOfAction")


    def absorption_and_distribution_comments(self):
        return self._get_molecular_json().get("absorptionAndDistribution")


    def metabolism_comments(self):
        return self._get_molecular_json().get("metabolism")


    def elimination_comments(self):
        return self._get_molecular_json().get("elimination")


    def population_pharmacokinetics_comments(self):
        return self._get_molecular_json().get("populationPharmacokinetics")


    def organ_function_impairments_comments(self):
        return self._get_molecular_json().get("organFunctionImpairment")


    def mutations_and_pathophysiology_comments(self):
        return self._get_molecular_json().get("mutationsAndPathophysiology")


    def database_links(self):
        return [DatabaseLink(link_json) for link_json in self._get_database_json()]


    def _get_structure_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/structure" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_molecular_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/molecularProperties" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_synonym_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/synoynms" % self._ligand_id
        )
        return json_object if json_object else []


    def _get_comments_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/comments" % self._ligand_id
        )
        return json_object if json_object else {}


    def _get_database_json(self):
        json_object = gtop.get_json_from_gtop(
         "ligands/%i/databaseLinks" % self._ligand_id
        )
        return json_object if json_object else []




'''





class Ligand:
    """A Guide to PHARMACOLOGY ligand object.

    :param json_data: A dictionary obtained from the web services.

    .. py:attribute:: ligand_id:

        The ligand's GtoP ID.

    .. py:attribute:: name:

        The ligand's name.

    .. py:attribute:: abbreviation:

        The ligand's abbreviated name.

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
    """


    def get_interactions(self):
        """Returns a list of all interactions which this ligand is involved in.

        :returns: list of :py:class:`.Interaction` objects"""

        from .interactions import Interaction
        interactions_json = gtop.get_json_from_gtop(
         "/ligands/%i/interactions" % self.ligand_id
        )
        if interactions_json:
            return [Interaction(json) for json in interactions_json]
        else:
            return []


    get_interaction_by_id = interactions.get_interaction_by_id
    """Returns an Interaction object of a given ID belonging to the ligand.

    :param int interaction_id: The interactions's ID.
    :rtype: :py:class:`.Interaction`
    :raises: :class:`.NoSuchInteractionError`: if no such interaction exists in the database."""


    def get_targets(self):
        """Returns a list of all targets which this ligand interacts with.

        :returns: list of :py:class:`.Target` objects"""

        targets = []
        for interaction in self.get_interactions():
            target = interaction.get_target()
            if target not in targets:
                targets.append(target)
        return targets


    def get_species_targets(self):
        """Returns a list of all species-specific targets which this ligand interacts with.

        :returns: list of :py:class:`.SpeciesTarget` objects"""

        species_targets = []
        for interaction in self.get_interactions():
            species_target = interaction.get_species_target()
            if species_target not in species_targets:
                species_targets.append(species_target)
        return species_targets


    @pdb.ask_about_molecupy
    def get_gtop_pdbs(self):
        """Returns a list of PDBs which the Guide to PHARMACOLOGY says contain
        this ligand.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        pdbs = []
        for interaction in self.get_interactions():
            for pdb in interaction.get_gtop_pdbs():
                if pdb not in pdbs:
                    pdbs.append(pdb)
        return pdbs


    @pdb.ask_about_molecupy
    def find_pdbs_by_smiles(self, search_type="exact"):
        """Queries the RSCB PDB database with the ligand's SMILES string.

        :param str search_type: The type of search to run - whether exact matches\
        only should be returned.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if "smiles" not in self.__dict__:
            self.request_structural_properties()
        if self.smiles:
            xml = pdb.query_rcsb("smilesQuery", {
             "smiles": self.smiles,
             "search_type": search_type
            })
            if xml:
                ligand_elements = list(xml[0])
                return [element.attrib["structureId"] for element in ligand_elements]
            else:
                return []
        else:
            return []


    @pdb.ask_about_molecupy
    def find_pdbs_by_inchi(self):
        """Queries the RSCB PDB database with the ligand's InChI string.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if "inchi" not in self.__dict__:
            self.request_structural_properties()
        if self.inchi:
            results = pdb.query_rcsb_advanced("ChemCompDescriptorQuery", {
             "descriptor": self.inchi,
             "descriptorType": "InChI"
            })
            return results if results else []
        else:
            return []


    @pdb.ask_about_molecupy
    def find_pdbs_by_name(self, comparator="equals"):
        """Queries the RSCB PDB database with the ligand's name.

        :param str comparator: The type of search to run - whether exact matches\
        only should be returned, or substrings etc.
        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        results = pdb.query_rcsb_advanced("ChemCompNameQuery", {
         "comparator": comparator.title(),
         "name": self.name,
         "polymericType": "Any"
        })
        return results if results else []


    @pdb.ask_about_molecupy
    def find_pdbs_by_sequence(self):
        """Queries the RSCB PDB database with the ligand's amino acid sequence,\
        if that ligand is a peptide.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        if "one_letter_sequence" not in self.__dict__:
            self.request_structural_properties()
        if self.one_letter_sequence:
            results = pdb.query_rcsb_advanced("SequenceQuery", {
             "sequence": self.one_letter_sequence,
             "eCutOff": "0.01",
             "searchTool": "blast",
             "sequenceIdentityCutoff": "100"
            })
            return results if results else []
        else:
            return []


    @pdb.ask_about_molecupy
    def find_all_external_pdbs(self):
        """Queries the RSCB PDB database by all parameters.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.find_pdbs_by_smiles() +
         self.find_pdbs_by_inchi() +
         self.find_pdbs_by_name() +
         self.find_pdbs_by_sequence()
        ))


    @pdb.ask_about_molecupy
    def find_all_pdbs(self):
        """Get a list of PDB codes using all means available - annotated and
        external.

        :param bool as_molecupy: Returns the PDBs as \
        `molecuPy <http://molecupy.readthedocs.io>`_ PDB objects.
        :returns: list of ``str`` PDB codes"""

        return list(set(
         self.get_gtop_pdbs() +
         self.find_all_external_pdbs()
        ))


    def find_in_pdb_by_smiles(self, molecupy_pdb):
        self.request_structural_properties()
        if self.smiles:
            formula = Counter([char.upper() for char in self.smiles
             if char.isalpha() and char.upper() != "H"])
            for molecule in molecupy_pdb.model.small_molecules:
                if molecule.get_formula() == formula:
                    return molecule


    def find_in_pdb_by_name(self, molecupy_pdb):
        if self.name:
            for molecule in molecupy_pdb.model.small_molecules:
                molecule_name = molecupy_pdb.data_file.het_names.get(molecule.molecule_name)
                if molecule_name and self.name.lower() == molecule_name.lower():
                    return molecule


    def find_in_pdb_by_mass(self, molecupy_pdb):
        self.request_molecular_properties()
        if self.molecular_weight:
            molecules = sorted(
             list(molecupy_pdb.model.small_molecules),
             key=lambda k: abs(k.get_mass() - self.molecular_weight)
            )
            if molecules and -40 < (molecules[0].get_mass() - self.molecular_weight) < 40:
                return molecules[0]


    def find_in_pdb_by_peptide_string(self, molecupy_pdb):
        if "inchi" not in self.__dict__: self.request_structural_properties()
        if self.one_letter_sequence:
            for chain in molecupy_pdb.model.chains:
                if self.one_letter_sequence in chain.get_sequence_string() and 0.9 <= (
                 len(self.one_letter_sequence) / len(chain.get_sequence_string())
                ) <= 1:
                    return chain


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

        json_data = gtop.get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, gtop.STRUCTURAL_PROPERTIES))
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

            Log of partition coefficient - a measure of solubility.

        .. py:attribute:: lipinksi_rules_broken:

            Number of Lipinski's rules the ligand breaks (a measure of druglikeness)."""

        json_data = gtop.get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, gtop.MOLECULAR_PROPERTIES))
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

            A list of  :class:`.DatabaseLink` objects."""

        json_data = gtop.get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, gtop.DATABASE_PROPERTIES))
        self.database_links = [
         DatabaseLink(link) for link in json_data] if json_data else []


    def request_synonym_properties(self):
        """Give ligand object synonym properties:

        .. py:attribute:: synonyms:

            A list of synonym :py:class:`str` objects."""

        json_data = gtop.get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, gtop.SYNONYM_PROPERTIES))
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

        json_data = gtop.get_json_from_gtop(
         "ligands/%i/%s" % (self.ligand_id, gtop.COMMENT_PROPERTIES))
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

            A list of  :class:`.Precursor` objects"""

        json_data = gtop.get_json_from_gtop("ligands/%i/%s" % (
         self.ligand_id, gtop.PRECURSOR_PROPERTIES))
        self.precursors = [Precursor(p) for p in json_data] if json_data else []



'''
