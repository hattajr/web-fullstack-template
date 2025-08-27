import subprocess
import shlex
import sys
from pathlib import Path
import sqlite3


DATABASE_PATH = "data/{{ cookiecutter.project_name }}.db"

def init_venv():
    # logger.info("Initializing virtual environment...")
    uv_command = "uv init --bare"
    args = shlex.split(uv_command)
    result = subprocess.run(args, capture_output=True, text=True)
    # logger.debug(result.stdout)
    # logger.debug(result.stderr)
    if result.returncode != 0:
        # logger.error("Failed to initialize virtual environment.")
        sys.exit(1)

def install_core_dependencies():
    # logger.info("Installing core dependencies...")
    dev_dependencies = [
        "aiosqlite",
        "fastapi",
        "pydantic",
        "uvicorn",
        "jinja2",
        "python-multipart",
        "loguru"
    ]
    command = shlex.split(f"uv add {' '.join(dev_dependencies)}")
    result = subprocess.run(command, capture_output=True, text=True)
    # logger.debug(result.stdout)
    # logger.debug(result.stderr)

    if result.returncode != 0:
        # logger.error("Failed to install core dependencies.")
        sys.exit(1)

def create_migration_versioning_table(db_file_path):
    # SQLite
    # logger.info("Creating migration versioning...")
    db_file_path = Path(db_file_path)

    sql_schema_migration = """
        PRAGMA foreign_keys = ON;
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -20000;

        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename TEXT PRIMARY KEY,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
    
    conn = sqlite3.connect(db_file_path)
    with conn:
        conn.executescript(sql_schema_migration)
    
    # logger.info("Migration versioning table created.")

if __name__ == "__main__":
    init_venv()
    install_core_dependencies()
    create_migration_versioning_table(DATABASE_PATH)
