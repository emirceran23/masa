#!/usr/bin/env bash
# Initialize the database: run Alembic migrations and seed data.
set -euo pipefail

echo "⏳  Running Alembic migrations..."
cd "$(dirname "$0")/../backend"
alembic upgrade head

echo "⏳  Seeding initial data..."
cd "$(dirname "$0")/.."
python scripts/seed-data.py

echo "✅  Database initialized."
