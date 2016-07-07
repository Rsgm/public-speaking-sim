#!/bin/bash


# Install python and python dependencies for later
apt-get -y update
apt-get --no-install-recommends --no-install-suggests -y install \
    python3 python3-pip python3-pil python3-dev libjpeg-dev libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev
pip3 install --upgrade pip
ln -s /usr/bin/python3 /usr/local/bin/python


# create non-root user
groupadd -r django
useradd -r -g django django
mkdir /app
chmod 777 /app
chown django /app


# extract speakeazy
tar -zxf /tmp/speakeazy.tar.gz -C /app

mv /app/devops/files/django/gunicorn.sh /app/gunicorn.sh
mv /app/devops/files/fix_permissions.sh /app/fix_permissions.sh

# fix speakeazy file permissions
bash /app/fix_permissions.sh

# install pip dependencies
pip3 install -r /app/requirements/production.txt
echo test1

mv /app/devops/files/django/django.service /lib/systemd/system/django.service
echo test2
systemd enable django.service
echo test3
