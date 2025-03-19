#!/bin/bash
# entrypoint.sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec gunicorn --bind 0.0.0.0:8000 scraper.wsgi:application