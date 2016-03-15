"""Objects not specific to ligands or targets."""

class DatabaseLink:
    """A link to an external database, containing accession and species
    information.

    :param json_data: A dictionary obtained from the web services.

    :var accession: The Accession code.
    :var database: The Database being linked to.
    :var url: The URL for this database entry.
    :var species: The specific species the database entry refers to."""

    def __init__(self, json_data):
        self.json_data = json_data

        self.accession = json_data["accession"]
        self.database = json_data["database"]
        self.url = json_data["url"]
        self.species = None if json_data["species"] == "None" else json_data["species"]


    def __repr__(self):
        return "<%s link (%s)%s>" % (
         self.database,
         self.accession,
         " for " + self.species if self.species else ""
        )


class Precursor:
    """A precursor to a Guide to PHARMACOLOGY ligand/target.

    :param json_data: A dictionary obtained from the web services.

    :var precursor_id: GtoP ID for this precursor.
    :var gene_name: gene name.
    :var gene_symbol: gene symbol.
    :var official_gene_id: official gene ID.
    :var protein_name: protein's name.
    :var species: species.
    :var synonyms: a list of str objects."""

    def __init__(self, json_data):
        self.json_data = json_data

        self.precursor_id = json_data["precursorId"]
        self.gene_symbol = json_data["geneSymbol"]
        self.gene_name = json_data["geneName"]
        self.official_gene_id = json_data["officialGeneId"]
        self.protein_name = json_data["proteinName"]
        self.species = json_data["species"]
        self.synonyms = [s["name"] for s in json_data["synonyms"]]


    def __repr__(self):
        return "<Precursor %i (%s)>" % (self.precursor_id, self.protein_name)
