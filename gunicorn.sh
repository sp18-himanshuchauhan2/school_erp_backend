#!/bin/bash
gunicorn school_erp_backend.wsgi:application \
--bind 0.0.0.0:8000 \
--workers 3 \
--worker-class gthread \
--threads 2 \
--timeout 30 \
--reload \
--access-logfile logs/access.log \
--error-logfile logs/error.log \
--log-level info \
--daemon
