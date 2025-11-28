#!/usr/bin/env bash

# --- FIX: Go inside the sub-folder ---
cd polling_system
# -------------------------------------

# 1. Start Celery Worker in background
celery -A polling_system worker --loglevel=info --concurrency 2 &

# 2. Start Celery Beat in background
celery -A polling_system beat --loglevel=info &

# 3. Start Django (Gunicorn) in foreground
gunicorn polling_system.wsgi:application --bind 0.0.0.0:$PORT