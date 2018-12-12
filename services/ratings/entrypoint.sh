#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z ratings-db 5433; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0
