#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --http-socket :$PORT --master --enable-threads --module netmanga_website.wsgi