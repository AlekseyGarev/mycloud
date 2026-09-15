# My Cloud — дипломное облачное хранилище

My Cloud — fullstack SPA-приложение для облачного хранения файлов, разработанное в рамках дипломного проекта.

Приложение позволяет пользователям регистрироваться, авторизовываться, загружать и хранить файлы, изменять их данные, скачивать, удалять и создавать публичные ссылки.

Администратор может управлять пользователями и работать с их файловыми хранилищами.

## Технологии

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Gunicorn
- WhiteNoise

### Frontend

- React
- Redux Toolkit
- React Router
- Axios
- Vite

### Deployment

- Docker
- Docker Compose
- PostgreSQL в отдельном контейнере
- Git / GitHub

---

## Возможности приложения

### Пользователь

Пользователь может:

- зарегистрироваться;
- войти и выйти из системы;
- просматривать собственное файловое хранилище;
- загружать один или несколько файлов;
- задавать имя файла;
- добавлять комментарий;
- переименовывать файл;
- изменять комментарий;
- скачивать файл;
- удалять файл;
- создавать специальную публичную ссылку;
- копировать публичную ссылку;
- просматривать дату загрузки;
- просматривать дату последнего скачивания;
- просматривать размер файла.

Пользователь имеет доступ только к собственному хранилищу.

### Администратор

Администратор может:

- просматривать список пользователей;
- просматривать количество файлов пользователя;
- просматривать общий объём файлов пользователя;
- открывать хранилище любого пользователя;
- загружать файлы в хранилище пользователя;
- редактировать файлы пользователя;
- скачивать файлы;
- удалять файлы;
- назначать пользователя администратором;
- снимать права администратора;
- удалять пользователей.

---

## Структура проекта

```text
mycloud/
├── backend/
│   ├── config/                 # Настройки Django
│   ├── storage/                # Работа с файлами
│   ├── users/                  # Пользователи и авторизация
│   ├── media/                  # Загруженные файлы
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── api/
│   ├── package.json
│   └── vite.config.js
│
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Переменные окружения

Файл с реальными настройками `.env` не хранится в Git.

Пример настроек находится в:

```text
backend/.env.example
```

Для запуска необходимо создать `.env` в корне проекта рядом с `docker-compose.yml`.

Пример:

```env
DEBUG=False

SECRET_KEY=your-secret-key

DB_NAME=mycloud
DB_USER=mycloud
DB_PASSWORD=your-strong-database-password
DB_HOST=db
DB_PORT=5432

ALLOWED_HOSTS=your-server-ip,127.0.0.1,localhost

ADMIN_USERNAME=cloudadmin
ADMIN_EMAIL=admin@example.com
ADMIN_INITIAL_PASSWORD=

SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

> Не публикуйте реальные значения `SECRET_KEY`, `DB_PASSWORD` и пароли пользователей в GitHub.

При работе через обычный HTTP:

```env
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

После настройки HTTPS необходимо использовать:

```env
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

# Запуск проекта через Docker

## 1. Клонирование репозитория

```bash
git clone git@github.com:AlekseyGarev/mycloud.git
cd mycloud
```

---

## 2. Создание `.env`

Создайте файл:

```text
.env
```

в корневой директории проекта.

Заполните параметры PostgreSQL, Django и адрес сервера.

Для генерации `SECRET_KEY` на Linux можно использовать:

```bash
openssl rand -hex 32
```

Для генерации пароля PostgreSQL:

```bash
openssl rand -hex 24
```

---

## 3. Сборка и запуск контейнеров

```bash
docker compose up -d --build
```

Docker выполняет:

1. установку frontend-зависимостей;
2. production-сборку React;
3. установку Python-зависимостей;
4. копирование frontend-сборки в Django;
5. `collectstatic`;
6. запуск Django через Gunicorn;
7. запуск PostgreSQL.

---

## 4. Применение миграций

После первого запуска:

```bash
docker compose exec web python manage.py migrate
```

---

## 5. Создание администратора

Администратора можно создать стандартной командой Django:

```bash
docker compose exec web python manage.py createsuperuser
```

После создания пользователь получает права Django superuser и имеет доступ к панели администратора My Cloud.

При необходимости поле `is_admin` можно дополнительно установить через панель приложения.

В проекте также предусмотрена команда:

```bash
docker compose exec web python manage.py init_admin
```

Она использует переменные:

```env
ADMIN_USERNAME=cloudadmin
ADMIN_EMAIL=admin@example.com
ADMIN_INITIAL_PASSWORD=your-password
```

Пароль администратора не должен храниться в Git.

---

## 6. Проверка контейнеров

```bash
docker compose ps
```

Оба контейнера должны находиться в состоянии `Up`:

```text
db
web
```

Логи Django/Gunicorn:

```bash
docker compose logs web --tail=100
```

Логи PostgreSQL:

```bash
docker compose logs db --tail=100
```

---

## Открытие приложения

При текущем HTTP-развёртывании приложение доступно по адресу:

```text
http://SERVER_IP:8000
```

Необходимо заменить `SERVER_IP` на публичный IP-адрес сервера.

---

# Обновление проекта на сервере

Основная версия исходного кода хранится в GitHub.

Рабочий процесс:

```text
VS Code
   ↓
Git commit
   ↓
GitHub
   ↓
Server: git pull
   ↓
Docker rebuild
```

После изменения проекта локально:

```bash
git add .
git commit -m "Описание изменения"
git push origin main
```

На сервере:

```bash
cd /opt/mycloud/mycloud
git pull origin main
docker compose up -d --build
```

`collectstatic` выполняется автоматически во время Docker-сборки.

Данные PostgreSQL и пользовательские файлы хранятся в Docker volumes, поэтому обычная пересборка контейнеров их не удаляет.

Не используйте:

```bash
docker compose down -v
```

если необходимо сохранить данные, поскольку параметр `-v` удаляет volumes.

---

# API

## Авторизация

```text
GET  /api/auth/csrf/
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/
```

Авторизация реализована через Django Session Authentication.

Изменяющие запросы защищены CSRF.

---

## Файлы

```text
GET    /api/files/
POST   /api/files/
PATCH  /api/files/<id>/
DELETE /api/files/<id>/
GET    /api/files/<id>/download/
POST   /api/files/<id>/share/
```

Администратор может работать с хранилищем выбранного пользователя.

---

## Публичные ссылки

```text
GET /api/public/files/<uuid>/
GET /api/public/files/<uuid>/download/
```

Публичная ссылка использует UUID и не раскрывает внутренний путь хранения файла.

---

## Администрирование

```text
GET    /api/admin/users/
PATCH  /api/admin/users/<id>/
DELETE /api/admin/users/<id>/
GET    /api/admin/users/<id>/files/
```

Доступ разрешён только администраторам.

---

# Хранение файлов

Физические файлы находятся в `media`.

Для хранения на диске используется уникальное имя, что предотвращает конфликт файлов с одинаковыми исходными названиями.

В базе данных сохраняется информация о файле, включая:

- исходное имя;
- размер;
- дату загрузки;
- дату последнего скачивания;
- комментарий;
- путь хранения;
- специальную публичную ссылку;
- владельца файла.

При удалении записи физический файл также удаляется.

---

# Безопасность

В проекте используются:

- Django Session Authentication;
- CSRF-защита;
- проверка прав доступа;
- разграничение пользовательских хранилищ;
- ограничения административных API;
- уникальные UUID для публичных ссылок;
- переменные окружения для секретных данных;
- исключение `.env` из Git;
- ограничения частоты запросов для регистрации и авторизации.

Реальные пароли и `SECRET_KEY` не должны попадать в GitHub.

---

# Локальная разработка

## Backend

Создание виртуального окружения:

```bash
cd backend
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Создайте `.env` на основе `.env.example`, затем:

```bash
python manage.py migrate
python manage.py runserver
```

---

## Frontend

```bash
cd frontend
npm ci
npm run dev
```

Vite запускает frontend в dev-режиме и проксирует `/api` на Django.

---

# Проверка проекта

## Backend-тесты

Для тестового запуска можно использовать SQLite:

```bash
cd backend
DB_ENGINE=sqlite python manage.py test
```

## Frontend

```bash
cd frontend
npm run lint
npm run build
```

---

# Production и HTTPS

Текущий вариант может работать непосредственно через:

```text
http://SERVER_IP:8000
```

Для полноценного production-развёртывания рекомендуется использовать доменное имя, reverse proxy и HTTPS.

После настройки HTTPS необходимо установить:

```env
DEBUG=False
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

а также указать домен в:

```env
ALLOWED_HOSTS=your-domain.ru
CSRF_TRUSTED_ORIGINS=https://your-domain.ru
```

После изменения `.env` необходимо пересоздать web-контейнер:

```bash
docker compose up -d --force-recreate web
```

---

# Важные файлы, которые не должны попадать в Git

Не публикуются:

```text
.env
node_modules/
backend/media/*
backend/staticfiles/
__pycache__/
*.pyc
```

Правила находятся в `.gitignore`.

---

# Репозиторий

Проект разработан как дипломная работа — облачное хранилище файлов My Cloud.

Исходный код хранится в публичном GitHub-репозитории.