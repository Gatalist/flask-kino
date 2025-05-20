#!/bin/sh

# Check if FLASK_PORT is set, otherwise show an error and exit
: "${FLASK_PORT:?error missing FLASK_PORT env}"

# Получаем IP адрес flask-app
FLASK_IP=$(getent hosts flask-app | awk '{ print $1 }')
POSTGRES_IP=$(getent hosts flask-postgres | awk '{ print $1 }')

# Добавляем flask-app в /etc/hosts (если нужно переопределить)
if [ -n "$FLASK_IP" ]; then
    echo "Добавляем flask-app с IP $FLASK_IP в /etc/hosts"
    echo "$FLASK_IP flask-app" >> /etc/hosts
else
    echo "Не удалось найти IP flask-app"
    exit 1
fi

# Получаем IP flask-postgres
PG_IP=$(getent hosts flask-postgres | awk '{ print $1 }')

# Добавляем flask-postgres в /etc/hosts
if [ -n "$PG_IP" ]; then
    echo "Добавляем flask-postgres с IP $PG_IP в /etc/hosts"
    echo "$PG_IP flask-postgres" >> /etc/hosts
else
    echo "❌ Не удалось найти IP flask-postgres"
    exit 1
fi



# Function to wait for the FLASK service to be healthy
wait_for_app_service() {
    echo "Waiting for app service on port PORT..."
    while ! curl -s "http://flask-app:$FLASK_PORT" > /dev/null; do
        echo "App service not ready, waiting..."
        sleep 5
    done
    echo "App service is ready."
}

wait_for_wireguard_port() {
    echo "⏳ Waiting for WireGuard tunnel wg0... [port: 51820]"
    while ! nc -z wireguard-vpn 51820; do
        echo "WireGuard service not ready, waiting... [port: 51820]"
        sleep 5
    done
    echo "✅ WireGuard tunnel is active [port: 51820]"
}

wait_for_app_service
wait_for_wireguard

echo "🚀 Запуск парсера..."
exec python main.py