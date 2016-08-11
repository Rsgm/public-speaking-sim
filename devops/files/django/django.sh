#!/bin/bash


# install python and python dependencies for later
apt-get -y update
apt-get --no-install-recommends --no-install-suggests -y install \
    python3 python3-pip python3-pil python3-dev libjpeg-dev libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev
pip3 install --upgrade pip
ln -s /usr/bin/python3 /usr/local/bin/python


# create non-root user
groupadd -r django
useradd -r -g django django
mkdir /app
chown django:django /app


# extract speakeazy
tar -zxf /tmp/django.tar.gz -C /app


# setup vsftp
apt-get --no-install-recommends --no-install-suggests -y install vsftpd
mv /app/devops/files/django/vsftpd.conf /etc/vsftpd.conf
echo anonymous > /etc/vsftpd.allowed_users
systemd enable vsftpd.service

mkdir /ftp
mkdir /ftp/recordings
chmod 555 /ftp
mount --bind /app/recordings /ftp/recordings


# install pip dependencies
pip3 install -r /app/requirements/production.txt
echo test0


# fix speakeazy file permissions
bash /app/devops/files/fix_permissions.sh
echo test1


mv /app/devops/files/django/django.service /lib/systemd/system/django.service
echo test2
systemd enable django.service
echo test3
