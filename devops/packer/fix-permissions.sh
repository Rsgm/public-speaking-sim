#!/bin/bash


echo ------ FIXING FILE PERMISSIONS ------

# Set root readonly
chmod 750 /app
chmod 750 $(find /app/ -type d)
find /app/ -type f -exec chmod 740 {} + # argument list was too long the other way


# Media files must be writable
chmod 770 $(find /app/speakeazy/media/ -type d)
chmod 660 $(find /app/speakeazy/media/ -type f)

# allow others to read/write recordings
chmod 776 $(find /app/recordings/ -type d)
chmod 666 $(find /app/recordings/ -type f)

# One off files
chmod 760 /app/speakeazy.db
chmod 770 /app/manage.py
chmod 770 /app/speakeazy/static/css/
chmod 770 /app/speakeazy/static/js/


chmod 750 /app/gunicorn.sh
chmod 750 /app/.env.sh
