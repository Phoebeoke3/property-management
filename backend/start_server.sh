#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the backend directory
cd "$SCRIPT_DIR"

echo "Starting server from directory: $(pwd)"

# Start uvicorn with the correct module path
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000