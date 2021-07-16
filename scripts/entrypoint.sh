#!/bin/sh

set -e

python manage.py collectstatic --noinput

gunicorn netmanga_website.wsgi:application -- bind 0.0.0.0:$(PORT)