#!/bin/bash


echo ------ SETTING UP DJANGO ------


echo test0


echo test1

mv /app/devops/files/django/django.service /lib/systemd/system/django.service
echo test2
systemd enable django.service
echo test3
