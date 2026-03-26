FROM python:3.11-slim
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Установка python зависимостей (кэшируем этот слой)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

ENV DJANGO_SETTINGS_MODULE=safeisol.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Сборка статики с фейковыми переменными
# После collectstatic мы удаляем этот временный файл, чтобы он не попал в финальный образ.
RUN touch .env && \
    SECRET_KEY=build-placeholder \
    ALLOWED_HOSTS=* \
    DB_NAME=temp \
    DB_USER=temp \
    DB_PASSWORD=temp \
    DB_HOST=localhost \
    DB_PORT=5432 \
    EMAIL_HOST_USER=temp \
    EMAIL_HOST_PASSWORD=temp \
    DEFAULT_FROM_EMAIL=temp \
    CELERY_BROKER_URL=redis://localhost:6379 \
    CELERY_RESULT_BACKEND=redis://localhost:6379 \
    python manage.py collectstatic --noinput && \
    rm .env

CMD ["gunicorn", "safeisol.wsgi:application", "--bind", "0.0.0.0:8000"]