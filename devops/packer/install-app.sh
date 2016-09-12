#!/bin/bash


echo ------ SETTING UP APP DIRECTORY AND USERS ------

groupadd -r django
useradd -r -g django django
mkdir /app

tar -zxf /tmp/server.tar.gz -C /app
