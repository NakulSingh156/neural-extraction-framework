from linker import get_best_entity, extract_entity_spans
from sentence_transformers import SentenceTransformer, util

# --- 1. RELATION EXTRACTOR LOGIC (Rebel/BERT Simulation) ---
class RelationExtractor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.predicates = {
            "dbo:team": ["plays for", "signed with", "club", "team"],
            "dbo:award": ["won", "received", "awarded", "trophy"],
            "dbo:manager": ["coached by", "under", "manager"],
            "dbo:recipient": ["received by", "awarded to"]
        }
        self.embeddings = {k: self.model.encode(v) for k, v in self.predicates.items()}

    def extract(self, text, subj, obj):
        subj_idx = text.find(subj)
        obj_idx = text.find(obj)

        # Fix: Only slice if both entities are actually found
        if subj_idx != -1 and obj_idx != -1:
            start = subj_idx + len(subj)
            end = obj_idx
            if start < end:
                phrase = text[start:end].strip()
            else:
                phrase = text # Fallback
        else:
            phrase = text # Fallback if not found

        # Semantic Match
        query_vec = self.model.encode(phrase)
        best_pred, best_score = "None", 0.0
        
        for pred, emb in self.embeddings.items():
            score = util.cos_sim(query_vec, emb).max().item()
            if score > best_score:
                best_score = score
                best_pred = pred
        
        return best_pred, best_score, phrase

# --- 2. DEMO RUNNERS ---

def run_sentence_linking_demo():
    print("\n=== SENTENCE-LEVEL ENTITY LINKING ===")
    sentences = [
        "Cristiano Ronaldo plays for Al-Nassr.",
        "Barca won La Liga in 2015.",
        "Man City won the Premier League."
    ]
    for sent in sentences:
        print(f"\nInput: {sent}")
        spans = extract_entity_spans(sent)
        for span in spans:
            ent, types = get_best_entity(span, sentence_context=sent)
            print(f"   '{span}' -> {ent} {types[:2]}")

def run_complex_extraction_demo():
    print("\n=== COMPLEX SENTENCE EXTRACTION ===")
    extractor = RelationExtractor()
    text = "Ronaldo plays for Real Madrid and they won the UCL in 2017 under Zinedine Zidane."
    
    triples = [("Ronaldo", "Real Madrid"), ("Real Madrid", "UCL"), ("Real Madrid", "Zinedine Zidane")]
    
    print(f"Sentence: {text}")
    for s, o in triples:
        pred, score, phrase = extractor.extract(text, s, o)
        print(f"   [{s}] ... [{o}] -> Phrase: '{phrase}' -> Predicate: {pred} ({score:.2f})")

if __name__ == "__main__":
    run_sentence_linking_demo()
    run_complex_extraction_demo()