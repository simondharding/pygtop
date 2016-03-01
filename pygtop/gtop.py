import json
import requests

ROOT_URL = "http://www.guidetopharmacology.org/services/"

STRUCTURAL_PROPERTIES = "structure"
MOLECULAR_PROPERTIES = "molecularProperties"
DATABASE_PROPERTIES = "databaseLinks"
SYNONYM_PROPERTIES = "synonyms"
COMMENT_PROPERTIES = "comments"
PRECURSOR_PROPERTIES = "precursors"


def get_json_from_gtop(query):
    response = requests.get("%s%s" % (ROOT_URL, query))
    if response.status_code == 200 and len(response.text) > 1:
        return json.loads(response.text)
    else:
        # Try ONE more time...
        response = requests.get("%s%s" % (ROOT_URL, query))
        if response.status_code == 200 and len(response.text) > 1:
            return json.loads(response.text)
