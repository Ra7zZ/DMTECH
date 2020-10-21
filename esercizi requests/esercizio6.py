# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"


def get_film(endpoint_url, year):

    query = """SELECT ?item ?itemLabel ?ImdbLabel ?ddp
WHERE
{
   ?item wdt:P31 wd:Q11424 .                  #istanza - film
   ?item wdt:P495 wd:Q38 .                #origine - italiana
   ?item wdt:P577 ?ddp.             #anno di publicazione - variabile
   OPTIONAL {?item wdt:P345 ?Imdb}.  #OPTIONAL ammette record vuoti perciò è possibile che alcuni non abbiano il codice imdb indicato
                                     #altrimenti senza OPTIONAL taglierebbe i risultati senza luogo di nascita
   FILTER (YEAR(?ddp) ="""+str(year)+""")
  SERVICE wikibase:label {bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it,en" .}
}"""
    risultati = get_results(endpoint_url, query)
    return risultati



def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_film_of(anno):

    results = get_film(endpoint_url, anno)
    film = {}
    for result in results["results"]["bindings"]:
        if "ImdbLabel" in result:
            titolo = result["itemLabel"]["value"]
            data = str(result["ddp"]["value"]).split("T")
            pub_y = str(data[0])
            imdb_cod = result["ImdbLabel"]["value"]
            if imdb_cod not in film:
                film[imdb_cod] = {"title" : titolo, "data" : pub_y}
            else:
                film[imdb_cod]["data"] = [film[imdb_cod].get("data")]
                film[imdb_cod]["data"].append(pub_y)
    print(film)
    #return results


"""'item': {'type': 'uri', 'value': 'http://www.wikidata.org/entity/Q305839'},
'ddp': {'datatype': 'http://www.w3.org/2001/XMLSchema#dateTime', 'type': 'literal', 'value': '1940-01-01T00:00:00Z'},
'itemLabel': {'xml:lang': 'it', 'type': 'literal', 'value': 'Abbandono'},
'ImdbLabel': {'type': 'literal', 'value': 'tt0032180'}"""
