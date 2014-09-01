#!/usr/bin/env bash
export REPROF_REST_SETTINGS='../dev_settings.py'
gunicorn --log-file=- -k gevent -b 127.0.0.1:5000 reprof_rest.application:app
