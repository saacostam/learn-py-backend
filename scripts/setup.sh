#!/usr/bin/env bash

set -euo pipefail

echo "Installing dependencies..."
uv sync

echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Running pre-commit..."
uv run pre-commit run --all-files

echo "Setup complete."
