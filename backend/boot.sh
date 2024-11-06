#!/bin/bash
exec gunicorn run:app --workers 4 -t 120 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
