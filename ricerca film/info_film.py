# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"



def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def print_film_info(Qcode):

    query = """SELECT ?item ?itemLabel 
        (GROUP_CONCAT(distinct ?directorLabel;separator="; ") AS ?directors) 
        (GROUP_CONCAT(distinct ?screenwriterLabel;separator="; ") AS ?screenwriter)
        ?imdb_code
        #?publication_date
        (GROUP_CONCAT(distinct ?castLabel;separator="; ") AS ?cast)
        #(GROUP_CONCAT(distinct ?pdLabel;separator="; ") AS ?pd)
        (GROUP_CONCAT(distinct ?pub_countryLabel;separator="; ") AS ?pub_country)
        (GROUP_CONCAT(distinct ?distributorLabel;separator="; ") AS ?distributor)
        (GROUP_CONCAT(distinct ?genreLabel;separator="; ") AS ?genre)  
WHERE {
  
  VALUES ?item {wd:"""+str(Qcode)+"""}
  ?item wdt:P31 ?P31 
  #OPTIONAL {?item wdt:P577 ?pd}
  OPTIONAL {?item wdt:P345 ?imdb_code .}
  OPTIONAL {?item wdt:P57 ?director .}
  OPTIONAL {?item wdt:P136 ?genre .}
  OPTIONAL {?item wdt:P58 ?screenwriter .}
  OPTIONAL {?item wdt:P495 ?pub_country .}
  OPTIONAL {?item wdt:P161 ?cast .}
  OPTIONAL {?item wdt:P750 ?distributor .}
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,it,es,de,fr,hu,ro,nl" .
                            ?item rdfs:label ?itemLabel .
                            ?director rdfs:label ?directorLabel .
                            ?screenwriter rdfs:label ?screenwriterLabel.
                             ?pub_country rdfs:label ?pub_countryLabel.
                             ?imdb_code rdfs:label ?imdb_code.
                             ?genre rdfs:label ?genreLabel.
                               ?cast rdfs:label ?castLabel.
                                ?distributor rdfs:label ?distributorLabel.}
                           #?pd rdfs:label ?pdLabel.}
} group by ?item ?itemLabel ?imdb_code ?genreLabel ?distributorLabel ?pub_country #?pdLabel
"""

    results = get_results(endpoint_url, query)

    #print(results)
    info = []

    for result in results["results"]["bindings"]:

        titolo = result["itemLabel"]["value"]
        director = result["directors"]["value"].split("; ")
        screenwriter = result["screenwriter"]["value"].split("; ")

        if "imdb_code" in result:
            imdb_cod = result["imdb_code"]["value"]
        else:
            imdb_cod = "UNKNOWN"

        if "country" in result:
            country = result["pub_country"]["value"]
        else:
            country = "UNKNOWN"

        if "cast" in result:
            cast = result["cast"]["value"].split("; ")
        else:
            cast = "UNKNOWN"

        if "distributor" in result:
            distributor = result["distributor"]["value"]
        else:
            distributor = "UNKNOWN"

        if "genre" in result:
            genre = result["genre"]["value"]
        else:
            genre = "UNKNOWN"

        info.append(dict(title=titolo, imdb=imdb_cod, director = director, screenwriter = screenwriter, country = country, distributor = distributor, genre = genre, cast = cast))

        return info
