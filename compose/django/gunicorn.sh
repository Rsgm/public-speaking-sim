#!/bin/sh
python /app/manage.py compress
python /app/manage.py collectstatic --noinput
python /app/manage.py check_permissions
/usr/local/bin/gunicorn config.wsgi -w 3 -b 0.0.0.0:5000 --chdir=/app --timeout 90 --log-level debug