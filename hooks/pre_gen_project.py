"""Pre-generation hook for cookiecutter template validation."""

import re
import sys


def validate_database_url():
    """Validate database URL if provided."""
    database_url = "{{ cookiecutter.database_url }}".strip()

    # If no database URL provided, skip validation
    if not database_url:
        print("No database URL provided - skipping database setup")
        return

    print("Validating database URL format...")

    # Check if database name is missing (ends with port or host without a database)
    # Pattern for URL without database: postgres://user:pass@host:port or postgres://user:pass@host
    no_db_pattern = r"^postgres(?:ql)?://[^:]+:[^@]+@[^:/]+(?::\d+)?/?(?:\?.*)?$"

    if re.match(no_db_pattern, database_url):
        print("  ℹ No database name found in URL")
        print("  → Will use project name as database name")
        return

    # Validate URL format with database name
    postgres_pattern = r"^postgres(?:ql)?://[^:]+:[^@]+@[^:/]+(?::\d+)?/[^/]+(?:\?.*)?$"
    if not re.match(postgres_pattern, database_url):
        print("ERROR: Invalid DATABASE_URL format")
        print("Expected format: postgres://username:password@host:port/database_name")
        print(
            "  or: postgres://username:password@host:port (database name will be set to project name)"
        )
        print(f"Received: {database_url}")
        sys.exit(1)

    print("✓ DATABASE_URL format is valid")
    print("  Connection will be tested after dependencies are installed...")


if __name__ == "__main__":
    validate_database_url()
