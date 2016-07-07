#!/bin/bash

certbot certonly

systemd start letsencrypt.timer
