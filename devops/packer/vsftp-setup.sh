#!/bin/bash


echo ------ SETTING UP VSFTP ------


apt-get --no-install-recommends --no-install-suggests -y install vsftpd

mv /app/devops/files/django/vsftpd.conf /etc/vsftpd.conf
echo anonymous > /etc/vsftpd.allowed_users
systemd enable vsftpd.service  # docker: Excess arguments.

mkdir /ftp
mkdir /ftp/recordings
chmod 555 /ftp

mount --bind /app/recordings /ftp/recordings
