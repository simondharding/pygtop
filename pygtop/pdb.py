import requests
import xml.etree.ElementTree as ElementTree

ROOT_URL = "http://www.rcsb.org/pdb/rest/"

def query_rcsb(query_type, criteria):
    param_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    response = requests.get(
     "%s%s?%s" % (ROOT_URL, query_type, param_string)
    )
    if "xml" in response.headers["Content-Type"]:
        return ElementTree.fromstring(response.text)
    else:
        return None
