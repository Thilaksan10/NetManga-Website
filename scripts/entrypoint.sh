#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket=/tmp/uwsgi.socket --buffer-size=32768 --master --enable-threads --module netmanga_website.wsgi