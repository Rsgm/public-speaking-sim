#!/bin/bash


echo fixing file permissions

# Set root readonly
chmod 755 $(find ./ -type d)
find ./ -type f -exec chmod 744 {} + # argument list was too long the other way


# Media files must be writable
chmod 777 $(find ./speakeazy/media/ -type d)
chmod 666 $(find ./speakeazy/media/ -type f)

chmod 777 $(find ./speakeazy/media/ -type d)
chmod 666 $(find ./recordings/ -type f)


# One off files
chmod 766 ./speakeazy.db
chmod 777 ./manage.py
chmod 777 ./speakeazy/static/css/
chmod 777 ./speakeazy/static/js/


# Obviously these need execute
chmod 755 ./compose/**/*.sh

