#!/bin/bash


echo ------ SETTING UP WORKER ------

if ! grep -Fxq "deb http://packages.dotdeb.org jessie all" /etc/apt/sources.list
then
    wget https://www.dotdeb.org/dotdeb.gpg
    sudo apt-key add dotdeb.gpg

    echo deb http://packages.dotdeb.org jessie all >> /etc/apt/sources.list
    echo deb-src http://packages.dotdeb.org jessie all >> /etc/apt/sources.list
    apt-get update -y
fi

apt-get install --no-install-recommends --no-install-suggests -y redis-server

systemctl enable redis-server.service
sync
