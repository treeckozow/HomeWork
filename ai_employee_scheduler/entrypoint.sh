#!/bin/bash
# entrypoint.sh

set -e

echo "=== entrypoint starting ==="
echo "Working directory: $(pwd)"
echo "Contents of /app:"
ls -al /app

# Wait for PostgreSQL to start
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started."

# echo "Starting Telegram bot…"
python ./app/chat_bot/telegram_chat_bot.py &

# Start the FastAPI app using uvicorn
echo "Starting FastAPI server…"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
