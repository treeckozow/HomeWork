#!/bin/bash
# entrypoint.sh

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started."

# Start the FastAPI app using uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
