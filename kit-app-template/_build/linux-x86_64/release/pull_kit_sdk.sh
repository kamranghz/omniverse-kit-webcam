#!/bin/bash
set -e
SCRIPT_DIR=$(dirname ${BASH_SOURCE})

if [ -d "$SCRIPT_DIR/kit/python" ]; then
    "$SCRIPT_DIR/kit/python/python" "$SCRIPT_DIR/dev/tools/tinypull.py" $@
else
    exec "$SCRIPT_DIR/dev/repo.sh" pull_extensions -c release $@ || exit $?
fi
