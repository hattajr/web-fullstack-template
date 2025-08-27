# /// script
# dependencies = [
#   "loguru",
# ]
# ///

import sqlite3
from pathlib import Path
import sys
import datetime
import os
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")

def run_migrations(db_path:Path):
    if not db_path.exists():
        logger.error(f"Database file not found: {db_path}")
        raise Exception("Database file not found")
    
    migration_dir = Path("migrations")
    if not migration_dir.exists():
        logger.error(f"Migrations directory not found: {migration_dir}")
        raise Exception("Migrations directory not found")

    conn = sqlite3.connect(db_path)
    with conn:
        cur = conn.cursor()
        # read sql file
        for sql_file in migration_dir.glob("*.sql"):
            filename = sql_file.name
            logger.info(f"Applying migration: {filename}")
            conn.execute(
                "SELECT 1 FROM schema_migrations WHERE filename = ?", (filename,)
            )
            applied = cur.fetchone()
            if applied:
                logger.info(f"Already applied: {filename}")
                continue

            with open(sql_file) as f:
                sql = f.read()

            conn.executescript(sql)
            cur.execute(
                "INSERT INTO schema_migrations (filename, applied_at) VALUES (?, ?)",
                (filename, datetime.datetime.now(datetime.timezone.utc).isoformat(" ")),
            )

if __name__ == "__main__":
    db_path = os.getenv("DATABASE_PATH")
    if not db_path:
        logger.error("DATABASE_PATH environment variable not set")
        sys.exit(1)
    
    db_path = Path(db_path)
    args = sys.argv[1:]
    if args and args[0] == "--reset":
        conn = sqlite3.connect(db_path)
        keep_table= "schema_migrations"
        with conn:
            cur = conn.cursor()
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name != '{keep_table}';")
            tables = cur.fetchall()
            for table in tables:
                cur.execute(f"DROP TABLE IF EXISTS {table[0]};")
            cur.execute(f"DELETE FROM {keep_table};")
        logger.info(f"Reset database")

    run_migrations(db_path)
