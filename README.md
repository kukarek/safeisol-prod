# 🛡 Safeisol — сайт компании "Безопасная теплоизоляция"

Веб-платформа для демонстрации и продажи теплоизоляционных чехлов, разработанная для ООО «Безопасная теплоизоляция». Проект включает каталог продукции, SEO-оптимизацию, административную панель, очередь задач и полную CI/CD-интеграцию.

---

## 🚀 Основной функционал

- Каталог категорий и товаров
- Умные хлебные крошки
- Панель администратора (Django Admin)
- Отложенные задачи (Celery + Redis)
- Статическая оптимизация (Collectstatic)
- CI/CD пайплайн
- Полностью настроенный backend (Gunicorn, Nginx)
- SEO-оптимизация

---

## 🛠 Технологии

- Python 3.11
- Django 4.x
- PostgreSQL 15+
- Celery + Redis
- Gunicorn + Nginx
- CI/CD (GitHub Actions или другой пайплайн)
- HTML5 + адаптивная вёрстка
- Ubuntu 22.04 (на сервере)

---

## ⚙️ Установка и запуск (локально)

```bash
git clone https://github.com/your-username/safeisol.git
cd safeisol

# Настройка окружения
cp .env.example .env
# отредактируйте .env

# Установите (если не установлена) и зайдите в PostgreSQL
psql -U postgres

# Создайте базу 
CREATE DATABASE safeisol;

# Запустить контейнеры
docker-compose up -d --build

# Запускаем тесты и смотрим покрытие
docker-compose run --rm web coverage run --source='.' manage.py test && docker-compose run --rm web coverage report -m

# Применить миграции
docker-compose exec web python manage.py migrate

# Загрузить начальные данные
docker-compose exec web python manage.py loaddata data.json

# По желанию можно создать суперюзера для управления админ панелью
docker-compose exec web python manage.py createsuperuser
