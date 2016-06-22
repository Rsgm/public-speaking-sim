#!/bin/bash

python3 /app/manage.py collectstatic_js_reverse
python3 /app/manage.py collectstatic --noinput
python3 /app/manage.py check_permissions

/usr/local/bin/gunicorn config.wsgi \
    --workers  3 \
    --worker-class gevent \
    -b 0.0.0.0:5000 \
    --chdir=/app \
    --timeout 90 \
    --log-level $GUNICORN_LOG_LEVEL \
    --access-logfile $GUNICORN_LOG_FILE
