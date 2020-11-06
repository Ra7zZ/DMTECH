# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from bs4 import BeautifulSoup
import requests as rq

endpoint_url = "https://query.wikidata.org/sparql"

movieposterdb = "https://www.movieposterdb.com/search?category=title&q="

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_image(searchurl):
    req = rq.get(searchurl)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")

    imagelinks = []
    #quì inizia il parsing dell'html della pagina
    results = soup.findAll("img")
    for result in results:
        txt = str(result)
        if "https" in txt:
            txt=txt.split("src=\"")
            txt=txt[1].split("\" ")
            link=txt[0]
            imagelinks.append(txt)

    if(len(imagelinks)==0):
        return "UNKNOWN"
    else:
        return link


def rearrange_data(results):

    titoli = []
    for result in results["results"]["bindings"]:
      link = str(result["item"]["value"]).split("/")
      q_code = link[4]
      titolo = result["itemLabel"]["value"]
      data = str(result["publication_date"]["value"]).split("T")
      pub_y = str(data[0])

      if "imdb_code" in result:
          imdb_cod = result["imdb_code"]["value"]
          search_poster = movieposterdb + imdb_cod
          poster_link = get_image(search_poster)
      else:
          imdb_cod = "UNKNOWN"
          poster_link = "UNKNOWN"

      titoli.append(dict(q_code = q_code, imdb=imdb_cod, title=titolo, date=pub_y, poster = poster_link))

    return titoli


def get_film_by_name(nome_film):

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
   SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,it,es,de,fr,hu,ro,el,nl,pl,pt,sq" .
                             ?item rdfs:label ?itemLabel .}
  } group by ?item ?itemLabel ?publication_date ?imdb_code
"""


  results = get_results(endpoint_url, query1)

  titoli = rearrange_data(results)

  return titoli



def get_film_by_name_and_year(nome_film, pub_y):

  query2 = """SELECT ?item ?itemLabel (group_concat(distinct ?imdb_code;separator="; ") as ?imdb)  ?publication_date
#(group_concat(distinct ?publication_date;separator="; ") as ?publication_date)
WHERE {
 SERVICE wikibase:mwapi
 {
   bd:serviceParam wikibase:api "Search" .
   bd:serviceParam wikibase:endpoint "www.wikidata.org" .
   bd:serviceParam mwapi:srnamespace "0" .
   bd:serviceParam mwapi:srsearch "haswbstatement:P31=Q11424 inlabel:'star wars'@en" .
   ?item wikibase:apiOutputItem mwapi:title.
 }
  ?item wdt:P577 ?publication_date. hint:Prior hint:rangeSafe true.
  #FILTER("1996-12-31"^^xsd:dateTime < ?publication_date && ?publication_date < "1998-00-00"^^xsd:dateTime)
  FILTER(YEAR(?publication_date) < 1990)
  OPTIONAL {?item wdt:P345 ?imdb_code .}
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,it,es,de,fr,hu,ro" .
                            ?item rdfs:label ?itemLabel .}
} group by ?item ?itemLabel ?publication_date"""

  results = get_results(endpoint_url, query2)
  titoli = rearrange_data(results)
  return titoli




def get_film_by_year(pub_y):

  query3 = """SELECT ?item ?itemLabel ?ImdbLabel ?publication_date
WHERE
{
   ?item wdt:P31 wd:Q11424 .                  #istanza - film           +
   ?item wdt:P577 ?publication_date.             #anno di publicazione - variabile
   OPTIONAL {?item wdt:P345 ?Imdb}.
   FILTER (YEAR(?publication_date) = """+str(pub_y)+""")
  SERVICE wikibase:label {bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,it,es,de,fr,hu,ro,el,nl,pl,pt,sq" .}
}"""

  results = get_results(endpoint_url, query3)
  titoli = rearrange_data(results)
  return titoli
