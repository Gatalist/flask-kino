#!/bin/sh

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


echo "🚀 Запуск парсера..."
exec python main.py