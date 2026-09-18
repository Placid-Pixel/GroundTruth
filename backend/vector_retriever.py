from backend.db import get_connection
from backend.semantic_retriever import retriever


def retrieve_from_pgvector(query: str, top_k: int = 5):
    """
    Retrieve the most semantically similar environmental documents
    from PostgreSQL using pgvector cosine distance.

    Args:
        query: Natural-language environmental query.
        top_k: Number of documents to retrieve.

    Returns:
        List of retrieved documents with similarity scores
        and source metadata.
    """

    # Create embedding for the user's query
    query_embedding = retriever.model.encode(
        query,
        normalize_embeddings=True
    )

    # Search PostgreSQL + pgvector
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    topic,
                    title,
                    source,
                    year,
                    document_type,
                    source_url,
                    content,
                    metrics,
                    1 - (embedding <=> %s) AS similarity_score
                FROM environmental_knowledge
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT %s;
                """,
                (
                    query_embedding,
                    query_embedding,
                    top_k,
                )
            )

            rows = cursor.fetchall()

    # Convert database rows into dictionaries
    results = []

    for row in rows:
        results.append({
            "id": row[0],
            "topic": row[1],
            "title": row[2],
            "source": row[3],
            "year": row[4],
            "document_type": row[5],
            "source_url": row[6],
            "content": row[7],
            "metrics": row[8],
            "similarity_score": round(
                float(row[9]),
                4
            ),
        })

    return results