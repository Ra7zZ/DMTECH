# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys 
from SPARQLWrapper import *

endpoint_url = "https://query.wikidata.org/sparql"

def get_poets_from(endpoint_url, codice):

    #rendere una stringa parametrica
    query = """SELECT ?itemLabel
    WHERE
    {
        ?item wdt:P31 wd:Q5 .
        ?item wdt:P27 wd:"""+codice+""" .
        ?item wdt:P106 wd:Q49757 .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" .}
        OPTIONAL { ?item wdt:P2561 ?nome. }
    }"""

    results = get_results(endpoint_url, query)
    return results



def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_poets_from(endpoint_url, "Q38")

#Q38 italia
#Q21 inghilterra
#Q29 spagna
#Q258 sud africa
#Q28 ungheria

for result in results["results"]["bindings"]:
    itemLabel = result["itemLabel"]
    if "xml:lang" in itemLabel:
        q = itemLabel["value"]
        print(q)
