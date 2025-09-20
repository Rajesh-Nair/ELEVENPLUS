#!/usr/bin/env python3
import sys
from pathlib import Path
import runpy

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <relative/path/to/python_script.py> [args...]")
        sys.exit(1)

    # 1. Get project root (folder containing this launcher)
    project_root = Path(__file__).resolve().parent

    # 2. Target script relative to project root
    target_script = project_root / sys.argv[1]

    if not target_script.exists():
        print(f"Error: Script not found: {target_script}")
        sys.exit(1)

    # 3. Add project root to sys.path temporarily
    sys.path.insert(0, str(project_root))

    # 4. Pass remaining arguments to the target script
    sys.argv = [str(target_script)] + sys.argv[2:]

    # 5. Run the target script as if python ran it directly
    runpy.run_path(str(target_script), run_name="__main__")

if __name__ == "__main__":
    main()


# python test.py src/application/ingest_words.py
