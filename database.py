"""
TommyTech Infrastructure Database Client.
Uses PostgreSQL (psycopg2) for vector embeddings storage
and DuckDB as a secondary analytical layer.
"""

import duckdb
import os
import sqlalchemy
from sqlalchemy import create_engine, text

ENV = os.getenv("DATABASE_URL", "postgresql://postgres:localhost@localhost:5432/tommytech")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_store.duckdb")


def get_duckdb_engine():
    """Get DuckDB engine for local vector analytics."""
    return create_engine(f"duckdb:///{VECTOR_DB_PATH}", isolation_level='AUTOCOMMIT')


def initialize_system_info_table(client):
    """Create system_info table for tracking infrastructure state."""
    with client.connection() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS system_info (
                    id SERIAL PRIMARY KEY,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT,
                    written_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )


def get_vector_store_schema(client):
    """Get DuckDB vector embeddings table schema."""
    with get_duckdb_engine().connect() as conn:
        result = conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS vector_embeddings (
                    id INTEGER PRIMARY KEY,
                    content_id TEXT NOT NULL,
                    embedding_vector DOUBLE PRECISION[],
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )
        return "vector_embeddings"


def upsert_vector_embedding(content_id, embedding_vector, metadata=None):
    """Upsert a vector embedding into DuckDB."""
    with get_duckdb_engine().connect() as conn:
        conn.execute(
            text(
                """
                INSERT INTO vector_embeddings (content_id, embedding_vector, metadata)
                VALUES (%s, %s, %s)
                ON CONFLICT (content_id) DO UPDATE
                SET embedding_vector = EXCLUDED.embedding_vector,
                    metadata = COALESCE(Excluded.metadata, vector_embeddings.metadata)
                """
            ),
            (content_id, str(embedding_vector), str(metadata) if metadata else None),
        )
        conn.commit()


def upsert_system_info(client, key: str, value: str):
    """Upsert system info for tracking infrastructure state."""
    with client.connection() as conn:
        conn.execute(
            text(
                """
                INSERT INTO system_info (key, value)
                VALUES (%s, %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
                """
            ),
            (key, value),
        )
        conn.commit()


def get_system_info(client, key: str):
    """Get system info by key."""
    with client.connection() as conn:
        result = conn.execute(
            text(
                "SELECT value FROM system_info WHERE key = :key",
                {"key": key},
            )
        ).fetchone()
    return result[0] if result else None


def get_vector_by_content_id(content_id: str):
    """Get vector embedding by content ID."""
    with get_duckdb_engine().connect() as conn:
        result = conn.execute(
            text(
                "SELECT embedding_vector FROM vector_embeddings WHERE content_id = %s",
                (content_id,),
            )
        ).fetchone()
    if result:
        import numpy as np
        return list(np.array(result[0]))
    return None


class InfrastructureClient:
    """Unified infrastructure client for PostgreSQL/DuckDB operations."""

    def __init__(self):
        self.engine = create_engine(
            ENV,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        self.vector_engine = get_duckdb_engine()
        return
