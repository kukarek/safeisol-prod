FROM python:3.11-slim

# Устанавливаем необходимые пакеты, включая netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=safeisol.settings

# Команды запускаем через shell
CMD sh -c "python manage.py collectstatic --noinput && exec gunicorn safeisol.wsgi:application --bind 0.0.0.0:8000"
