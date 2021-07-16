#!/bin/sh

set -e

python manage.py collectstatic --noinput

gunicorn netmanga_website.wsgi:application 