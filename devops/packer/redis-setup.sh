#!/bin/bash


echo ------ SETTING UP WORKER ------


apt-get --no-install-recommends --no-install-suggests -y install redis

mv /app/devops/files/redis/redis.service /lib/systemd/system/
sync

systemctl enable redis.service
sync
