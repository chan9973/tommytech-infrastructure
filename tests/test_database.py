# Test database connectivity and migrations
from database import client, engine

def test_db_connection():
    """Test PostgreSQL connection via SQLAlchemy."""
    assert client.is_initialized()
    assert engine.pool.status() == "checked out"

def test_db_read_write():
    """Test basic read/write operations."""
    with client.connection() as conn:
        # Write
        conn.execute(client.tables.system_info.insert().values(
            key="init_test",
            value="v1.0",
            written_at="2024-01-01T00:00:00Z"
        ))
    # Read
    with client.connection() as conn:
        result = conn.execute(
            client.tables.system_info.select().where(client.tables.system_info.c.key == "init_test")
        ).fetchone()
    assert result is not None
    assert result[1] == "v1.0"

def test_vector_store_schema():
    """Test DuckDB vector store schema."""
    assert client.engine.has_table("vector_embeddings")
    assert len(client.engine.get_table_schemas()) > 0
