#!/bin/bash

# Set root readonly
chmod -R 744 ./

# Set python read and execute
chmod -R 755 ./speakeazy/
chmod -R 755 ./config/

# Static files may be readonly
chmod -R 744 ./speakeazy/templates/
chmod -R 744 ./speakeazy/static/

# Media files must be writable
chmod -R 766 ./speakeazy/media/
chmod -R 766 ./recordings/

# One off files that need read write
chmod -R 766 ./speakeazy.db
chmod -R 766 ./speakeazy/static/css/
chmod -R 766 ./recordings

# Obviously these need execute
chmod -R 755 ./compose/**/*.sh
