#!/bin/sh
set -e

# Default DB URL if not provided
: "${DATABASE_URL:=postgresql://taskadmin:taskAdminPass123!@localhost:5432/taskmanager}"

# Wait for PostgreSQL (max 5 attempts)
echo "Waiting for Postgres..."
max_attempts=5
attempt=1

until psql "$DATABASE_URL" -c '\q' 2>/dev/null; do
  if [ $attempt -ge $max_attempts ]; then
    echo "Postgres not found after $max_attempts attempts"
    exit 1
  fi
  echo "Postgres is unavailable - sleeping (attempt $attempt/$max_attempts)"
  attempt=$((attempt + 1))
  sleep 1
done
echo "Postgres is up!"

# Ensure migrations folder exists
if [ ! -d "migrations" ]; then
  flask db init
fi

# Apply migrations safely
flask db migrate -m "Auto migration"
flask db upgrade

# Start Gunicorn
exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - taskmanager:taskmanager
