import spacy
import re
# We import the logic we built in the other files
from src.dbpedia_linker import get_best_entity

# Load Spacy
print("Loading Spacy Model...")
nlp = spacy.load("en_core_web_sm")

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def extract_entity_spans(sentence):
    """
    Finds potential entities in a sentence using Spacy.
    """
    doc = nlp(sentence)
    spans = set()
    for ent in doc.ents:
        spans.add(ent.text)
    
    # Heuristic: Merge consecutive Proper Nouns
    current = []
    for token in doc:
        if token.pos_ == "PROPN":
            current.append(token.text)
        else:
            if len(current) > 1: spans.add(" ".join(current))
            current = []
    if len(current) > 1: spans.add(" ".join(current))
    
    return list(spans)

def is_date_literal(text):
    """
    Checks if a string is just a date (so we don't try to link it to Wikipedia).
    """
    return bool(re.search(
        r'\b(\d{1,2}\s+\w+\s+\d{4}|\d{4}-\d{2}-\d{2}|\d{4})\b',
        text
    ))

# ==========================================
# TEST CASE 1: STANDARD SENTENCES
# ==========================================
def run_general_test():
    sentences = [
        "Barca won La Liga in 2015.",
        "Man City won the Premier League.",
        "Messi plays for Inter Miami."
    ]

    print("\n[TEST 1] GENERAL ENTITY LINKING")
    print("=" * 60)

    for i, sent in enumerate(sentences, 1):
        print(f"\n{i}. {sent}")
        spans = extract_entity_spans(sent)
        for span in spans:
            ent, types = get_best_entity(span)
            print(f"    {span:<20} → {ent:<30} {types[:2]}")

# ==========================================
# TEST CASE 2: THE "BALLON D'OR" CASE
# ==========================================
def run_fifa_test():
    print("\n[TEST 2] SPECIFIC CASE: FIFA BALLON D'OR")
    print("=" * 60)
    
    # We manually simulate what the Relation Extractor would find
    subject_raw = "2010 FIFA Ballon d'Or"
    relation_raw = "recipient"
    object_raw = "Lionel Messi"
    
    print(f"INPUT: {subject_raw} --[{relation_raw}]--> {object_raw}")
    
    # Run OUR Linker
    subj_label, subj_types = get_best_entity(subject_raw)
    obj_label, obj_types = get_best_entity(object_raw)
    
    print(f"    LINKED SUBJECT: {subj_label}")
    print(f"    LINKED OBJECT:  {obj_label}")
    
    if subj_label != "Unknown" and obj_label != "Unknown":
        print(f"SUCCESS: {subj_label} --[dbo:recipient]--> {obj_label}")
    else:
        print("FAILURE: Could not link entities.")

# ==========================================
# TEST CASE 3: THE "RONALDO/SPOUSE" CASE
# ==========================================
def run_neuro_symbolic_test():
    print("\n[TEST 3] PLAYER FACT VALIDATION (Neuro-Symbolic Logic)")
    print("=" * 60)

    test_cases = [
        {
            "subject": "Cristiano Ronaldo",
            "facts": [
                ("birth date", "5 February 1985", "dbo:birthDate"),
                ("spouse", "Georgina Rodríguez", "dbo:spouse") 
            ]
        }
    ]

    for case in test_cases:
        subj = case["subject"]
        subj_entity, _ = get_best_entity(subj)
        print(f"SUBJECT: {subj_entity}")

        for rel, obj, predicate in case["facts"]:
            # 1. Check if it's just a date
            if is_date_literal(obj):
                print(f"    {rel:12} -> [LITERAL DATE] \"{obj}\"")
                continue

            # 2. Link the Object
            obj_entity, obj_types = get_best_entity(obj)
            
            # 3. APPLY NEURO-SYMBOLIC LOGIC (The Fix)
            # Rule: If Relation is 'spouse' AND Types are missing, ASSUME 'Person'
            if predicate == "dbo:spouse" and not obj_types:
                obj_types = ["Person (Inferred)"] 
            
            print(f"    {rel:12} -> {subj_entity} --[{predicate}]--> {obj_entity} ({obj_types})")

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # We run all tests to show the mentor everything works
    run_general_test()
    run_fifa_test()
    run_neuro_symbolic_test()