#!/bin/bash


# install ffmpeg
echo deb http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list
echo deb-src http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5C808C2B65558117
apt-get -y update
apt-get --no-install-recommends --no-install-suggests -y install deb-multimedia-keyring
apt-get -y update
apt-get --no-install-recommends --no-install-suggests -y install ffmpeg


# Install python and python dependencies for later
apt-get --no-install-recommends --no-install-suggests -y install python3 python3-pip libjpeg62-turbo-dev zlib1g-dev gcc libffi-dev
apt-get clean
pip3 install --upgrade pip
ln -s /usr/bin/python3 /usr/local/bin/python


# create non-root user
groupadd -r worker
useradd -r -g worker worker
mkdir /app
chmod 777 /app
chown worker /app

cd /app

# extract speakeazy
tar -zxf /tmp/worker.tar.gz

# fix speakeazy file permissions
bash ./fix_permissions.sh

# install pip dependencies
pip3 install -r /app/requirements/production.txt


mv ./packer/worker/worker.service /lib/systemd/system/worker.service
systemd enable worker.service
