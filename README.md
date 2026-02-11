# Neuro-Symbolic Extraction & Reasoning Framework (Prototype)

A **GSoC 2026 Prototype** that enhances the DBpedia extraction pipeline by adding **Context-Aware Entity Resolution**, **Neuro-Symbolic Validation**, and **Graph Reasoning**.

This repository serves as a proof-of-concept for solving the "Data Quality" and "Scalability" bottlenecks identified in the Neural Extraction Framework.

---

## 🎯 The Core Innovation

### 1. The Problem: "Smart Models, Dumb Mistakes"
Current LLM-based extractors suffer from three critical failures:
* **Ambiguity:** They can't distinguish "Man City" (Club) from "Manchester" (City) or "Barca" (Boat) from "FC Barcelona" (Club).
* **Hallucinations:** They confidently invent facts (e.g., *Elon Musk → founder of → Amazon*).
* **Shallow Reasoning:** They extract facts in isolation but fail to connect them (e.g., inferring *Messi → Spain* via *Barcelona*).

### 2. The Solution: A Hybrid Architecture
Instead of relying solely on LLMs, this prototype implements a **Neuro-Symbolic Pipeline**:
1.  **Neural Layer (Rebel/Spacy):** Handles linguistic variance (Active/Passive voice, complex sentence structures).
2.  **Symbolic Layer (DBpedia/SPARQL):** Validates facts against the ontology (Domain/Range checks) and traverses the graph for reasoning.

---

## 🚀 Key Features & Evidence

### 🛡️ 1. The "Hallucination Buster" (Ontology Validation)
**Goal:** Prevent corruption of the Knowledge Graph.
**Mechanism:** The system cross-references extracted triples against live DBpedia constraints.
* **Result:** As shown below, it validates historical facts (*Ronaldo → Real Madrid*) but automatically rejects statistically probable but false hallucinations (*Elon Musk → Amazon*).

![Hallucination Check](assets/hallucination.png)

### 🧠 2. Graph Reasoning (Six Degrees of Separation)
**Goal:** Connect disjoint entities to find hidden relationships.
**Mechanism:** Implements a client-side **BFS (Breadth-First Search)** pathfinder.
* **Result:** Successfully reconstructed the semantic chain: `Lionel Messi` → `birthPlace` → `Argentina` → `Spain`.
* **Infrastructure Note:** Public API timeouts on this query validated the need for the **Dockerized Local Endpoint** proposed for GSoC 2026.

![Graph Reasoning](assets/graph_messi.png)

### 🔍 3. Context-Aware Entity Resolution
**Goal:** Resolve slang, acronyms, and ambiguous terms without crashing.
**Mechanism:** A multi-stage resolver (Strict Redirects → Opensearch → Fuzzy Matching).
* **Result:** Correctly disambiguates entities even within dense sentences (e.g., distinguishing "Man City" the club from the city context).

![Sentence Linking](assets/sentence_linking.png)

### 🗣️ 4. Linguistic Robustness (Active vs. Passive)
**Goal:** Handle complex sentence structures as requested in the project scope.
**Mechanism:** Dynamic predicate mapping based on dependency parsing.
* **Case Study:** Validated against the specific **"Messi / Ballon d'Or"** edge case.
    * *Passive:* "Award was received by Messi" → `dbo:recipient`
    * *Active:* "Messi won the award" → `dbo:award`

![Dynamic Voice](assets/dynamic_voice.png)

---

## 📊 Benchmarks

We stress-tested the resolver against a **Mega-Benchmark** of 20 ambiguous entities (Nicknames, Acronyms, Slang).

| Category | Input | Detected As | Status |
| :--- | :--- | :--- | :--- |
| **Slang** | "Barca" | FC Barcelona | ✅ PASS |
| **Acronym** | "KSA" | Saudi Arabia | ✅ PASS |
| **Ambiguity** | "Amazon" | Amazon (Company) | ✅ PASS |
| **Context** | "Man City" | Manchester City F.C. | ✅ PASS |

![Benchmark Logs](assets/benchmark.png)

---

## 🛠️ How to Run

### Prerequisites
```bash
# Navigate to the project folder first
cd "Desktop/Neural Extraction Framework Folder"

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

```

### Running the Modules

1. **Run the Full Pipeline Test:**

```bash
python src/main.py

```

2. **Run the Reasoning Engine (Graph Visualization):**

```bash
python src/reasoning.py

```

3. **Run the Fact Checker:**

```bash
python src/validation.py

```

---

## 🔮 Roadmap for GSoC 2026

This prototype confirms the logic is sound. The next phase focuses on **Infrastructure**:

1. **Dockerization:** Containerizing this pipeline to bypass public API rate limits (Draft PR in progress).
2. **Async/Batch Processing:** Upgrading the synchronous `requests` layer to `aiohttp` for 50x throughput.