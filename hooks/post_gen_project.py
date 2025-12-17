import subprocess
import shlex
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


if __name__ == "__main__":
    install_core_dependencies()
    # print(DATABASE_PATH)
    # create_migration_versioning_table(DATABASE_PATH)
