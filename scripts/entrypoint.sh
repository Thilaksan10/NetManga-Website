#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi /var/conf/uwsgi.ini