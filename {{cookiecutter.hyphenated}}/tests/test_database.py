"""Example tests using testcontainers for database testing."""
{% if cookiecutter.database_url %}
import pytest
from tests.conftest import get_test_connection


def test_database_connection():
    """Test that we can connect to the test database."""
    with get_test_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            assert result[0] == 1


def test_create_and_query_table():
    """Test creating a table and inserting data."""
    with get_test_connection() as conn:
        with conn.cursor() as cur:
            # Create test table
            cur.execute("""
                CREATE TABLE test_users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
            """)
            conn.commit()

            # Insert test data
            cur.execute(
                "INSERT INTO test_users (name, email) VALUES (%s, %s)",
                ("John Doe", "john@example.com")
            )
            conn.commit()

            # Query data
            cur.execute("SELECT name, email FROM test_users WHERE name = %s", ("John Doe",))
            result = cur.fetchone()
            
            assert result[0] == "John Doe"
            assert result[1] == "john@example.com"


def test_database_is_clean_between_tests():
    """Test that database is cleaned between tests."""
    with get_test_connection() as conn:
        with conn.cursor() as cur:
            # Check that test_users table doesn't exist from previous test
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'test_users'
                )
            """)
            result = cur.fetchone()
            # Table should not exist because clean_database fixture truncates it
            # Actually, truncate doesn't drop tables, so we expect it to exist but be empty
            if result[0]:
                cur.execute("SELECT COUNT(*) FROM test_users")
                count = cur.fetchone()[0]
                assert count == 0, "Table should be empty after cleanup"
{% else %}
def test_placeholder():
    """Placeholder test when no database is configured."""
    assert True
{% endif %}
