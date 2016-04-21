import requests
import xml.etree.ElementTree as ElementTree

ROOT_URL = "http://www.rcsb.org/pdb/rest/"

advanced_search_xml = """<orgPdbQuery>
    <queryType>org.pdb.query.simple.%s</queryType>
        %s
</orgPdbQuery>"""

def query_rcsb(query_type, criteria):
    param_string = "&".join(["%s=%s" % (key, criteria[key]) for key in criteria])
    response = requests.get(
     "%s%s?%s" % (ROOT_URL, query_type, param_string)
    )
    if "xml" in response.headers["Content-Type"]:
        return ElementTree.fromstring(response.text)
    else:
        return None


def query_rcsb_advanced(query_type, criteria):
    param_elements = "\n".join(["<%s>%s</%s>" % (key, criteria[key], key) for key in criteria])
    query_xml = advanced_search_xml % (query_type, param_elements)
    response = requests.post(
     "%ssearch" % ROOT_URL,
     data=query_xml.encode(),
     headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if "problem" not in response.text.lower():
        return response.text.split()
    else:
        return None
