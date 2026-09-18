import os

import psycopg
from pgvector.psycopg import register_vector


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://groundtruth:groundtruth123@localhost:5433/groundtruth"
)


def get_connection():
    connection = psycopg.connect(DATABASE_URL)
    register_vector(connection)
    return connection


def initialize_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE EXTENSION IF NOT EXISTS vector;"
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS environmental_knowledge (
                    id TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    title TEXT NOT NULL,
                    source TEXT NOT NULL,
                    year INTEGER,
                    document_type TEXT,
                    source_url TEXT,
                    content TEXT NOT NULL,
                    metrics JSONB,
                    embedding VECTOR(384)
                );
                """
            )

            cursor.execute(
                """
                ALTER TABLE environmental_knowledge
                ADD COLUMN IF NOT EXISTS document_type TEXT;
                """
            )

            cursor.execute(
                """
                ALTER TABLE environmental_knowledge
                ADD COLUMN IF NOT EXISTS source_url TEXT;
                """
            )

            connection.commit()


if __name__ == "__main__":
    initialize_database()
    print("GroundTruth database initialized successfully.")