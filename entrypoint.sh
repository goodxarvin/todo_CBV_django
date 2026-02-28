#!/bin/sh

until pg_isready -h db -p 5432; do
    echo "Waiting for database to be ready..."
    sleep 2
done

echo "Database is ready, running migrations..."


python manage.py migrate
python manage.py collectstatic --noinput
gunicorn todo_core.wsgi:application --bind 0.0.0.0:8000

exec "$@"