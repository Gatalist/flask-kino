#!/bin/bash

# Check if FLASK_PORT is set, otherwise show an error and exit
: "${FLASK_PORT:?error missing FLASK_PORT env}"

# Function to wait for the Django service to be healthy
wait_for_app_service() {
    echo "Waiting for app service on port PORT..."
    while ! curl -s "http://flask-app:$FLASK_PORT" > /dev/null; do
        echo "App service not ready, waiting..."
        sleep 5
    done
    echo "App service is ready."
}

# Wait for app service before starting NGINX
wait_for_app_service

# Run NGINX and set up auto-reload every 6 hours
echo "Starting NGINX with auto-reload every 6 hours..."
(
    while true; do
        sleep 6h
        echo "Reloading NGINX..."
        nginx -s reload
    done
) &

# Start NGINX in the foreground
nginx -g 'daemon off;'