#!/bin/bash

# todo: until consol/vault is setup
. /app/.env.sh
. /app/venv/bin/activate

celery -A speakeazy.taskapp worker -l INFO
