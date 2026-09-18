# 🌱 GroundTruth

## AI Biodiversity Intelligence Chatbot

GroundTruth is an evidence-grounded environmental intelligence system that analyzes biodiversity and ecosystem queries using semantic retrieval, multi-metric environmental reasoning, and scientific evidence.

---

## 🎯 Problem

Environmental conditions are interconnected. Changes in soil, water, climate, land use, and human pressure can jointly affect biodiversity.

GroundTruth analyzes relationships between:

- 🌱 Soil organic carbon
- 🧪 Soil pH
- 💧 Soil moisture
- 🦋 Biodiversity
- 💦 Water availability
- 🌾 Land use
- 🏭 Pollution
- 🌡️ Temperature
- 🌧️ Rainfall

It then produces actionable recommendations with supporting scientific evidence.

---

## 🧠 Architecture

```text
User Query / Environmental JSON
              ↓
           FastAPI
              ↓
         LangGraph
              ↓
      Input Validation
              ↓
       Query Embedding
              ↓
   PostgreSQL + pgvector
              ↓
      Semantic Retrieval
              ↓
     Multi-Metric Reasoning
              ↓
      Recommendation Engine
              ↓
       Evidence Validation
              ↓
     Evidence-Grounded Output
```

---

## 🔬 Key Features

### 1. Natural-Language Environmental Analysis

Users can ask questions such as:

> How can I protect biodiversity under heat and drought conditions?

The system combines the query with structured environmental measurements to perform contextual environmental analysis.

---

### 2. Retrieval-Augmented Knowledge System

GroundTruth uses:

- Sentence Transformers
- `all-MiniLM-L6-v2`
- PostgreSQL
- pgvector
- Cosine similarity
- HNSW vector indexing

The knowledge base currently contains **24 curated environmental entries**.

---

### 3. Multi-Metric Reasoning

GroundTruth identifies interactions between multiple environmental variables.

For example:

```text
High Temperature
       +
Low Rainfall
       +
Low Water Availability
       +
Low Biodiversity
       ↓
Potential Climate / Drought Stress
       ↓
Habitat + Water-Retention Recommendations
```

This allows GroundTruth to reason about combined environmental stress instead of treating each metric independently.

---

### 4. Evidence-Grounded Recommendations

Each recommendation includes:

- Action
- Scientific reasoning
- Impacted metrics
- Time horizon
- Supporting evidence
- Source
- Publication year
- Source URL
- Evidence strength

Evidence is classified as:

| Evidence Level | Meaning |
|---|---|
| `grounded` | Recommendation is directly supported by retrieved evidence |
| `related_only` | Retrieved evidence is related but does not directly support the recommendation |
| `insufficient` | Available evidence is insufficient |

---

## 📚 Knowledge Base

The knowledge base contains **24 structured environmental documents** covering:

- Soil health
- Soil biodiversity
- Agricultural biodiversity
- Agroforestry
- Habitat diversity
- Habitat fragmentation
- Climate change
- Drought
- Freshwater ecosystems
- Pollution
- Ecosystem restoration
- Crop diversification
- Pollination
- Natural pest regulation
- Climate resilience

### Scientific Sources

Sources represented include:

- FAO
- IPCC
- IPBES
- UNEP

Each knowledge record contains:

```text
id
topic
title
source
year
document_type
source_url
content
metrics
embedding
```

---

## 🗄️ Vector Database

GroundTruth uses **PostgreSQL + pgvector** for semantic retrieval.

### Embedding Model

```text
Model: all-MiniLM-L6-v2
Embedding Dimension: 384
```

An **HNSW index** is used for approximate nearest-neighbor vector search.

### Current Database Status

```text
24 documents
24 documents with embeddings
24 documents with source URLs
```

---

## 🔗 LangGraph Workflow

```text
START
  ↓
parse_input
  ↓
check_missing_data
  ↓
Missing data?
  ├── Yes → ask_for_information
  │
  └── No
        ↓
retrieve_evidence
        ↓
multi_metric_analysis
        ↓
generate_recommendations
        ↓
validate_evidence
        ↓
END
```

The workflow allows the system to identify missing environmental information before performing the full analysis.

---

## ⚡ FastAPI API

GroundTruth provides a REST API using **FastAPI**.

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API root |
| `GET` | `/health` | Health check |
| `POST` | `/recommend` | Generate environmental recommendations |

### Interactive Swagger Documentation

After starting the API, open:

```text
http://127.0.0.1:8000/docs
```

---

## 📥 Example Request

### `POST /recommend`

```json
{
  "query": "How can I protect biodiversity under heat and drought conditions?",
  "environment": {
    "temperature": 32,
    "rainfall": 400,
    "water_availability": 30,
    "biodiversity": 25
  }
}
```

The API returns environmental findings and evidence-grounded recommendations.

---

## 🧪 Evaluation

Automated tests currently cover:

- Water–biodiversity reasoning
- Temperature–biodiversity reasoning
- Rainfall–water–biodiversity reasoning
- Multi-metric reasoning
- Healthy-environment stress detection

### Current Result

```text
5/5 tests passed
Execution time: 0.03 seconds
```

Run the tests using:

```bash
python -m pytest tests/test_groundtruth.py -v
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Workflow | LangGraph |
| Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | PostgreSQL + pgvector |
| Vector Index | HNSW |
| Validation | Pydantic |
| Testing | Pytest |
| Database Container | Docker |

---

## 🚀 Local Setup

### 1. Clone

```bash
git clone https://github.com/Placid-Pixel/GroundTruth.git
cd GroundTruth
```

### 2. Create Environment

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL + pgvector

```powershell
docker run --name groundtruth-postgres `
  -e POSTGRES_USER=groundtruth `
  -e POSTGRES_PASSWORD=groundtruth123 `
  -e POSTGRES_DB=groundtruth `
  -p 5433:5432 `
  -d pgvector/pgvector:pg17
```

If the container already exists:

```bash
docker start groundtruth-postgres
```

### 5. Initialize Database

```bash
python -m backend.db
```

### 6. Ingest Knowledge Base

```bash
python -m backend.ingest
```

Expected output:

```text
Successfully ingested 24 documents.
```

### 7. Start API

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```text
GroundTruth/
│
├── backend/
│   ├── db.py
│   ├── graph.py
│   ├── ingest.py
│   ├── input_validator.py
│   ├── main.py
│   ├── models.py
│   ├── recommendation.py
│   ├── reasoning.py
│   ├── semantic_retriever.py
│   └── vector_retriever.py
│
├── data/
│   └── knowledge_base.json
│
├── evaluation/
│
├── tests/
│   └── test_groundtruth.py
│
├── docs/
│
├── requirements.txt
│
└── README.md
```

---

## ⚠️ Limitations

GroundTruth is currently a prototype.

Current limitations include:

- Environmental thresholds are screening heuristics rather than universal ecological thresholds.
- The knowledge base consists of curated evidence summaries and metadata.
- Some source URLs point to organization-level reports or landing pages rather than exact page-level citations.
- The current prototype runs locally and does not have public cloud deployment.
- Persistent conversational memory is not currently implemented.
- Geographic coordinate-aware reasoning is not currently implemented.

---

## 🔮 Future Work

Planned improvements include:

- 🧠 Persistent conversational memory
- 📍 Geographic coordinate-aware analysis
- 🛰️ Satellite/GIS data integration
- 🌦️ Real-time weather and climate data
- 📚 Larger scientific knowledge collections
- 🧬 More advanced ecological models
- 🧪 Automated evaluation datasets
- 🔄 CI/CD and cloud deployment
- 📄 Page-level scientific citations

---

## 🏆 Hackathon Alignment

| Requirement | GroundTruth Implementation |
|---|---|
| Structured Knowledge Base | 24 structured environmental documents |
| RAG / Embeddings | Sentence Transformers + pgvector |
| Scientific Evidence | FAO, IPCC, IPBES, UNEP |
| Multi-Metric Reasoning | Climate + water + biodiversity analysis |
| Actionable Recommendations | Recommendation engine |
| Evidence Grounding | Metric-to-evidence matching |
| Query Clarification | Missing-data validation |
| Structured JSON | Pydantic environmental schema |
| Evaluation | Automated pytest suite |

---

## 🌍 Example Reasoning Scenario

Given the following environmental conditions:

```json
{
  "temperature": 32,
  "rainfall": 400,
  "water_availability": 30,
  "biodiversity": 25
}
```

GroundTruth can identify relationships such as:

```text
High Temperature
        ↓
Increased Environmental Stress
        │
        ├───────────────┐
        ↓               ↓
Low Rainfall     Low Water Availability
        │               │
        └───────┬───────┘
                ↓
       Increased Ecosystem Stress
                ↓
        Reduced Biodiversity
                ↓
    Evidence-Based Recommendations
```

The recommendation engine connects the detected environmental conditions with relevant scientific evidence retrieved from the knowledge base.

---

## 📊 Core Pipeline

```text
User Input
    ↓
Input Validation
    ↓
Environmental Data Check
    ↓
Query Embedding
    ↓
Semantic Vector Retrieval
    ↓
Multi-Metric Environmental Analysis
    ↓
Recommendation Generation
    ↓
Evidence Validation
    ↓
Evidence-Grounded Response
```

GroundTruth combines **structured environmental data** with **scientific knowledge retrieval** to produce explainable recommendations.

---

## 👤 Author

**Placid-Pixel**

GitHub:

https://github.com/Placid-Pixel/GroundTruth

---

## 📌 Project Status

| Component | Status |
|---|---|
| Core RAG + Reasoning Pipeline | ✅ Complete |
| FastAPI API | ✅ Working |
| Vector Database | ✅ Working |
| Evidence Validation | ✅ Working |
| Automated Evaluation | ✅ 5/5 Tests Passing |
| Public Deployment | ⏳ Not Implemented |

---

## 🌱 GroundTruth

> **From environmental data to evidence-grounded biodiversity intelligence.**