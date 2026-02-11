import requests
import os
import re

# REMOVED: urllib3.disable_warnings (It hides real security issues)

class FactChecker:
    def __init__(self):
        # Fix: Read from Docker Environment Variable
        self.endpoint = os.getenv("DBPEDIA_ENDPOINT", "http://dbpedia.org/sparql")
        self.weak_predicates = [
            "http://dbpedia.org/ontology/wikiPageWikiLink",
            "http://dbpedia.org/property/wikiPageUsesTemplate",
            "http://www.w3.org/2002/07/owl#sameAs",
            "http://purl.org/dc/terms/subject"
        ]

    def _sanitize_uri(self, uri):
        """Prevents SPARQL Injection by ensuring valid URI characters."""
        # Simple check: URIs shouldn't have spaces or weird control characters
        clean = re.sub(r'[^a-zA-Z0-9_:/?#=\-\.]', '', uri)
        return clean

    def verify_relationship(self, subj_uri, obj_uri):
        # Fix: Sanitize inputs
        subj_clean = self._sanitize_uri(subj_uri)
        obj_clean = self._sanitize_uri(obj_uri)

        if not subj_clean.startswith("http"): 
            subj_clean = f"http://dbpedia.org/resource/{subj_clean}"
        if not obj_clean.startswith("http"): 
            obj_clean = f"http://dbpedia.org/resource/{obj_clean}"

        query = f"SELECT ?p WHERE {{ <{subj_clean}> ?p <{obj_clean}> . }}"
        params = {"query": query, "format": "json"}
        
        try:
            # Fix: Add timeout
            response = requests.get(self.endpoint, params=params, timeout=10)
            if response.status_code != 200: return False, []
                
            data = response.json()
            bindings = data.get("results", {}).get("bindings", [])
            
            all_preds = [b["p"]["value"] for b in bindings]
            strong_preds = [p for p in all_preds if p not in self.weak_predicates]
            
            return bool(strong_preds), strong_preds

        except Exception as e:
            print(f"[FactChecker Error] {e}")
            return False, []

if __name__ == "__main__":
    checker = FactChecker()
    print("Testing FactChecker: Ronaldo -> Real Madrid...")
    exists, preds = checker.verify_relationship("Cristiano_Ronaldo", "Real_Madrid_CF")
    print(f"Verified: {exists}, Predicates: {preds}")
