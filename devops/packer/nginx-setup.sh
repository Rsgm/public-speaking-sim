#!/bin/bash


echo ------ SETTING UP NGINX ------

echo deb http://ftp.debian.org/debian jessie-backports main >> /etc/apt/sources.list
apt-get update
apt-get upgrade
apt-get install --no-install-recommends --no-install-suggests -y nginx -t jessie-backports certbot

useradd --no-create-home nginx
mkdir /etc/letsencrypt/

mv /app/devops/files/nginx/nginx.conf /etc/nginx/nginx.conf
mv /app/devops/files/nginx/nginx.service /lib/systemd/system/
mv /app/devops/files/nginx/letsencrypt.ini /etc/letsencrypt/cli.ini
mv /app/devops/files/nginx/certbot-install.service /lib/systemd/system/
mv /app/devops/files/nginx/certbot-renew.service /lib/systemd/system/
mv /app/devops/files/nginx/certbot-renew.timer /lib/systemd/system/

systemctl enable certbot-install.service
systemctl enable certbot-renew.service
systemctl enable certbot-renew.timer

openssl dhparam -outform PEM -out /etc/speakeazy_dhparam.pem 2048
