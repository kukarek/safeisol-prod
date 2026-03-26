FROM python:3.11-slim
WORKDIR /app

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

# --- ДОБАВЛЯЕМ ЭТИ СТРОКИ ДЛЯ СБОРКИ ---
ARG SECRET_KEY
ARG ALLOWED_HOSTS
ENV SECRET_KEY=$SECRET_KEY
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS
# ---------------------------------------

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "safeisol.wsgi:application", "--bind", "0.0.0.0:8000"]