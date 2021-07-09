#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --chdir=./netmanga_website \ 
    --module=netmanga_website.wsgi:application \ 
    --env DJANGO_SETTINGS_MODULE=mysite.settings \ 
    --master --pidfile=/tmp/project-master.pid \
    --http-socket=127.0.0.1:$PORT \
    --processes=5 \
    --uid=1000 --gid=2000 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --home=/path/to/virtual/env \
    --daemonize=/var/log/uwsgi/netmanga.log