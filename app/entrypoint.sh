#!/bin/bash
set -e

# Ждём пока PostgreSQL будет доступен
echo "⏳ Ожидание PostgreSQL на $DB_HOST:$DB_PORT..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "✅ PostgreSQL доступен. Выполняем миграции..."

# Инициализация миграций, если папки ещё нет
if [ ! -d "migrations" ]; then
  flask db init
fi

flask db migrate || true
flask db upgrade

echo "🚀 Запуск приложения..."
#exec gunicorn --bind 0.0.0.0:5000 run:app
exec python run.py