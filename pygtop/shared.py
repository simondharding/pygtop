class DatabaseLink:

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
