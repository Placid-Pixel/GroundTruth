# 🌱 GroundTruth

## AI Biodiversity Intelligence Chatbot

GroundTruth is an evidence-grounded environmental intelligence system that analyzes biodiversity and ecosystem queries using semantic retrieval, multi-metric environmental reasoning, and scientific evidence.

## 🎯 Problem

Environmental conditions are interconnected. Changes in soil, water, climate, land use, and human pressure can jointly affect biodiversity.

GroundTruth analyzes relationships between:

- Soil organic carbon
- Soil pH
- Soil moisture
- Biodiversity
- Water availability
- Land use
- Pollution
- Temperature
- Rainfall

It then produces actionable recommendations with supporting evidence.

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

🔬 Key Features
Natural-language environmental analysis

Users can ask questions such as:

How can I protect biodiversity under heat and drought conditions?

The system combines the query with structured environmental measurements.

Retrieval-Augmented Knowledge System

The system uses:

Sentence Transformers
all-MiniLM-L6-v2
PostgreSQL
pgvector
cosine similarity
HNSW vector indexing

The knowledge base currently contains 24 curated environmental entries.

Multi-metric reasoning

GroundTruth identifies interactions between environmental variables.

For example:

High temperature
       +
Low rainfall
       +
Low water availability
       +
Low biodiversity
       ↓
Potential climate / drought stress
       ↓
Habitat + water-retention recommendations
Evidence-grounded recommendations

Each recommendation includes:

Action
Scientific reasoning
Impacted metrics
Time horizon
Supporting evidence
Source
Publication year
Source URL
Evidence strength

Evidence is classified as:

grounded
related_only
insufficient
📚 Knowledge Base

The knowledge base contains 24 structured environmental documents covering:

Soil health
Soil biodiversity
Agricultural biodiversity
Agroforestry
Habitat diversity
Habitat fragmentation
Climate change
Drought
Freshwater ecosystems
Pollution
Ecosystem restoration
Crop diversification
Pollination
Natural pest regulation
Climate resilience

Sources represented include:

FAO
IPCC
IPBES
UNEP

Each knowledge record contains:

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
🗄️ Vector Database

GroundTruth uses PostgreSQL + pgvector.

Embeddings are generated using:

all-MiniLM-L6-v2

Embedding dimension:

384

An HNSW index is used for approximate nearest-neighbor vector search.

Current database status:

24 documents
24 documents with embeddings
24 documents with source URLs
🔗 LangGraph Workflow
START
  ↓
parse_input
  ↓
check_missing_data
  ↓
Missing data?
  ├── Yes → ask_for_information
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

The workflow allows the system to identify missing environmental information before performing the full analysis.

⚡ FastAPI API

Endpoints:

GET  /
GET  /health
POST /recommend

Interactive Swagger documentation:

http://127.0.0.1:8000/docs

Example request:

{
  "query": "How can I protect biodiversity under heat and drought conditions?",
  "environment": {
    "temperature": 32,
    "rainfall": 400,
    "water_availability": 30,
    "biodiversity": 25
  }
}

The API returns environmental findings and evidence-grounded recommendations.

🧪 Evaluation

Automated tests currently cover:

Water–biodiversity reasoning
Temperature–biodiversity reasoning
Rainfall–water–biodiversity reasoning
Multi-metric reasoning
Healthy-environment stress detection

Current result:

5/5 tests passed
Execution time: 0.03 seconds

Run:

python -m pytest tests/test_groundtruth.py -v
🛠️ Technology Stack
Component	Technology
Language	Python
API	FastAPI
Workflow	LangGraph
Embeddings	Sentence Transformers
Embedding Model	all-MiniLM-L6-v2
Vector Database	PostgreSQL + pgvector
Vector Index	HNSW
Validation	Pydantic
Testing	Pytest
Database Container	Docker
🚀 Local Setup
1. Clone
git clone https://github.com/Placid-Pixel/GroundTruth.git
cd GroundTruth
2. Create environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Start PostgreSQL + pgvector
docker run --name groundtruth-postgres `
  -e POSTGRES_USER=groundtruth `
  -e POSTGRES_PASSWORD=groundtruth123 `
  -e POSTGRES_DB=groundtruth `
  -p 5433:5432 `
  -d pgvector/pgvector:pg17

If the container already exists:

docker start groundtruth-postgres
5. Initialize database
python -m backend.db
6. Ingest knowledge base
python -m backend.ingest

Expected:

Successfully ingested 24 documents.
7. Start API
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

Then open:

http://127.0.0.1:8000/docs
📁 Project Structure
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
├── tests/
│   └── test_groundtruth.py
├── docs/
├── requirements.txt
└── README.md
⚠️ Limitations

GroundTruth is currently a prototype.

Environmental thresholds are screening heuristics rather than universal ecological thresholds.
The knowledge base consists of curated evidence summaries and metadata.
Some source URLs point to organization-level reports or landing pages rather than exact page-level citations.
The current prototype runs locally and does not have public cloud deployment.
Persistent conversational memory and geographic coordinate-aware reasoning are future extensions.
🔮 Future Work

Planned improvements include:

Persistent conversational memory
Geographic coordinate-aware analysis
Satellite/GIS data integration
Real-time weather and climate data
Larger scientific knowledge collections
More advanced ecological models
Automated evaluation datasets
CI/CD and cloud deployment
Page-level scientific citations
🏆 Hackathon Alignment
Requirement	GroundTruth Implementation
Structured knowledge base	24 structured environmental documents
RAG / embeddings	Sentence Transformers + pgvector
Scientific evidence	FAO, IPCC, IPBES, UNEP
Multi-metric reasoning	Climate + water + biodiversity analysis
Actionable recommendations	Recommendation engine
Evidence grounding	Metric-to-evidence matching
Query clarification	Missing-data validation
Structured JSON	Pydantic environmental schema
Evaluation	Automated pytest suite
👤 Author

Placid-Pixel

GitHub:
https://github.com/Placid-Pixel/GroundTruth

Project Status

Core RAG + reasoning pipeline: Complete

FastAPI API: Working

Vector database: Working

Evidence validation: Working

Automated evaluation: 5/5 tests passing

Public deployment: Not implemented in current prototype