import json
from pathlib import Path

from backend.db import get_connection
from backend.semantic_retriever import retriever


KNOWLEDGE_BASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "knowledge_base.json"
)


def ingest_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    with get_connection() as connection:
        with connection.cursor() as cursor:

            for document in documents:
                text = retriever._document_text(document)

                embedding = retriever.model.encode(
                    text,
                    normalize_embeddings=True
                )

                cursor.execute(
                    """
                    INSERT INTO environmental_knowledge (
                        id,
                        topic,
                        title,
                        source,
                        year,
                        document_type,
                        source_url,
                        content,
                        metrics,
                        embedding
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (id)
                    DO UPDATE SET
                        topic = EXCLUDED.topic,
                        title = EXCLUDED.title,
                        source = EXCLUDED.source,
                        year = EXCLUDED.year,
                        document_type = EXCLUDED.document_type,
                        source_url = EXCLUDED.source_url,
                        content = EXCLUDED.content,
                        metrics = EXCLUDED.metrics,
                        embedding = EXCLUDED.embedding;
                    """,
                    (
                        document["id"],
                        document["topic"],
                        document["title"],
                        document["source"],
                        document.get("year"),
                        document.get("document_type"),
                        document.get("source_url"),
                        document["content"],
                        json.dumps(document.get("metrics", [])),
                        embedding,
                    )
                )

        connection.commit()

    print(
        f"Successfully ingested {len(documents)} documents."
    )


if __name__ == "__main__":
    ingest_knowledge_base()