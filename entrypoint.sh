# entrypoint.sh
#!/bin/sh
set -e

echo "Applying migrations..."
python manage.py migrate

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000