#!/bin/bash

# Start the FastAPI app in the background and redirect logs to both file and stdout
uvicorn main:app --host 0.0.0.0 --port 8000 2>&1 | tee fastapi.log &

# Start the worker process in the foreground and redirect logs to both file and stdout
python3 worker.py 2>&1 | tee worker.log
