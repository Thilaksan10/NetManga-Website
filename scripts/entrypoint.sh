#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi uwsgi.ini