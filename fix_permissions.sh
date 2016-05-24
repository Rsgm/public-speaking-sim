#!/bin/bash

# Set root readonly
chmod 755 $(find ./ -type d)
#chmod 644 $(find ./ -type f)
find ./ -type f -exec chmod 744 {} +


# Media files must be writable
chmod 777 $(find ./speakeazy/media/ -type d)
chmod 666 $(find ./speakeazy/media/ -type f)

chmod 777 $(find ./speakeazy/media/ -type d)
chmod 666 $(find ./recordings/ -type f)


# One off files that need read write
chmod 766 ./speakeazy.db
chmod 777 ./speakeazy/static/css/
chmod 766 ./speakeazy/static/js/reverse.js


# Obviously these need execute
chmod 755 ./compose/**/*.sh

