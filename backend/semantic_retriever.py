from pathlib import Path
import json

from sentence_transformers import SentenceTransformer
import numpy as np


KNOWLEDGE_BASE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
)

MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticRetriever:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.documents = self._load_documents()
        self.embeddings = self._create_embeddings()

    def _load_documents(self):
        with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    def _document_text(self, document):
        return " ".join(
            [
                document.get("topic", ""),
                document.get("title", ""),
                document.get("content", ""),
                " ".join(document.get("metrics", [])),
            ]
        )

    def _create_embeddings(self):
        texts = [
            self._document_text(document)
            for document in self.documents
        ]

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )

    def retrieve(self, query: str, top_k: int = 3):
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        scores = np.dot(
            self.embeddings,
            query_embedding
        )

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in top_indices:
            document = self.documents[index].copy()
            document["similarity_score"] = round(
                float(scores[index]), 4
            )
            results.append(document)

        return results


retriever = SemanticRetriever()