"""Pytest configuration and fixtures for testing."""
{% if cookiecutter.database_url %}
import os

import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

# Set test environment variables before starting containers
os.environ.setdefault("APP_HOST", "127.0.0.1")
os.environ.setdefault("APP_PORT", "8000")
os.environ.setdefault("APP_WORKERS", "1")
os.environ.setdefault("APP_HOT_RELOAD", "false")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")

# Module-scoped PostgreSQL container - starts once for all tests
postgres_container = PostgresContainer("postgres:16-alpine")


def get_test_connection():
    """
    Get a connection to the test database container.
    
    This function should be used in tests instead of app.db.connection.get_connection()
    to ensure tests connect to the testcontainer database.
    """
    conn_url = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "")
    return psycopg2.connect(f"postgresql://{conn_url}")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database(request):
    """
    Start PostgreSQL container for all tests.
    
    This fixture runs once per test session and provides a clean
    PostgreSQL database for testing.
    """
    postgres_container.start()

    def cleanup():
        postgres_container.stop()

    request.addfinalizer(cleanup)

    # Set environment variables for database connection
    os.environ["DATABASE_URL"] = postgres_container.get_connection_url()
    
    # Reload settings to pick up the new DATABASE_URL
    import importlib
    from app.core import config
    importlib.reload(config)

    return postgres_container


@pytest.fixture(scope="function", autouse=True)
def clean_database(setup_test_database):
    """
    Clean database before each test.
    
    This ensures each test runs with a fresh database state.
    """
    import psycopg2

    # Use the container connection URL directly (strip SQLAlchemy dialect)
    conn_url = postgres_container.get_connection_url().replace("postgresql+psycopg2://", "")
    with psycopg2.connect(f"postgresql://{conn_url}") as conn:
        with conn.cursor() as cur:
            # Get all table names
            cur.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cur.fetchall()
            
            # Truncate all tables
            for (table,) in tables:
                cur.execute(f'TRUNCATE TABLE "{table}" CASCADE')
            
            conn.commit()
{% endif %}
