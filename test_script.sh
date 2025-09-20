#!/bin/bash
# Exit if any command fails
set -e

# Usage check
if [ $# -lt 1 ]; then
  echo "Usage: $0 <relative/path/to/python_script.py> [args...]"
  exit 1
fi

# Get project root (parent of this script)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Target script (relative to project root)
TARGET_SCRIPT="$1"
shift  # remove first arg so $@ passes remaining args to Python script

# Ensure PYTHONPATH includes project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Run the target script with optional extra arguments
python "$PROJECT_ROOT/$TARGET_SCRIPT" "$@"

# bash test_script.sh src/application/ingest_words.py
