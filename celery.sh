#!/bin/bash
celery -A school_erp_backend worker \
--loglevel=info \
--logfile=logs/celery_worker.log \
--detach
