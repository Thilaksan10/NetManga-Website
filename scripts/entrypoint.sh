#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py compress --force

uwsgi --ini /var/conf/uwsgi.ini