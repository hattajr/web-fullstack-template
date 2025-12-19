import os
import shlex
import shutil
import subprocess
import sys


def install_core_dependencies():
    print("Installing core dependencies...")
    try:
        command = shlex.split("uv sync")
        result = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
        print(f"Error installing core dependencies: {e}")
        sys.exit(1)

    print(f"STDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")

    if result.returncode != 0:
        print(f"Failed to install core dependencies. Exit code: {result.returncode}")
        sys.exit(1)

    print("✓ Dependencies installed successfully!")


def setup_database():
    """Set up database environment files and create dev database if database_url provided."""
    database_url = "{{ cookiecutter.database_url }}".strip()

    if not database_url:
        print("\nNo database URL provided - removing database-related files...")

        # Remove database-related directories and files
        paths_to_remove = [
            "app/db",
            "migrations",
        ]

        for path in paths_to_remove:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"  Removed directory: {path}")
                else:
                    os.remove(path)
                    print(f"  Removed file: {path}")

        print("✓ Database files removed")
        return

    print("\nSetting up database environment...")

    # Test connection using the project's Python environment (where psycopg2 is installed)
    test_connection_script = f"""
import sys
try:
    import psycopg2
    from sqlalchemy.engine.url import make_url
    
    url = make_url('{database_url}')
    conn = psycopg2.connect(
        host=url.host,
        port=url.port or 5432,
        user=url.username,
        password=url.password,
        database='postgres',
        connect_timeout=10
    )
    conn.close()
    print('  ✓ Successfully connected to PostgreSQL server at', url.host)
except Exception as e:
    print('  ✗ Failed to connect to PostgreSQL server')
    print('    Error:', str(e))
    print('\\nPlease verify:')
    print('  - PostgreSQL server is running')
    print('  - Host and port are correct')
    print('  - Credentials are valid')
    sys.exit(1)
"""

    print("Testing connection to PostgreSQL server...")
    try:
        result = subprocess.run(
            ["uv", "run", "python", "-c", test_connection_script],
            capture_output=True,
            text=True,
            timeout=15,
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"  ✗ Failed to test connection: {e}")
        sys.exit(1)

    # Parse URL using project's Python environment
    parse_url_script = f"""
from sqlalchemy.engine.url import make_url
url = make_url('{database_url}')
print(url.database)
dev_db = url.database + "_dev"
print(dev_db)
# Render with password visible
dev_url = url.set(database=dev_db)
print(dev_url.render_as_string(hide_password=False))
"""

    try:
        result = subprocess.run(
            ["uv", "run", "python", "-c", parse_url_script],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            print("  ⚠ Failed to parse DATABASE_URL")
            print(result.stderr)
            return

        lines = result.stdout.strip().split("\n")
        prod_db_name = lines[0]
        dev_db_name = lines[1]
        dev_url_str = lines[2]

        # Write to .env.prod
        env_prod_path = ".env.prod"
        if os.path.exists(env_prod_path):
            with open(env_prod_path, "a") as f:
                f.write(f"\nDATABASE_URL={database_url}\n")
            print(f"  ✓ Added DATABASE_URL to {env_prod_path}")

        # Write to .env.dev
        env_dev_path = ".env.dev"
        if os.path.exists(env_dev_path):
            with open(env_dev_path, "a") as f:
                f.write(f"\nDATABASE_URL={dev_url_str}\n")
            print(f"  ✓ Added DATABASE_URL to {env_dev_path} (database: {dev_db_name})")

        # Try to create production database using dbmate
        print(f"\nAttempting to create production database: {prod_db_name}")
        try:
            env = os.environ.copy()
            env["DATABASE_URL"] = database_url
            env["DBMATE_SCHEMA_FILE"] = "migrations/schema.sql"

            result = subprocess.run(
                ["dbmate", "create"],
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                print(f"  ✓ Production database '{prod_db_name}' created successfully")
            else:
                print("  ⚠ Could not create production database (may already exist)")
                if result.stderr:
                    print(f"    {result.stderr.strip()}")

        except FileNotFoundError:
            print("  ⚠ dbmate not found - please install it to manage migrations")
            print("    Installation: https://github.com/amacneil/dbmate#installation")
        except subprocess.TimeoutExpired:
            print("  ⚠ Database creation timed out")
        except Exception as e:
            print(f"  ⚠ Error creating production database: {e}")

        # Try to create dev database using dbmate
        print(f"\nAttempting to create development database: {dev_db_name}")
        try:
            env = os.environ.copy()
            env["DATABASE_URL"] = dev_url_str
            env["DBMATE_SCHEMA_FILE"] = "migrations/schema.sql"

            result = subprocess.run(
                ["dbmate", "create"],
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                print(f"  ✓ Development database '{dev_db_name}' created successfully")
            else:
                print("  ⚠ Could not create dev database (may already exist)")
                if result.stderr:
                    print(f"    {result.stderr.strip()}")

        except FileNotFoundError:
            print("  ⚠ dbmate not found - please install it to manage migrations")
            print("    Installation: https://github.com/amacneil/dbmate#installation")
        except subprocess.TimeoutExpired:
            print("  ⚠ Database creation timed out")
        except Exception as e:
            print(f"  ⚠ Error creating dev database: {e}")

        print("\n✓ Database environment configured")
        print(f"  Production DB: {prod_db_name}")
        print(f"  Development DB: {dev_db_name}")

    except ImportError:
        print("  ⚠ sqlalchemy not installed - skipping URL parsing")
        print("    Please install: pip install sqlalchemy")
    except Exception as e:
        print(f"  ⚠ Error setting up database: {e}")


if __name__ == "__main__":
    install_core_dependencies()
    setup_database()
