#!/bin/bash


echo ------ SETTING UP DJANGO ------


mv /app/devops/files/django/django.service /lib/systemd/system/django.service
sync

systemctl enable django.service
sync
