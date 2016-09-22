#!/bin/bash


echo ------ FIXING FILE PERMISSIONS ------

#
#chown -R django:django /app
#
## Set root readonly
#chmod 500 /app
#chmod 500 $(find /app/ -type d)
#find /app/ -type f -exec chmod 500 {} + # argument list was too long the other way
#
#
## Media files must be writable
##chmod 700 $(find /app/speakeazy/media/ -type d)
##chmod 600 $(find /app/speakeazy/media/ -type f)
#
## allow others to read/write recordings
##chmod 700 $(find /app/recordings/ -type d)
##chmod 600 $(find /app/recordings/ -type f)
#
## One off files
#chmod 500 /app/manage.py
#chmod 400 /app/speakeazy/static/css/
#chmod 400 /app/speakeazy/static/js/
#
#
## non-local files
#chmod 400 /app/devops/files/**
#chmod 500 /app/devops/files/**/*.sh
#chmod 400 /app/.env.sh


chown -R django:django /app

# Set root readonly
chmod -R 700 /app
