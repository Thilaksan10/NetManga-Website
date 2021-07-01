#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --http-socket :$PORT --buffer-size=32768 --master --enable-threads --module netmanga_website.wsgi