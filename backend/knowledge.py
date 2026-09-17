import json
from pathlib import Path
from typing import List, Dict


KNOWLEDGE_BASE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
)


def load_knowledge_base() -> List[Dict]:
    """Load environmental knowledge from the local JSON knowledge base."""
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_evidence(query: str, top_k: int = 3) -> List[Dict]:
    """
    Retrieve the most relevant knowledge entries for an environmental query.

    Current MVP uses keyword matching.
    This will later be upgraded to embedding + pgvector retrieval.
    """
    documents = load_knowledge_base()

    query_words = set(query.lower().split())

    scored_documents = []

    for document in documents:
        searchable_text = " ".join(
            [
                document.get("topic", ""),
                document.get("title", ""),
                document.get("content", ""),
                " ".join(document.get("metrics", [])),
            ]
        ).lower()

        score = sum(
            1 for word in query_words
            if len(word) > 2 and word in searchable_text
        )

        if score > 0:
            scored_documents.append((score, document))

    scored_documents.sort(key=lambda item: item[0], reverse=True)

    return [
        document
        for score, document in scored_documents[:top_k]
    ]