#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1920x1080x24 -ac &
export DISPLAY=:99

# Wait for Xvfb to be ready
sleep 2

# Start dbus
mkdir -p /var/run/dbus
dbus-daemon --system --fork

# Start the application
exec uvicorn app.server:app --host 0.0.0.0 --port 8000