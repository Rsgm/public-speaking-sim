#!/bin/bash

set -e

/app/.env.sh

exec "$@"
