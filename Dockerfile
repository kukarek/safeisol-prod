FROM python:3.11-slim

WORKDIR /app

# Только runtime-зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       netcat-openbsd \
       libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=safeisol.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# collectstatic — ОДИН РАЗ при сборке
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "safeisol.wsgi:application", "--bind", "0.0.0.0:8000"]
