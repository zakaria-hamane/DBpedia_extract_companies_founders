import json
from SPARQLWrapper import SPARQLWrapper, JSON

def get_organization_founders():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?organization ?org_name ?founder ?founder_name
        WHERE {
            ?organization dbo:foundedBy ?founder .
            ?organization rdf:type dbo:Company .
            ?organization rdfs:label ?org_name .
            ?founder rdfs:label ?founder_name .
            FILTER (lang(?org_name) = 'en' && lang(?founder_name) = 'en')
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    organizations_and_founders = []
    for result in results["results"]["bindings"]:
        organization = result["organization"]["value"].replace("http://dbpedia.org/resource/", "")
        organization_url = result["organization"]["value"]
        founder = result["founder"]["value"].replace("http://dbpedia.org/resource/", "")
        founder_url = result["founder"]["value"]
        organizations_and_founders.append({"organization": organization, "organization_url": organization_url, "founder": founder, "founder_url": founder_url})

    return organizations_and_founders

def save_to_json(organizations_and_founders, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(organizations_and_founders, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    org_founders = get_organization_founders()
    save_to_json(org_founders, 'organizations_and_founders.json')
