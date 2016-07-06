"""Objects not specific to ligands or targets."""

import re

class DatabaseLink:
    """A link to an external database, containing accession and species
    information.

    :param json_data: A dictionary obtained from the web services.

    .. py:attribute:: accession:

        The Accession code.

    .. py:attribute:: database:

        The Database being linked to.

    .. py:attribute:: url:

        The URL for this database entry.

    .. py:attribute:: species:

        The specific species the database entry refers to."""

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



class Gene:

    def __init__(self, json_data):
        self.json_data = json_data

        self.target_id = json_data["targetId"]
        self.species = json_data["species"]
        self.gene_symbol = json_data["geneSymbol"]
        self.gene_name = json_data["geneName"]
        self.official_gene_id = json_data["officialGeneId"]
        self.genomic_location = json_data["genomicLocation"]
        self.amino_acids = int(json_data["aminoAcids"]) if json_data["aminoAcids"] else 0
        self.transmembrane_domains = int(json_data["transmembraneDomains"]) if json_data["transmembraneDomains"] else 0
        self.pore_loops = int(json_data["poreLoops"]) if json_data["poreLoops"] else 0


    def __repr__(self):
        return "<%s Gene (%s)>" % (self.species, self.gene_symbol)



def strip_html(func):
    cleaner = re.compile("<.*?>")
    def new_func(*args, strip_html=False, **kwargs):
        name = func(*args, **kwargs)
        if strip_html:
            return re.sub(cleaner, "", name).replace("&ndash;", "–")
        else:
            return name
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    return new_func
