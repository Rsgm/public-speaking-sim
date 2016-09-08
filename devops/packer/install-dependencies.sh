#!/bin/bash


echo ------ INSTALLING PYTHON DEPENDENCIES ------

# install python and python dependencies for later
apt-get --no-install-recommends --no-install-suggests -y install python3 python3-pip python3-pil python3-dev libjpeg-dev libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev
pip3 install --upgrade pip

# python2 may exist, set python3 as default
ln -s /usr/bin/python3 /usr/local/bin/python

# install pip dependencies
pip3 install -r /app/requirements/production.txt
