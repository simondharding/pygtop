import json
import requests
import warnings
warnings.filterwarnings("ignore")

ROOT_URL = "http://www.guidetopharmacology.org/services/"

STRUCTURAL_PROPERTIES = "structure"
MOLECULAR_PROPERTIES = "molecularProperties"
DATABASE_PROPERTIES = "databaseLinks"
SYNONYM_PROPERTIES = "synonyms"
COMMENT_PROPERTIES = "comments"
PRECURSOR_PROPERTIES = "precursors"


def get_json_from_gtop(query):
    warnings.filterwarnings("ignore")
    response = requests.get("%s%s" % (ROOT_URL, query))
    if response.status_code == 200 and len(response.text) > 1:
        return json.loads(response.text)
    else:
        # Try ONE more time...
        warnings.filterwarnings("ignore")
        response = requests.get("%s%s" % (ROOT_URL, query))
        if response.status_code == 200 and len(response.text) > 1:
            return json.loads(response.text)
