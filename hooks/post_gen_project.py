import subprocess
import shlex
import sys
from pathlib import Path
import sqlite3
import os


# DATABASE_PATH = os.getenv("DATABASE_PATH")

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


if __name__ == "__main__":
    init_venv()
    install_core_dependencies()
    # print(DATABASE_PATH)
    # create_migration_versioning_table(DATABASE_PATH)
