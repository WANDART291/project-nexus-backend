#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies (This is in the root, so we run it first)
pip install -r requirements.txt

# --- FIX: Go inside the sub-folder ---
cd polling_system
# -------------------------------------

# Convert static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate