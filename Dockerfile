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
RUN SECRET_KEY=build-time-ignore ALLOWED_HOSTS=* python manage.py collectstatic --noinput

CMD ["gunicorn", "safeisol.wsgi:application", "--bind", "0.0.0.0:8000"]