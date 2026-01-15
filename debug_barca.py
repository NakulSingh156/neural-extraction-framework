import requests

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
HEADERS = {
    "User-Agent": "NeuralExtractionBot/1.0 (student_research_project)"
}

def debug_opensearch(term):
    print(f"--- DEBUGGING TERM: '{term}' ---")
    try:
        r = requests.get(
            WIKIPEDIA_API,
            params={
                "action": "opensearch",
                "search": term,
                "limit": 5,
                "namespace": 0,
                "format": "json"
            },
            headers=HEADERS,
            timeout=5
        )
        data = r.json()
        
        titles = data[1]
        descriptions = data[2]
        urls = data[3]
        
        print(f"Raw Response for '{term}':")
        for i, (t, d) in enumerate(zip(titles, descriptions)):
            print(f"  Result {i}: Title='{t}', Desc='{d}'")
            
    except Exception as e:
        print(f"CRASHED: {e}")

if __name__ == "__main__":
    debug_opensearch("Barca")