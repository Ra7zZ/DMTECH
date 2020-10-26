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



def get_film_by(nome_film):

  query1 = """SELECT ?item
       ?itemLabel
       ?publication_date
       ?imdb_code

  WHERE {

  SERVICE wikibase:mwapi
  {
     bd:serviceParam wikibase:api "Search" .
    bd:serviceParam wikibase:endpoint "www.wikidata.org" .
     bd:serviceParam mwapi:srnamespace "0" .
     bd:serviceParam mwapi:srsearch "haswbstatement:P31=Q11424 inlabel:'"""+nome_film+"""'@en" .
     ?item wikibase:apiOutputItem mwapi:title.
  }

    OPTIONAL {?item wdt:P577 ?publication_date . }
   OPTIONAL {?item wdt:P345 ?imdb_code .}
   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,it,es,de,fr,hu,ro" .
                             ?item rdfs:label ?itemLabel .}
  } group by ?item ?itemLabel ?publication_date ?imdb_code
"""

  results = get_results(endpoint_url, query1)

  titoli = []

  for result in results["results"]["bindings"]:
        titolo = result["itemLabel"]["value"]
        data = str(result["publication_date"]["value"]).split("T")
        pub_y = str(data[0])

        if "imdb_code" in result:
            imdb_cod = result["imdb_code"]["value"]
            titoli.append(dict(imdb=imdb_cod, title=titolo, data=pub_y))
        else:
            imdb_cod = "UNKNOWN"
            titoli.append(dict(imdb=imdb_cod, title=titolo, data=pub_y))

  return titoli
