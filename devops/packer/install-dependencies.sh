#!/bin/bash


echo ------ INSTALLING PYTHON DEPENDENCIES ------

# install python and python dependencies for later
apt-get --no-install-recommends --no-install-suggests -y install python3 python3-pip python3-pil python3-dev \
    libjpeg-dev libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev

# todo: remove once https://github.com/bread-and-pepper/django-userena/pull/530 and https://github.com/boto/boto/pull/3607 are merged
apt-get --no-install-recommends --no-install-suggests -y install git


# python2 may exist, set python3 as default
ln -s /usr/bin/python3 /usr/local/bin/python

# install pip dependencies
pip3 install --upgrade pip

pip install google-compute-engine  # needed before building boto, todo: remove once https://github.com/boto/boto/pull/3607 is merged
# fixes using python2.7 google_compute_engine library, todo: move to end after above is fixed
python3 -c "from google_compute_engine.boto.boto_config import BotoConfig; BotoConfig()"

pip3 install -r /app/requirements/production.txt
