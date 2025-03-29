#!/usr/bin/env bash

if [[ "$BOOT_MODE" == "web" ]]; then
    ./manage.py migrate
    ./manage.py collectstatic --no-input
    gunicorn --capture-output -b 0.0.0.0:8000 -w ${GUNICORN_WORKERS:-5} --threads ${GUNICORN_THREADS:-5} gpslogger.wsgi:application
else
    echo "BOOT_MODE not known: $BOOT_MODE"
fi
