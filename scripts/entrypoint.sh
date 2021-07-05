#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket :$PORT --master --enable-threads --module netmanga_website.wsgi