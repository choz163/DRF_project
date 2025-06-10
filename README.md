# Проект: Django REST + Celery + Docker

## 1. Требования
- Docker
- Docker Compose ≥ 1.27

## 2. Клонирование репозитория
git clone <URL вашего репо> && cd <repo>

## 3. Создание и заполнение .env
cp .env.example .env  
# Откройте .env и пропишите:
# SECRET_KEY, DEBUG, параметры БД и Redis

## 4. Сборка и запуск всех сервисов
docker-compose up --build -d

## 5. Миграции и суперпользователь
# Применить миграции
docker-compose exec web python manage.py migrate
# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

## 6. Проверка работы
- Django API: http://localhost:8000/
- Django Admin: http://localhost:8000/admin/
- Логи Celery Worker: docker-compose logs -f celery
- Логи Celery Beat: docker-compose logs -f celery-beat
- Redis на порту 6379, PostgreSQL — 5432 (localhost)

## 7. Остановка и очистка
docker-compose down  
# Чтобы удалить тома (данные БД):
docker-compose down -v


