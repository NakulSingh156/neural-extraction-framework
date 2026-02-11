import requests
import re
from rapidfuzz import fuzz
import spacy

# Load Spacy for NER
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("⚠️ Warning: Spacy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
DBPEDIA_LOOKUP = "https://lookup.dbpedia.org/api/search"
DBPEDIA_SPARQL = "https://dbpedia.org/sparql"

STOPWORDS = {"fc", "club", "sc", "the", "of", "and", "in", "inc"}
EXCLUDED_FOR_ORG = {"Season", "Event", "Tournament", "Competition"}

TYPE_PRIOR = {
    "Person": 1.8, "Athlete": 1.9, "Politician": 1.8, "Artist": 1.7,
    "Company": 1.9, "Organisation": 1.7,
    "SportsTeam": 2.0, "FootballClub": 2.1, "SoccerClub": 2.1,
    "Place": 1.7, "City": 1.7, "Country": 1.7,
    "SportsLeague": 1.8, "SoccerLeague": 1.8,
    "Album": 1.5, "Film": 1.4, "Work": 1.2,
    "Event": 0.3, "Season": 0.05, "List": 0.01
}

def clean_label(label):
    label = re.sub('<[^<]+?>', '', label)
    label = re.sub(r'\s*\(.*?\)', '', label)
    return label.strip()

def expand_alias(term):
    """Data-driven alias expansion using Wikipedia Search."""
    term = term.strip()
    if len(term) > 25: return term
    try:
        r = requests.get(WIKIPEDIA_API, params={
            "action": "query", "list": "search", "srsearch": term, "format": "json", "srlimit": 1
        }).json()
        results = r.get("query", {}).get("search", [])
        return results[0]["title"] if results else term
    except:
        return term

def resolve_redirect(term):
    """Resolves Wikipedia redirects (e.g. UK -> United Kingdom)."""
    if len(term.split()) > 5 or term.isdigit(): return term
    try:
        r = requests.get(WIKIPEDIA_API, params={
            "action": "opensearch", "search": term, "limit": 5, "namespace": 0, "format": "json"
        }).json()
        titles, descriptions = r[1], r[2]
        for title, desc in zip(titles, descriptions):
            if "disambiguation" not in desc.lower() and (title.lower() != term.lower() or desc):
                return title
    except:
        pass
    return term

def context_score(sentence, candidate_label):
    return fuzz.token_set_ratio(sentence.lower(), candidate_label.lower()) / 100.0

def get_best_entity(query, sentence_context=None):
    if query.isdigit() and len(query) == 4: return query, ["xsd:gYear"]
    
    query = expand_alias(query)
    clean_query = resolve_redirect(query)
    
    candidates = [clean_query]
    if "fc" not in clean_query.lower(): candidates.append(clean_query + " FC")

    all_matches = []
    for term in candidates:
        try:
            r = requests.get(DBPEDIA_LOOKUP, params={"query": term, "format": "json", "MaxHits": 15}).json()
            for doc in r.get("docs", []):
                raw_label = doc.get("label", [""])[0]
                label = clean_label(raw_label)
                if label.startswith("List of"): continue

                lex = fuzz.token_set_ratio(clean_query.lower(), label.lower()) / 100.0
                if lex < 0.65: continue

                types = doc.get("typeName", [])
                refCount = int(doc.get("refCount", [0])[0])
                
                type_bonus = max([TYPE_PRIOR.get(t, 1.0) for t in types], default=1.0)
                popularity = 1 + min(refCount / 8000, 1.0)
                ctx = 1.0
                if sentence_context:
                    ctx = 0.7 + (0.6 * context_score(sentence_context, label))

                score = lex * type_bonus * popularity * ctx
                all_matches.append({"label": label, "types": types, "score": score})
        except: continue

    if not all_matches: return "Unknown", []
    best = max(all_matches, key=lambda x: x["score"])
    return best["label"], best["types"]

def extract_entity_spans(sentence):
    if not nlp: return []
    doc = nlp(sentence)
    spans = set([ent.text for ent in doc.ents])
    # Fallback: Merge consecutive PROPNs
    current = []
    for token in doc:
        if token.pos_ == "PROPN": current.append(token.text)
        else:
            if len(current) > 1: spans.add(" ".join(current))
            current = []
    if len(current) > 1: spans.add(" ".join(current))
    
    normalized = set([s.lstrip("the ").strip() for s in spans])
    return list(normalized)
