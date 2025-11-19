#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn epp_project.wsgi:application --bind 0.0.0.0:8000
