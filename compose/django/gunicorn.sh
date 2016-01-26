#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py check_permissions --noinput
/usr/local/bin/gunicorn config.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/app