#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket :8000 --buffer-size=32768 --master --enable-threads --module netmanga_website.wsgi