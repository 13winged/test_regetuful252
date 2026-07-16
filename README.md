# DevProd FAPI

## Описание
FastAPI приложение с PostgreSQL и Redis, развернутое через Docker и Ansible

## рхитектура
- **FastAPI** - веб-фреймворк
- **PostgreSQL** - основная БД
- **Redis** - кеширование
- **Nginx** - reverse proxy + SSL
- **Docker** - контейнеризация
- **Ansible** - автоматизация деплоя
- **GitHub Actions** - CI/CD

## Быстрый старт

# Установка зависимостей
pip install -r requirements.txt

# Запуск
uvicorn app.main:app --reload
Docker
bash

# Сборка и запуск
docker compose up -d

# Проверка
curl http://localhost:8000/health
Ansible деплой
bash
cd ansible-deploy
ansible-playbook -i inventory.ini playbook.yml

CI/CD Pipeline

✅ Lint (flake8)

✅ Tests (pytest)

✅ Build Docker image

✅ Deploy via Ansible

Доступность

HTTPS: https://hissihyss2.com/

Health: https://hissihyss2.com/health

Безопасность
Non-root пользователь в контейнере

Минимальный образ (slim)

Rate Limiting (5 req/sec)

SSL (Let's Encrypt)

UFW Firewall

Структура
text
my-app/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── ansible-deploy/
│   ├── inventory.ini
│   ├── playbook.yml
│   └── roles/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
