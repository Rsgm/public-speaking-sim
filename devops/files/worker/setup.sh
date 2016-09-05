#!/bin/bash


echo ------ SETTING UP WORKER ------


# install ffmpeg
echo deb http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list
echo deb-src http://www.deb-multimedia.org jessie main non-free >> /etc/apt/sources.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5C808C2B65558117
apt-get -y update
apt-get --no-install-recommends --no-install-suggests -y install deb-multimedia-keyring
apt-get -y update
apt-get --no-install-recommends --no-install-suggests -y install ffmpeg


# fix speakeazy file permissions
bash /app/devops/files/fix_permissions.sh
echo test1


mv /app/devops/files/worker/worker.service /lib/systemd/system/worker.service
echo test2
systemd enable worker.service
echo test3

# So, this script fails inexplicably somewhere after 'echo test1' without each 'echo testx'.
# I guess I have no choice but to leave them. Future archaeologists have been warned.
