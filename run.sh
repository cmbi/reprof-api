#!/usr/bin/env bash
which reprof || echo error, no reprof installed!

export REPROF_REST_SETTINGS='../dev_settings.py'
gunicorn --log-file=- -k gevent -b 127.0.0.1:5000 reprof_rest.application:app
