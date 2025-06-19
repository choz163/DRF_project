Проект DRF_project

REST API на Django с настроенным CI/CD и автоматическим деплоем на удалённый Ubuntu-сервер.


Содержание


Описание

Требования

Локальная разработка

Тестирование

Конфигурация окружения

Деплой на удалённый сервер (Block 1)

CI/CD через GitHub Actions (Block 2)

.gitignore

Структура проекта



1. Описание

Этот проект реализует REST API на Django Rest Framework.

Реализован процесс непрерывной интеграции и доставки (CI/CD):



При пуше в ветку develop автоматически запускаются тесты.

После успешного прохождения тестов происходит SSH-деплой на удалённый сервер, где проект обновляется, миграции и статические файлы собираются, перезапускается Gunicorn.



2. Требования


Python 3.11+

Git

Удалённая VM Ubuntu 20.04 LTS (или аналогичная)

SSH-доступ к серверу

Аккаунт на GitHub



3. Локальная разработка



Клонируем репозиторий:


git clone git@github.com:choz163/DRF_project.gitt
cd DRF_project
Копировать



Создаём и активируем виртуальное окружение:


python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
Копировать



Копируем шаблон .env и заполняем свои значения:


cp .env.template .env
# Редактируем .env: SECRET_KEY, DB_*, DEBUG и т.п.
Копировать



Применяем миграции и запускаем сервер:


python manage.py migrate
python manage.py runserver
Копировать



API будет доступен по адресу http://127.0.0.1:8000/



4. Тестирование


Django-тесты:
python manage.py test
Копировать


Pytest (опционально):
pytest --maxfail=1 --disable-warnings -q
Копировать




5. Конфигурация окружения

Файл .env.template содержит список необходимых переменных:


DEBUG=
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

Не коммитим реальный .env в репозиторий — он игнорируется через .gitignore.



6. Деплой на удалённый сервер (Block 1)

Шаг 1. SSH-доступ


На локальном ПК сгенерировать ключ (если ещё нет):
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
Копировать


Скопировать публичный ключ на сервер:
ssh-copy-id user@server_ip
Копировать


На сервере в /etc/ssh/sshd_config отключить парольный логин:
PasswordAuthentication no
PermitRootLogin no

sudo systemctl reload sshd
Копировать



Шаг 2. Установка ПО

ssh user@server_ip
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git nginx ufw
Копировать

Шаг 3. Клонирование и окружение

cd ~
git clone git@github.com:your_username/DRF_project.git
cd DRF_project

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.template .env   # и заполнить
Копировать

Шаг 4. Миграции и статика

python manage.py migrate --noinput
python manage.py collectstatic --noinput
Копировать

Шаг 5. Gunicorn + systemd



Установить Gunicorn:


pip install gunicorn
Копировать



Создать /etc/systemd/system/gunicorn.service:


[Unit]
Description=gunicorn daemon for DRF_project
After=network.target

[Service]
User=your_unix_user
Group=www-data
WorkingDirectory=/home/your_unix_user/DRF_project
EnvironmentFile=/home/your_unix_user/DRF_project/.env
ExecStart=/home/your_unix_user/DRF_project/venv/bin/gunicorn \
    --access-logfile - --workers 3 \
    --bind unix:/home/your_unix_user/DRF_project/gunicorn.sock \
    DRF_project.wsgi:application

[Install]
WantedBy=multi-user.target



Запустить сервис:


sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
Копировать



Шаг 6. Nginx



Удалить default и создать свой в /etc/nginx/sites-available/DRF_project:


server {
    listen 80;
    server_name your_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/your_unix_user/DRF_project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/your_unix_user/DRF_project/gunicorn.sock;
    }
}



Активировать и перезапустить:


sudo ln -s /etc/nginx/sites-available/DRF_project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
Копировать



Шаг 7. Настройка брандмауэра

sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
Копировать


7. CI/CD через GitHub Actions (Block 2)

Секреты в GitHub

Настройки → Secrets and variables → Actions:



SSH_PRIVATE_KEY – приватный ключ deploy_key

SERVER_HOST – IP/домен сервера

SERVER_USER – Unix-пользователь (например ubuntu)

SERVER_SSH_PORT – (обычно 22)

PROJECT_DIR – /home/ubuntu/DRF_project


workflow: .github/workflows/ci-cd.yml

name: CI/CD Pipeline

on:
  push:
    branches:
      - develop

jobs:
  tests:
    name: Run Django Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with: python-version: '3.11'
      - run: |
          pip install --upgrade pip
          pip install -r requirements.txt
      - run: |
          python manage.py migrate --noinput
      - run: |
          pytest --maxfail=1 --disable-warnings -q

  deploy:
    name: Deploy to Server
    needs: tests
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: webfactory/ssh-agent@v0.8.1
        with: ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
      - run: |
          ssh -o StrictHostKeyChecking=no \
            ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} \
            -p ${{ secrets.SERVER_SSH_PORT }} << 'EOF'
            set -e
            cd ${{ secrets.PROJECT_DIR }}
            git fetch --all
            git reset --hard origin/develop
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate --noinput
            python manage.py collectstatic --noinput
            sudo systemctl restart gunicorn
          EOF
Копировать


8. .gitignore

.env
venv/
__pycache__/
*.pyc
.idea/


9. Структура проекта

DRF_project/
├── config/               
├── lms              
├── .env.template
├── .gitignore
├── manage.py
├── requirements.txt
└── .github/
    └── workflows/
        └── ci-cd.yml

