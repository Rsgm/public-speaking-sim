#!/bin/bash


echo fixing file permissions

# Set root readonly
chmod 755 $(find /app/ -type d)
find /app/ -type f -exec chmod 744 {} + # argument list was too long the other way


# Media files must be writable
chmod 777 $(find /app/speakeazy/media/ -type d)
chmod 666 $(find /app/speakeazy/media/ -type f)

chmod 777 $(find /app/recordings/ -type d)
chmod 666 $(find /app/recordings/ -type f)


# One off files
chmod 766 /app/speakeazy.db
chmod 777 /app/manage.py
chmod 777 /app/speakeazy/static/css/
chmod 777 /app/speakeazy/static/js/


chmod 755 /app/gunicorn.sh
chmod 755 /app/.env.sh
