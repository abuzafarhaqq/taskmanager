#!/bin/sh

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Apply migrations
flask db init
flask db migrate -m "Initial migration: Users and Tasks"
flask db upgrade

# Start app
exec gunicorn -b :5000 --access-logfile - --error-logfile - taskmanager:taskmanager
