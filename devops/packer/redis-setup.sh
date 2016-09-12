#!/bin/bash


echo ------ SETTING UP WORKER ------


apt-get --no-install-recommends --no-install-suggests -y install redis

systemd enable worker.service
sync
