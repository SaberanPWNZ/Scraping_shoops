#!/bin/bash
# entrypoint.sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

