#!/bin/bash

VENV="$HOME/virgil-env-310"
ENTRYPOINT="./main.py"

# Check if we're already inside a venv
if [ -n "$VIRTUAL_ENV" ]; then
    echo "⚠️  Already in a virtual environment: $VIRTUAL_ENV"
    echo "🧠 Launching Virgil with existing Python..."
    python3 "$ENTRYPOINT" "$@"
    exit $?
fi

# Check if venv exists
if [ ! -f "$VENV/bin/activate" ]; then
    echo "❌ Virtual environment not found at $VENV"
    exit 1
fi

# Check if entrypoint exists
if [ ! -f "$ENTRYPOINT" ]; then
    echo "❌ Could not find $ENTRYPOINT"
    exit 1
fi

# Activate venv
echo "🐍 Activating Virgil's environment..."
source "$VENV/bin/activate"

