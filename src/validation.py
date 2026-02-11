import requests
import urllib3

# Suppress SSL warnings for DBpedia
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FactChecker:
    def __init__(self):
        self.endpoint = "http://dbpedia.org/sparql"
        self.weak_predicates = [
            "http://dbpedia.org/ontology/wikiPageWikiLink",
            "http://dbpedia.org/property/wikiPageUsesTemplate",
            "http://www.w3.org/2002/07/owl#sameAs",
            "http://purl.org/dc/terms/subject"
        ]

    def verify_relationship(self, subj_uri, obj_uri):
        """
        Checks if a semantic relationship exists between two URIs.
        Returns: (bool exists, list predicates)
        """
        # Ensure proper URI formatting
        if not subj_uri.startswith("http"): subj_uri = f"http://dbpedia.org/resource/{subj_uri.replace(' ', '_')}"
        if not obj_uri.startswith("http"): obj_uri = f"http://dbpedia.org/resource/{obj_uri.replace(' ', '_')}"

        query = f"""
        SELECT ?p WHERE {{
            <{subj_uri}> ?p <{obj_uri}> .
        }}
        """
        params = {"query": query, "format": "json"}
        
        try:
            response = requests.get(self.endpoint, params=params, verify=False, timeout=5)
            if response.status_code != 200: return False, []
                
            data = response.json()
            bindings = data.get("results", {}).get("bindings", [])
            
            all_preds = [b["p"]["value"] for b in bindings]
            strong_preds = [p for p in all_preds if p not in self.weak_predicates]
            
            return bool(strong_preds), strong_preds

        except Exception as e:
            return False, []

if __name__ == "__main__":
    # Quick Test
    checker = FactChecker()
    print("Testing FactChecker: Ronaldo -> Real Madrid...")
    exists, preds = checker.verify_relationship("Cristiano_Ronaldo", "Real_Madrid_CF")
    print(f"Verified: {exists}, Predicates: {preds}")
