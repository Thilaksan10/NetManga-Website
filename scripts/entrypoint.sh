#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --http-socket --buffer-size=32768 --master --enable-threads --module netmanga_website.wsgi