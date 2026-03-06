#!/usr/bin/env bash
set -euo pipefail
 
# Gunicorn + UvicornWorker, bind to Azure's port
exec gunicorn api:app \
  -k uvicorn.workers.UvicornWorker \
  -w ${WEB_CONCURRENCY:-6} \
  --bind 0.0.0.0:${PORT:-8000} \
  -t 1800 --keep-alive 1800 \
  --log-level debug \
  --access-logfile - \
  --error-logfile - \
  --capture-output
