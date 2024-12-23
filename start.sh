#!/bin/bash
# Start Xvfb
Xvfb :99 -screen 0 1024x768x16 &
export DISPLAY=:99

# Start the application
exec uvicorn app.server:app --host 0.0.0.0 --port 8000