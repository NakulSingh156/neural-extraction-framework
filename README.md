# DBpedia Entity Linker & Resolver (Prototype)

**A Neuro-Symbolic Entity Linking pipeline that resolves ambiguous short-forms, acronyms, and slang (e.g., "Barca", "UK") to their canonical DBpedia URIs.**

It solves the "Link Linking" problem where standard tools fail on colloquialisms by leveraging a **Hybrid Wikipedia Strategy** (Strict Redirects + Opensearch) before applying fuzzy matching and type inference.

## Pipeline Architecture

```mermaid
graph LR
    A[Input Text] --> B(Named Entity Recognition)
    B --> C{Hybrid Resolver}
    C -- Exact Redirect --> D[Wiki Redirect API]
    C -- Slang/Fuzzy --> E[Wiki Opensearch API]
    D & E --> F[Candidate Scoring]
    F --> G[Neuro-Symbolic Validation]
    G --> H[Final DBpedia URI]
(Note: If the diagram above doesn't render on your viewer, it represents the flow from Spacy NER -> Wikipedia API -> DBpedia Lookup -> Final Scoring.)

How to Run
Clone and Install dependencies:

Bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
Run the Main Pipeline (includes 3 demo test suites):

Bash
python src/main.py
📊 Example Outputs
The system handles three distinct levels of difficulty:

Input Entity	Detected As	Strategy Used
"UK"	United Kingdom	Strict Redirect (Wikipedia API)
"Barca"	FC Barcelona	Opensearch (Autocomplete API)
"Man City"	Manchester City F.C.	Fuzzy Matching + Type Scoring
"Georgina Rodríguez"	Person (Inferred)	Neuro-Symbolic Relation Inference
⚠️ Known Limitations
Context Blindness: The current resolver is context-agnostic. It may link "Champions League" to the most popular Wikipedia result (UEFA) even if the context implies another sport, though the Opensearch fallback mitigates this.

API Rate Limits: Relies on live Wikipedia/DBpedia APIs. Heavy usage requires caching (planned for GSoC '26).

Benchmarks
A curated dataset of 50 sentences covering Sports, Politics, and Tech is included in benchmarks/sentences.json to test the resolver's robustness against real-world variance.


---

### 2. The Benchmark Dataset (`benchmarks/sentences.json`)
You need to show you care about **data**.
1. Create a folder named `benchmarks`.
2. Inside it, create `sentences.json`.
3. Paste this massive list. It covers every edge case we discussed.

```json
[
  {
    "id": 1,
    "text": "Cristiano Ronaldo plays for Al-Nassr in the Saudi Pro League.",
    "focus": ["Cristiano Ronaldo", "Al-Nassr"]
  },
  {
    "id": 2,
    "text": "Lionel Messi won his 8th Ballon d'Or after the World Cup.",
    "focus": ["Lionel Messi", "Ballon d'Or"]
  },
  {
    "id": 3,
    "text": "Barca won La Liga in 2015 with MSN leading the attack.",
    "focus": ["Barca", "La Liga"]
  },
  {
    "id": 4,
    "text": "Man City won the Premier League under Pep Guardiola.",
    "focus": ["Man City", "Premier League", "Pep Guardiola"]
  },
  {
    "id": 5,
    "text": "Real Madrid is the king of the Champions League.",
    "focus": ["Real Madrid", "Champions League"]
  },
  {
    "id": 6,
    "text": "The UK decided to leave the EU after the Brexit vote.",
    "focus": ["UK", "EU", "Brexit"]
  },
  {
    "id": 7,
    "text": "JFK was the 35th president of the USA.",
    "focus": ["JFK", "USA"]
  },
  {
    "id": 8,
    "text": "NASA plans to send humans to Mars by 2040.",
    "focus": ["NASA", "Mars"]
  },
  {
    "id": 9,
    "text": "Elon Musk acquired Twitter and rebranded it to X.",
    "focus": ["Elon Musk", "Twitter", "X"]
  },
  {
    "id": 10,
    "text": "OpenAI released ChatGPT, changing the AI landscape.",
    "focus": ["OpenAI", "ChatGPT", "AI"]
  },
  {
    "id": 11,
    "text": "KSA is investing heavily in NEOM.",
    "focus": ["KSA", "NEOM"]
  },
  {
    "id": 12,
    "text": "Man Utd fans are unhappy with the Glazers.",
    "focus": ["Man Utd", "Glazers"]
  },
  {
    "id": 13,
    "text": "PSG signed Neymar for a record transfer fee.",
    "focus": ["PSG", "Neymar"]
  },
  {
    "id": 14,
    "text": "The iPhone 15 features a USB-C port.",
    "focus": ["iPhone 15", "USB-C"]
  },
  {
    "id": 15,
    "text": "Taylor Swift's Eras Tour became a global phenomenon.",
    "focus": ["Taylor Swift", "Eras Tour"]
  },
  {
    "id": 16,
    "text": "Formula 1 is growing rapidly in the US.",
    "focus": ["Formula 1", "US"]
  },
  {
    "id": 17,
    "text": "Max Verstappen dominates the grid with Red Bull.",
    "focus": ["Max Verstappen", "Red Bull"]
  },
  {
    "id": 18,
    "text": "Lewis Hamilton drives for Mercedes.",
    "focus": ["Lewis Hamilton", "Mercedes"]
  },
  {
    "id": 19,
    "text": "Ferrari needs to fix their strategy calls.",
    "focus": ["Ferrari"]
  },
  {
    "id": 20,
    "text": "Google DeepMind is working on Gemini.",
    "focus": ["Google DeepMind", "Gemini"]
  },
  {
    "id": 21,
    "text": "Microsoft invested billions in OpenAI.",
    "focus": ["Microsoft", "OpenAI"]
  },
  {
    "id": 22,
    "text": "AWS controls a large share of the cloud market.",
    "focus": ["AWS"]
  },
  {
    "id": 23,
    "text": "The UN discussed climate change at COP28.",
    "focus": ["UN", "COP28"]
  },
  {
    "id": 24,
    "text": "NATO is expanding its membership in Europe.",
    "focus": ["NATO", "Europe"]
  },
  {
    "id": 25,
    "text": "Bitcoin reached a new all-time high.",
    "focus": ["Bitcoin"]
  },
  {
    "id": 26,
    "text": "Ethereum is moving to proof-of-stake.",
    "focus": ["Ethereum"]
  },
  {
    "id": 27,
    "text": "The Beatles are the best-selling band in history.",
    "focus": ["The Beatles"]
  },
  {
    "id": 28,
    "text": "Harry Potter was written by J.K. Rowling.",
    "focus": ["Harry Potter", "J.K. Rowling"]
  },
  {
    "id": 29,
    "text": "Game of Thrones is based on books by GRRM.",
    "focus": ["Game of Thrones", "GRRM"]
  },
  {
    "id": 30,
    "text": "The NBA finals were watched by millions.",
    "focus": ["NBA"]
  },
  {
    "id": 31,
    "text": "LeBron James plays for the Lakers.",
    "focus": ["LeBron James", "Lakers"]
  },
  {
    "id": 32,
    "text": "Curry changed the game with his 3-point shooting.",
    "focus": ["Curry"]
  },
  {
    "id": 33,
    "text": "The NFL Super Bowl halftime show was spectacular.",
    "focus": ["NFL", "Super Bowl"]
  },
  {
    "id": 34,
    "text": "Tom Brady is considered the GOAT of football.",
    "focus": ["Tom Brady", "GOAT"]
  },
  {
    "id": 35,
    "text": "Federer has retired from professional tennis.",
    "focus": ["Federer"]
  },
  {
    "id": 36,
    "text": "Nadal is known as the King of Clay.",
    "focus": ["Nadal"]
  },
  {
    "id": 37,
    "text": "Djokovic holds the record for most Grand Slams.",
    "focus": ["Djokovic", "Grand Slams"]
  },
  {
    "id": 38,
    "text": "Kohli is a legend of Indian Cricket.",
    "focus": ["Kohli", "Indian Cricket"]
  },
  {
    "id": 39,
    "text": "The IPL is the richest cricket league.",
    "focus": ["IPL"]
  },
  {
    "id": 40,
    "text": "Dhoni led CSK to another title.",
    "focus": ["Dhoni", "CSK"]
  },
  {
    "id": 41,
    "text": "COVID-19 changed global work culture.",
    "focus": ["COVID-19"]
  },
  {
    "id": 42,
    "text": "WHO declared the end of the pandemic emergency.",
    "focus": ["WHO"]
  },
  {
    "id": 43,
    "text": "The ISS orbits the Earth every 90 minutes.",
    "focus": ["ISS", "Earth"]
  },
  {
    "id": 44,
    "text": "Einstein developed the theory of relativity.",
    "focus": ["Einstein"]
  },
  {
    "id": 45,
    "text": "Turing is the father of modern computing.",
    "focus": ["Turing"]
  },
  {
    "id": 46,
    "text": "Python is the most popular language for Data Science.",
    "focus": ["Python", "Data Science"]
  },
  {
    "id": 47,
    "text": "React is maintained by Meta.",
    "focus": ["React", "Meta"]
  },
  {
    "id": 48,
    "text": "Linux powers most of the web servers.",
    "focus": ["Linux"]
  },
  {
    "id": 49,
    "text": "Docker simplified containerization.",
    "focus": ["Docker"]
  },
  {
    "id": 50,
    "text": "Kubernetes orchestrates container deployment.",
    "focus": ["Kubernetes"]
  }
]
3. Your requirements.txt

Just in case you forgot this file, create requirements.txt and add:

Plaintext
requests==2.31.0
spacy==3.7.2
rapidfuzz==3.6.1