class DatabaseLink:

    def __init__(self, json_data):
        self.json_data = json_data

        self.accession = json_data["accession"]
        self.database = json_data["database"]
        self.url = json_data["url"]
        self.species = json_data["species"]
