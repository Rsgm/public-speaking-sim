#!/bin/bash

set -e

# todo: move this to .env
export REDIS_URL=redis://$REDIS_PORT_6379_TCP_ADDR:$REDIS_PORT_6379_TCP_PORT/0

. /app/.env.sh

exec "$@"
