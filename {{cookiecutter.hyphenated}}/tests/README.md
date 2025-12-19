# Testing with Testcontainers

Use [Testcontainers](https://testcontainers-python.readthedocs.io/) to test business logic in `app/services/` with a real PostgreSQL database in Docker. The test database automatically loads migrations from `migrations/` directory. Each test runs with a clean database state via `get_test_connection()` from `conftest.py`.

## How It Works

1. `conftest.py` starts a PostgreSQL container once per test session
2. Automatically runs all migration files from `migrations/` directory (excluding `schema.sql`)
3. Each test gets a clean database via the `clean_database` fixture that truncates all tables
4. Tests use `get_test_connection()` to connect to the test database

## Example

**migrations/20231201_create_customers.sql**
```sql
-- migrate:up
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- migrate:down
DROP TABLE customers;
```

**app/services/customer.py**
```python
def add_customer(conn, name, email):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM customers WHERE email = %s", (email,))
        if cur.fetchone():
            raise ValueError(f"Customer with email {email} already exists")
        
        cur.execute(
            "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id, name, email",
            (name, email)
        )
        row = cur.fetchone()
        conn.commit()
        return {"id": row[0], "name": row[1], "email": row[2]}


def get_customer_by_id(conn, customer_id):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, email FROM customers WHERE id = %s", (customer_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "email": row[2]}
```

**tests/test_customer.py**
```python
import pytest
from tests.conftest import get_test_connection
from app.services.customer import add_customer, get_customer_by_id


def test_add_customer():
    with get_test_connection() as conn:
        customer = add_customer(conn, name="John Doe", email="john@example.com")
        
        assert customer["id"] is not None
        assert customer["name"] == "John Doe"
        assert customer["email"] == "john@example.com"


def test_get_customer_by_id():
    with get_test_connection() as conn:
        created = add_customer(conn, name="John Doe", email="john@example.com")
        customer = get_customer_by_id(conn, created["id"])
        
        assert customer is not None
        assert customer["name"] == "John Doe"
        assert customer["email"] == "john@example.com"
```

## Running Tests

```bash
# Run all tests
uv run --env-file .env.dev pytest

# Run specific test file
uv run --env-file .env.dev pytest tests/test_customer.py

# Run with verbose output
uv run --env-file .env.dev pytest -v

# Run with coverage
uv run --env-file .env.dev pytest --cov=app
```

## Resources

- [Getting Started with Testcontainers for Python](https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/) - Real use case examples
- [Testcontainers Python Documentation](https://testcontainers-python.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
