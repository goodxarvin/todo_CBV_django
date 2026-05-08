#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn todo_core.wsgi:application --bind 0.0.0.0:8000

exec "$@"